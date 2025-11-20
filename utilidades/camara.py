from picamera2 import Picamera2
from PIL import Image
import io


"""
Diccionario de controles de la cámara 

AeConstraintMode: Define el modo de restricción del algoritmo AEC/AGC | "Normal" para ponderación normal, "Highlight" para resaltar, "Shadows" para sombras y "Custom" para medición personalizada.

AeEnable: Permite activar o desactivar el algoritmo AEC/AGC | "False" para desactivar y "True" para activar.

AeExposureMode: Define el modo de exposición del algoritmo AEC/AGC | "Normal" para exposiciones normales, "Short" para exposiciones cortas, "Long" para exposiciones largas y "Custom" para exposiciones personalizadas.

AeFlickerMode: Define el modo de evitación de parpadeo del algoritmo AEC/AGC | "FlickerOff" para sin evitación, "FlickerManual" para evitar parpadeo con un período definido en el control "AeFlickerPeriod".

AeFlickerPeriod: Define el período de parpadeo de la iluminación en microsegundos | Por ejemplo, para iluminación de 50Hz, el período sería 10000 microsegundos.

AeMeteringMode: Define el modo de medición del algoritmo AEC/AGC | "CentreWeighted" para ponderación central, "Spot" para medición puntual, "Matrix" para medición matricial y "Custom" para medición personalizada.

AfMetering: Define dónde se debe medir el enfoque | "Auto" para usar la región central de la imagen y "Windows" para usar las ventanas dadas en el control AfWindows.

AfMode: Define el modo de enfoque automático | "Manual" para modo manual, "Auto" para modo automático y "Continuous" para modo continuo.

AfPause: Pausa el enfoque automático continuo | "Deferred" para pausar cuando no se está escaneando, "Immediate" para pausar inmediatamente y "Resume" para reanudar el enfoque automático continuo.

AfRange: Define el rango de posiciones del lente a buscar | "Normal" para rango normal, "Macro" para rango cercano y "Full" para buscar todo.

AfSpeed: Define la velocidad de búsqueda del enfoque automático | "Normal" para velocidad normal y "Fast" para intentar mover más rápido.

AfTrigger: Inicia un ciclo de enfoque automático | "Start" para iniciar el ciclo y "Cancel" para cancelar un ciclo en progreso.

AfWindows: Define las ventanas en la imagen para medir el enfoque | Una lista de rectángulos (tuplas de 4 números que indican x_offset, y_offset, ancho y alto).

AnalogueGain: Ganancia analógica aplicada por el sensor | Consultar la propiedad camera_controls.

AwbEnable: Permite activar o desactivar el algoritmo de balance de blancos automático (AWB) | "False" para desactivar y "True" para activar.

AwbMode: Define el modo del algoritmo AWB | "Auto" para cualquier iluminación, "Tungsten" para iluminación de tungsteno, "Fluorescent" para iluminación fluorescente, "Indoor" para iluminación interior, "Daylight" para iluminación diurna, "Cloudy" para iluminación nublada y "Custom" para configuración personalizada.

Brightness: Ajusta el brillo de la imagen | -1.0 para muy oscuro, 1.0 para muy brillante y 0.0 para brillo "normal".

ColourCorrectionMatrix: Matriz 3x3 utilizada por el procesador de señal de imagen (ISP) para convertir los colores del sensor a sRGB | Tupla de nueve números flotantes entre -16.0 y 16.0.

ColourGains: Par de números donde el primero es la ganancia roja (aplicada a los píxeles rojos por el algoritmo AWB) y el segundo es la ganancia azul | Tupla de dos números flotantes entre 0.0 y 32.

ColourTemperature: Estimación de la temperatura de color (en Kelvin) de la imagen actual | Disponible solo en metadatos de imagen capturada y es de solo lectura.

Contrast: Ajusta el contraste de la imagen | Donde cero es "sin contraste", 1.0 es el contraste "normal" predeterminado y valores más altos aumentan el contraste proporcionalmente

DigitalGain: Cantidad de ganancia digital aplicada a una imagen | La ganancia digital se utiliza automáticamente cuando la ganancia analógica del sensor no es suficiente, y este valor solo se reporta en los metadatos de imagen capturada. No se puede establecer directamente; los usuarios deben establecer la ganancia analógica (AnalogueGain) y la ganancia digital se utilizará cuando sea necesario.

ExposureTime: Tiempo de exposición para que el sensor use, medido en microsegundos | Consultar la propiedad camera_controls.

ExposureValue: Valor de compensación de exposición en "stops", que ajusta el objetivo del algoritmo AEC/AGC | Valores positivos aumentan el brillo objetivo, valores negativos lo disminuyen y cero representa el nivel de exposición base o "normal".

FrameDuration: Tiempo (en microsegundos) desde el fotograma anterior | Este valor solo está disponible en los metadatos de imagen capturada y es de solo lectura.

FrameDurationLimits: Tiempo máximo y mínimo que el sensor puede tardar en entregar un fotograma, medido en microsegundos | Los recíprocos de estos valores (primero dividido por 1000000) darán las tasas de fotogramas mínima y máxima que el sensor puede entregar. Consultar la propiedad camera_controls.

HdrChannel: Informa qué canal HDR representa el fotograma actual | Es de solo lectura y no se puede establecer. HdrChannelEnum seguido de uno de: HdrChannelNone (imagen no utilizada para HDR), HdrChannelShort (imagen de exposición corta para HDR), HdrChannelMedium (imagen de exposición media para HDR) y HdrChannelLong (imagen de exposición larga para HDR).

HdrMode: Define si se ejecuta la cámara en un modo HDR (distinto del HDR en cámara admitido por la Cámara Módulo 3) | HdrModeEnum seguido de uno de: Off (desactivar HDR), SingleExposure (combinar múltiples imágenes de exposición corta, recomendado en Pi 5), MultiExposure (combinar imágenes cortas y largas, recomendado solo cuando la escena es completamente estática en Pi 5), Night (modo HDR que combina múltiples imágenes de baja luz y puede recuperar algunos reflejos, recomendado en Pi 5) y MultiExposureUnmerged (devolver imágenes de exposición corta y larga no fusionadas). 

LensPosition: Posición del lente | Las unidades son dioptrías (recíproco de la distancia en metros). Consultar la propiedad camera_controls.

Lux: Estimación del brillo (en lux) de la escena | Disponible solo en los metadatos de imagen capturada y es de solo lectura.

NoiseReductionMode: Selecciona un modo adecuado de reducción de ruido | Normalmente, la configuración de Picamera2 seleccionará un modo apropiado automáticamente, por lo que no debería ser necesario cambiarlo. El modo de reducción de ruido de alta calidad puede afectar la tasa de fotogramas máxima alcanzable.

Saturation: Cantidad de saturación del color | Donde cero produce imágenes en escala de grises, 1.0 representa la saturación "normal" predeterminada y valores más altos producen colores más saturados | Número flotante de 0.0 a 32.

ScalerCrop: El rectángulo de recorte del escalador determina qué parte de la imagen recibida del sensor se recorta y luego se escala para producir una imagen de tamaño correcto. Se puede usar para implementar zoom digital | Un libcamera.Rectangle que consiste en: x_offset, y_offset, ancho, alto.

SensorTimestamp: Hora en que este fotograma fue producido por el sensor, medida en nanosegundos desde que el sistema se inició | El tiempo se muestrea en la interrupción de inicio de fotograma de la cámara, que ocurre cuando se escribe el primer píxel del nuevo fotograma por el sensor. Este control aparece solo en los metadatos de imagen capturada y es de solo lectura.

SensorBlackLevels: Los niveles de negro de la imagen cruda del sensor. Este control aparece solo en los metadatos de imagen capturada y es de solo lectura. Se informa un valor para cada uno de los cuatro canales Bayer, escalado como si el rango completo de píxeles fuera de 16 bits (por lo que 4096 representa un nivel de negro 16 en los datos crudos de 10-bits). | tuple o 4 integrales.

Sharpness: Establece la nitidez de la imagen, donde cero implica que no se aplica nitidez adicional, 1.0 es el nivel predeterminado de "nitidez normal" y valores más altos aplican una nitidez más fuerte | Número flotante de 0.0 a 16.0.

SyncMode: Para captura sincronizada desde múltiples cámaras. Establece el dispositivo en modo de sincronización "servidor" o "cliente". | Off - desactivar el modo de sincronización, Server - habilitar el modo de sincronización y actuar como servidor, Client - habilitar el modo de sincronización y actuar como cliente.

SyncReady: Cuando está en modo de sincronización, indica a la aplicación el primer fotograma para el cual las cámaras están sincronizadas. Las aplicaciones deben esperar a que este valor sea distinto de cero antes de usar los fotogramas. Antes de este punto, los fotogramas pueden no estar sincronizados | Entero.

SyncTimer: Cuando las cámaras están en modo de sincronización, este valor representa el tiempo estimado en microsegundos hasta el "punto de sincronización" en el que el control "SyncReady" se volverá distinto de cero. Después de este punto, el valor informado aquí será negativo (ya que el tiempo ha transcurrido) | Entero.

SyncFrames: Cuando las cámaras están en modo de sincronización, este valor se puede establecer solo para el servidor como el retraso (en fotogramas) antes de que todas las cámaras se marquen como sincronizadas (al volverse "SyncReady" distinto de cero). El retraso aquí debe ser lo suficientemente largo para que todos los clientes hayan sido iniciados y hayan tenido tiempo para ajustarse a los mensajes de temporización del servidor | Entero positivo.
"""

