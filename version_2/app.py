import os
import ollama
import google.generativeai as genai
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")

def get_weather_data(location):
    """Get weather data for a location using Gemini API (free solution)"""
    try:
        # Use Gemini to get current weather information
        weather_prompt = f"""
        What is the current weather in {location}? 
        Include only these pieces of information in a JSON format: temperature in Celsius, 
        weather description, humidity percentage, and wind speed in m/s.
        
        Format your answer as a valid JSON object with these exact keys:
        {{
          "temp": (temperature as a number),
          "description": (weather condition as a string),
          "humidity": (humidity as a number),
          "wind_speed": (wind speed as a number),
          "icon": (one of: "01d" for clear sky, "02d" for few clouds, "03d" for scattered clouds, 
                  "04d" for broken clouds, "09d" for shower rain, "10d" for rain, 
                  "11d" for thunderstorm, "13d" for snow, "50d" for mist)
        }}
        
        Provide ONLY the JSON object, nothing else.
        """
        
        weather_response = model.generate_content(weather_prompt)
        weather_text = weather_response.text
        
        # Extract JSON from the response
        json_match = re.search(r'\{.*\}', weather_text, re.DOTALL)
        if json_match:
            weather_json = json_match.group(0)
            try:
                weather_data = json.loads(weather_json)
                # Ensure all required fields are present
                required_fields = ["temp", "description", "humidity", "wind_speed", "icon"]
                if all(field in weather_data for field in required_fields):
                    return weather_data
            except json.JSONDecodeError:
                pass
                
        # If JSON extraction fails, create a placeholder with estimated data
        # This ensures the app continues to function even if parsing fails
        fallback_weather = {
            "temp": 22,  # default reasonable temperature
            "description": "weather information unavailable",
            "humidity": 60,
            "wind_speed": 5,
            "icon": "01d"  # default to clear sky icon
        }
        return fallback_weather
        
    except Exception as e:
        print(f"Weather data error: {str(e)}")
        return None

def get_local_time(location):
    """Get approximate local time for a location"""
    try:
        # For precise time, you would use a geocoding API + timezone API
        # This is a simplified version
        url = f"http://worldtimeapi.org/api/timezone/Etc/UTC"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("datetime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Time API error: {str(e)}")
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_currency_exchange(base="USD"):
    """Get currency exchange rates"""
    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("rates", {})
        else:
            return {}
    except Exception as e:
        print(f"Currency API error: {str(e)}")
        return {}

def get_travel_info(travel_option, travel_location):
    """Get travel information using both Gemini and Ollama"""
    
    # Current date for up-to-date recommendations
    current_date = datetime.now().strftime("%B %d, %Y")
    
    try:
        # Get additional context from Gemini for more informed recommendations
        context_prompt = f"""
        Provide factual, current information about {travel_location} as a travel destination.
        Include details about:
        - Current season and typical weather
        - Any notable ongoing events or seasonal activities
        - Recent travel advisories or situations travelers should know about
        - Cultural considerations for visitors
        Keep your response under 200 words and focus on facts that would be relevant for 
        travelers interested in {travel_option} as of {current_date}.
        """
        
        context_response = model.generate_content(context_prompt)
        destination_context = context_response.text
        
        # Use Ollama with the enriched context for personalized recommendations
        enriched_prompt = f"""
        Context information about {travel_location}: {destination_context}
        
        Based on this context and current information as of {current_date}, provide 5 excellent {travel_option} 
        recommendations for {travel_location}. For each recommendation:
        
        1. Provide a specific name/place
        2. Add a brief description (2-3 sentences)
        3. Mention any practical tips (best time to visit, cost range, etc.)
        
        Format as a clean JSON array with "name", "description", and "tips" keys for each item.
        """
        
        # Get recommendations from Ollama
        ollama_response = ollama.generate(
            model="llama3.2", 
            prompt=enriched_prompt
        )
        
        # Try to extract JSON from the response
        response_text = ollama_response['response']
        
        # Look for JSON array in the response
        try:
            # Try to find and parse JSON in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                recommendations = json.loads(json_str)
            else:
                # If no valid JSON array was found, format the text response
                recommendations = [{"name": "Formatted Recommendations", 
                                   "description": response_text,
                                   "tips": ""}]
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response with minimal formatting
            recommendations = [{"name": "Travel Recommendations", 
                               "description": response_text,
                               "tips": ""}]
        
        return {
            "recommendations": recommendations,
            "context": destination_context
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "recommendations": [{"name": "Error", "description": f"Error generating recommendations: {str(e)}", "tips": "Please try again later"}],
            "context": "Could not retrieve context information."
        }

@app.route('/', methods=["GET", "POST"])
def main():
    result = None
    weather = None
    local_time = None
    currency_rates = None
    context_info = None
    
    if request.method == "POST":
        travel_option = request.form.get("option")
        travel_location = request.form.get("location")
        
        # Get local info
        weather = get_weather_data(travel_location)
        local_time = get_local_time(travel_location)
        currency_rates = get_currency_exchange()
        
        # Get travel recommendations
        travel_data = get_travel_info(travel_option, travel_location)
        result = travel_data.get("recommendations")
        context_info = travel_data.get("context")
    
    return render_template(
        "index.html", 
        result=result, 
        weather=weather, 
        local_time=local_time, 
        currency_rates=currency_rates,
        context_info=context_info
    )

@app.route('/api/weather', methods=["GET"])
def get_weather():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Location required"}), 400
        
    weather_data = get_weather_data(location)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Could not retrieve weather data"}), 500

if __name__ == "__main__":
    app.run(debug=True)