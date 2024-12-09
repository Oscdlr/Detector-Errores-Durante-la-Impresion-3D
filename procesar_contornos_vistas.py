# Importo las librerias y modulos necesarios
import os
import cv2
from contorno_mas_grande import ProcesarContorno
from dibujar_contorno import DibujaContorno

# Se encarga de procesar las vistas STL buscando el contorno mas grande, lo dibuja y guarda
class ProcesarVistasSTL:
    def __init__(self, ruta_imagen, carpeta_salida, indice_vista):
        self.ruta_imagen = ruta_imagen
        self.carpeta_salida = carpeta_salida
        self.indice_vista = indice_vista

    def procesar(self):

        # Verifico si la carpeta de salida existe, si no, la crea
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)

        # Convierto la imagen a binario y detecto el contorno exterior
        imagen_binaria = ProcesarContorno(self.ruta_imagen).convierte_a_binario()

        contorno = ProcesarContorno(self.ruta_imagen).detecta_contorno_esterior(imagen_binaria)

        # Si hay un contorno, lo dibujo y lo guardo
        if contorno is not None:
            contorno_vista = DibujaContorno(imagen_binaria).dibuja_contorno(contorno)
            # Guardo el contorno en la carpeta
            ruta_salida = os.path.join(self.carpeta_salida, f'contorno_vista_{self.indice_vista}.png')
            cv2.imwrite(ruta_salida, contorno_vista)
            # Devuelvo el contorno para tratarlo
            return contorno_vista
        else:
            print(f"No se detectaron contornos en la vista {self.indice_vista}.")

        return None
