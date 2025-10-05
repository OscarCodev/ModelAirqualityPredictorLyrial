"""
Script principal para predecir la calidad del aire
Usa datos de OpenWeatherMap API y modelos entrenados
"""

import pandas as pd
from datetime import datetime, timedelta
import os
import json

import config
from weather_api import WeatherAPI
from train_model import AirQualityModel


class AirQualityPredictor:
    """Clase principal para hacer predicciones de calidad del aire"""
    
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.model = AirQualityModel()
        
        # Crear directorio de predicciones
        os.makedirs(config.PREDICTIONS_PATH, exist_ok=True)
        
    def predict_current_and_forecast(self, days=7):
        """
        Predice la calidad del aire para hoy y los próximos días
        
        Args:
            days (int): Número de días a predecir (incluyendo hoy)
            
        Returns:
            DataFrame: Predicciones de calidad del aire
        """
        print("=== PREDICCIÓN DE CALIDAD DEL AIRE ===\n")
        
        # Cargar modelos
        print("1. Cargando modelos entrenados...")
        if not self.model.load_models():
            print("   ERROR: No se pudieron cargar los modelos.")
            print("   Ejecuta primero: python train_model.py")
            return None
        
        # Obtener datos meteorológicos actuales
        print("\n2. Obteniendo datos meteorológicos actuales...")
        current_weather = self.weather_api.get_current_weather()
        
        if not current_weather:
            print("   ERROR: No se pudieron obtener datos meteorológicos actuales")
            return None
        
        print(f"   Temperatura: {current_weather['temperature'] - 273.15:.1f}°C")
        print(f"   Presión: {current_weather['pressure']/100:.1f} hPa")
        print(f"   Precipitación: {current_weather['precipitation']*1000:.2f} mm/h")
        
        # Obtener pronóstico
        print(f"\n3. Obteniendo pronóstico para {days} días...")
        forecast = self.weather_api.get_forecast(days)
        
        if not forecast:
            print("   ERROR: No se pudo obtener el pronóstico")
            return None
        
        print(f"   Pronóstico obtenido para {len(forecast)} días")
        
        # Preparar datos para predicción
        weather_data_list = [current_weather] + forecast
        
        # Hacer predicciones
        print("\n4. Generando predicciones de calidad del aire...")
        predictions = self.model.predict(weather_data_list)
        
        if predictions is None or predictions.empty:
            print("   ERROR: No se pudieron generar predicciones")
            return None
        
        print(f"   Predicciones generadas para {len(predictions)} días")
        
        return predictions
    
    def get_air_quality_index(self, predictions):
        """
        Calcula un índice de calidad del aire basado en los contaminantes
        
        Args:
            predictions (DataFrame): Predicciones de contaminantes
            
        Returns:
            DataFrame: Predicciones con índice de calidad del aire
        """
        df = predictions.copy()
        
        # Normalizar contaminantes (valores típicos como referencia)
        # Estos son valores aproximados basados en los datos históricos
        pollutant_scales = {
            'NO2': 5e-5,    # ~50 µg/m³
            'CO': 0.03,     # ~30 mg/m³
            'O3': 0.12,     # ~120 µg/m³
            'SO2': 1e-4,    # ~100 µg/m³
            'aerosol_index': 3.0
        }
        
        aqi_components = []
        
        for pollutant, scale in pollutant_scales.items():
            if pollutant in df.columns:
                # Normalizar a escala 0-100
                normalized = (df[pollutant] / scale) * 100
                aqi_components.append(normalized)
        
        if aqi_components:
            # Calcular AQI como promedio ponderado
            df['AQI'] = pd.concat(aqi_components, axis=1).mean(axis=1)
            
            # Clasificar calidad del aire
            def classify_aqi(aqi):
                if aqi <= 50:
                    return 'Buena'
                elif aqi <= 100:
                    return 'Moderada'
                elif aqi <= 150:
                    return 'Dañina para grupos sensibles'
                elif aqi <= 200:
                    return 'Dañina'
                elif aqi <= 300:
                    return 'Muy dañina'
                else:
                    return 'Peligrosa'
            
            df['Calidad'] = df['AQI'].apply(classify_aqi)
        
        return df
    
    def display_predictions(self, predictions):
        """
        Muestra las predicciones de forma legible
        
        Args:
            predictions (DataFrame): Predicciones de calidad del aire
        """
        print("\n" + "="*80)
        print("PREDICCIONES DE CALIDAD DEL AIRE - HUAMANGA, AYACUCHO, PERÚ")
        print("="*80 + "\n")
        
        predictions_with_aqi = self.get_air_quality_index(predictions)
        
        for idx, row in predictions_with_aqi.iterrows():
            date = row['date']
            if isinstance(date, str):
                date = datetime.fromisoformat(date)
            
            if idx == 0:
                print(f"📅 HOY - {date.strftime('%d/%m/%Y')}")
            else:
                print(f"📅 {date.strftime('%A, %d/%m/%Y')}")
            
            print("-" * 80)
            
            # Mostrar contaminantes
            print("\nContaminantes:")
            if 'NO2' in row:
                print(f"  NO₂ (Dióxido de nitrógeno):  {row['NO2']*1e6:.2f} µg/m³")
            if 'CO' in row:
                print(f"  CO (Monóxido de carbono):    {row['CO']*1e3:.2f} mg/m³")
            if 'O3' in row:
                print(f"  O₃ (Ozono):                  {row['O3']*1e6:.2f} µg/m³")
            if 'SO2' in row:
                print(f"  SO₂ (Dióxido de azufre):     {row['SO2']*1e6:.2f} µg/m³")
            if 'aerosol_index' in row:
                print(f"  Índice de aerosoles:         {row['aerosol_index']:.2f}")
            
            # Mostrar índice de calidad
            if 'AQI' in row:
                aqi = row['AQI']
                calidad = row['Calidad']
                
                # Emoji según calidad
                emoji_map = {
                    'Buena': '🟢',
                    'Moderada': '🟡',
                    'Dañina para grupos sensibles': '🟠',
                    'Dañina': '🔴',
                    'Muy dañina': '🟣',
                    'Peligrosa': '🔴'
                }
                emoji = emoji_map.get(calidad, '⚪')
                
                print(f"\n{emoji} ÍNDICE DE CALIDAD DEL AIRE (AQI): {aqi:.1f}")
                print(f"   Clasificación: {calidad}")
                
                # Recomendaciones
                if calidad == 'Buena':
                    print("   ✓ Calidad del aire satisfactoria, sin riesgos")
                elif calidad == 'Moderada':
                    print("   ⚠ Aceptable para la mayoría, grupos sensibles deben limitar esfuerzos prolongados al aire libre")
                else:
                    print("   ⚠ Se recomienda reducir actividades al aire libre")
            
            print("\n")
        
        print("="*80)
    
    def save_predictions(self, predictions):
        """
        Guarda las predicciones en archivos CSV y JSON
        
        Args:
            predictions (DataFrame): Predicciones de calidad del aire
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Agregar AQI
        predictions_with_aqi = self.get_air_quality_index(predictions)
        
        # Guardar CSV
        csv_filename = os.path.join(config.PREDICTIONS_PATH, f'predicciones_{timestamp}.csv')
        predictions_with_aqi.to_csv(csv_filename, index=False)
        print(f"\n📁 Predicciones guardadas en: {csv_filename}")
        
        # Guardar JSON
        json_filename = os.path.join(config.PREDICTIONS_PATH, f'predicciones_{timestamp}.json')
        
        # Convertir fechas a string para JSON
        predictions_json = predictions_with_aqi.copy()
        if 'date' in predictions_json.columns:
            predictions_json['date'] = predictions_json['date'].astype(str)
        
        predictions_dict = predictions_json.to_dict(orient='records')
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(predictions_dict, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Predicciones guardadas en: {json_filename}")
    
    def run(self, days=7, save=True):
        """
        Ejecuta el proceso completo de predicción
        
        Args:
            days (int): Número de días a predecir (incluyendo hoy)
            save (bool): Si se deben guardar las predicciones
        """
        # Hacer predicciones
        predictions = self.predict_current_and_forecast(days)
        
        if predictions is not None:
            # Mostrar predicciones
            self.display_predictions(predictions)
            
            # Guardar si se solicita
            if save:
                self.save_predictions(predictions)
            
            return predictions
        
        return None


def main():
    """Función principal"""
    predictor = AirQualityPredictor()
    
    # Predecir para hoy y los próximos 6 días (7 días en total)
    predictions = predictor.run(days=7, save=True)
    
    if predictions is None:
        print("\n❌ No se pudieron generar las predicciones")
        print("\nAsegúrate de:")
        print("1. Tener conexión a internet")
        print("2. Haber entrenado los modelos primero: python train_model.py")
        print("3. Que la API key de OpenWeatherMap sea válida")


if __name__ == "__main__":
    main()
