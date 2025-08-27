from agents import Agent, Runner, set_tracing_disabled, ModelSettings, RunContextWrapper, function_tool
from agent_tool_calling.assignment.connection import gemini_model
from pydantic import BaseModel
import os
from dotenv import load_dotenv 
import requests

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")
currency_api_key = os.getenv("CURRENCY_API_KEY")

set_tracing_disabled(disabled=True)

class userContext(BaseModel):
  user_id: int
  tier: str = "free"
  role: str = "user"
  
  
def is_premium_enabled(ctx: RunContextWrapper, agent: Agent):
    is_enabled = ctx.context.tier.lower() == "premium"
    if is_enabled:
        print("✅ Premium is enabled")
        return True
    else:
        print("ℹ️ You are in free tier.")
        return False
    

def is_admin(ctx: RunContextWrapper, agent: Agent):
    is_admin = ctx.context.role.lower() == "admin"
    if is_admin:
        print("✅ Admin access granted")
        return True
    else:
        print("ℹ️ You are a normal user.")
        return False
    

def premium_or_admin(ctx: RunContextWrapper, agent: Agent):
    return is_premium_enabled(ctx, agent) or is_admin(ctx, agent)
    
@function_tool
def get_weather(city: str) -> str:
  """
    Fetches the current weather for a given city using WeatherAPI.
    
    Args:
        city (str): The name of the city to fetch weather for.
    
    Returns:
        str: A formatted string with temperature (°C) and condition,
             or an error message if the API call fails.
    """
  try:
        response = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
        )
        
        if response.status_code != 200:
            return f"⚠️ Error: Could not fetch weather for {city}. (Status {response.status_code})"
        
        data = response.json()
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        
        return f"The current weather in {city} is {temp}°C with {condition}."
    
  except Exception as e:
        return f"⚠️ Error while fetching weather for {city}: {str(e)}"


@function_tool(is_enabled=premium_or_admin)
def currency_tool(base_currency: str, target_currency: str, amount: int | float = 1):
    """
    🔥 added
    Converts a given amount from one currency to another using ExchangeRate-API.
    
    Args:
        base_currency (str): The source currency code (e.g., 'USD').
        target_currency (str): The target currency code (e.g., 'PKR').
        amount (int | float, optional): The amount to convert. Defaults to 1.
    
    Returns:
        str: A formatted string showing the converted value,
             or an error message if the API call fails.
    🔥 added
    """
    base_currency = base_currency.upper()
    target_currency = target_currency.upper()
  
    try:
        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/{currency_api_key}/pair/{base_currency}/{target_currency}/{amount}"
        )
        data = response.json()
        if "conversion_result" in data:
            return f"{amount} {base_currency} = {data['conversion_result']} {target_currency}"
        else:
            return f"⚠️ Error: {data}"
    except Exception as e:
        return {"error": str(e)}
  

@function_tool(is_enabled=is_admin)
def get_user_data(by_id:int) -> list:
    """
    Fetch user data from the JSONPlaceholder API by user ID.

    Args:
        by_id (int): The unique identifier of the user to retrieve.

    Returns:
        list: A list containing the user's data as a JSON object.

    Notes:
        - The data is fetched from the public testing API (https://jsonplaceholder.typicode.com).
        - Ensure that the `is_admin` flag is enabled before using this function.
    """
    url = f"https://jsonplaceholder.typicode.com/users/{by_id}"
    res = requests.get(url)
    return res.json()

gemini_agent = Agent(
    name="Tier manager agent",
    instructions="You are an intelligent agent responsible for managing user subscription tiers and delivering services based on their plan.",
    model=gemini_model,
    model_settings=ModelSettings(
      temperature=0.4,
    ),
    tools=[get_weather, currency_tool, get_user_data]
  )


def main():
  
  context = userContext(user_id=1, tier="free", role="user")
  context1 = userContext(user_id=2, tier="premium", role="user")
  context2 = userContext(user_id=3, tier="free", role="admin")
  
  
  while True:
    prompt = input("You: ").lower().strip()
    
    if not prompt:
      print("Please enter your queries, or type 'exit' or 'quit' to leave.")
      continue
    
    if prompt in ("exit", "quit"):
      print("Goodbye")
      break
    
    try:
        result = Runner.run_sync(
            starting_agent=gemini_agent,
            input=prompt,
            context=context2
        )
        print("Agent:", result.final_output)
    except Exception as e:
        print(f"⚠️ Agent error: {str(e)}")
    
    
if __name__ == "__main__":
    main()