from agents import Agent, Runner, set_tracing_disabled, ModelSettings
from agent_tool_calling.assignment.connection import gemini_model
from agent_tool_calling.assignment.tool import calculator_tool

set_tracing_disabled(disabled=True)


def main():
  math_agent = Agent(
    name = "Math Agent",
    instructions = "You are an intelligent and reliable math assistant, specializing in solving problems, explaining concepts clearly, and providing accurate step-by-step solutions.",
    model_settings=ModelSettings(
      temperature=0.1,
      ),
    tools = [calculator_tool],
    model=gemini_model
  )
  
  while True:
    
    prompt = input("You: ").lower().strip()
    
    if not prompt:
      print("Please enter your queries, or type 'exit' or 'quit' to leave.")
      continue
    
    if prompt in ("exit", "quit"):
      print("Goodbye")
      break
    
    result = Runner.run_sync(
      starting_agent=math_agent,
      input=prompt
    )
    
    
    print("Agent:", result.final_output)
    
    
if __name__ == "__main__":
    main()