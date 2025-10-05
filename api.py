"""
API REST con FastAPI para predicción de calidad del aire
Expone endpoints para obtener predicciones y datos meteorológicos
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uvicorn

from weather_api import WeatherAPI
from train_model import AirQualityModel
from predict import AirQualityPredictor
import config


# Modelos Pydantic para respuestas
class WeatherData(BaseModel):
    """Modelo para datos meteorológicos"""
    temperature_celsius: float = Field(..., description="Temperatura en °C")
    temperature_kelvin: float = Field(..., description="Temperatura en K")
    dewpoint_celsius: float = Field(..., description="Punto de rocío en °C")
    dewpoint_kelvin: float = Field(..., description="Punto de rocío en K")
    pressure_hpa: float = Field(..., description="Presión en hPa")
    pressure_pa: float = Field(..., description="Presión en Pa")
    wind_u: float = Field(..., description="Componente U del viento (m/s)")
    wind_v: float = Field(..., description="Componente V del viento (m/s)")
    wind_speed: float = Field(..., description="Velocidad del viento (m/s)")
    precipitation_mm: float = Field(..., description="Precipitación en mm/h")
    timestamp: str = Field(..., description="Timestamp de los datos")


class ForecastDay(BaseModel):
    """Modelo para un día de pronóstico"""
    date: str = Field(..., description="Fecha del pronóstico")
    temperature_celsius: float = Field(..., description="Temperatura promedio en °C")
    dewpoint_celsius: float = Field(..., description="Punto de rocío promedio en °C")
    pressure_hpa: float = Field(..., description="Presión promedio en hPa")
    wind_speed: float = Field(..., description="Velocidad del viento promedio (m/s)")
    precipitation_mm: float = Field(..., description="Precipitación promedio en mm/h")


class AirPollution(BaseModel):
    """Modelo para datos de contaminación del aire"""
    NO2: float = Field(..., description="Dióxido de nitrógeno (µg/m³)")
    CO: float = Field(..., description="Monóxido de carbono (mg/m³)")
    O3: float = Field(..., description="Ozono (µg/m³)")
    SO2: float = Field(..., description="Dióxido de azufre (µg/m³)")
    pm2_5: float = Field(..., description="PM2.5 (µg/m³)")
    pm10: float = Field(..., description="PM10 (µg/m³)")


class PredictionResult(BaseModel):
    """Modelo para resultado de predicción"""
    date: str = Field(..., description="Fecha de la predicción")
    NO2_ugm3: float = Field(..., description="NO₂ predicho (µg/m³)")
    CO_mgm3: float = Field(..., description="CO predicho (mg/m³)")
    O3_ugm3: float = Field(..., description="O₃ predicho (µg/m³)")
    SO2_ugm3: float = Field(..., description="SO₂ predicho (µg/m³)")
    aerosol_index: float = Field(..., description="Índice de aerosoles predicho")
    AQI: float = Field(..., description="Índice de Calidad del Aire")
    quality: str = Field(..., description="Clasificación de calidad del aire")


class HealthInfo(BaseModel):
    """Información de salud según AQI"""
    aqi: float
    classification: str
    color: str
    health_implications: str
    cautionary_statement: str


class ApiInfo(BaseModel):
    """Información de la API"""
    name: str
    version: str
    description: str
    location: Dict[str, Any]
    endpoints: List[str]


# Crear aplicación FastAPI
app = FastAPI(
    title="API de Predicción de Calidad del Aire - Huamanga",
    description="API REST para predecir la calidad del aire en Huamanga, Ayacucho, Perú usando Machine Learning y datos de OpenWeatherMap",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias globales
weather_api = WeatherAPI()
predictor = AirQualityPredictor()

# Cargar modelos al inicio
@app.on_event("startup")
async def startup_event():
    """Cargar modelos al iniciar la API"""
    print("🚀 Iniciando API de Calidad del Aire...")
    print("📦 Cargando modelos de Machine Learning...")
    success = predictor.model.load_models()
    if success:
        print("✅ Modelos cargados exitosamente")
    else:
        print("⚠️ Advertencia: No se pudieron cargar todos los modelos")
    print("🌐 API lista en http://localhost:8000")
    print("📚 Documentación en http://localhost:8000/docs")


# ==================== ENDPOINTS ====================

@app.get("/", response_model=ApiInfo, tags=["General"])
async def root():
    """
    Endpoint raíz - Información de la API
    """
    return {
        "name": "Air Quality Prediction API",
        "version": "1.0.0",
        "description": "API para predecir la calidad del aire en Huamanga, Ayacucho, Perú",
        "location": {
            "city": "Huamanga",
            "department": "Ayacucho",
            "country": "Perú",
            "latitude": config.LATITUDE,
            "longitude": config.LONGITUDE
        },
        "endpoints": [
            "/",
            "/health",
            "/weather/current",
            "/weather/forecast",
            "/weather/pollution",
            "/predict",
            "/predict/today",
            "/aqi/info"
        ]
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check - Verificar estado de la API
    """
    models_loaded = len(predictor.model.models) > 0
    return {
        "status": "healthy" if models_loaded else "degraded",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len(predictor.model.models),
        "api_connected": True
    }


