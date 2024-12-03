import google.generativeai as genai
from datetime import datetime
from config import GEMINI_API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS

genai.configure(api_key=GEMINI_API_KEY)

def create_model(username=None):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    system_instruction = f"Current date: {current_date}"
    
    if username:
        system_instruction += f"\nCurrent User: {username}"

    return genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0801",
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
        system_instruction=system_instruction
    )