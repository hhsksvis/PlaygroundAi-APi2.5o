import os
from datetime import datetime
import google.generativeai as genai

# API Configuration
GEMINI_API_KEY = "AIzaSyCTqTUGgSZSsQXo0MPd7Ig0jxPoDICSvV4"
WEBHOOK_URL = "https://discord.com/api/webhooks/1280499522597814363/u155heIK-SIx8H5RilXa9FVPp-TO-e7bYQOr9u5KGEaVgJwfpUApf5tUEkxGzIE0N7zx"

# Model Configuration
GENERATION_CONFIG = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 55,
    "max_output_tokens": 2000000,
    "response_mime_type": "text/plain",
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Server Configuration
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5000