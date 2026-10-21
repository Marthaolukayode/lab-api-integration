import os
import time
from openai import OpenAI
from anthropic import Anthropic
from typing import Optional, Dict, Any, Iterator
from cohere import ClientV2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cohere_client = ClientV2(api_key=os.getenv("COHERE_API_KEY"))             
# anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
DAILY_BUDGET = float(os.getenv("DAILY_BUDGET", "5.00"))

# Default models
OPENAI_MODEL = "gpt-4o-mini"
COHERE_MODEL = "command-a-plus-05-2026"
ANTHROPIC_MODEL = ""

print("✅ Setup complete!")

def validate_config():
    """Check that all required API keys are available."""

    missing_keys = []

    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")

    if not os.getenv("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")

    if not NEWS_API_KEY:
        missing_keys.append("NEWS_API_KEY")

    if missing_keys:
        print("Missing API keys:", ", ".join(missing_keys))
        return False

    print("Configuration validated successfully!")
    return True

if __name__ == "__main__":
    validate_config()