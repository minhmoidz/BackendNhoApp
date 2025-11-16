"""
Configuration Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NGROK_TOKEN = os.getenv("NGROK_TOKEN", "")

# Tesseract Configuration
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Storage Configuration
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)
DIARY_FILE = STORAGE_DIR / "diaries.json"
MEMORY_FILE = STORAGE_DIR / "memories.json"
NOTE_FILE = STORAGE_DIR / "notes.json"
REMINDER_FILE = STORAGE_DIR / "reminders.json"
USER_PROFILE_FILE = STORAGE_DIR / "user_profile.json"
HEALTH_LOG_FILE = STORAGE_DIR / "health_logs.json"
CONVERSATION_FILE = STORAGE_DIR / "conversations.json"

# API Configuration
API_TITLE = "Memory & Diary OCR API (Groq Edition)"
API_VERSION = "2.2.0"

# AI Model Configuration
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 1000