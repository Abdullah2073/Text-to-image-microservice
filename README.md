# Text-to-Image Microservice (DreamShaper)

A simple AI microservice that generates images from text prompts using the DreamShaper model. It uses a gRPC API, supports concurrent requests, and includes a minimal frontend using Gradio or Streamlit.

---

## Features

- Text-to-image generation (DreamShaper)
- gRPC API with concurrency support
- JSON error handling
- Postman gRPC testing
- Minimal frontend (Gradio / Streamlit)

---

## Tech Stack

| Component       | Tool/Library                     |
|----------------|----------------------------------|
| Model           | DreamShaper (Hugging Face)       |
| Backend         | Python, gRPC                     |
| Frontend        | Gradio / Streamlit               |
| Testing         | Pytest, Postman (gRPC)           |

---
## Setup

```bash
git clone https://github.com/abdullah2073/text-to-image-microservice.git
cd text-to-image-microservice
python app/server.py
