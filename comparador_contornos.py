# Importo los modulos y las librerias necesarios
import cv2
import numpy as np
import os
from gestor_errores import GestorErrores

# Compara los contornos de dos imagenes y llama a gestor de errores cuando detecta error de coincidencia
class ComparadorContornos:
    def __init__(self, umbral_coincidencia=90, directorio_salida="Contornos_comparados",
                 correo_destino="usuario@gmail.com"):
        self.contador_comparaciones = 1
        self.umbral_coincidencia = umbral_coincidencia
        self.directorio_salida = directorio_salida
        self.correo_destino = correo_destino
        # Creo el gestor con correo electronico y contraseña de aplicacion
        self.gestor_correo = GestorErrores("usuario@gmail.com", "xxxx xxxx xxxx xxxx")

        if not os.path.exists(self.directorio_salida):
            os.makedirs(self.directorio_salida)

    # Funcion que compara los dos contornos recibidos como parametro
    def comparar(self, imagen_contorno1, imagen_contorno2, correo_destino=None):
        if imagen_contorno1 is None or imagen_contorno2 is None:
            print("Una o ambas imágenes de contorno son None.")
            return

        # Si se pasa un correo_destino, actualiza el valor de self.correo_destino
        if correo_destino:
            self.correo_destino = correo_destino

        # Convierto a escala de grises las dos imagenes para tratarlas
        gris1 = cv2.cvtColor(imagen_contorno1, cv2.COLOR_BGR2GRAY) if len(
            imagen_contorno1.shape) > 2 else imagen_contorno1
        gris2 = cv2.cvtColor(imagen_contorno2, cv2.COLOR_BGR2GRAY) if len(
            imagen_contorno2.shape) > 2 else imagen_contorno2

        # Guardo en una variable los contornos mas grandes de las imagenes
        contorno1 = max(cv2.findContours(gris1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea,
                        default=None)
        contorno2 = max(cv2.findContours(gris2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea,
                        default=None)

        # Error si no encuentra los contornos
        if len(contorno1) == 0 or len(contorno2) == 0:
            print("No se han encontrado contornos en las imágenes.")
            return

        # Escalo los contornos para que coincidan los tamaños
        contorno1, contorno2 = self.escalar_contornos(contorno1, contorno2)
        # Calculo la coincidencia entre los dos contornos comparados
        coincidencia = self.calcular_coincidencia(contorno1, contorno2)

        # Si la coincidencia supera un umbral, se envía notificación e imagen a correo
        if coincidencia < self.umbral_coincidencia and self.correo_destino:
            self.guardar_comparacion(contorno1, contorno2, coincidencia)
            # Llamo al gestor de errores para enviar el correo a correo destino
            self.gestor_correo.enviar_correo(self.correo_destino, coincidencia)
        else:
            self.guardar_comparacion(contorno1, contorno2, coincidencia)
        print(f"Coincidencia: {coincidencia:.2f}%")

    # Funcion que escala los contornos calculando el area de cada contorno
    def escalar_contornos(self, contorno1, contorno2):
        # Calculo las dos areas
        area1, area2 = cv2.contourArea(contorno1), cv2.contourArea(contorno2)
        # Llamo a escalar contorno para que los dos contornos tengan igual area
        if area1 > area2:
            contorno2 = self.escalar_contorno(contorno2, np.sqrt(area1 / area2))
        elif area2 > area1:
            contorno1 = self.escalar_contorno(contorno1, np.sqrt(area2 / area1))
        return contorno1, contorno2

    # Funcion que escala los contornos por medio de un factor de escala recibido como parametro
    @staticmethod
    def escalar_contorno(contorno, factor_escala):
        # El contorno recibido es el de menor area. Lo multiplico por factor de escala para igualar areas
        contorno_escalado = contorno * factor_escala
        # Aseguro que el contorno escapado es tipo entero
        return contorno_escalado.astype(np.int32)

    # Funcion que calcula el porcentaje de pixeles coincidentes sobre el total
    def calcular_coincidencia(self, contorno1, contorno2):
        # Llamada a funcion que calcula cual es la imagen mas grande
        alto, ancho = self.dimension_maxima(contorno1, contorno2)
        # Llamada a funcion centrar_contorno para centrar los contornos en centro de ventana
        img1_centrada = self.centrar_contorno(contorno1, ancho, alto)
        img2_centrada = self.centrar_contorno(contorno2, ancho, alto)
        # Calculo los pixeles comunes a las dos imagenes (interseccion)
        interseccion = cv2.bitwise_and(img1_centrada, img2_centrada)
        # Calculo los pixeles union de ambas imagenes (union)
        union = cv2.bitwise_or(img1_centrada, img2_centrada)
        # Calculo los pixeles que coinciden en ambas imagenes. 255 es el valor de pixel para el blanco
        interseccion_pixeles = np.sum(interseccion / 255)
        # Calculo los pixeles que son blancos en al menos una de las dos imagenes (union)
        union_pixeles = np.sum(union / 255)

        # Si se han encontrado pixeles en la union calculo el porcentaje de coincidencia
        if union_pixeles:
            porcentaje_coincidencia = (interseccion_pixeles / union_pixeles) * 100
        else:
            porcentaje_coincidencia = 0  # Si no hay píxeles en común, la coincidencia es 0

        return porcentaje_coincidencia

    # Funcion que calcula la anchura y altura del contorno mas grande.
    # contorno[:, 0, 1] obtiene las coordenadas y de todos los puntos del contorno
    # contorno[:, 0, 0] obtiene las coordenadas x de todos los puntos del contorno
    @staticmethod
    def dimension_maxima(contorno1, contorno2):
        # Calculo el valor "y" maximo  del alto de cada contorno y guardo el maximo valor
        alto = max(contorno1[:, 0, 1].max(), contorno2[:, 0, 1].max()) + 10 # sumo 10 de margen
        # Calculo el valor "x" maximo  del ancho de cada contorno y guardo el maximo valor
        ancho = max(contorno1[:, 0, 0].max(), contorno2[:, 0, 0].max()) + 10 # sumo 10 de margen
        # retorno las dimensiones maximas
        return alto, ancho

    # Funcion que centra los contornos en el punto central de la imagen
    @staticmethod
    def centrar_contorno(contorno, ancho, alto):
        contorno_centrado = np.zeros((alto, ancho), dtype=np.uint8)
        # Utilizo momentos de HU para calcular el centroide del contorno (centro de masas)
        # "m00" = area
        # "m10" y "m01" = centro de masa
        momento = cv2.moments(contorno)
        if momento["m00"] != 0:
            # cx y cy indican el centroide del contorno
            cx, cy = int(momento["m10"] / momento["m00"]), int(momento["m01"] / momento["m00"])
            # (ancho // 2), alto // 2) son centro de la imagen de salida
            # Calculo desplazamiento en el eje x
            dx = (ancho // 2) - cx
            # Calculo desplazamiento en el eje y
            dy = (alto // 2) - cy
            # desplazo el contorno hacia el centro de la imagen
            contorno_desplazado = contorno + [dx, dy]
            cv2.drawContours(contorno_centrado, [contorno_desplazado], -1, (255,0),
                             thickness=cv2.FILLED)
        # Devuelvo el contorno centrado
        return contorno_centrado

    # Funcion para guardar la imagen comparada
    def guardar_comparacion(self, contorno1, contorno2, coincidencia):
        # Calculo las dimensiones del contorno mas grande
        alto, ancho = self.dimension_maxima(contorno1, contorno2)
        # Centro los contornos
        cont1_centrado = self.centrar_contorno(contorno1, ancho, alto)
        cont2_centrado = self.centrar_contorno(contorno2, ancho, alto)

        # Generar imagen resaltada de comparación (3 canales de color: rojo, verde, azul)
        imagen_comparacion = np.zeros((alto, ancho, 3), dtype=np.uint8)
        imagen_comparacion[..., 1] = cont1_centrado  # Contorno1 en verde
        imagen_comparacion[..., 0] = cont2_centrado  # Contorno2 en verde oscuro
        # Si hay diferencias entre pixeles se asigna color rojo (0,0,255)
        diferencias = cv2.bitwise_xor(cont1_centrado, cont2_centrado)
        imagen_comparacion[diferencias == 255] = (0, 0, 255)  # Resaltar diferencias en rojo
        # cv2.imshow("imagen", imagen_comparacion)
        # Guardar la imagen y devolver el nombre de archivo
        nombre_archivo = f'{self.directorio_salida}/comparacion_{self.contador_comparaciones:03d}_{coincidencia:.2f}.png'
        cv2.imwrite(nombre_archivo, imagen_comparacion)
        # Convierto la imagen en formato correcto "a bytes" para poderla enviar al correo
        _, imagen_bytes = cv2.imencode('.png', imagen_comparacion)
        imagen_error = imagen_bytes.tobytes()
        self.contador_comparaciones += 1
        # Devuelvo el nombre del archivo y la imagen del error
        return imagen_error
