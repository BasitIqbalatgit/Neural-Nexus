# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Gemini Model Configuration
GEMINI_MODEL = "gemini-1.5-pro"  # Adjust based on available models

# Context Manager Configuration
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 10))

# Allowed File Types for Upload
ALLOWED_FILE_TYPES = [
    'png', 'jpg', 'jpeg', 'gif', 'bmp',           # Images
    'pdf', 'doc', 'docx', 'txt', 'rtf',           # Documents
    'mp3', 'wav', 'ogg',                          # Audio
    'mp4', 'avi', 'mov', 'mkv',                   # Video
    'csv', 'geojson'                              # Data files for hackathon
]

# Temporary Upload Directory
TEMP_UPLOAD_DIR = os.getenv("TEMP_UPLOAD_DIR", os.path.join(os.path.expanduser("~"), "temp_uploads"))
if not os.path.exists(TEMP_UPLOAD_DIR):
    os.makedirs(TEMP_UPLOAD_DIR)

# Maximum File Size (10MB)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))

# Logging Configuration (optional, can be set in main app)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate critical settings
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env file")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in .env file")