camara = Picamera2()

if not camara.started:
    config = camara.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
    camara.align_configuration(config)
    camara.configure(config)

    camara.set_controls(
        {
            "AwbEnable": True,
            "AwbMode": 0,  # Auto
            "AeEnable": True,
            "HdrMode": 0,
            "Saturation": 1.0,
            "Contrast": 1.0,
            "Sharpness": 1.0,
        }
    )
    camara.start()
    print(camara.camera_controls["ScalerCrop"])


def capturarFotogramaJpg():
    """
    Obtiene un fotograma en JPEG desde la cámara.
    Picamera2 devuelve los bytes en BGR aunque se especifique RGB888,
    por lo tanto se convierte manualmente a RGB antes de convertir a JPEG.
    """

    fotograma = camara.capture_array()  # Buffer BGR de libcamera
    # Convertimos BGR → RGB (forma eficiente)
    fotograma = fotograma[..., ::-1]

    img = Image.fromarray(fotograma, "RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)

    return buffer.getvalue()


def obtenerControlesCamara():
    controles = {}

    for nombre, info in camara.camera_controls.items():
        minimo, maximo, pred = info

        control = {
            "min": minimo,
            "max": maximo,
            "predeterminado": pred,
        }
        controles[nombre] = control

    return controles


def _convertir_valor(valor, minimo):
    """
    Convierte un valor al tipo adecuado según el tipo del mínimo.
    """
    # booleano
    if isinstance(minimo, bool):
        if isinstance(valor, str):
            return valor.lower() in ("true", "1", "yes", "on")
        return bool(valor)

    # array / lista / tupla
    if isinstance(minimo, (list, tuple)):
        return [_convertir_valor(v, minimo[0]) for v in valor]

    # entero
    if isinstance(minimo, int):
        return int(valor)

    # flotante
    return float(valor)


def _validar_rango(nombre, valor, minimo, maximo):
    # No validar controles sin rango real
    if minimo is None or maximo is None:
        return

    # Validación de array (ScalerCrop, ColourGains, etc.)
    if isinstance(minimo, (list, tuple)):
        for i, v in enumerate(valor):

            # NO validar offsets (posición X/Y)
            if i in (0, 1):
                continue

            min_i = minimo[i]
            max_i = maximo[i]

            if min_i is None or max_i is None:
                continue

            if v < min_i or v > max_i:
                raise ValueError(
                    f"Elemento {i} de {nombre} fuera de rango: {v} "
                    f"(min={min_i}, max={max_i})"
                )
    else:
        if valor < minimo or valor > maximo:
            raise ValueError(
                f"Valor fuera de rango para {nombre}: {valor} "
                f"(min={minimo}, max={maximo})"
            )


def detenerCamara():
    if camara.started:
        camara.stop()
        print("Cámara detenida.")
    else:
        print("La cámara ya está detenida.")


def iniciarCamara():
    if not camara.started:
        camara.start()
        print("Cámara iniciada.")
    else:
        print("La cámara ya está en funcionamiento.")


def establecerControl(nombre, valor):
    """
    Ajusta un control de la cámara validando rango y tipo.
    Ejemplos de uso:
        establecerControl("ExposureTime", 8000)
        establecerControl("AnalogueGain", 1.5)
    """

    if nombre == "ScalerCrop" and not isinstance(valor, (list, tuple)):
        raise ValueError("ScalerCrop debe ser una lista de 4 elementos.")

    controles = camara.camera_controls

    if nombre not in controles:
        raise ValueError(f"Control '{nombre}' no existe.")

    minimo, maximo, _ = controles[nombre]

    valor_cast = _convertir_valor(valor, minimo)
    _validar_rango(nombre, valor_cast, minimo, maximo)

    camara.set_controls({nombre: valor_cast})
    return {"ok": True, "nombre": nombre, "valor": valor_cast}


def establecerMultiplesControles(datos: dict):
    controles = camara.camera_controls
    cambios = {}

    for nombre, valor in datos.items():
        if nombre not in controles:
            raise ValueError(f"Control '{nombre}' no existe.")

        minimo, maximo, _ = controles[nombre]

        valor_cast = _convertir_valor(valor, minimo)
        _validar_rango(nombre, valor_cast, minimo, maximo)

        cambios[nombre] = valor_cast

    camara.set_controls(cambios)
    return {"ok": True, "cambios": cambios}
