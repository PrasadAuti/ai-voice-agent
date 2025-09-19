# 🏥 AI Healthcare Voice Agent

This project is a **voice-enabled healthcare assistant** built using [LiveKit Agents](https://docs.livekit.io/agents/) along with plugins like **Deepgram**, **ElevenLabs**, **Silero VAD**, and **Groq LLM**.  

The assistant:
- Understands spoken health-related queries.
- Responds with clear, concise, health-focused answers.
- Politely declines unrelated topics (sports, movies, tech, etc.).
- Suggests consulting a professional for serious concerns.

⚠️ **Disclaimer**: This is **not a substitute for medical advice**. Always consult a licensed healthcare professional.

---

## 🔑 Components & Their Roles

- **LiveKit Agents** → Manages real-time audio streaming, sessions, and worker lifecycle.  
- **Groq LLM (Llama-3.1-8B-Instant)** → Generates natural, health-focused responses.  
- **Deepgram STT (nova-3)** → Converts user speech into text with punctuation, filler handling, and smart formatting.  
- **ElevenLabs TTS** → Converts text responses into natural-sounding speech.  
- **Silero VAD** → Detects when the user starts and stops speaking (voice activity detection).  
- **Noise Cancellation (BVC)** → Improves call quality by reducing background noise.  
- **Metrics Collector** → Tracks usage (tokens, audio, etc.) for logging and analysis.  

---

## 📂 Project Structure
```
.
├── agent.py           # Entry point
├── requirements.txt   # Python dependencies
├── .env               # API keys and secrets (not committed)
└── venv/              # Virtual environment

````

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/PrasadAuti/ai-voice-agent.git
````

### 2️⃣ Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a **.env** file in the project root:

```env
LIVEKIT_URL=<your LiveKit server URL>
LIVEKIT_API_KEY=<your API Key>
LIVEKIT_API_SECRET=<your API Secret>

# STT / LLM / TTS providers
GROQ_API_KEY=<your API Secret>
DEEPGRAM_API_KEY=<your API Secret>
ELEVEN_API_KEY=<your API Secret>

```

---

## ⚙️ Requirements

- **Python version**: 3.9 or higher 

---

## ▶️ Running the Agent

Use one of these commands depending on your environment:

| Mode         | Command                         | Purpose                                                   |
|---------------|----------------------------------|-----------------------------------------------------------|
| Local / console | `python agent,py console`       | Run locally, with local audio input/output, for testing.  |
| Development    | `python agent,py dev`           | Run the agent against LiveKit Sandbox   |
| Production     | `python agent,py start`          | Production mode (optimize for deployment)                 |

---

## 📊 Metrics

On shutdown, usage metrics (tokens, audio, etc.) are logged:

```bash
INFO: Usage: {...summary...}
```

---

## 🔎 References

* [LiveKit Agents](https://docs.livekit.io/agents/)
* [Deepgram STT](https://developers.deepgram.com/)
* [ElevenLabs TTS](https://elevenlabs.io/)
* [Groq LLM](https://groq.com/)
* [Silero VAD](https://github.com/snakers4/silero-vad)

---

## 🧑‍⚕️ Disclaimer

This agent is for **educational and informational purposes only**.
It does **not** provide medical diagnoses, treatments, or prescriptions.
