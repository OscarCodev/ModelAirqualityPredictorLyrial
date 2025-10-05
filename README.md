# Modelo de Predicción de Calidad del Aire - Huamanga, Ayacucho, Perú

Sistema de predicción de calidad del aire para la ciudad de Huamanga utilizando datos históricos (2020-2025) y pronósticos meteorológicos de OpenWeatherMap API.

## 📋 Descripción

Este proyecto predice la calidad del aire para Huamanga, Ayacucho, Perú para el día actual y los próximos 6 días. El modelo utiliza:

- **Datos históricos**: Calidad del aire de 2020 a 2025
- **OpenWeatherMap API**: Datos meteorológicos actuales y pronósticos
- **Machine Learning**: Modelos de Gradient Boosting para cada contaminante

### Contaminantes Predichos

- **NO₂** (Dióxido de nitrógeno)
- **CO** (Monóxido de carbono)
- **O₃** (Ozono)
- **SO₂** (Dióxido de azufre)
- **Índice de aerosoles**

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- pandas
- numpy
- scikit-learn
- requests
- joblib
- matplotlib
- seaborn

## 📊 Uso

### 1. Entrenar los Modelos

Primero debes entrenar los modelos con los datos históricos:

```bash
python train_model.py
```

Este proceso:
- Carga los datos históricos de `data/huamanga_air_quality_2020_2025.csv`
- Entrena un modelo para cada contaminante
- Guarda los modelos en la carpeta `models/`
- Muestra métricas de rendimiento (R², MAE, RMSE)

**Tiempo estimado**: 1-3 minutos

### 2. Hacer Predicciones

Una vez entrenados los modelos, ejecuta:

```bash
python predict.py
```

Este script:
1. Carga los modelos entrenados
2. Obtiene datos meteorológicos actuales de OpenWeatherMap API
3. Obtiene el pronóstico para los próximos 6 días
4. Genera predicciones de calidad del aire
5. Muestra los resultados en consola
6. Guarda las predicciones en `predictions/`

### 3. Probar la API de OpenWeatherMap

Para verificar que la API funciona correctamente:

```bash
python weather_api.py
```

## 🔑 Configuración

### API Key de OpenWeatherMap

La API key ya está configurada en `config.py`:
```python
OPENWEATHER_API_KEY = "7e2e121dba238439a5276c8b5c956fb6"
```

