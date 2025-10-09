import requests
from datetime import datetime
from zoneinfo import ZoneInfo


def geocode(city_name):
    """Look up latitude/longitude for a city using Open-Meteo geocoding API."""
    print(f"[TOOL] Executing geocode with parameters: city_name='{city_name}'")
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
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
    except Exception as e:
        return {"error": str(e)}


def get_weather(latitude, longitude):
    """Get weather information from weather.gov API."""
    print(f"[TOOL] Executing get_weather with parameters: latitude={latitude}, longitude={longitude}")
    try:
        url = f"https://api.weather.gov/points/{latitude},{longitude}"
        headers = {"User-Agent": "ReActAgent/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Get forecast URL
        forecast_url = data["properties"]["forecast"]
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
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
    except Exception as e:
        return {"error": str(e)}


def get_time(timezone):
    """Get current time for a timezone."""
    print(f"[TOOL] Executing get_time with parameters: timezone='{timezone}'")
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
    if tool_name == "geocode":
        return geocode(parameters)
    elif tool_name == "weather":
        # Parameters should be "latitude,longitude"
        parts = parameters.split(',')
        if len(parts) == 2:
            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                return get_weather(lat, lon)
            except ValueError:
                return {"error": "Invalid latitude/longitude format"}
        return {"error": "Weather requires latitude,longitude"}
    elif tool_name == "time":
        return get_time(parameters)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

