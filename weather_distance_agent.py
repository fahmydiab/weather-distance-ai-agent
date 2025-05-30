import requests
import math
import sys
import os
from strands import Agent, tool
from strands_tools import calculator

# Disable proxies globally for all requests
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

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

# Dictionary of major city coordinates (latitude, longitude)
CITY_COORDINATES = {
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "paris": (48.8566, 2.3522),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "cairo": (30.0444, 31.2357),
    "giza": (29.9773, 31.1325),
    "beijing": (39.9042, 116.4074),
    "moscow": (55.7558, 37.6173),
    "dubai": (25.2048, 55.2708),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "toronto": (43.6532, -79.3832),
    "mexico city": (19.4326, -99.1332),
    "sao paulo": (-23.5505, -46.6333),
    "mumbai": (19.0760, 72.8777),
    "singapore": (1.3521, 103.8198),
    "berlin": (52.5200, 13.4050),
    "rome": (41.9028, 12.4964),
    "madrid": (40.4168, -3.7038),
    "amsterdam": (52.3676, 4.9041),
    "bangkok": (13.7563, 100.5018),
    "seoul": (37.5665, 126.9780),
    "johannesburg": (-26.2041, 28.0473),
    "istanbul": (41.0082, 28.9784),
    "rio de janeiro": (-22.9068, -43.1729),
    "san francisco": (37.7749, -122.4194),
    "barcelona": (41.3851, 2.1734),
    "vienna": (48.2082, 16.3738),
    "athens": (37.9838, 23.7275),
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
    
    # Normalize city name for lookup
    city_lower = city.lower()
    
    # Check if we have the coordinates for this city
    if city_lower in CITY_COORDINATES:
        city_lat, city_lon = CITY_COORDINATES[city_lower]
    else:
        # For cities not in our database, use a fallback approach
        # This is a simplified approach that doesn't require an API key
        return f"I don't have the exact coordinates for {city} in my database. I can provide distances for major cities like New York, London, Paris, Tokyo, etc."
    
    # Calculate distance using Haversine formula
    R = 6371  # Earth radius in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(giza_lat)
    lon1 = math.radians(giza_lon)
    lat2 = math.radians(city_lat)
    lon2 = math.radians(city_lon)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return f"Distance from {city.title()} to Giza, Egypt: {distance:.2f} kilometers ({distance/1.609:.2f} miles)"

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

# Simple function to process queries without using an AI model
def process_query(query):
    query = query.lower()
    
    if "weather" in query:
        # Extract city name - this is a simple approach
        for city in CITY_COORDINATES.keys():
            if city in query:
                return get_weather(city)
        return "Please specify a city for weather information."
    
    elif "distance" in query or "far" in query or "from giza" in query:
        # Extract city name
        for city in CITY_COORDINATES.keys():
            if city in query:
                return distance_from_giza(city)
        return "Please specify a city to calculate distance from Giza."
    
    elif "help" in query:
        return """I can help you with:
1. Weather information for major cities (e.g., "What's the weather in London?")
2. Distance from Giza, Egypt to major cities (e.g., "How far is Tokyo from Giza?")

Available cities: New York, London, Paris, Tokyo, Sydney, Cairo, Beijing, Moscow, Dubai, Los Angeles, Chicago, Toronto, Mexico City, Sao Paulo, Mumbai, Singapore, Berlin, Rome, Madrid, Amsterdam, Bangkok, Seoul, Johannesburg, Istanbul, Rio de Janeiro, San Francisco, Barcelona, Vienna, Athens."""
    
    else:
        return """I'm not sure what you're asking. I can help with:
1. Weather information (e.g., "What's the weather in London?")
2. Distance from Giza (e.g., "How far is Tokyo from Giza?")

Type 'help' for more information."""

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
For cities not in your database, let the user know which major cities you can calculate distances for."""
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
