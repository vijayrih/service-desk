import os
from dotenv import load_dotenv

load_dotenv()

# LLM Engine
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in the .env file.")
    
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Integrations
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

# Database Paths
DB_URI = os.getenv("DB_PATH", "sqlite:///service_desk.db")


RAW_DB_PATH = DB_URI.replace("sqlite:///", "")