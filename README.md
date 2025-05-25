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
```
---
Fantastic project, Aadharsh. You're essentially assembling a Hollywood production line, but the stars are LLM agents, and they don't ask for trailers or green M\&Ms. Below is a solid, scalable folder structure and a `README.md` template tailored for your project: **`aiinfluencer`**.

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
