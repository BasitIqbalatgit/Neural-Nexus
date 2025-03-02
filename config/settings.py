# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Context Manager Configuration
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 10))

# Allowed File Types for Upload
ALLOWED_FILE_TYPES = [
    'png', 'jpg', 'jpeg', 'gif', 'bmp',           # Images
    'pdf', 'doc', 'docx', 'txt', 'rtf',           # Documents
    'csv', 'geojson'                              # Data files for hackathon
]

# Temporary Upload Directory
TEMP_UPLOAD_DIR = os.getenv("TEMP_UPLOAD_DIR", os.path.join(os.path.expanduser("~"), "temp_uploads"))
if not os.path.exists(TEMP_UPLOAD_DIR):
    os.makedirs(TEMP_UPLOAD_DIR)

# Maximum File Size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate critical settings
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in .env file")