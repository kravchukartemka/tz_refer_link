import asyncio
from fastapi import FastAPI
from app.api.api import app as api_app

# Создаем экземпляр FastAPI
app = FastAPI()

# Включаем эндпоинты API
app.include_router(api_app.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
