import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("FEATHERLESS_API_KEY")

if not api_key:
    raise ValueError("FEATHERLESS_API_KEY not found in .env")

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=api_key
)

MODEL = "Qwen/Qwen3.5-9B"