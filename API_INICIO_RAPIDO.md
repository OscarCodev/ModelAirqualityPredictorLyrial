# 🚀 INICIO RÁPIDO - API REST

## ✅ API FastAPI Creada

He creado una **API REST completa** con FastAPI que expone:

### 🎯 Funcionalidades:

1. **Predicciones de Calidad del Aire** (Machine Learning)
   - Para hoy
   - Para los próximos 7 días
   
2. **Datos de OpenWeatherMap API**
   - Clima actual
   - Pronóstico meteorológico
   - Contaminación actual

3. **Información Adicional**
   - Clasificación de AQI
   - Información de contaminantes

---

## 🚀 CÓMO INICIAR LA API

### Opción 1: Script de inicio (Recomendado)
```bash
python start_api.py
```

### Opción 2: Directamente
```bash
python api.py
```

### Opción 3: Con Uvicorn
```bash
uvicorn api:app --reload
```

---

## 🌐 URLs

Una vez iniciada, la API estará disponible en:

- **API Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs ⭐
- **Documentación Alternativa**: http://localhost:8000/redoc

---

## 📡 ENDPOINTS PRINCIPALES

### 🎯 Predicciones (Lo más importante)

```bash
# Predicción para HOY
curl http://localhost:8000/predict/today

# Predicción para 7 días
curl http://localhost:8000/predict?days=7
```

### 🌤️ Datos Meteorológicos

```bash
# Clima actual
curl http://localhost:8000/weather/current

# Pronóstico
curl http://localhost:8000/weather/forecast?days=3

# Contaminación actual
curl http://localhost:8000/weather/pollution
```

### ℹ️ Información

```bash
# Info de la API
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Info de AQI
curl http://localhost:8000/aqi/info?aqi=75

# Info de contaminantes
curl http://localhost:8000/pollutants/info
```

---

## 📊 EJEMPLO DE USO

### Python
```python
import requests

# Predicción para hoy
response = requests.get("http://localhost:8000/predict/today")
data = response.json()

print(f"Fecha: {data['date']}")
print(f"AQI: {data['AQI']:.1f}")
print(f"Calidad: {data['quality']}")
print(f"NO₂: {data['NO2_ugm3']:.2f} µg/m³")
print(f"CO: {data['CO_mgm3']:.2f} mg/m³")
print(f"O₃: {data['O3_ugm3']:.2f} µg/m³")
```

### JavaScript
```javascript
fetch('http://localhost:8000/predict/today')
  .then(res => res.json())
  .then(data => {
    console.log(`AQI: ${data.AQI}`);
    console.log(`Calidad: ${data.quality}`);
  });
```

### Excel / Power BI / Tableau
Puedes conectar estas herramientas directamente a los endpoints JSON:
```
http://localhost:8000/predict
http://localhost:8000/weather/current
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Para ver la documentación completa con todos los endpoints, ejemplos y esquemas:

**👉 http://localhost:8000/docs** (después de iniciar la API)

O lee: `API_DOCUMENTATION.md`

---

## ✨ CARACTERÍSTICAS DE LA API

- ✅ **9 endpoints** disponibles
- ✅ Documentación automática (Swagger + ReDoc)
- ✅ Validación de datos automática
- ✅ Respuestas en JSON
- ✅ CORS habilitado (para web/móvil)
- ✅ Manejo de errores completo
- ✅ Type hints y autocompletado

---

## 🔧 ARCHIVOS CREADOS

1. **`api.py`** - Código principal de la API ⭐
2. **`start_api.py`** - Script para iniciar la API
3. **`API_DOCUMENTATION.md`** - Documentación completa
4. **`API_INICIO_RAPIDO.md`** - Esta guía

---

## 🎯 FLUJO COMPLETO

```
1. Iniciar API
   → python start_api.py

2. Abrir documentación
   → http://localhost:8000/docs

3. Probar endpoint de predicción
   → GET /predict/today

4. Ver resultado JSON con predicciones
```

---

## 💡 EJEMPLOS DE RESPUESTAS

### GET /predict/today
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

### GET /weather/current
```json
{
  "temperature_celsius": 22.1,
  "pressure_hpa": 1012.0,
  "wind_speed": 3.08,
  "precipitation_mm": 0.0,
  "timestamp": "2025-10-05T12:00:00"
}
```

---

## 🛠️ COMANDOS ÚTILES

```bash
# Iniciar API
python start_api.py

# Verificar que funcione
curl http://localhost:8000/health

# Predicción de hoy
curl http://localhost:8000/predict/today

# Detener API
CTRL + C (en la terminal donde se ejecuta)
```

---

## 📱 INTEGRACIONES POSIBLES

La API puede integrarse con:

- ✅ Aplicaciones web (React, Vue, Angular)
- ✅ Aplicaciones móviles (Flutter, React Native)
- ✅ Power BI / Tableau / Excel
- ✅ Otros servicios backend
- ✅ Automatizaciones (Zapier, IFTTT)
- ✅ Chatbots / Asistentes virtuales

---

## 🎉 ¡LISTO PARA USAR!

**Para iniciar:**
```bash
python start_api.py
```

**Luego visita:**
```
http://localhost:8000/docs
```

---

**Documentación completa**: `API_DOCUMENTATION.md`
**Código de la API**: `api.py`
