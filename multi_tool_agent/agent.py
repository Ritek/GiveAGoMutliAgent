import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, SequentialAgent

# -----------------------
# Tools
# -----------------------

def get_weather(city: str) -> str:
    if city.lower() == "new york":
        return "The weather in New York is sunny with a temperature of 25°C (77°F)."
    else:
        return f"Weather information for '{city}' is not available."

def get_current_time(city: str) -> str:
    if city.lower() != "new york":
        return f"Sorry, I don't have timezone information for {city}."
    tz = ZoneInfo("America/New_York")
    now = datetime.datetime.now(tz)
    return f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'


# -----------------------
# Agents (only valid fields)
# -----------------------

time_agent = Agent(
    name="time_agent",
    model="gemini-2.5-flash",
    description="Get the time for a {data} and return it.",
    tools=[get_current_time],
    output_key="city_time",
)

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Get the weather for a city {city} and return it.",
    tools=[get_weather],
    output_key="city_weather",
)

# -----------------------
# Sequential pipeline
# -----------------------

pipeline_agent = SequentialAgent(
    name="TimeWeatherPipeline",
    description="Gets time, then weather, for a city.",
    sub_agents=[time_agent, weather_agent],
)

root_agent = pipeline_agent
