# 🎬 AI Influencer: Agentic AI for YouTube Shorts

`aiinfluencer` is an agentic framework that turns thematic prompts into compelling, fully-produced YouTube Shorts. Inspired by the capabilities of LangGraph and the rise of generative storytelling, this project orchestrates multiple AI agents to interpret themes, craft stories, synthesize media, and publish video content.

## 🚀 Project Vision

Transform a single idea—like *“a stitch in time saves nine”*—into a professional-grade video short through a seamless AI-driven pipeline.

---

## 🧠 Architecture Overview

- **Prompt Agent** – Understands the thematic prompt and extracts narrative cues.
- **Story Agent** – Generates a short-form story based on the prompt.
- **Screenplay Agent** – Translates story into a screenplay format.
- **Visual Agent** – Uses Synthesia to generate a video using my own avatar.
- **Assembly Agent** – Merges content and gets it ready for the final publication
- **Publishing Agent** – Uploads finalized video to YouTube Shorts.

Each stage is powered by LangGraph for stateful, multi-agent orchestration.

---

## 🛠️ Installation

```bash
git clone https://github.com/yourhandle/aiinfluencer.git
cd aiinfluencer
pip install -r requirements.txt

---
Fantastic project, Aadharsh. You're essentially assembling a Hollywood production line, but the stars are LLM agents, and they don't ask for trailers or green M\&Ms. Below is a solid, scalable folder structure and a `README.md` template tailored for your project: **`aiinfluencer`**.

---

## 📁 Recommended Folder Structure

```
aiinfluencer/
│
├── README.md
├── .gitignore
├── requirements.txt
├── setup.py
│
├── configs/
│   └── settings.yaml            # Configuration for agent orchestration, API keys, etc.
│
├── data/
│   ├── prompts/                 # Raw or example prompts
│   ├── outputs/                 # Generated content (narratives, scripts)
│   └── media/                   # Temp storage for videos/audio/images
│
├── aiinfluencer/
│   ├── __init__.py
│   ├── main.py                  # Entry point to trigger the full pipeline
│   ├── agent_orchestrator.py   # LangGraph-based agent orchestration
│   ├── utils.py                 # Helper functions (e.g., file I/O, logging)
│
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── prompt_agent.py          # Interprets thematic prompts
│   │   ├── story_agent.py           # Builds the narrative
│   │   ├── screenplay_agent.py      # Converts story to screenplay
│   │   ├── tts_agent.py             # Text-to-speech generation
│   │   ├── visual_agent.py          # Generates visuals or text-to-video
│   │   ├── assembly_agent.py        # Combines A/V into final short
│   │   └── publishing_agent.py      # Uploads video to YouTube Shorts
│
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py         # Unit tests for agent workflows
│
└── docs/
    └── architecture.md          # Extended documentation, diagrams, etc.
```

---

## 📝 `README.md`

````markdown
# 🎬 aiinfluencer: Agentic AI for YouTube Shorts

`aiinfluencer` is an agentic framework that turns thematic prompts into compelling, fully-produced YouTube Shorts. Inspired by the capabilities of LangGraph and the rise of generative storytelling, this project orchestrates multiple AI agents to interpret themes, craft stories, synthesize media, and publish video content.

## 🚀 Project Vision

Transform a single idea—like *“a stitch in time saves nine”*—into a professional-grade video short through a seamless AI-driven pipeline.

---

## 🧠 Architecture Overview

- **Prompt Agent** – Understands the thematic prompt and extracts narrative cues.
- **Story Agent** – Generates a short-form story based on the prompt.
- **Screenplay Agent** – Translates story into a screenplay format.
- **TTS Agent** – Generates voiceovers using TTS services like ElevenLabs or Polly.
- **Visual Agent** – Uses RunwayML, Pika Labs, or similar to generate matching visuals.
- **Assembly Agent** – Merges audio-visual content using MoviePy/FFmpeg.
- **Publishing Agent** – Uploads finalized video to YouTube Shorts.

Each stage is powered by LangGraph for stateful, multi-agent orchestration.

---

## 🛠️ Installation

```bash
git clone https://github.com/yourhandle/aiinfluencer.git
cd aiinfluencer
pip install -r requirements.txt
````

Set up your configuration in `configs/settings.yaml`.

---

## 🧪 Run the Pipeline

```bash
python aiinfluencer/main.py --prompt "a stitch in time saves nine"
```

Or run tests:

```bash
pytest tests/
```

---

## 📦 Tech Stack

* **LangGraph** – Agent orchestration
* **GPT-4o** – Story and screenplay generation
* **Synthesia** – Visual synthesis
* **YouTube Data API** – Publishing

---

## 📈 Scaling & Deployment

* Cloud compute for media rendering (Synthesia)
* Local storage for media assets (move to cloud in the future)
* LangSmith for agent observability and logging

---

## 🧾 License

Copyrighted work by Aadharsh Kannan. Contact aadharshkannan@gmail.com for licensing.

---

## 🙏 Acknowledgments

Inspired by the LangGraph ecosystem and the creative potential of AI media generation.
