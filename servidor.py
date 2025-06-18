from fastapi import FastAPI, WebSocket
from utilidades.camara import capturarFotogramaJpg, camara
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
    controles = {}
    for nombre, info in camara.camera_controls.items():
        control = {
            "type": str(info[0]),
            "default": info[1] if len(info) > 1 else None,
            "min": info[2] if len(info) > 2 else None,
            "max": info[3] if len(info) > 3 else None,
            "step": info[4] if len(info) > 4 else None,
        }
        controles[nombre] = control
    return controles


@aplicacion.websocket("/ws")
async def camaraEnVivo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            fotograma = capturarFotogramaJpg()
            fotograma_b64 = base64.b64encode(fotograma).decode("utf-8")
            await websocket.send_text(fotograma_b64)
            await asyncio.sleep(0.05)  # 20 fps aprox
    except WebSocketDisconnect:
        print("Cliente desconectado.")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