Si necesitas usar tu propia API key:
1. Obtén una gratis en [OpenWeatherMap](https://openweathermap.org/api)
2. Modifica `OPENWEATHER_API_KEY` en `config.py`

### Coordenadas

Las coordenadas de Huamanga están configuradas en `config.py`:
```python
LATITUDE = -13.1631
LONGITUDE = -74.2236
```

## 📁 Estructura del Proyecto

```
ModelAirQualityPredictor/
│
├── data/
│   └── huamanga_air_quality_2020_2025.csv  # Datos históricos
│
├── models/                                  # Modelos entrenados (generados)
│   ├── model_NO2.joblib
│   ├── model_CO.joblib
│   ├── model_O3.joblib
│   ├── model_SO2.joblib
│   ├── model_aerosol_index.joblib
│   └── feature_columns.joblib
│
├── predictions/                             # Predicciones guardadas (generadas)
│   ├── predicciones_YYYYMMDD_HHMMSS.csv
│   └── predicciones_YYYYMMDD_HHMMSS.json
│
├── config.py                                # Configuración del proyecto
├── weather_api.py                           # Módulo API de OpenWeatherMap
├── train_model.py                           # Entrenamiento de modelos
├── predict.py                               # Script de predicción
├── requirements.txt                         # Dependencias
├── instructions.md                          # Instrucciones originales
└── README.md                                # Este archivo
```

## 📈 Salida del Programa

### Ejemplo de Predicción

```
=== PREDICCIÓN DE CALIDAD DEL AIRE ===

1. Cargando modelos entrenados...
  Modelo NO2 cargado
  Modelo CO cargado
  Modelo O3 cargado
  Modelo SO2 cargado
  Modelo aerosol_index cargado

2. Obteniendo datos meteorológicos actuales...
   Temperatura: 18.5°C
   Presión: 680.7 hPa
   Precipitación: 0.00 mm/h

3. Obteniendo pronóstico para 7 días...
   Pronóstico obtenido para 7 días

4. Generando predicciones de calidad del aire...
   Predicciones generadas para 7 días

================================================================================
PREDICCIONES DE CALIDAD DEL AIRE - HUAMANGA, AYACUCHO, PERÚ
================================================================================

📅 HOY - 05/10/2025
--------------------------------------------------------------------------------

Contaminantes:
  NO₂ (Dióxido de nitrógeno):  35.42 µg/m³
  CO (Monóxido de carbono):    21.30 mg/m³
  O₃ (Ozono):                  110.25 µg/m³
  SO₂ (Dióxido de azufre):     12.50 µg/m³
  Índice de aerosoles:         -1.45

🟢 ÍNDICE DE CALIDAD DEL AIRE (AQI): 72.3
   Clasificación: Moderada
   ⚠ Aceptable para la mayoría, grupos sensibles deben limitar esfuerzos prolongados al aire libre

...
```

## 🎯 Características del Modelo

### Variables de Entrada (Features)

El modelo utiliza las siguientes características meteorológicas:

- **temperature**: Temperatura (Kelvin)
- **dewpoint**: Punto de rocío (Kelvin)
- **pressure**: Presión atmosférica (Pa)
- **wind_u**: Componente U del viento (m/s)
- **wind_v**: Componente V del viento (m/s)
- **precipitation**: Precipitación (m)
- **day_of_year**: Día del año (1-366)
- **month**: Mes (1-12)
- Promedios móviles de 7 y 30 días de variables meteorológicas

### Algoritmo

- **Gradient Boosting Regressor**
  - 200 estimadores
  - Learning rate: 0.1
  - Max depth: 5
  - Optimizado para series temporales

### Rendimiento

Los modelos han sido evaluados con métricas estándar:
- **R² Score**: Coeficiente de determinación
- **MAE**: Error absoluto medio
- **RMSE**: Raíz del error cuadrático medio

## 🔍 Índice de Calidad del Aire (AQI)

El sistema calcula un AQI basado en los niveles de contaminantes:

| AQI | Clasificación | Color |
|-----|--------------|-------|
| 0-50 | Buena | 🟢 Verde |
| 51-100 | Moderada | 🟡 Amarillo |
| 101-150 | Dañina para grupos sensibles | 🟠 Naranja |
| 151-200 | Dañina | 🔴 Rojo |
| 201-300 | Muy dañina | 🟣 Púrpura |
| 301+ | Peligrosa | 🔴 Marrón |

## 📝 Notas Importantes

1. **Conexión a Internet**: Necesaria para obtener datos de OpenWeatherMap API
2. **Precisión**: Las predicciones son estimaciones basadas en patrones históricos
3. **Actualización**: Se recomienda reentrenar los modelos periódicamente con datos nuevos
4. **Limitaciones API**: OpenWeatherMap tiene límites de llamadas (60/min gratis)

## 🛠️ Solución de Problemas

### Error: "No se pudieron cargar los modelos"
- Ejecuta primero `python train_model.py`

### Error: "No se pudieron obtener datos meteorológicos"
- Verifica tu conexión a internet
- Comprueba que la API key sea válida
- Revisa si has excedido el límite de llamadas

### Error: "ModuleNotFoundError"
- Instala las dependencias: `pip install -r requirements.txt`

## 📧 Contacto

Para preguntas o sugerencias sobre este proyecto, consulta la documentación de las APIs utilizadas:
- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [Scikit-learn Documentation](https://scikit-learn.org/)

## 📄 Licencia

Este proyecto fue creado con fines educativos y de investigación.

---

**Última actualización**: Octubre 2025
**Ubicación**: Huamanga, Ayacucho, Perú
**Coordenadas**: 13.1631°S, 74.2236°W
