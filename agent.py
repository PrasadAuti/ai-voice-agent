import logging
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

from livekit import api
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.voice import MetricsCollectedEvent
from livekit.plugins import deepgram, silero, groq, elevenlabs
from livekit.plugins import noise_cancellation

load_dotenv(dotenv_path=".env")

logger = logging.getLogger("healthcare-agent")


# Simple healthcare-related instructions
common_instructions = (
    "Hello! I am your AI healthcare assistant. I am not a doctor, but I can share general health information. "
    "Only answer questions related to health, medicine, symptoms, or wellness. "
    "If a user asks about unrelated topics (sports, movies, technology, etc.), respond politely: "
    "'That is outside my expertise. Please ask me only health-related questions.' "
    "Keep your answers short, clear, and easy to understand. "
    "When questions seem serious, suggest consulting a qualified healthcare professional."
)


@dataclass
class SessionData:
    last_question: Optional[str] = None


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


class SimpleHealthcareAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=common_instructions,
            tts=elevenlabs.TTS(),  # default voice
        )

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession[SessionData](
        vad=ctx.proc.userdata["vad"],
        llm=groq.LLM(
            model="llama-3.1-8b-instant",
            temperature=0.7
        ),
        stt=deepgram.STT(
            model="nova-3",
            language="en-US",
            interim_results=True,
            punctuate=True,
            smart_format=True,
            filler_words=True,
            endpointing_ms=25,
            sample_rate=16000
        ),
        tts=elevenlabs.TTS(),
        userdata=SessionData(),
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the simple agent
    await session.start(
        agent=SimpleHealthcareAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))