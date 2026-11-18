
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

if api_key:
    print("OpenAI API key loaded successfully!")
    print("API key configured:", True)
    print("Model:", model)
else:
    print("OpenAI API key not found!")
