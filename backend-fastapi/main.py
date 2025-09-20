from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Привет Мир API",
    description="Простое API с одним методом, возвращающим 'Привет мир!'",
    version="1.0.0"
)

# Настройка CORS для возможности обращения с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Корневой эндпоинт API
    """
    return {"message": "API работает! Используйте /hello для получения приветствия."}

@app.get("/hello")
async def hello_world():
    """
    Главный метод API, возвращающий приветствие
    """
    return {"message": "Привет мир!"}

@app.get("/hello/json")
async def hello_world_json():
    """
    Альтернативный метод, возвращающий более подробный JSON
    """
    return {
        "status": "success",
        "message": "Привет мир!",
        "timestamp": "2025-09-20",
        "api_version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """
    Проверка состояния API
    """
    return {"status": "healthy", "message": "API работает корректно"}

if __name__ == "__main__":
    # Запуск сервера для разработки
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоматическая перезагрузка при изменении кода
        log_level="info"
    )