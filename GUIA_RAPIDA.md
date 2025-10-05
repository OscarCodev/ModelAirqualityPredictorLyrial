# 🚀 GUÍA RÁPIDA DE USO

## Ejecutar Predicción (LO MÁS IMPORTANTE)

```bash
python predict.py
```

**Esto predice la calidad del aire para HOY y los próximos 6 días en Huamanga, Ayacucho.**

---

## ¿Qué hace el sistema?

1. ✅ Obtiene datos meteorológicos actuales de OpenWeatherMap
2. ✅ Obtiene pronóstico meteorológico para 6 días
3. ✅ Usa modelos de Machine Learning entrenados
4. ✅ Predice contaminantes: NO₂, CO, O₃, SO₂, Aerosoles
5. ✅ Calcula Índice de Calidad del Aire (AQI)
6. ✅ Muestra resultados en pantalla con emojis
7. ✅ Guarda predicciones en CSV y JSON

---

## Archivos Principales

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| `predict.py` | 🎯 **Script principal** | Úsalo para hacer predicciones |
| `train_model.py` | Entrenar modelos | Solo si quieres reentrenar |
| `weather_api.py` | Probar API | Para verificar conexión |
| `ejemplo_uso.py` | Ejemplos | Ver más formas de uso |

---

## Estructura del Proyecto

```
ModelAirQualityPredictor/
│
├── 📊 data/                          # Datos históricos
│   └── huamanga_air_quality_2020_2025.csv
│
├── 🤖 models/                        # Modelos entrenados (11 archivos)
│   ├── model_NO2.joblib
│   ├── model_CO.joblib
│   ├── model_O3.joblib
│   ├── model_SO2.joblib
│   ├── model_aerosol_index.joblib
│   └── ... (scalers y features)
│
├── 📁 predictions/                   # Predicciones generadas
│   ├── predicciones_YYYYMMDD_HHMMSS.csv
│   └── predicciones_YYYYMMDD_HHMMSS.json
│
├── 🔧 config.py                      # Configuración (API key, coordenadas)
├── 🌐 weather_api.py                 # Conexión con OpenWeatherMap
├── 🎓 train_model.py                 # Entrenamiento de modelos
├── 🎯 predict.py                     # SCRIPT PRINCIPAL
├── 📝 ejemplo_uso.py                 # Ejemplos de uso
│
└── 📚 Documentación
    ├── README.md                     # Documentación completa
    ├── RESUMEN.md                    # Resumen del proyecto
    └── GUIA_RAPIDA.md               # Esta guía
```

---

## Comandos Rápidos

### 1. Hacer Predicción (Principal)
```bash
python predict.py
```

### 2. Reentrenar Modelos (Opcional)
```bash
python train_model.py
```

### 3. Probar API (Verificación)
```bash
python weather_api.py
```

### 4. Ver Ejemplos
```bash
python ejemplo_uso.py
```

---

## Salida Esperada

```
=== PREDICCIÓN DE CALIDAD DEL AIRE ===

1. Cargando modelos entrenados... ✓
2. Obteniendo datos meteorológicos actuales... ✓
3. Obteniendo pronóstico para 7 días... ✓
4. Generando predicciones... ✓

📅 HOY - 05/10/2025
Contaminantes:
  NO₂: 46.06 µg/m³
  CO: 27.08 mg/m³
  O₃: 117.94 µg/m³
  SO₂: 66.11 µg/m³

🟡 AQI: 69.4 (Moderada)
```

---

## Archivos Generados

Cada vez que ejecutas `predict.py`, se crean 2 archivos en `predictions/`:

1. **CSV**: `predicciones_20251005_121326.csv`
   - Formato tabular
   - Fácil de abrir en Excel
   - Columnas: date, NO2, CO, O3, SO2, aerosol_index, AQI, Calidad

2. **JSON**: `predicciones_20251005_121326.json`
   - Formato estructurado
   - Para integración con otras aplicaciones
   - Más legible para programadores

---

