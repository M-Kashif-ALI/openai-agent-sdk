from streaming_agent_clone.assignment.connection import gemini_model
from agents import Agent, Runner, set_tracing_disabled, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from pydantic import BaseModel


set_tracing_disabled(disabled=True)

class SelectAgent(BaseModel):  switch_to: str = "General"


async def main():
  print("Welcome! You can switch agent anytime using:")
  print("  switch to [General | Friendly | Precise]\n")
  
  user = SelectAgent()
  
  general_agent = Agent(
    name = "General Agent",
    instructions = """
        You are a reliable and versatile assistant.  
        Provide clear, accurate, and well-structured responses across a wide range of topics.  
        Focus on being practical, trustworthy, and easy to understand.  
        """,
    model_settings=ModelSettings(
      temperature=0.6,
      ),
    model=gemini_model
  )
  
  agents = {
    "general": {
            "agent": general_agent,
            "intro": "👋 Hello! I’m your General Agent. I can help with a wide range of tasks, giving clear and accurate answers."
        },
    
    "friendly": {
            "agent": general_agent.clone(
                name="Friendly Agent",
                instructions = """
                    You are a warm, supportive, and approachable assistant.  
                    Communicate in a polite and encouraging tone, adding emojis where helpful 😊✨.  
                    Make users feel comfortable, valued, and motivated while answering their questions.  
                    """,
                model_settings=ModelSettings(temperature=0.8),
            ),
            "intro": "😊 Hey there! I’m your Friendly Agent. I’ll chat with you in a supportive way."
        },
    "precise": {
            "agent": general_agent.clone(
                name="Precise Agent",
                instructions = """
                  You are a precise and efficient assistant.  
                  Deliver short, clear, and accurate answers without unnecessary detail.  
                  Focus on being direct, professional, and to-the-point.  
                  """,
                model_settings=ModelSettings(temperature=0.2),
            ),
            "intro": "📌 Hello. I’m your Precise Agent. I’ll keep my answers short, clear, and straight to the point."
        },
  }
  
  current_agent = agents["general"]["agent"]
  
  while True:
    
    prompt = input(f"You [{user.switch_to}]: ").strip()
    
    if not prompt:
      print("⚠️ Please enter your queries, or type 'exit' or 'quit' to leave.")
      continue
    
    if prompt.lower() in ("exit", "quit"):
      print("Goodbye")
      break
    
    if prompt.lower().startswith("switch to"):
      selected_agent = prompt[len("switch to") :].strip().lower()
      if selected_agent in agents:
          user.switch_to = selected_agent.capitalize()
          current_agent = agents[selected_agent]["agent"]
          print(f"\n✅ Agent switched to {user.switch_to}")
          print(agents[selected_agent]["intro"])
      else:
                print("⚠️ Unknown agent. Please choose: General | Friendly | Precise")
      continue
    
    result = Runner.run_streamed(
      starting_agent=current_agent,
      input=prompt
    )
    
    
    async for event in result.stream_events():
      if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)
    
      
asyncio.run(main())