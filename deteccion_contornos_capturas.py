# Importo las librerias necesarias
import cv2
import numpy as np

# Clase que implementa la detección de contorno de la captura del objeto impreso
class DetectorDeContornos:
    def __init__(self, umbral_cambios=50, umbral_inferior=160, umbral_superior=255):
        self.umbral_cambios = umbral_cambios
        self.umbral_inferior = umbral_inferior
        self.umbral_superior = umbral_superior

        # Rangos de colores de los filamentos en formato BGR
        self.rangos_colores = {
            'blanco': (np.array([160, 160, 160]), np.array([255, 255, 255])),
            'negro': (np.array([0, 0, 0]), np.array([50, 50, 50])),
            'rojo': (np.array([0, 0, 100]), np.array([50, 50, 255])),
            'verde': (np.array([0, 100, 0]), np.array([50, 255, 50])),
            'azul': (np.array([100, 0, 0]), np.array([255, 50, 50])),
            'amarillo': (np.array([0, 100, 100]), np.array([50, 255, 255])),
            'gris': (np.array([50, 50, 50]), np.array([200, 200, 200])),
            'otro color': (np.array([50, 50, 50]), np.array([255, 255, 255]))
        }

    # Creo una mascara para filtrado de color del filamento
    @staticmethod
    def filtrar_por_color(imagen, rango_inferior, rango_superior):
        # Aplico filtro de color en la imagen "mascara"
        mascara = cv2.inRange(imagen, rango_inferior, rango_superior)
        return mascara

    # Funcion de deteccion de contornos usando imagen base, imagen objeto y color filamento
    def detectar_contornos(self, imagen_base, imagen_objeto, color):
        # Convierto a escala de grises
        gris_base = cv2.cvtColor(imagen_base, cv2.COLOR_BGR2GRAY)
        gris_objeto = cv2.cvtColor(imagen_objeto, cv2.COLOR_BGR2GRAY)

        # Calculo la diferencia absoluta entre las imagenes para detectar cambios
        diferencia = cv2.absdiff(gris_base, gris_objeto)

        # Aplico un umbral para que solo los cambios significativos se pongan en blanco
        _, cambios_significativos = cv2.threshold(diferencia, self.umbral_cambios, 255, cv2.THRESH_BINARY)

        # Obtengo el rango de color correspondiente al color del filamento
        rango_inferior, rango_superior = self.rangos_colores.get(color.lower(), (None, None))

        if rango_inferior is None or rango_superior is None:
            raise ValueError(f"Color '{color}' no reconocido. Por favor, "
                             f"elija uno de: {', '.join(self.rangos_colores.keys())}")

        # Creo una nueva mascara utilizando el rango de color indicado
        mascara_colores = self.filtrar_por_color(imagen_objeto, rango_inferior, rango_superior)

        # Aplico operaciones morfologicas para eliminar ruido de mascara
        kernel = np.ones((3, 3), np.uint8)
        mascara_colores = cv2.morphologyEx(mascara_colores, cv2.MORPH_CLOSE, kernel)

        # Obtengo la interseccion de las dos mascaras
        interseccion = cv2.bitwise_and(cambios_significativos, mascara_colores)

        # Detecto bordes usando Canny
        bordes = cv2.Canny(interseccion, 100, 200)

        # Aplico cierre morfologico para cerrar aberturas en los contornos
        kernel_cierre = np.ones((5, 5), np.uint8)
        bordes_cerrados = cv2.morphologyEx(bordes, cv2.MORPH_CLOSE, kernel_cierre)

        # Busco los contornos en la imagen con los bordes ya cerrados
        contornos, _ = cv2.findContours(bordes_cerrados, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtro los contornos según su área y selecciono los 3 más grandes para eliminar pequeños contornos
        contornos_filtrados = sorted(contornos, key=cv2.contourArea, reverse=True)[:3]

        # Inicializar imagen para dibujar contornos
        imagen_contorno_grande = np.zeros_like(interseccion)

        if contornos_filtrados:
            # Buscar el contorno con el área más grande
            contorno_mas_grande = max(contornos_filtrados, key=cv2.contourArea)
            # Dibujar el contorno más grande
            cv2.drawContours(imagen_contorno_grande, [contorno_mas_grande], -1, (255, 0), 2)  # Dibuja en blanco
            return imagen_contorno_grande  # Retorna la imagen con el contorno más grande

        return None  # Retorna None si no se encontraron contornos válidos
