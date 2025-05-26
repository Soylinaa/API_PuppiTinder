from fastapi import APIRouter, HTTPException, status,Depends
from typing import List
from models.models import Producto
from services.services import scraping, delete
from db.database import database

router = APIRouter()

@router.post("/productos",status_code=status.HTTP_201_CREATED)
async def post_productos():
    nuevos = scraping()
    if nuevos is None:
        raise HTTPException(status_code=500, detail="Error al insertar en la base de datos")
    return {"inserted": nuevos}

@router.get("/productos", status_code=status.HTTP_200_OK)
async def get_productos():
    comida = database.get_collection("productos")
    productos = list(comida.find({}, {"_id": False}))
    return productos

@router.delete("/productos/{id}", status_code=status.HTTP_200_OK)
async def delete_productos(id: str):
    return delete(id)