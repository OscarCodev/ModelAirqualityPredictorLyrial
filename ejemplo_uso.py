"""
Script de ejemplo para usar el predictor de calidad del aire
"""

from predict import AirQualityPredictor
from weather_api import WeatherAPI

def ejemplo_basico():
    """Ejemplo básico de uso del predictor"""
    print("=" * 80)
    print("EJEMPLO BÁSICO - PREDICCIÓN DE CALIDAD DEL AIRE")
    print("=" * 80)
    
    # Crear instancia del predictor
    predictor = AirQualityPredictor()
    
    # Hacer predicción para 7 días
    predictions = predictor.run(days=7, save=True)
    
    if predictions is not None:
        print("\n✓ Predicción completada exitosamente")
        print(f"✓ Se generaron predicciones para {len(predictions)} días")
    else:
        print("\n✗ Error al generar predicciones")


def ejemplo_solo_datos_api():
    """Ejemplo de cómo obtener solo datos meteorológicos"""
    print("\n" + "=" * 80)
    print("EJEMPLO - OBTENER DATOS METEOROLÓGICOS")
    print("=" * 80 + "\n")
    
    api = WeatherAPI()
    
    # Datos actuales
    print("1. DATOS METEOROLÓGICOS ACTUALES:")
    current = api.get_current_weather()
    if current:
        print(f"   Temperatura: {current['temperature'] - 273.15:.1f}°C")
        print(f"   Punto de rocío: {current['dewpoint'] - 273.15:.1f}°C")
        print(f"   Presión: {current['pressure']/100:.1f} hPa")
        print(f"   Precipitación: {current['precipitation']*1000:.2f} mm/h")
        print(f"   Viento U: {current['wind_u']:.2f} m/s")
        print(f"   Viento V: {current['wind_v']:.2f} m/s")
    
    # Pronóstico
    print("\n2. PRONÓSTICO PARA 3 DÍAS:")
    forecast = api.get_forecast(3)
    if forecast:
        for day in forecast:
            print(f"\n   Fecha: {day['date']}")
            print(f"   Temperatura: {day['temperature'] - 273.15:.1f}°C")
            print(f"   Presión: {day['pressure']/100:.1f} hPa")
    
    # Contaminación actual
    print("\n3. CONTAMINACIÓN DEL AIRE ACTUAL:")
    pollution = api.get_air_pollution()
    if pollution:
        print(f"   NO₂: {pollution.get('NO2', 0)*1e6:.2f} µg/m³")
        print(f"   CO: {pollution.get('CO', 0)*1e3:.2f} mg/m³")
        print(f"   O₃: {pollution.get('O3', 0)*1e6:.2f} µg/m³")
        print(f"   SO₂: {pollution.get('SO2', 0)*1e6:.2f} µg/m³")
        print(f"   PM2.5: {pollution.get('pm2_5', 0):.2f} µg/m³")
        print(f"   PM10: {pollution.get('pm10', 0):.2f} µg/m³")


def ejemplo_prediccion_personalizada():
    """Ejemplo de predicción personalizada para diferente número de días"""
    print("\n" + "=" * 80)
    print("EJEMPLO - PREDICCIÓN PERSONALIZADA")
    print("=" * 80 + "\n")
    
    predictor = AirQualityPredictor()
    
    # Predecir solo para los próximos 3 días
    print("Predicción para 3 días:")
    predictions = predictor.predict_current_and_forecast(days=3)
    
    if predictions is not None:
        print(f"\n✓ Predicciones generadas para {len(predictions)} días")
        
        # Mostrar solo resumen
        predictions_with_aqi = predictor.get_air_quality_index(predictions)
        print("\nRESUMEN:")
        for idx, row in predictions_with_aqi.iterrows():
            date = row['date']
            aqi = row.get('AQI', 0)
            calidad = row.get('Calidad', 'N/A')
            print(f"  {date}: AQI={aqi:.1f} ({calidad})")


if __name__ == "__main__":
    # Ejecutar ejemplos
    
    # Ejemplo 1: Uso básico del predictor
    ejemplo_basico()
    
    # Ejemplo 2: Solo obtener datos de la API
    ejemplo_solo_datos_api()
    
    # Ejemplo 3: Predicción personalizada
    ejemplo_prediccion_personalizada()
    
    print("\n" + "=" * 80)
    print("EJEMPLOS COMPLETADOS")
    print("=" * 80)
