from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
import requests
import os


# Create your views here.

class HelloView(APIView):
    def get(self,request):
        visitor_name = request.query_params.get('visitor_name', 'Guest')
        # client_ip  = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        client_ip = '105.112.17.199'
        # print(client_ip)
        # Geting location based on visitor ip address
        
        try:
            geo_response = requests.get( f'http://ip-api.com/json/{client_ip}')
            geo_response.raise_for_status()
            goe_data = geo_response.json()
            # print(geo_response.json)
            city = goe_data.get('city', 'Unknown')
        
            if city == 'Unknown':
                raise ValueError("City name could not be determined from IP.")
        except requests.RequestException as e:
            return Response({"error": "Failed to get location data.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as ve:
            return Response({"error": "Failed to determine city name.", "details": str(ve)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Getting the weather Information 
        try:
            weather_api_key = settings.WEATHER_API_KEY
            weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            
            weather_data = weather_response.json()
            print("Weather Data: ",weather_data)
            if 'current' in weather_data:
                temperature = weather_data['current']['temp_c']
            else:
                raise KeyError("The 'current' key is not in the weather data.")
        except requests.HTTPError as http_err:
            return Response({"error": "Failed to get weather data.", "details": f"HTTP error occurred: {http_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.RequestException as req_err:
            return Response({"error": "Failed to get weather data.", "details": f"Request exception: {req_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError as key_err:
            return Response({"error": "Weather data is unavailable for the provided location.", "details": f"Key error: {key_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Print the type and content of weather_data to debug
            # print("Type of weather_data:", type(weather_data))
            # print("Content of weather_data:", weather_data)
            return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response_data = {
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {visitor_name}! The temperature is {temperature} degrees Celcius in {city}."
        }
        
        return Response(response_data)
        
        