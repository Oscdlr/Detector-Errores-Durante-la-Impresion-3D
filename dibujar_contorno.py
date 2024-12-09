# Importo librerias necesarias open CV y numpy
import cv2
import numpy as np

# Clase encargada de dibujar el contorno en blanco a partir de imagen binaria
class DibujaContorno:
    def __init__(self, imagen_binaria):
        self.imagen_binaria = imagen_binaria

    # Creo imagen en negro con contorno blanco y devuelvo esa imagen
    def dibuja_contorno(self, contorno):
        contorno_imagen = np.zeros_like(self.imagen_binaria)
        cv2.drawContours(contorno_imagen, [contorno], -1,
                         (255,255,255), thickness=2)
        return contorno_imagen
