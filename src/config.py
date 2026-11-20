"""
Configuration Module for Email Automation & Reminder System.
Loads environment variables safely and defines paths and defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Directory Paths
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"
IMAGES_DIR = BASE_DIR / "images"
DOCS_DIR = BASE_DIR / "docs"

# Ensure all essential directories exist
for folder in [DATA_DIR, TEMPLATES_DIR, OUTPUTS_DIR, LOGS_DIR, IMAGES_DIR, DOCS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Data File Paths
CONTACTS_FILE = DATA_DIR / "contacts.csv"
REMINDERS_FILE = DATA_DIR / "reminders.csv"

# Log File Paths
SYSTEM_LOG_FILE = LOGS_DIR / "system.log"
DISPATCH_LOG_FILE = LOGS_DIR / "dispatch.log"

# SMTP Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "automation.test.demo@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_NAME = os.getenv("SENDER_NAME", "Enterprise Operations Automated Dispatcher")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "False").lower() in ("true", "1", "yes")

# Operational Settings
# If password is empty or DRY_RUN environment is true, default to simulation mode
ENV_DRY_RUN = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
DEFAULT_DRY_RUN = True if not SMTP_PASSWORD or SMTP_PASSWORD == "your_16_char_app_password" else ENV_DRY_RUN

# Retry & Network Timeout
SMTP_TIMEOUT_SECONDS = int(os.getenv("SMTP_TIMEOUT", "15"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY", "2"))
