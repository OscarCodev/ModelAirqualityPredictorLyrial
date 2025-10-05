"""
Script para iniciar la API REST de predicción de calidad del aire
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 80)
    print("🌍 API DE PREDICCIÓN DE CALIDAD DEL AIRE - HUAMANGA")
    print("=" * 80)
    print("\n📍 Ubicación: Huamanga, Ayacucho, Perú")
    print("📐 Coordenadas: -13.1631, -74.2236")
    print("\n🚀 Iniciando servidor...")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("\n⏸️  Presiona CTRL+C para detener\n")
    print("=" * 80)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
