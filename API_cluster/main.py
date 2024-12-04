from app.api import router
import logging
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
import asyncio

# Configura el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Incluir las rutas de la API
app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a mi API"}