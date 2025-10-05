"""
Módulo para obtener datos meteorológicos de OpenWeatherMap API
"""

import requests
from datetime import datetime, timedelta
import config


class WeatherAPI:
    """Clase para interactuar con OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = config.OPENWEATHER_API_KEY
        self.lat = config.LATITUDE
        self.lon = config.LONGITUDE
        
    def get_current_weather(self):
        """
        Obtiene los datos meteorológicos actuales
        
        Returns:
            dict: Datos meteorológicos actuales
        """
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extraer características relevantes
            weather_data = {
                'temperature': data['main']['temp'] + 273.15,  # Convertir a Kelvin
                'dewpoint': self._calculate_dewpoint(
                    data['main']['temp'], 
                    data['main']['humidity']
                ),
                'pressure': data['main']['pressure'] * 100,  # Convertir a Pa
                'wind_u': data['wind']['speed'] * (-1 if data['wind'].get('deg', 0) > 180 else 1),
                'wind_v': data['wind']['speed'] * (-1 if 90 < data['wind'].get('deg', 0) < 270 else 1),
                'precipitation': data.get('rain', {}).get('1h', 0) / 1000,  # Convertir a m
                'timestamp': datetime.now()
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del clima: {e}")
            return None
    
    def get_forecast(self, days=7):
        """
        Obtiene el pronóstico meteorológico para los próximos días
        
        Args:
            days (int): Número de días de pronóstico (máximo 7)
            
        Returns:
            list: Lista de diccionarios con datos meteorológicos por día
        """
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': min(days * 8, 40)  # API devuelve datos cada 3 horas
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Agrupar por día y promediar
            daily_forecasts = {}
            
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                
                weather_point = {
                    'temperature': item['main']['temp'] + 273.15,
                    'dewpoint': self._calculate_dewpoint(
                        item['main']['temp'],
                        item['main']['humidity']
                    ),
                    'pressure': item['main']['pressure'] * 100,
                    'wind_u': item['wind']['speed'] * (-1 if item['wind'].get('deg', 0) > 180 else 1),
                    'wind_v': item['wind']['speed'] * (-1 if 90 < item['wind'].get('deg', 0) < 270 else 1),
                    'precipitation': item.get('rain', {}).get('3h', 0) / 1000 / 3,  # Por hora
                }
                
                daily_forecasts[date].append(weather_point)
            
            # Promediar los datos por día
            averaged_forecasts = []
            for date in sorted(daily_forecasts.keys())[:days]:
                day_data = daily_forecasts[date]
                averaged = {
                    'date': date,
                    'temperature': sum(d['temperature'] for d in day_data) / len(day_data),
                    'dewpoint': sum(d['dewpoint'] for d in day_data) / len(day_data),
                    'pressure': sum(d['pressure'] for d in day_data) / len(day_data),
                    'wind_u': sum(d['wind_u'] for d in day_data) / len(day_data),
                    'wind_v': sum(d['wind_v'] for d in day_data) / len(day_data),
                    'precipitation': sum(d['precipitation'] for d in day_data) / len(day_data),
                }
                averaged_forecasts.append(averaged)
            
            return averaged_forecasts
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener pronóstico del clima: {e}")
            return None
    
    def get_air_pollution(self):
        """
        Obtiene datos de contaminación del aire actuales
        
        Returns:
            dict: Datos de contaminación del aire
        """
        url = "http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['list']:
                components = data['list'][0]['components']
                return {
                    'NO2': components.get('no2', 0) / 1e6,  # Convertir a las unidades del dataset
                    'CO': components.get('co', 0) / 1e3,
                    'O3': components.get('o3', 0) / 1e6,
                    'SO2': components.get('so2', 0) / 1e6,
                    'pm2_5': components.get('pm2_5', 0),
                    'pm10': components.get('pm10', 0),
                }
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de contaminación: {e}")
            return None
    
    def _calculate_dewpoint(self, temp_celsius, humidity):
        """
        Calcula el punto de rocío usando la fórmula de Magnus
        
        Args:
            temp_celsius (float): Temperatura en Celsius
            humidity (float): Humedad relativa en porcentaje
            
        Returns:
            float: Punto de rocío en Kelvin
        """
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp_celsius) / (b + temp_celsius)) + (humidity / 100.0)
        dewpoint_celsius = (b * alpha) / (a - alpha)
        
        return dewpoint_celsius + 273.15  # Convertir a Kelvin


if __name__ == "__main__":
    # Prueba del módulo
    api = WeatherAPI()
    
    print("=== DATOS METEOROLÓGICOS ACTUALES ===")
    current = api.get_current_weather()
    if current:
        for key, value in current.items():
            print(f"{key}: {value}")
    
    print("\n=== PRONÓSTICO 7 DÍAS ===")
    forecast = api.get_forecast(7)
    if forecast:
        for day in forecast:
            print(f"\nFecha: {day['date']}")
            for key, value in day.items():
                if key != 'date':
                    print(f"  {key}: {value:.2f}")
    
    print("\n=== CONTAMINACIÓN DEL AIRE ===")
    pollution = api.get_air_pollution()
    if pollution:
        for key, value in pollution.items():
            print(f"{key}: {value}")
