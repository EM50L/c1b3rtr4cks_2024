1) Coloca estos archivos en el ESP
2) configura Settings.toml
3) carga librerias (en carpeta lib)
- adafruit_connection_manager.mpy
- adafruit_hid
- adafruit_requests.mpy

Al reiniciar la placa deberias tener el bot listo

Nota: para ocultar/steal la placa se ha desabilitado el disco

Para arrancar el disco puedes usar

import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
microcontroller.reset()

