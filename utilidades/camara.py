from picamera2 import Picamera2
from PIL import Image
import io

camara = Picamera2()
if not camara.started:
    camara.configure(camara.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    camara.start()

def capturarFotogramaJpg():
    fotograma = camara.capture_array()
    img = Image.fromarray(fotograma)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return buffer.getvalue()
