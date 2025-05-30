#!/usr/bin/env python3
import sys
from weather_distance_agent import get_weather, distance_from_giza

def test_agent():
    """
    Test the agent's core functionality without running the full interactive loop
    """
    print("Testing Weather and Distance from Giza Agent...")
    
    # Test cities
    test_cities = ["London", "Tokyo", "New York", "Sydney", "Cairo", "Mumbai"]
    
    for city in test_cities:
        print(f"\n--- Testing with city: {city} ---")
        
        # Test weather function
        print("\nWeather information:")
        weather_result = get_weather(city)
        print(weather_result)
        
        # Test distance function
        print("\nDistance information:")
        distance_result = distance_from_giza(city)
        print(distance_result)
        
        print("-" * 50)
    
    print("\nTesting complete!")

if __name__ == "__main__":
    test_agent()
