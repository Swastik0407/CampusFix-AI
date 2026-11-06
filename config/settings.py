
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/campusfix.db"
)

APP_NAME = "CampusFix AI"
APP_VERSION = "1.0.0"

if not GEMINI_API_KEY:
    print("WARNING: Gemini API key is missing!")
