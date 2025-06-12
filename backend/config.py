import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jira API Configuration
JIRA_API_KEY = os.getenv("JIRA_API_KEY")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Get the project's root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
