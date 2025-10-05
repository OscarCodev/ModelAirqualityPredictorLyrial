"""
Configuración del proyecto
"""

# API Key de OpenWeatherMap
OPENWEATHER_API_KEY = "7e2e121dba238439a5276c8b5c956fb6"

# Coordenadas de Huamanga, Ayacucho, Perú
LATITUDE = -13.1631
LONGITUDE = -74.2236

# Rutas de archivos
DATA_PATH = "data/huamanga_air_quality_2020_2025.csv"
MODEL_PATH = "models/"
PREDICTIONS_PATH = "predictions/"

# Parámetros del modelo
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Características meteorológicas que se usarán del modelo
WEATHER_FEATURES = [
    'temperature',
    'dewpoint', 
    'pressure',
    'wind_u',
    'wind_v',
    'precipitation'
]

# Contaminantes objetivo a predecir
TARGET_POLLUTANTS = [
    'NO2',  # Dióxido de nitrógeno
    'CO',   # Monóxido de carbono
    'O3',   # Ozono
    'SO2',  # Dióxido de azufre
    'aerosol_index'  # Índice de aerosoles
]
