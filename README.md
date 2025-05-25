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