## Índice de Calidad del Aire (AQI)

| AQI | Clasificación | Emoji | ¿Qué hacer? |
|-----|--------------|-------|------------|
| 0-50 | Buena | 🟢 | ✅ Actividades normales |
| 51-100 | Moderada | 🟡 | ⚠️ Grupos sensibles: precaución |
| 101-150 | Dañina (sensibles) | 🟠 | ⚠️ Reducir esfuerzos prolongados |
| 151-200 | Dañina | 🔴 | 🚫 Evitar actividades al aire libre |
| 201-300 | Muy dañina | 🟣 | 🚨 Alerta de salud |
| 301+ | Peligrosa | 🔴 | 🆘 Emergencia |

---

## Solución de Problemas

### ❌ Error: "No se pudieron cargar los modelos"
**Solución:**
```bash
python train_model.py
```
(Entrena los modelos primero)

### ❌ Error: "No se pudieron obtener datos meteorológicos"
**Posibles causas:**
1. Sin conexión a Internet
2. API key inválida
3. Límite de llamadas excedido

**Solución:**
- Verifica tu conexión a Internet
- Espera unos minutos y vuelve a intentar

### ❌ Error: "ModuleNotFoundError"
**Solución:**
```bash
pip install -r requirements.txt
```

---

## Información de la API

- **Proveedor**: OpenWeatherMap
- **API Key**: `7e2e121dba238439a5276c8b5c956fb6`
- **Límite**: 60 llamadas/minuto (gratis)
- **Ubicación**: Huamanga, Ayacucho, Perú
- **Coordenadas**: 13.1631°S, 74.2236°W

---

## Contaminantes Predichos

| Contaminante | Símbolo | Unidad | Descripción |
|-------------|---------|--------|-------------|
| Dióxido de Nitrógeno | NO₂ | µg/m³ | Gases de vehículos e industrias |
| Monóxido de Carbono | CO | mg/m³ | Combustión incompleta |
| Ozono | O₃ | µg/m³ | Contaminante secundario |
| Dióxido de Azufre | SO₂ | µg/m³ | Combustibles fósiles |
| Aerosoles | - | - | Partículas suspendidas |

---

## Rendimiento de los Modelos

| Contaminante | Precisión (R²) | Calidad |
|-------------|----------------|---------|
| O₃ (Ozono) | 0.83 | ⭐⭐⭐⭐⭐ Excelente |
| CO | 0.67 | ⭐⭐⭐⭐ Bueno |
| NO₂ | 0.64 | ⭐⭐⭐⭐ Bueno |
| Aerosoles | 0.33 | ⭐⭐ Moderado |
| SO₂ | -0.09 | ⭐ Limitado* |

*SO₂ tiene muchos valores faltantes en datos históricos

---

## Consejos

1. ✅ Ejecuta `predict.py` diariamente para obtener predicciones actualizadas
2. ✅ Los archivos se guardan automáticamente en `predictions/`
3. ✅ Puedes abrir los CSV en Excel o Google Sheets
4. ✅ Los JSON son útiles para aplicaciones web o móviles
5. ⚠️ No ejecutes el script más de 20 veces por minuto (límite API)
6. 🔄 Reentrena los modelos cada 3-6 meses para mejor precisión

---

## Ejemplo de Uso Programático

```python
from predict import AirQualityPredictor

# Crear predictor
predictor = AirQualityPredictor()

# Hacer predicción para 7 días
predictions = predictor.run(days=7, save=True)

# Usar las predicciones
if predictions is not None:
    print(f"Predicciones para {len(predictions)} días generadas")
```

---

## ¿Necesitas Ayuda?

📚 **Documentación Completa**: Lee `README.md`
📊 **Resumen del Proyecto**: Lee `RESUMEN.md`
💡 **Ejemplos**: Ejecuta `python ejemplo_uso.py`

---

**¡Listo para usar!** 🎉

Ejecuta:
```bash
python predict.py
```

Y obtendrás la predicción de calidad del aire para Huamanga. 🌍
