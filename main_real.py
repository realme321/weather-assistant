from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import requests
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.
    Return temperature in Fareheit and weather description."""
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        'units': 'metric'  # Use 'metric' for Celsius
    }
    # In a real implementation, you would make an API call here
    response = requests.get(base_url, params=params)
    data = response.json()
    temperature_celsius = data['main']['temp']
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32
    return f"Temperature: {temperature_fahrenheit:.2f}°F, Description: {data['weather'][0]['description']}"
@tool
def get_location():
    """Get the current location of the user. Use these coordinates to get the weather."""
    response = requests.get("https://ipinfo.io/json", timeout=10)
    data = response.json()
    city= data['city']
    country = data.get('country')
    return f"{city}, {country}"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)
system_prompt = """You are a helpful weather assistant.
YOUR WORKFLOW:
1. if the user asks about the weather WITHOUT providing a city, use the get_location tool to determine their location.
 - Then, use the get_weather tool to get the weather for the determined location.
 2. if the user asks about the weather WITH a city, use the get_weather tool to get the weather for that city.
"""
connection = SqliteSaver.from_conn_string('checkpoints.db')
checkpointer = connection.__enter__()   
 
agent = create_agent(
        model=llm,
        tools=[get_weather, get_location],
        system_prompt=system_prompt,
        checkpointer=checkpointer  # Use InMemorySaver for checkpointing
    )

         
