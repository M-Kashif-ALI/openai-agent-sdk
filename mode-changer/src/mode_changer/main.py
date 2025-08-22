# imports
from agents import Agent, OpenAIChatCompletionsModel, Runner, AsyncOpenAI, RunContextWrapper, RunConfig
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
  raise ValueError("Api key is not set in .env file")

client = AsyncOpenAI(
  api_key=gemini_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

gemini_model = OpenAIChatCompletionsModel(
      model="gemini-2.0-flash",
      openai_client=client
)

config = RunConfig(
  model=gemini_model,
  model_provider=client,
  tracing_disabled=True
)


class user_info(BaseModel):
  name: str
  mode: str = "shakespeare"   
  
def dynamic_instructions(context: RunContextWrapper, agent: Agent):
  """
    Return dynamic instructions for the agent’s speaking style 
    (Shakespeare, Gen Z, or normal) while talking to the user.
  """
  
  name = getattr(context.context, "name", "user")
  mode = getattr(context.context, "mode", "shakespere")
  
  if mode == "shakespeare":
    return f"Thou art a noble assistant. Speak in the tongue of Shakespeare, with poetic grace and olden charm, whilst conversing with {name}."
  elif mode == "genz":
      return f"Yo fam, you’re a chill AI. Talk like Gen Z — casual, short, full of vibes, memes, and slang, while chatting with {name}."
  else:
      return f"You are a helpful assistant. Speak normally in simple, clear English while talking to {name}."
  

def main():
  
  user = user_info(name="Kashif", mode="shakespeare")
  
  
  while True:
    user_input = input("You: ").lower().strip()
    
    
    if not user_input:
      continue
    
    if user_input.lower() in ("exit", "quit"):
      print("Goodbye!")
      break
    
    
    if user_input.lower().startswith("switch to"):
      new_mode = user_input[ len("switch to") : ].strip().lower()
      
      if new_mode in ("shakespeare","genz"):
        user.mode = new_mode
        
        print(f"Mode switched to {user.mode}")
        
      else:
        print("This mode is not Available right now. Only (shakespeare and genz) mode availabke right now")
        
      continue 
    
    agent = Agent(
      name="mode changer",
      instructions=dynamic_instructions
    )
    
    response  = Runner.run_sync(
      agent,
      input=user_input,
      run_config=config,
      context=user
    )
    
    print("Bot ", response .final_output)