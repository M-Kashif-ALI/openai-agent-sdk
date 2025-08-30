from .connection import gemini_model
from agents import Agent, Runner, ModelSettings, SQLiteSession, set_tracing_disabled 
from pydantic import BaseModel

set_tracing_disabled(disabled=True)

session_memory = SQLiteSession("user_2", "conversation.db")

def main():
  agent = Agent(
    name= "Assistant",
    instructions="You are a helpfull assitant",
    model_settings=ModelSettings(
      temperature=0.5,
      ),
    model=gemini_model
  )

  while True:
    
    prompt = input("You: ").strip().lower()
    
    if not prompt:
      print("Please enter some query or type exit to leave.")
      continue
    elif prompt in "exit":
      print("Goodbye!")
      break
    
    result = Runner.run_sync(
      starting_agent=agent,
      input=prompt,
      session=session_memory
    )
    
    print("Agent:", result.final_output)
    
    
if __name__ == "__main__":
    main()
    
