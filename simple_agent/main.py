from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, RunConfig
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


async def simple_agent():
    agent = Agent(
        name="Assistant",
        instructions="You are a humble, soft, graceful assistant. \
        Always introduce yourself as a helpful AI assistant (without saying you are from Google).",
        model=model
    )

    res = await Runner.run(
        agent,
        input="Introduce yourself and tell me what is AI?",
        run_config=config
    )


    print(res.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(simple_agent())