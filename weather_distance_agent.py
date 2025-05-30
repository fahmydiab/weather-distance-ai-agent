import requests
import math
import sys
import os
from strands import Agent, tool
from strands_tools import calculator
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

# Disable proxies globally for all requests
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# Initialize the geocoder with a custom user agent
geocoder = Nominatim(user_agent="weather_distance_agent/1.0")

# Tool to get weather information for a city
@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a specified city.
    
    Args:
        city (str): The name of the city to get weather for
        
    Returns:
        str: Weather information for the specified city
    """
    try:
        # Using wttr.in - a free weather API that doesn't require an API key
        url = f"https://wttr.in/{city}?format=%l:+%C+%t+%h+%w"
        
        # Create a session that doesn't use proxies
        session = requests.Session()
        session.trust_env = False  # Don't use environment variables for proxy
        
        response = session.get(url, headers={"User-Agent": "curl/7.64.1"})
        
        if response.status_code == 200:
            weather_info = response.text.strip()
            return f"Weather: {weather_info}"
        else:
            return f"Error getting weather for {city}: HTTP status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Dictionary of major city coordinates as fallback (latitude, longitude)
CITY_COORDINATES = {
    "giza": (29.9773, 31.1325),  # Keep Giza coordinates for fallback
}

# Tool to calculate distance from Giza
@tool
def distance_from_giza(city: str) -> str:
    """
    Calculate the approximate distance between a city and Giza, Egypt.
    
    Args:
        city (str): The name of the city to calculate distance from Giza
        
    Returns:
        str: Distance information between the city and Giza
    """
    # Giza coordinates (latitude, longitude)
    giza_lat = 29.9773
    giza_lon = 31.1325
    giza_coords = (giza_lat, giza_lon)
    
    try:
        # Try to geocode the city
        location = geocoder.geocode(city, exactly_one=True)
        
        # If geocoding successful, calculate distance
        if location:
            city_coords = (location.latitude, location.longitude)
            
            # Calculate distance using geodesic distance (more accurate than Haversine)
            distance_km = geodesic(giza_coords, city_coords).kilometers
            distance_miles = distance_km / 1.609
            
            return f"Distance from {city} to Giza, Egypt: {distance_km:.2f} kilometers ({distance_miles:.2f} miles)"
        else:
            # Fallback to our dictionary for common cities
            city_lower = city.lower()
            if city_lower in CITY_COORDINATES:
                city_lat, city_lon = CITY_COORDINATES[city_lower]
                city_coords = (city_lat, city_lon)
                distance_km = geodesic(giza_coords, city_coords).kilometers
                distance_miles = distance_km / 1.609
                return f"Distance from {city} to Giza, Egypt: {distance_km:.2f} kilometers ({distance_miles:.2f} miles)"
            else:
                return f"Could not find coordinates for {city}. Please try a different city name or format."
    
    except Exception as e:
        return f"Error calculating distance: {str(e)}"

# Simple function to process queries without using an AI model
def process_query(query):
    query = query.lower()
    
    if "weather" in query or "temp" in query or "temperature" in query:
        # Extract city name - this is a simple approach
        # Try to extract city name from the query
        city = extract_city_from_query(query)
        if city:
            # Get both weather and distance information
            weather_info = get_weather(city)
            # Add a small delay to avoid rate limiting from geocoding service
            time.sleep(1)
            distance_info = distance_from_giza(city)
            return f"{weather_info}\n\n{distance_info}"
        return "Please specify a city for weather information."
    
    elif "distance" in query or "far" in query or "from giza" in query:
        # Extract city name
        city = extract_city_from_query(query)
        if city:
            return distance_from_giza(city)
        return "Please specify a city to calculate distance from Giza."
    
    elif "help" in query:
        return """I can help you with:
1. Weather information for any city (e.g., "What's the weather in London?")
2. Distance from Giza, Egypt to any city (e.g., "How far is Tokyo from Giza?")

You can ask about any city in the world, and I'll try to find its coordinates and calculate the distance."""
    
    else:
        return """I'm not sure what you're asking. I can help with:
1. Weather information (e.g., "What's the weather in London?")
2. Distance from Giza (e.g., "How far is Tokyo from Giza?")

Type 'help' for more information."""

# Helper function to extract city name from query
def extract_city_from_query(query):
    # List of common prepositions and articles that might precede city names
    prepositions = ["in", "at", "for", "from", "to", "of", "about"]
    
    # Split the query into words
    words = query.lower().split()
    
    # Look for city names after prepositions
    for i, word in enumerate(words):
        if word in prepositions and i < len(words) - 1:
            # Take all words after the preposition as the city name
            potential_city = " ".join(words[i+1:])
            # Remove punctuation from the end
            potential_city = potential_city.rstrip(",.!?;:")
            return potential_city
    
    # If no preposition found, try to find known city names in the query
    for city in CITY_COORDINATES.keys():
        if city in query:
            return city
    
    # If no city found, return None
    return None

# Function to check if Ollama server is running
def is_ollama_running():
    try:
        # Create a session that doesn't use proxies
        session = requests.Session()
        session.trust_env = False  # Don't use environment variables for proxy
        response = session.get("http://localhost:11434/api/version", timeout=2)
        return response.status_code == 200
    except:
        return False

# Function to run the agent
def run_agent():
    print("Welcome to the Weather & Distance from Giza Agent!")
    print("Ask about the weather in any city or its distance from Giza.")
    print("Type 'exit' to quit.")
    
    # Check if Ollama server is running
    if is_ollama_running():
        print("\nOllama server detected! Using Llama 3.2 model.")
        try:
            # Import here to avoid errors if not installed
            from strands.models.ollama import OllamaModel
            
            # Create Ollama model provider with Llama 3.2
            ollama_model = OllamaModel(
                host="http://localhost:11434",  # Default Ollama server address
                model_id="llama3.2:latest",  # Using Llama 3.2 model
                temperature=0.7,
                client_args={"proxies": None}  # Disable proxies for Ollama client
            )
            
            # Create the agent with Ollama model
            agent = Agent(
                model=ollama_model,
                tools=[get_weather, distance_from_giza, calculator],
                system_prompt="""You are a helpful assistant that provides weather information and calculates distances from Giza, Egypt.
You can get the current weather for any city and calculate how far it is from the Great Pyramids of Giza.
Always provide both metric and imperial units when discussing distances.
Be friendly and informative in your responses.
When a user asks about the weather or temperature of a city, always include the distance from Giza in your response.
If you can't find a city's coordinates, let the user know and suggest they try a different spelling or a major city nearby."""
            )
            
            # Use AI-powered agent
            use_ai = True
        except Exception as e:
            print(f"\nError initializing Llama 3.2 model: {str(e)}")
            print("Falling back to rule-based agent.")
            use_ai = False
    else:
        print("\nOllama server not detected. Using rule-based agent.")
        print("To use the Llama 3.2 model, please start Ollama with: ollama serve")
        print("And make sure to pull the model with: ollama pull llama3.2:latest")
        use_ai = False
    
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if use_ai:
            # Process the user's query with the AI agent
            try:
                response = agent(user_input)
                print(f"\nAgent: {response.message}")
            except Exception as e:
                print(f"Error with AI model: {str(e)}")
                print("Falling back to rule-based processing...")
                response = process_query(user_input)
                print(f"\nAgent: {response}")
        else:
            # Process the query directly without using an AI model
            response = process_query(user_input)
            print(f"\nAgent: {response}")

# Run the agent if this script is executed directly
if __name__ == "__main__":
    run_agent()
