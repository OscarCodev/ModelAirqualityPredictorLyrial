# 🚀 API REST - Predicción de Calidad del Aire

## 📋 Descripción

API REST construida con **FastAPI** que expone endpoints para:
- ✅ Obtener datos meteorológicos actuales de OpenWeatherMap
- ✅ Obtener pronósticos meteorológicos
- ✅ Obtener datos de contaminación actuales
- ✅ **Predecir la calidad del aire** usando Machine Learning
- ✅ Obtener información sobre AQI y contaminantes

---

## 🚀 CÓMO EJECUTAR LA API

### Opción 1: Ejecución directa
```bash
python api.py
```

### Opción 2: Con Uvicorn
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **URL Base**: http://localhost:8000
- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

---

## 📡 ENDPOINTS DISPONIBLES

### 🏠 General

#### `GET /`
Información general de la API
```json
{
  "name": "Air Quality Prediction API",
  "version": "1.0.0",
  "description": "...",
  "location": {...},
  "endpoints": [...]
}
```

#### `GET /health`
Health check - Estado de la API
```json
{
  "status": "healthy",
  "timestamp": "2025-10-05T12:00:00",
  "models_loaded": 5,
  "api_connected": true
}
```

---

### 🌤️ OpenWeatherMap

#### `GET /weather/current`
Obtener datos meteorológicos actuales

**Respuesta:**
```json
{
  "temperature_celsius": 22.1,
  "temperature_kelvin": 295.25,
  "dewpoint_celsius": 15.3,
  "dewpoint_kelvin": 288.45,
  "pressure_hpa": 1012.0,
  "pressure_pa": 101200,
  "wind_u": -2.5,
  "wind_v": 1.8,
  "wind_speed": 3.08,
  "precipitation_mm": 0.0,
  "timestamp": "2025-10-05T12:00:00"
}
```

**Ejemplo cURL:**
```bash
curl http://localhost:8000/weather/current
```

---

#### `GET /weather/forecast`
Obtener pronóstico meteorológico

**Parámetros:**
- `days` (opcional): Número de días (1-7, default: 7)

**Ejemplo:**
```bash
curl http://localhost:8000/weather/forecast?days=3
```

**Respuesta:**
```json
[
  {
    "date": "2025-10-05",
    "temperature_celsius": 22.5,
    "dewpoint_celsius": 15.0,
    "pressure_hpa": 1012.0,
    "wind_speed": 3.2,
    "precipitation_mm": 0.0
  },
  ...
]
```

---

#### `GET /weather/pollution`
Obtener datos de contaminación actuales de OpenWeatherMap

**Respuesta:**
```json
{
  "NO2": 45.2,
  "CO": 320.5,
  "O3": 65.8,
  "SO2": 15.3,
  "pm2_5": 12.5,
  "pm10": 25.8
}
```

**Ejemplo cURL:**
```bash
curl http://localhost:8000/weather/pollution
```

---

### 🎯 Predicción (Machine Learning)

#### `GET /predict`
**Predecir la calidad del aire** para los próximos días

**Parámetros:**
- `days` (opcional): Número de días a predecir (1-7, default: 7)

**Ejemplo:**
```bash
curl http://localhost:8000/predict?days=3
```

**Respuesta:**
```json
[
  {
    "date": "2025-10-05",
    "NO2_ugm3": 46.06,
    "CO_mgm3": 27.08,
    "O3_ugm3": 117.94,
    "SO2_ugm3": 66.11,
    "aerosol_index": 0.0,
    "AQI": 69.4,
    "quality": "Moderada"
  },
  {
    "date": "2025-10-06",
    "NO2_ugm3": 46.45,
    "CO_mgm3": 25.76,
    "O3_ugm3": 118.81,
    "SO2_ugm3": 4.74,
    "aerosol_index": 0.04,
    "AQI": 56.8,
    "quality": "Moderada"
  }
]
```

---

#### `GET /predict/today`
Predecir la calidad del aire **solo para hoy**

**Respuesta:**
```json
{
  "date": "2025-10-05",
  "NO2_ugm3": 46.06,
  "CO_mgm3": 27.08,
  "O3_ugm3": 117.94,
  "SO2_ugm3": 66.11,
  "aerosol_index": 0.0,
  "AQI": 69.4,
  "quality": "Moderada"
}
```

**Ejemplo cURL:**
```bash
curl http://localhost:8000/predict/today
```

---

### ℹ️ Información

#### `GET /aqi/info`
Obtener información de salud según el AQI

**Parámetros:**
- `aqi` (requerido): Valor del AQI (0-500)

**Ejemplo:**
```bash
curl http://localhost:8000/aqi/info?aqi=75
```

**Respuesta:**
```json
{
  "aqi": 75,
  "classification": "Moderada",
  "color": "Amarillo",
  "emoji": "🟡",
  "health_implications": "...",
  "cautionary_statement": "...",
  "ranges": {
    "Buena": "0-50",
    "Moderada": "51-100",
    ...
  }
}
```

---

#### `GET /pollutants/info`
Información sobre los contaminantes

**Respuesta:**
```json
{
  "pollutants": [
    {
      "symbol": "NO₂",
      "name": "Dióxido de Nitrógeno",
      "unit": "µg/m³",
      "description": "...",
      "sources": ["Vehículos", "..."],
      "health_effects": "...",
      "who_limit": 40
    },
    ...
  ]
}
```

---

