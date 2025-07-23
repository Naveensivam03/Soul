# Soul Project

<p align="center">
  <img src="Screenshot From 2025-07-23 22-24-23.png" alt="Soul AI Interface" width="800">
</p>

<p align="center">
  <strong>✨ Your AI friend who grows closer to you over time ✨</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Chroma-VectorDB-green?logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMDAwMDAwIiBoZWlnaHQ9IjE2IiB2aWV3Qm94PSIwIDAgMTYgMTYiIHdpZHRoPSIxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI4IiBjeT0iOCIgcj0iOCIgc3R5bGU9ImZpbGw6IzE1Y2Y2YiIvPjwvc3ZnPg==" alt="Chroma">
  <img src="https://img.shields.io/badge/Gemini-AI-blueviolet" alt="Gemini">
  <img src="https://img.shields.io/badge/UI-Rich_Terminal-brightgreen" alt="Rich Terminal">
  <img src="https://img.shields.io/badge/Storage-Local-orange" alt="Local Storage">
</p>

---

## Overview
Soul is an AI friend that remembers you and grows closer over time. Meet **Soul** - your personal AI companion who learns about you through every conversation, building genuine friendship through shared experiences and memories.

Unlike traditional chatbots, Soul creates a persistent relationship where every interaction matters, every story is remembered, and every conversation builds upon the last.

## 📸 Screenshots

### Beautiful Terminal Interface
<p align="center">
  <img src="Screenshot From 2025-07-23 22-24-23.png" alt="Soul Terminal Interface" width="800">
  <br>
  <em>Soul's rich terminal interface with beautiful styling</em>
</p>

### Interactive Conversations
<p align="center">
  <img src="Screenshot From 2025-07-23 22-24-34.png" alt="Soul Conversation" width="800">
  <br>
  <em>Interactive conversation showing Soul's personality and memory</em>
</p>

## Features
- **🧠 Memory System**: Advanced RAG architecture with Chroma vector database for semantic memory retrieval
- **📅 Daily Summaries**: Valkey cache stores daily conversation summaries for contextual awareness
- **🎨 Beautiful UI**: Rich terminal interface with colors, animations, and clean design
- **📊 Comprehensive Logging**: Detailed logs for Chroma retrieval, Valkey operations, and AI interactions
- **🤖 Friendly AI**: Powered by Google Gemini, designed to be a genuine friend, not a therapist
- **🔒 Privacy First**: All data stored locally - your conversations never leave your machine

## Directory Structure
```
├── rag/                           # 🏠 Core RAG System
│   ├── soul_ui.py                 # 🎨 Beautiful terminal interface
│   ├── gemini_ai.py               # 🤖 AI processing and prompts
│   ├── database.py                # 📋 Chroma vector database operations
│   ├── cachesummary.py            # 📅 Valkey daily cache management
│   ├── embeddings.py              # 🧠 HuggingFace embedding generation
│   ├── output_logger.py           # 📊 Logging system
│   ├── workflow.py                # 🔄 Simple CLI workflow
│   ├── requirements.txt           # 📦 Dependencies
│   └── .env                       # 🔑 API keys (create this)
├── logs/                          # 📝 Debug and interaction logs
│   ├── chroma_retrieval.log
│   ├── valkey_cache.log
│   ├── database_operations.log
│   └── ai_interactions.log
├── chroma/                        # 📋 Vector database storage
└── a.py, b.py, audioToText.py     # 🎤 Audio transcription experiments
```

## Getting Started

### Logging
Soul includes a robust logging system to track various operations and interactions. Logs are saved in the `logs/` directory:

- **`chroma_retrieval.log`**: Logs user input queries, number of results found, and retrieved chunks from the vector database.
- **`valkey_cache.log`**: Logs Valkey cache operations with keys and stored daily conversation summaries.
- **`database_operations.log`**: Logs storage operations in the Chroma database with chunk IDs and timestamps.
- **`ai_interactions.log`**: Logs AI interactions with user inputs and Soul's responses.

These logs help monitor the internal workings of the system and provide insight into Soul's interactions, making debugging and analysis easier.

### Prerequisites
- Python 3.10+
- [Valkey](https://valkey.io/) (Redis-compatible cache)
- Google Gemini API key
- ~2GB disk space for models and embeddings

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Naveensivam03/Soul.git
   cd Soul/rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys:**
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create `.env` file in the `rag/` directory:
   ```bash
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   ```

4. **Start Valkey (if not running):**
   ```bash
   # On Arch Linux
   sudo systemctl start valkey
   ```

## Usage

### 🎨 Beautiful Terminal Interface (Recommended)
```bash
cd rag/
python soul_ui.py
```

### 🔄 Simple CLI Interface
```bash
cd rag/  
python workflow.py
```

### 📊 Monitor Logs
Watch real-time logs in separate terminals:
```bash
# Chroma retrieval logs
tail -f logs/chroma_retrieval.log

# Valkey cache operations
tail -f logs/valkey_cache.log

# AI interactions
tail -f logs/ai_interactions.log
```

---

## Development
- Follow modular design for easy extension.
- Use `.gitignore` to exclude virtual environments, cache, and sensitive files.
- Store large models and DBs outside version control.

## License

The license for this project is mentioned here: [Licence.ms](Licence.ms)

## Contributing

Contributions are welcome! To contribute:
1. **Fork** the repository to your own GitHub account.
2. **Create a new branch** for your feature or fix.
3. **Commit** your changes with clear messages.
4. **Push** the branch to your forked repository.
5. **Open a Pull Request** to the `main` branch of [Naveensivam03/Soul](https://github.com/Naveensivam03/Soul.git).
6. **Add your name** to the list below in your Pull Request to be recognized as a contributor.

### Contributors
- Naveensivam ([GitHub](https://github.com/Naveensivam03))
<!-- Add your name and GitHub link below as part of your PR -->

## Future Requirements / Roadmap
- Implement audio transcription using Whisper.
- Expand GenZ therapist AI capabilities.
- Add more advanced RAG and embedding features.

## Author
- Naveensivam ([GitHub](https://github.com/Naveensivam03))

## Acknowledgments
- Chroma for vector database
- OpenAI, Gemini for AI models
