# Importacion librerias
import cv2

class ProcesarContorno:
    # cargo la imagen
    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.imagen = cv2.imread(ruta_imagen)
        if self.imagen is None:
            raise ValueError(f"Error al cargar la imagen en ruta: {ruta_imagen}")

    # convierto a binario la imagen
    def convierte_a_binario(self):
        # convierto a escala de grises
        imagen_grises = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
        # convierto a binario THRESH_BINARY y retorno la imagen binaria
        _, imagen_binaria = cv2.threshold(imagen_grises, 50, 255, cv2.THRESH_BINARY)
        return imagen_binaria

    # Encuentro el contorno exterior de la imagen RETR_EXTERNAL
    @staticmethod
    def detecta_contorno_esterior(imagen_binaria):
        contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Si hubiera varios contornos me quedo con el de mayor area (mas exterior)
        if len(contornos) == 0:
            print("No se detectaron contornos.")
            return None
        contorno_exterior = max(contornos, key=cv2.contourArea)
        return contorno_exterior
