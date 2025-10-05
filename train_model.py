"""
Módulo para entrenar modelos de predicción de calidad del aire
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from datetime import datetime
import config


class AirQualityModel:
    """Clase para entrenar y usar modelos de predicción de calidad del aire"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = config.WEATHER_FEATURES
        self.target_pollutants = config.TARGET_POLLUTANTS
        
        # Crear directorio de modelos si no existe
        os.makedirs(config.MODEL_PATH, exist_ok=True)
        
    def load_and_prepare_data(self):
        """
        Carga y prepara los datos históricos
        
        Returns:
            tuple: (X, y_dict) donde X son las características y y_dict son los targets
        """
        print("Cargando datos...")
        df = pd.read_csv(config.DATA_PATH)
        
        # Convertir fecha a datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Agregar características temporales
        df['day_of_year'] = df['date'].dt.dayofyear
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        
        # Calcular promedios móviles para características meteorológicas
        for feature in self.feature_columns:
            if feature in df.columns:
                df[f'{feature}_ma7'] = df[feature].rolling(window=7, min_periods=1).mean()
                df[f'{feature}_ma30'] = df[feature].rolling(window=30, min_periods=1).mean()
        
        # Características finales
        feature_cols = self.feature_columns.copy()
        feature_cols.extend(['day_of_year', 'month'])
        
        # Agregar promedios móviles
        for feature in self.feature_columns:
            if f'{feature}_ma7' in df.columns:
                feature_cols.append(f'{feature}_ma7')
            if f'{feature}_ma30' in df.columns:
                feature_cols.append(f'{feature}_ma30')
        
        # Eliminar filas con valores faltantes en características
        df_clean = df.dropna(subset=feature_cols)
        
        X = df_clean[feature_cols]
        
        # Preparar targets (cada contaminante por separado)
        y_dict = {}
        for pollutant in self.target_pollutants:
            if pollutant in df_clean.columns:
                # Eliminar NaN en el target específico
                mask = df_clean[pollutant].notna()
                y_dict[pollutant] = {
                    'X': X[mask],
                    'y': df_clean.loc[mask, pollutant]
                }
        
        print(f"Datos cargados: {len(df_clean)} muestras")
        print(f"Características: {len(feature_cols)}")
        print(f"Contaminantes: {list(y_dict.keys())}")
        
        return feature_cols, y_dict
    
    def train_models(self):
        """
        Entrena modelos para cada contaminante
        """
        print("\n=== ENTRENANDO MODELOS ===\n")
        
        feature_cols, y_dict = self.load_and_prepare_data()
        
        results = {}
        
        for pollutant, data in y_dict.items():
            print(f"\nEntrenando modelo para {pollutant}...")
            
            X = data['X']
            y = data['y']
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=config.TEST_SIZE, 
                random_state=config.RANDOM_STATE,
                shuffle=True
            )
            
            # Escalar características
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Entrenar Gradient Boosting (mejor para series temporales)
            model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=4,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=config.RANDOM_STATE,
                verbose=1
            )
            
            model.fit(X_train_scaled, y_train)
            
            # Evaluar
            y_pred = model.predict(X_test_scaled)
            
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            print(f"  MAE: {mae:.6f}")
            print(f"  RMSE: {rmse:.6f}")
            print(f"  R²: {r2:.4f}")
            
            # Guardar modelo y scaler
            self.models[pollutant] = model
            self.scalers[pollutant] = scaler
            
            results[pollutant] = {
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'n_train': len(X_train),
                'n_test': len(X_test)
            }
            
            # Guardar en disco
            model_filename = os.path.join(config.MODEL_PATH, f'model_{pollutant}.joblib')
            scaler_filename = os.path.join(config.MODEL_PATH, f'scaler_{pollutant}.joblib')
            
            joblib.dump(model, model_filename)
            joblib.dump(scaler, scaler_filename)
            
            print(f"  Modelo guardado en: {model_filename}")
        
        # Guardar columnas de características
        features_filename = os.path.join(config.MODEL_PATH, 'feature_columns.joblib')
        joblib.dump(feature_cols, features_filename)
        
        print("\n=== ENTRENAMIENTO COMPLETADO ===")
        return results
    
    def load_models(self):
        """
        Carga modelos entrenados desde disco
        """
        print("Cargando modelos...")
        
        # Cargar columnas de características
        features_filename = os.path.join(config.MODEL_PATH, 'feature_columns.joblib')
        if os.path.exists(features_filename):
            self.feature_columns = joblib.load(features_filename)
        
        # Cargar cada modelo
        for pollutant in self.target_pollutants:
            model_filename = os.path.join(config.MODEL_PATH, f'model_{pollutant}.joblib')
            scaler_filename = os.path.join(config.MODEL_PATH, f'scaler_{pollutant}.joblib')
            
            if os.path.exists(model_filename) and os.path.exists(scaler_filename):
                self.models[pollutant] = joblib.load(model_filename)
                self.scalers[pollutant] = joblib.load(scaler_filename)
                print(f"  Modelo {pollutant} cargado")
            else:
                print(f"  Advertencia: Modelo {pollutant} no encontrado")
        
        return len(self.models) > 0
    
    def prepare_weather_features(self, weather_data, historical_df=None):
        """
        Prepara características a partir de datos meteorológicos
        
        Args:
            weather_data (dict): Datos meteorológicos de la API
            historical_df (DataFrame): Datos históricos para calcular promedios móviles
            
        Returns:
            DataFrame: Características preparadas
        """
        # Crear DataFrame con características básicas
        features = {}
        
        for feature in config.WEATHER_FEATURES:
            if feature in weather_data:
                features[feature] = weather_data[feature]
        
        # Agregar características temporales
        if 'date' in weather_data:
            date = weather_data['date']
        elif 'timestamp' in weather_data:
            date = weather_data['timestamp']
        else:
            date = datetime.now()
        
        features['day_of_year'] = date.timetuple().tm_yday
        features['month'] = date.month
        
        # Calcular promedios móviles si hay datos históricos
        if historical_df is not None:
            for feature in config.WEATHER_FEATURES:
                if feature in historical_df.columns:
                    ma7 = historical_df[feature].tail(7).mean()
                    ma30 = historical_df[feature].tail(30).mean()
                    features[f'{feature}_ma7'] = ma7
                    features[f'{feature}_ma30'] = ma30
        else:
            # Usar valores actuales si no hay históricos
            for feature in config.WEATHER_FEATURES:
                if feature in features:
                    features[f'{feature}_ma7'] = features[feature]
                    features[f'{feature}_ma30'] = features[feature]
        
        return pd.DataFrame([features])
    
    def predict(self, weather_data_list):
        """
        Predice la calidad del aire para datos meteorológicos dados
        
        Args:
            weather_data_list (list): Lista de diccionarios con datos meteorológicos
            
        Returns:
            DataFrame: Predicciones para cada contaminante
        """
        if not self.models:
            raise ValueError("No hay modelos cargados. Ejecuta load_models() primero.")
        
        # Cargar datos históricos para promedios móviles
        df_historical = pd.read_csv(config.DATA_PATH)
        df_historical['date'] = pd.to_datetime(df_historical['date'])
        
        predictions = []
        
        for weather_data in weather_data_list:
            # Preparar características
            X = self.prepare_weather_features(weather_data, df_historical)
            
            # Asegurar que las columnas coincidan con las del entrenamiento
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0
            
            X = X[self.feature_columns]
            
            # Predecir cada contaminante
            pred_row = {}
            
            if 'date' in weather_data:
                pred_row['date'] = weather_data['date']
            elif 'timestamp' in weather_data:
                pred_row['date'] = weather_data['timestamp']
            
            for pollutant, model in self.models.items():
                scaler = self.scalers[pollutant]
                X_scaled = scaler.transform(X)
                prediction = model.predict(X_scaled)[0]
                pred_row[pollutant] = max(0, prediction)  # No permitir valores negativos
            
            predictions.append(pred_row)
        
        return pd.DataFrame(predictions)


if __name__ == "__main__":
    # Entrenar modelos
    model = AirQualityModel()
    results = model.train_models()
    
    print("\n=== RESUMEN DE RESULTADOS ===")
    for pollutant, metrics in results.items():
        print(f"\n{pollutant}:")
        print(f"  R² Score: {metrics['r2']:.4f}")
        print(f"  MAE: {metrics['mae']:.6f}")
        print(f"  Muestras entrenamiento: {metrics['n_train']}")
        print(f"  Muestras prueba: {metrics['n_test']}")
