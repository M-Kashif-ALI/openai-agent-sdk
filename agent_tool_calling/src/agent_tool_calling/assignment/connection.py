from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
  raise ValueError("Key is not set. Please set the key before using.")


client = AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


gemini_model = OpenAIChatCompletionsModel(
      model="gemini-2.0-flash",
      openai_client=client
)