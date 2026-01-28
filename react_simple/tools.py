import requests
from datetime import datetime
from zoneinfo import ZoneInfo


def make_request(url, headers=None, timeout=10):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)


def geocode(city_name: str):
    """Look up latitude/longitude for a city."""
    #print(f"[TOOL] Executing geocode with parameters: city_name='{city_name}'")
    
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    success, data = make_request(url)
    
    if not success:
        return {"error": data}
    
    if "results" in data and len(data["results"]) > 0:
        result = data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result.get("country", ""),
            "timezone": result.get("timezone", "")
        }
    else:
        return {"error": f"City '{city_name}' not found"}


def weather(coordinates: str):
    """Get weather information from weather.gov API.
    
    Args:
        coordinates: String in format "latitude, longitude"
    
    Example API call:
    curl -L -H "User-Agent: ReActAgent/1.0" "https://api.weather.gov/points/47.6062,-122.3321"
        Given properties->forecast, curl that URL for the forecast data
    """
    #print(f"[TOOL] Executing weather with parameters: coordinates='{coordinates}'")
    
    # Parse the coordinates string
    parts = coordinates.split(',')
    try:
        latitude = float(parts[0].strip())
        longitude = float(parts[1].strip())
    except (ValueError, IndexError):
        return {"error": "Invalid latitude/longitude values"}
    
    # Step 1: Get the forecast URL from the points endpoint
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    success, data = make_request(url)
    
    if not success:
        return {"error": data}
    
    # Step 2: Get the forecast from the forecast URL
    forecast_url = data["properties"]["forecast"]
    success, forecast_data = make_request(forecast_url)
    
    if not success:
        return {"error": forecast_data}
    
    # Get first period (current/upcoming)
    if forecast_data["properties"]["periods"]:
        period = forecast_data["properties"]["periods"][0]
        return {
            "period": period["name"],
            "temperature": period["temperature"],
            "temperatureUnit": period["temperatureUnit"],
            "shortForecast": period["shortForecast"],
            "detailedForecast": period["detailedForecast"]
        }
    
    return {"error": "No forecast data available"}


def time(timezone):
    """Get current time for a timezone.
    
    Note: This is computed locally using Python's datetime and zoneinfo,
    not via an external API call.
    """
    #print(f"[TOOL] Executing time with parameters: timezone='{timezone}'")
    try:
        tz = ZoneInfo(timezone)
        current_time = datetime.now(tz)
        return {
            "timezone": timezone,
            "time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "formatted": current_time.strftime("%I:%M %p")
        }
    except Exception as e:
        return {"error": str(e)}


def execute_tool(tool_name, parameters):
    """Execute a tool with given parameters."""
    tools = {
        "geocode": geocode,
        "weather": weather,
        "time": time
    }
    
    tool = tools.get(tool_name)
    if tool:
        return tool(parameters)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

