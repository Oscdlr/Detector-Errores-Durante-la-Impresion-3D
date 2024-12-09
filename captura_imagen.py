# Importo las librerias necesarias
import cv2
import os

# Se encarga de capturar las imagenes y guardarlas en una lista y en carpeta externa
class CapturaImagen:
    def __init__(self, carpeta_salida='capturas_objeto/capturas_camara'):
        # Crear la carpeta principal si no existe
        if not os.path.exists(carpeta_salida):
            # Crea la carpeta y subcarpeta "makedirs"
            os.makedirs(carpeta_salida)

        self.carpeta_salida = carpeta_salida
        # Contador para nombrar capturas ordenadas
        self.contador = 0

    def captura_imagen(self, imagen):
        try:
            # Creo el nombre de la captura. Ej: "captura_1.png"
            nombre_fichero = os.path.join(self.carpeta_salida, f"captura_{self.contador}.png")
            self.contador += 1

            # Guardo la imagen en la carpeta
            guardado = cv2.imwrite(nombre_fichero, imagen)

            # Si se ha guardado correctamente, retorno el nombre del fichero
            if guardado:
                print(f"Imagen capturada y guardada en: {nombre_fichero}")
                return nombre_fichero  # Devolver el nombre del archivo guardado
            else:
                print("Se ha producido un error al guardar la imagen.")
                return None
        except Exception as e:
            print(f"Se produjo un error al capturar la imagen: {e}")
            return None