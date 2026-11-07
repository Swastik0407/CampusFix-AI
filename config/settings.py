
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# NVIDIA API Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = os.getenv(
    "NVIDIA_MODEL",
    "nvidia/nemotron-3.5-bolt-e4b"
)

NVIDIA_BASE_URL = os.getenv(
    "NVIDIA_BASE_URL",
    "https://integrate.api.nvidia.com/v1"
)

# Database Configuration
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/campusfix.db"
)

# Application Configuration
APP_NAME = "CampusFix AI"
APP_VERSION = "1.0.0"


# Check NVIDIA API key
if not NVIDIA_API_KEY:
    print("WARNING: NVIDIA API key is missing!")
