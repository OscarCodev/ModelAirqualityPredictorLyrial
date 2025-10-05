"""
Script de prueba para la API de predicción de calidad del aire
"""

import requests
import json
from datetime import datetime

# URL base de la API
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime una sección con formato"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_health():
    """Probar endpoint de health check"""
    print_section("🏥 TEST: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        print(f"Status: {data['status']}")
        print(f"Modelos cargados: {data['models_loaded']}")
        print(f"API conectada: {data['api_connected']}")
        print(f"✅ Health check OK")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_current_weather():
    """Probar endpoint de clima actual"""
    print_section("🌤️ TEST: Clima Actual")
    
    try:
        response = requests.get(f"{BASE_URL}/weather/current")
        data = response.json()
        
        print(f"Temperatura: {data['temperature_celsius']:.1f}°C")
        print(f"Presión: {data['pressure_hpa']:.1f} hPa")
        print(f"Velocidad del viento: {data['wind_speed']:.2f} m/s")
        print(f"Precipitación: {data['precipitation_mm']:.2f} mm/h")
        print(f"✅ Datos meteorológicos obtenidos")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_forecast():
    """Probar endpoint de pronóstico"""
    print_section("📅 TEST: Pronóstico Meteorológico (3 días)")
    
    try:
        response = requests.get(f"{BASE_URL}/weather/forecast?days=3")
        data = response.json()
        
        for day in data:
            print(f"\n{day['date']}:")
            print(f"  Temperatura: {day['temperature_celsius']:.1f}°C")
            print(f"  Presión: {day['pressure_hpa']:.1f} hPa")
        
        print(f"\n✅ Pronóstico obtenido para {len(data)} días")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pollution():
    """Probar endpoint de contaminación"""
    print_section("💨 TEST: Contaminación Actual")
    
    try:
        response = requests.get(f"{BASE_URL}/weather/pollution")
        data = response.json()
        
        print(f"NO₂: {data['NO2']:.2f} µg/m³")
        print(f"CO: {data['CO']:.2f} mg/m³")
        print(f"O₃: {data['O3']:.2f} µg/m³")
        print(f"SO₂: {data['SO2']:.2f} µg/m³")
        print(f"PM2.5: {data['pm2_5']:.2f} µg/m³")
        print(f"PM10: {data['pm10']:.2f} µg/m³")
        print(f"✅ Datos de contaminación obtenidos")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_today():
    """Probar endpoint de predicción para hoy"""
    print_section("🎯 TEST: Predicción de Hoy")
    
    try:
        response = requests.get(f"{BASE_URL}/predict/today")
        data = response.json()
        
        print(f"Fecha: {data['date']}")
        print(f"\nContaminantes predichos:")
        print(f"  NO₂: {data['NO2_ugm3']:.2f} µg/m³")
        print(f"  CO: {data['CO_mgm3']:.2f} mg/m³")
        print(f"  O₃: {data['O3_ugm3']:.2f} µg/m³")
        print(f"  SO₂: {data['SO2_ugm3']:.2f} µg/m³")
        print(f"  Índice de aerosoles: {data['aerosol_index']:.2f}")
        
        print(f"\n📊 AQI: {data['AQI']:.1f}")
        print(f"📋 Calidad del Aire: {data['quality']}")
        print(f"\n✅ Predicción para hoy generada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_week():
    """Probar endpoint de predicción para varios días"""
    print_section("📈 TEST: Predicción de 7 Días")
    
    try:
        response = requests.get(f"{BASE_URL}/predict?days=7")
        data = response.json()
        
        print(f"Predicciones generadas para {len(data)} días:\n")
        
        for pred in data:
            date = pred['date']
            aqi = pred['AQI']
            quality = pred['quality']
            
            # Emoji según calidad
            emoji_map = {
                'Buena': '🟢',
                'Moderada': '🟡',
                'Dañina para grupos sensibles': '🟠',
                'Dañina': '🔴',
                'Muy dañina': '🟣',
                'Peligrosa': '🔴'
            }
            emoji = emoji_map.get(quality, '⚪')
            
            print(f"{emoji} {date}: AQI={aqi:.1f} ({quality})")
        
        print(f"\n✅ Predicción de 7 días generada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_aqi_info():
    """Probar endpoint de información de AQI"""
    print_section("ℹ️ TEST: Información de AQI")
    
    try:
        response = requests.get(f"{BASE_URL}/aqi/info?aqi=75")
        data = response.json()
        
        print(f"AQI: {data['aqi']}")
        print(f"Clasificación: {data['classification']}")
        print(f"Color: {data['color']}")
        print(f"Emoji: {data['emoji']}")
        print(f"\nImplicaciones de salud:")
        print(f"  {data['health_implications']}")
        print(f"\nRecomendación:")
        print(f"  {data['cautionary_statement']}")
        print(f"\n✅ Información de AQI obtenida")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pollutants_info():
    """Probar endpoint de información de contaminantes"""
    print_section("🔬 TEST: Información de Contaminantes")
    
    try:
        response = requests.get(f"{BASE_URL}/pollutants/info")
        data = response.json()
        
        print(f"Contaminantes: {len(data['pollutants'])}\n")
        
        for pollutant in data['pollutants'][:3]:  # Mostrar solo 3
            print(f"{pollutant['symbol']} - {pollutant['name']}")
            print(f"  Unidad: {pollutant['unit']}")
            print(f"  Fuentes: {', '.join(pollutant['sources'])}")
            print()
        
        print(f"✅ Información de contaminantes obtenida")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("\n" + "█"*80)
    print("  🧪 SUITE DE PRUEBAS - API DE CALIDAD DEL AIRE")
    print("█"*80)
    print(f"\n⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API URL: {BASE_URL}")
    
    # Lista de pruebas
    tests = [
        ("Health Check", test_health),
        ("Clima Actual", test_current_weather),
        ("Pronóstico", test_forecast),
        ("Contaminación Actual", test_pollution),
        ("Predicción de Hoy", test_predict_today),
        ("Predicción de 7 Días", test_predict_week),
        ("Información de AQI", test_aqi_info),
        ("Información de Contaminantes", test_pollutants_info),
    ]
    
    results = []
    
    # Ejecutar cada prueba
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen de resultados
    print_section("📊 RESUMEN DE RESULTADOS")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*80}")
    print(f"  Total: {passed}/{total} pruebas exitosas ({passed/total*100:.1f}%)")
    print(f"{'='*80}\n")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
    else:
        print(f"⚠️ {total - passed} prueba(s) fallaron")
    
    print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  NOTA: Asegúrate de que la API esté ejecutándose")
    print("  Ejecuta en otra terminal: python start_api.py")
    print("="*80)
    
    input("\nPresiona ENTER para iniciar las pruebas...")
    
    run_all_tests()
