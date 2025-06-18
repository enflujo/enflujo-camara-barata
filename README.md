# Una cámara barata

Un proyecto en desarrollo para construir cámaras usando Raspberry Pi y sensores imx477 que permiten capturar imágenes de alta resolución 4056x3040 pixeles.

## Servidor 

```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt
```

En Raspberry Pi 5 no viene instalado picamera2 para usar con python, debemos instalarlo:

```bash
sudo apt install -y python3-picamera2 python3-libcamera libcamera-apps
```

correr servidor en puerto 8000

```bash
uvicorn servidor:aplicacion --host 0.0.0.0 --port 8000 --reload
```