@app.get("/weather/current", response_model=WeatherData, tags=["OpenWeatherMap"])
async def get_current_weather():
    """
    Obtener datos meteorológicos actuales de OpenWeatherMap
    
    Retorna temperatura, presión, viento, precipitación, etc.
    """
    try:
        data = weather_api.get_current_weather()
        if not data:
            raise HTTPException(status_code=503, detail="No se pudieron obtener datos meteorológicos")
        
        import math
        wind_speed = math.sqrt(data['wind_u']**2 + data['wind_v']**2)
        
        return {
            "temperature_celsius": data['temperature'] - 273.15,
            "temperature_kelvin": data['temperature'],
            "dewpoint_celsius": data['dewpoint'] - 273.15,
            "dewpoint_kelvin": data['dewpoint'],
            "pressure_hpa": data['pressure'] / 100,
            "pressure_pa": data['pressure'],
            "wind_u": data['wind_u'],
            "wind_v": data['wind_v'],
            "wind_speed": wind_speed,
            "precipitation_mm": data['precipitation'] * 1000,
            "timestamp": data['timestamp'].isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos meteorológicos: {str(e)}")


@app.get("/weather/forecast", response_model=List[ForecastDay], tags=["OpenWeatherMap"])
async def get_weather_forecast(
    days: int = Query(default=7, ge=1, le=7, description="Número de días de pronóstico (1-7)")
):
    """
    Obtener pronóstico meteorológico para los próximos días
    
    - **days**: Número de días de pronóstico (1-7)
    """
    try:
        forecast = weather_api.get_forecast(days)
        if not forecast:
            raise HTTPException(status_code=503, detail="No se pudo obtener el pronóstico")
        
        import math
        result = []
        for day in forecast:
            wind_speed = math.sqrt(day['wind_u']**2 + day['wind_v']**2)
            result.append({
                "date": str(day['date']),
                "temperature_celsius": day['temperature'] - 273.15,
                "dewpoint_celsius": day['dewpoint'] - 273.15,
                "pressure_hpa": day['pressure'] / 100,
                "wind_speed": wind_speed,
                "precipitation_mm": day['precipitation'] * 1000
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pronóstico: {str(e)}")


@app.get("/weather/pollution", response_model=AirPollution, tags=["OpenWeatherMap"])
async def get_air_pollution():
    """
    Obtener datos actuales de contaminación del aire de OpenWeatherMap
    
    Retorna niveles de NO₂, CO, O₃, SO₂, PM2.5 y PM10
    """
    try:
        pollution = weather_api.get_air_pollution()
        if not pollution:
            raise HTTPException(status_code=503, detail="No se pudieron obtener datos de contaminación")
        
        return {
            "NO2": pollution['NO2'] * 1e6,  # Convertir a µg/m³
            "CO": pollution['CO'] * 1e3,     # Convertir a mg/m³
            "O3": pollution['O3'] * 1e6,     # Convertir a µg/m³
            "SO2": pollution['SO2'] * 1e6,   # Convertir a µg/m³
            "pm2_5": pollution['pm2_5'],
            "pm10": pollution['pm10']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de contaminación: {str(e)}")


@app.get("/predict", response_model=List[PredictionResult], tags=["Predicción"])
async def predict_air_quality(
    days: int = Query(default=7, ge=1, le=7, description="Número de días a predecir (1-7)")
):
    """
    Predecir la calidad del aire para los próximos días
    
    Utiliza modelos de Machine Learning entrenados con datos históricos
    y pronósticos meteorológicos de OpenWeatherMap.
    
    - **days**: Número de días a predecir incluyendo hoy (1-7)
    
    Retorna predicciones de contaminantes y AQI para cada día.
    """
    try:
        # Hacer predicción
        predictions = predictor.predict_current_and_forecast(days)
        
        if predictions is None:
            raise HTTPException(
                status_code=503,
                detail="No se pudieron generar predicciones. Verifica que los modelos estén entrenados."
            )
        
        # Agregar AQI
        predictions_with_aqi = predictor.get_air_quality_index(predictions)
        
        # Formatear respuesta
        result = []
        for _, row in predictions_with_aqi.iterrows():
            result.append({
                "date": str(row['date']) if 'date' in row else datetime.now().date().isoformat(),
                "NO2_ugm3": row['NO2'] * 1e6 if 'NO2' in row else 0,
                "CO_mgm3": row['CO'] * 1e3 if 'CO' in row else 0,
                "O3_ugm3": row['O3'] * 1e6 if 'O3' in row else 0,
                "SO2_ugm3": row['SO2'] * 1e6 if 'SO2' in row else 0,
                "aerosol_index": row['aerosol_index'] if 'aerosol_index' in row else 0,
                "AQI": row['AQI'] if 'AQI' in row else 0,
                "quality": row['Calidad'] if 'Calidad' in row else "N/A"
            })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar predicciones: {str(e)}")


@app.get("/predict/today", response_model=PredictionResult, tags=["Predicción"])
async def predict_today():
    """
    Predecir la calidad del aire solo para el día de hoy
    
    Retorna predicción de contaminantes y AQI para hoy.
    """
    try:
        predictions = predictor.predict_current_and_forecast(1)
        
        if predictions is None or predictions.empty:
            raise HTTPException(
                status_code=503,
                detail="No se pudo generar predicción para hoy"
            )
        
        predictions_with_aqi = predictor.get_air_quality_index(predictions)
        row = predictions_with_aqi.iloc[0]
        
        return {
            "date": str(row['date']) if 'date' in row else datetime.now().date().isoformat(),
            "NO2_ugm3": row['NO2'] * 1e6 if 'NO2' in row else 0,
            "CO_mgm3": row['CO'] * 1e3 if 'CO' in row else 0,
            "O3_ugm3": row['O3'] * 1e6 if 'O3' in row else 0,
            "SO2_ugm3": row['SO2'] * 1e6 if 'SO2' in row else 0,
            "aerosol_index": row['aerosol_index'] if 'aerosol_index' in row else 0,
            "AQI": row['AQI'] if 'AQI' in row else 0,
            "quality": row['Calidad'] if 'Calidad' in row else "N/A"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar predicción: {str(e)}")


@app.get("/aqi/info", response_model=Dict[str, Any], tags=["Información"])
async def get_aqi_info(
    aqi: float = Query(..., ge=0, le=500, description="Valor del AQI (0-500)")
):
    """
    Obtener información de salud según el valor del AQI
    
    - **aqi**: Valor del Índice de Calidad del Aire (0-500)
    
    Retorna clasificación, color, implicaciones de salud y recomendaciones.
    """
    if aqi <= 50:
        classification = "Buena"
        color = "Verde"
        emoji = "🟢"
        health = "La calidad del aire es satisfactoria y la contaminación del aire presenta poco o ningún riesgo."
        caution = "Ninguna precaución necesaria. Disfrute de actividades al aire libre."
    elif aqi <= 100:
        classification = "Moderada"
        color = "Amarillo"
        emoji = "🟡"
        health = "La calidad del aire es aceptable. Sin embargo, puede haber un riesgo moderado para un número pequeño de personas."
        caution = "Las personas excepcionalmente sensibles deben considerar limitar los esfuerzos prolongados al aire libre."
    elif aqi <= 150:
        classification = "Dañina para grupos sensibles"
        color = "Naranja"
        emoji = "🟠"
        health = "Los miembros de grupos sensibles pueden experimentar efectos en la salud. El público en general probablemente no se verá afectado."
        caution = "Los niños, ancianos y personas con enfermedades respiratorias deben limitar los esfuerzos prolongados al aire libre."
    elif aqi <= 200:
        classification = "Dañina"
        color = "Rojo"
        emoji = "🔴"
        health = "Todos pueden comenzar a experimentar efectos en la salud. Los miembros de grupos sensibles pueden experimentar efectos más graves."
        caution = "Todos deben evitar los esfuerzos prolongados al aire libre. Los grupos sensibles deben permanecer en interiores."
    elif aqi <= 300:
        classification = "Muy dañina"
        color = "Púrpura"
        emoji = "🟣"
        health = "Advertencia de salud: todos pueden experimentar efectos más graves en la salud."
        caution = "Todos deben evitar todos los esfuerzos físicos al aire libre. Los grupos sensibles deben permanecer en interiores."
    else:
        classification = "Peligrosa"
        color = "Marrón"
        emoji = "🔴"
        health = "Alerta de salud: todos pueden experimentar efectos graves en la salud."
        caution = "Todos deben permanecer en interiores y mantener los niveles de actividad bajos."
    
    return {
        "aqi": aqi,
        "classification": classification,
        "color": color,
        "emoji": emoji,
        "health_implications": health,
        "cautionary_statement": caution,
        "ranges": {
            "Buena": "0-50",
            "Moderada": "51-100",
            "Dañina para grupos sensibles": "101-150",
            "Dañina": "151-200",
            "Muy dañina": "201-300",
            "Peligrosa": "301-500"
        }
    }


@app.get("/pollutants/info", tags=["Información"])
async def get_pollutants_info():
    """
    Información sobre los contaminantes predichos
    
    Retorna descripciones, fuentes y límites de cada contaminante.
    """
    return {
        "pollutants": [
            {
                "symbol": "NO₂",
                "name": "Dióxido de Nitrógeno",
                "unit": "µg/m³",
                "description": "Gas reactivo que se forma principalmente por la combustión en motores de vehículos.",
                "sources": ["Vehículos", "Centrales eléctricas", "Industrias"],
                "health_effects": "Puede irritar las vías respiratorias y agravar enfermedades respiratorias.",
                "who_limit": 40  # µg/m³ promedio anual
            },
            {
                "symbol": "CO",
                "name": "Monóxido de Carbono",
                "unit": "mg/m³",
                "description": "Gas tóxico e incoloro producido por la combustión incompleta de combustibles.",
                "sources": ["Vehículos", "Calefacción", "Industrias"],
                "health_effects": "Reduce el suministro de oxígeno al cuerpo, afecta el sistema cardiovascular.",
                "who_limit": 10  # mg/m³ 8 horas
            },
            {
                "symbol": "O₃",
                "name": "Ozono",
                "unit": "µg/m³",
                "description": "Contaminante secundario formado por reacciones químicas entre NOx y COV bajo luz solar.",
                "sources": ["Reacciones fotoquímicas", "No emitido directamente"],
                "health_effects": "Irrita las vías respiratorias, reduce la función pulmonar.",
                "who_limit": 100  # µg/m³ 8 horas
            },
            {
                "symbol": "SO₂",
                "name": "Dióxido de Azufre",
                "unit": "µg/m³",
                "description": "Gas producido principalmente por la combustión de combustibles fósiles con azufre.",
                "sources": ["Centrales eléctricas", "Industrias", "Refinería"],
                "health_effects": "Puede causar problemas respiratorios, especialmente en asmáticos.",
                "who_limit": 20  # µg/m³ 24 horas
            },
            {
                "symbol": "AI",
                "name": "Índice de Aerosoles",
                "unit": "Adimensional",
                "description": "Medida de partículas suspendidas en la atmósfera que absorben luz UV.",
                "sources": ["Polvo", "Humo", "Contaminación industrial"],
                "health_effects": "Partículas pueden penetrar en los pulmones y afectar la salud respiratoria.",
                "who_limit": None
            }
        ]
    }


# Ejecutar la API
if __name__ == "__main__":
    print("=" * 80)
    print("🌍 API DE PREDICCIÓN DE CALIDAD DEL AIRE - HUAMANGA")
    print("=" * 80)
    print(f"\n📍 Ubicación: Huamanga, Ayacucho, Perú")
    print(f"📐 Coordenadas: {config.LATITUDE}, {config.LONGITUDE}")
    print(f"\n🚀 Iniciando servidor...")
    print(f"🌐 URL: http://localhost:8000")
    print(f"📚 Documentación: http://localhost:8000/docs")
    print(f"📖 ReDoc: http://localhost:8000/redoc")
    print(f"\n⏸️  Presiona CTRL+C para detener\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
