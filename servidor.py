from fastapi import FastAPI, WebSocket, Body
from utilidades.camara import (
    capturarFotogramaJpg,
    obtenerControlesCamara,
    establecerControl,
    establecerMultiplesControles,
)
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import base64

aplicacion = FastAPI()
aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@aplicacion.get("/controles")
async def obtener_controles():
    return obtenerControlesCamara()


@aplicacion.websocket("/ws")
async def camaraEnVivo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            fotograma = capturarFotogramaJpg()
            fotogramaB64 = base64.b64encode(fotograma).decode("utf-8")
            await websocket.send_text(fotogramaB64)
            await asyncio.sleep(0.05)  # 20 fps aprox

    except WebSocketDisconnect:
        print("Cliente desconectado.")
    except Exception as e:
        print(f"Error en WebSocket: {e}")


@aplicacion.post("/controlar")
async def controlar(payload: dict = Body(...)):
    try:
        return establecerControl(payload["nombre"], payload["valor"])
    except Exception as e:
        return {"ok": False, "error": str(e)}


@aplicacion.post("/controlar-multiples")
async def controlar_multiples(payload: dict = Body(...)):
    try:
        return establecerMultiplesControles(payload)
    except Exception as e:
        return {"ok": False, "error": str(e)}
