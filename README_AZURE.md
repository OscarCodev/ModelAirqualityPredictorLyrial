# Guía de Despliegue en Azure

## Método: GitHub → Azure Web App

Este proyecto está configurado para desplegarse automáticamente desde GitHub a Azure App Service.

---

## 📋 Pre-requisitos

1. **Cuenta de Azure** con una suscripción activa
2. **Repositorio GitHub** con el código del proyecto
3. **Azure CLI** instalado (opcional, pero recomendado)

---

## 🚀 Pasos de Configuración

### 1. Crear Azure Web App

#### Opción A: Desde Azure Portal

1. Ir a [portal.azure.com](https://portal.azure.com)
2. Clic en **"Create a resource"** → **"Web App"**
3. Configurar:
   - **Resource Group**: Crear o seleccionar uno
   - **Name**: Nombre único para tu app (ej: `air-quality-predictor-huamanga`)
   - **Publish**: `Code`
   - **Runtime stack**: `Python 3.12`
   - **Operating System**: `Linux`
   - **Region**: Elegir la más cercana
   - **Pricing Plan**: Seleccionar plan (F1 Free o superior)
4. Clic en **"Review + Create"** → **"Create"**

#### Opción B: Usando Azure CLI

```bash
# Login a Azure
az login

# Crear un Resource Group
az group create --name air-quality-rg --location eastus

# Crear un App Service Plan
az appservice plan create --name air-quality-plan --resource-group air-quality-rg --sku B1 --is-linux

# Crear la Web App
az webapp create --resource-group air-quality-rg --plan air-quality-plan --name air-quality-predictor-huamanga --runtime "PYTHON:3.12"
```

---

### 2. Configurar Variables de Entorno en Azure

1. En Azure Portal, ir a tu Web App
2. En el menú lateral: **Configuration** → **Application settings**
3. Agregar las siguientes variables:

| Nombre | Valor | Descripción |
|--------|-------|-------------|
| `OPENWEATHER_API_KEY` | `tu_api_key_aqui` | API Key de OpenWeatherMap |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` | Construir durante deployment |
| `WEBSITES_PORT` | `8000` | Puerto de la aplicación |

4. Clic en **"Save"**

---

### 3. Conectar GitHub con Azure

#### Opción A: Deployment Center (Recomendado)

1. En Azure Portal, ir a tu Web App
2. En el menú lateral: **Deployment Center**
3. Seleccionar **Source**: `GitHub`
4. Autorizar acceso a GitHub si es necesario
5. Seleccionar:
   - **Organization**: Tu cuenta de GitHub
   - **Repository**: El repositorio de tu proyecto
   - **Branch**: `main` (o la que uses)
6. Azure creará automáticamente un workflow en `.github/workflows/`
7. Clic en **"Save"**

#### Opción B: Usar el workflow incluido

Si prefieres usar nuestro workflow personalizado (`.github/workflows/azure-deploy.yml`):

1. En tu repositorio GitHub, ir a **Settings** → **Secrets and variables** → **Actions**
2. Crear los siguientes secrets:

   **Secret 1: `AZURE_WEBAPP_NAME`**
   - Valor: El nombre de tu Web App en Azure
   
   **Secret 2: `AZURE_WEBAPP_PUBLISH_PROFILE`**
   - En Azure Portal → Tu Web App → **Get publish profile**
   - Copiar todo el contenido XML
   - Pegarlo como valor del secret

3. Hacer push a la rama `main` para activar el deployment automático

---

### 4. Subir los Modelos a Azure

Los modelos entrenados (archivos `.joblib`) deben estar en el repositorio para que se desplieguen.

**Importante**: Asegúrate de que la carpeta `models/` con todos los archivos esté incluida en Git:

```bash
# Verificar que models/ no esté en .gitignore
git status

# Si models/ aparece como untracked, agregarla:
git add models/
git commit -m "Add trained models for deployment"
git push origin main
```

**Archivos necesarios en `models/`**:
- `model_NO2.joblib`
- `model_CO.joblib`
- `model_O3.joblib`
- `model_SO2.joblib`
- `model_aerosol_index.joblib`
- `scaler_NO2.joblib`
- `scaler_CO.joblib`
- `scaler_O3.joblib`
- `scaler_SO2.joblib`
- `scaler_aerosol_index.joblib`
- `feature_columns.joblib`

---

### 5. Verificar el Deployment

Una vez completado el deployment:

1. **Ver logs de deployment**:
   - En Azure Portal → Web App → **Deployment Center** → **Logs**
   
2. **Probar la API**:
   ```
   https://tu-app-name.azurewebsites.net/
   https://tu-app-name.azurewebsites.net/health
   https://tu-app-name.azurewebsites.net/docs
   ```

3. **Ver logs de aplicación**:
   - Azure Portal → Web App → **Log stream**

---

## 🔧 Archivos de Configuración Incluidos

Este proyecto incluye los siguientes archivos para Azure:

- **`startup.txt`**: Comando de inicio con Gunicorn
- **`runtime.txt`**: Especifica Python 3.12
- **`.deployment`**: Configuración de build de Azure
- **`requirements.txt`**: Dependencias Python (incluye gunicorn)
- **`.gitignore`**: Excluye archivos innecesarios
- **`.github/workflows/azure-deploy.yml`**: GitHub Actions para CI/CD

---

## 🐛 Troubleshooting

### Problema: "Application Error"

**Solución**:
1. Verificar logs en Azure Portal → **Log stream**
2. Revisar que `WEBSITES_PORT` esté configurado en 8000
3. Verificar que `gunicorn` esté en `requirements.txt`

### Problema: "Module not found"

**Solución**:
1. Verificar que `requirements.txt` incluye todas las dependencias
2. Asegurarse de que `SCM_DO_BUILD_DURING_DEPLOYMENT=true` en Configuration

### Problema: Modelos no se cargan

**Solución**:
1. Verificar que la carpeta `models/` está en el repositorio
2. Comprobar que todos los archivos `.joblib` están presentes
3. Ver logs para errores específicos

### Problema: Timeout en inicio

**Solución**:
1. El timeout está configurado en 120 segundos en `startup.txt`
2. Si necesitas más tiempo, edita `startup.txt`:
   ```
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000 --timeout 180
   ```

---

## 📊 Endpoints Disponibles

Una vez desplegado, tu API tendrá estos endpoints:

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Información básica de la API |
| `GET /health` | Health check |
| `GET /predict` | Predicciones para 7 días |
| `GET /predict/today` | Predicción solo para hoy |
| `GET /weather/current` | Clima actual |
| `GET /weather/forecast` | Pronóstico 5 días |
| `GET /weather/pollution` | Datos de contaminación actuales |
| `GET /aqi/info` | Información sobre AQI |
| `GET /pollutants/info` | Información sobre contaminantes |

**Documentación interactiva**: `https://tu-app.azurewebsites.net/docs`

---

## 🔐 Seguridad

**Importante**: Para producción, considera:

1. **Eliminar la API Key hardcodeada** de `config.py`:
   ```python
   # Cambiar:
   OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "7e2e121dba238439a5276c8b5c956fb6")
   
   # Por:
   OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
   if not OPENWEATHER_API_KEY:
       raise ValueError("OPENWEATHER_API_KEY no configurada")
   ```

2. **Configurar CORS** específicamente:
   - En `api.py`, limitar origins en producción

3. **Usar Azure Key Vault** para secrets sensibles

---

## 💡 Tips

1. **Monitoreo**: Habilita Application Insights en Azure para monitoreo avanzado
2. **Escalado**: Configura auto-scaling en el App Service Plan si esperas mucho tráfico
3. **Custom Domain**: Puedes agregar un dominio personalizado en Azure Portal
4. **SSL**: Azure provee SSL gratis para dominios `.azurewebsites.net`

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Azure Portal
2. Verifica la configuración de variables de entorno
3. Consulta la documentación de Azure: [docs.microsoft.com/azure/app-service](https://docs.microsoft.com/azure/app-service)

---

**¡Listo!** Tu API de predicción de calidad del aire ahora está desplegada en Azure 🎉