## 🔧 Ejemplos de Uso

### Python con requests
```python
import requests

# Obtener predicción para hoy
response = requests.get("http://localhost:8000/predict/today")
data = response.json()
print(f"AQI: {data['AQI']}")
print(f"Calidad: {data['quality']}")

# Obtener pronóstico de 3 días
response = requests.get("http://localhost:8000/predict?days=3")
predictions = response.json()
for pred in predictions:
    print(f"{pred['date']}: AQI={pred['AQI']:.1f} ({pred['quality']})")
```

### JavaScript (Fetch API)
```javascript
// Obtener predicción para hoy
fetch('http://localhost:8000/predict/today')
  .then(response => response.json())
  .then(data => {
    console.log(`AQI: ${data.AQI}`);
    console.log(`Calidad: ${data.quality}`);
  });

// Obtener datos meteorológicos actuales
fetch('http://localhost:8000/weather/current')
  .then(response => response.json())
  .then(data => {
    console.log(`Temperatura: ${data.temperature_celsius}°C`);
  });
```

### cURL (Bash)
```bash
# Predicción para hoy
curl -X GET "http://localhost:8000/predict/today"

# Predicción para 7 días
curl -X GET "http://localhost:8000/predict?days=7"

# Datos meteorológicos actuales
curl -X GET "http://localhost:8000/weather/current"

# Pronóstico de 3 días
curl -X GET "http://localhost:8000/weather/forecast?days=3"

# Información de AQI
curl -X GET "http://localhost:8000/aqi/info?aqi=75"
```

---

## 📊 Respuestas y Códigos de Estado

### Códigos HTTP
- **200**: Solicitud exitosa
- **400**: Solicitud incorrecta (parámetros inválidos)
- **404**: Endpoint no encontrado
- **500**: Error interno del servidor
- **503**: Servicio no disponible (error de API externa o modelos no cargados)

### Formato de Error
```json
{
  "detail": "Descripción del error"
}
```

---

## 🌐 CORS

La API tiene CORS habilitado para todos los orígenes (`*`), lo que permite:
- Solicitudes desde navegadores web
- Aplicaciones frontend (React, Vue, Angular, etc.)
- Aplicaciones móviles

---

## 📚 Documentación Interactiva

### Swagger UI (Recomendado)
http://localhost:8000/docs

Características:
- ✅ Interfaz interactiva
- ✅ Probar endpoints directamente
- ✅ Ver esquemas de datos
- ✅ Ejemplos de respuestas

### ReDoc
http://localhost:8000/redoc

Características:
- ✅ Documentación estática elegante
- ✅ Navegación por secciones
- ✅ Mejor para leer documentación

---

## 🔐 Seguridad

### Recomendaciones para Producción

1. **Agregar autenticación** (API Key, JWT, OAuth2)
2. **Limitar rate limiting** (número de solicitudes por minuto)
3. **Usar HTTPS** (certificado SSL/TLS)
4. **Configurar CORS** específicamente para tus dominios
5. **Validar entrada de usuario** (ya incluido con Pydantic)
6. **Logs y monitoreo** (integrar con servicios de logging)

---

## 🚀 Despliegue

### Desarrollo Local
```bash
python api.py
```

### Producción con Gunicorn
```bash
pip install gunicorn
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔍 Pruebas

### Verificar que la API esté funcionando
```bash
# Health check
curl http://localhost:8000/health

# Debería retornar:
# {"status": "healthy", "timestamp": "...", "models_loaded": 5, "api_connected": true}
```

### Probar predicción
```bash
curl http://localhost:8000/predict/today | python -m json.tool
```

---

## ⚙️ Variables de Configuración

Las variables se configuran en `config.py`:

```python
OPENWEATHER_API_KEY = "7e2e121dba238439a5276c8b5c956fb6"
LATITUDE = -13.1631
LONGITUDE = -74.2236
```

---

## 📈 Rendimiento

- **Tiempo de respuesta**: < 2 segundos (predicción completa)
- **Concurrencia**: Soporta múltiples solicitudes simultáneas
- **Caché**: No implementado (considera Redis para producción)

---

## 🐛 Solución de Problemas

### Error: "models_loaded: 0"
```bash
# Entrenar los modelos primero
python train_model.py
```

### Error: "Service unavailable"
- Verificar conexión a internet
- Verificar API key de OpenWeatherMap
- Comprobar límite de llamadas a la API

### Puerto 8000 en uso
```bash
# Usar otro puerto
uvicorn api:app --port 8001
```

---

## 📞 Endpoints Resumidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/weather/current` | Clima actual |
| GET | `/weather/forecast` | Pronóstico meteorológico |
| GET | `/weather/pollution` | Contaminación actual |
| GET | `/predict` | Predicción de calidad del aire |
| GET | `/predict/today` | Predicción solo para hoy |
| GET | `/aqi/info` | Información sobre AQI |
| GET | `/pollutants/info` | Información sobre contaminantes |

---

## ✨ Características

- ✅ FastAPI (rápida y moderna)
- ✅ Documentación automática (Swagger + ReDoc)
- ✅ Validación de datos con Pydantic
- ✅ CORS habilitado
- ✅ Respuestas en JSON
- ✅ Manejo de errores
- ✅ Type hints completos
- ✅ Código autodocumentado

---

**¡API lista para usar!** 🎉

Para iniciar:
```bash
python api.py
```

Luego visita: http://localhost:8000/docs
