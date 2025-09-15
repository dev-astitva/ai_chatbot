from google import genai
from google.genai import types
from config import load_conf
import os

conf = load_conf()
api_key = conf.get("google_api_key") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Google Gemini API key not set in config or environment variable.")

client = genai.Client(api_key=api_key)

def chat_gemini(msg, history=None):
    contents = [{"parts": [{"text": msg}]}]
    conf_opts = {"thinkingConfig": {"thinkingBudget": 0}}
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=conf_opts
    )
    return response.text
