import cv2
import time
import numpy as np
import tkinter as tk
from tkinter import messagebox
import sys

# Es encargado de detectar la ausencia de movimiento, hacer la captura y finalizar
class DetectorMovimiento:
    def __init__(self, captura, tiempo_sin_movimiento_capt=2.5, tiempo_sin_movimiento_fin=10, tiempo_entre_capturas=0.1):
        self.captura = captura
        self.imagen_base = None
        self.ruta_captura = None
        self.tiempo_sin_movimiento_capt = tiempo_sin_movimiento_capt  # Tiempo sin movimiento antes de capturar
        self.tiempo_sin_movimiento_fin = tiempo_sin_movimiento_fin  # Tiempo sin movimiento para finalizar
        self.tiempo_entre_capturas = tiempo_entre_capturas  # Tiempo entre capturas de video
        self.ultima_deteccion_tiempo = time.time()  # Tiempo de la ultima deteccion de movimiento
        self.ultima_captura_tiempo = time.time()  # Tiempo de la ultima vez que se proceso una imagen
        self.capturada = False  # Bandera para evitar multiples capturas durante la misma parada

    @staticmethod
    def mostrar_error(mensaje):
        root = tk.Tk()
        root.withdraw()  # Ocultamos la ventana principal
        messagebox.showerror("Error", mensaje)
        sys.exit()  # Termina el programa después de mostrar el error

    # Actualiza la imagen de video capturada
    def actualiza_imagen_base(self, imagen):
        self.imagen_base = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        self.imagen_base = cv2.GaussianBlur(self.imagen_base, (21, 21), 0)

    # Comprueba si no ha habido movimento durante tiempo pasado por parametro
    def no_hay_movimiento(self, tiempo):
        return (time.time() - self.ultima_deteccion_tiempo) > tiempo

    # Detecta si hubo cambios entre la imagen base y la ultima imagen (detecta movimiento)
    def detecta_movimiento(self, imagen):

        if imagen is None:
            print("Error: No se puede procesar la imagen. Revise la conexión de la cámara")
            self.mostrar_error("Error al detectar movimiento. Revise la conexión de la cámara.")
            return False

        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        imagen_gris = cv2.GaussianBlur(imagen_gris, (21, 21), 0)
        tiempo_actual = time.time()

        # Si es necesario actualizar la imagen base la actualiza
        if self.imagen_base is None or (tiempo_actual - self.ultima_captura_tiempo) > self.tiempo_entre_capturas:
            # Actualizo el tiempo de la ultima captura
            self.ultima_captura_tiempo = tiempo_actual

            # Calcula la diferencia entre los pixeles las dos capturas.
            if self.imagen_base is not None:
                diferencia = cv2.absdiff(self.imagen_base, imagen_gris)
                # Aplico umbral binario que muestra en blanco (255) los pixeles que cambian
                _, thresh = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)
                # sumo todos los pixeles, al dividir entre 255 sale numero de pixeles
                pixeles_distintos = np.sum(thresh) / 255

                # Mostrar la imagen binaria al usuario actualizada en tiempo real
                cv2.imshow("Deteccion Movimiento", thresh)

                # Si hay movimiento, reinicio la bandera y actualizo la imagen base
                if pixeles_distintos > 0:
                    self.capturada = False  # Permite que se haga una nueva captura en siguiente pausa
                    self.ultima_deteccion_tiempo = tiempo_actual  # Actualizo el tiempo de detección de movimiento
                    self.actualiza_imagen_base(imagen) # Actualizo la imagen base
                    return True

                # Si no hay movimiento, evaluo si se debe hacer una captura
                elif pixeles_distintos == 0:
                    # Verifico si ha pasado el tiempo necesario sin movimiento y si se debe capturar
                    if (( tiempo_actual - self.ultima_deteccion_tiempo) >= self.tiempo_sin_movimiento_capt
                            and not self.capturada):
                        self.capturada = True
                        self.actualiza_imagen_base(imagen)
                        # Capturo la imagen y la guardo en ruta a carpeta externa.
                        self.ruta_captura = self.captura.captura_imagen(imagen)
                        # Actualizo el tiempo de la ultima deteccion
                        self.ultima_deteccion_tiempo = tiempo_actual
                        # No se ha detectado movimiento y se ha realizado la captura
                        return False

            else:
                # No se ha detectado movimiento y se ha actualizado la imagen
                self.actualiza_imagen_base(imagen)

        # Si el tiempo de no movimiento excede el umbral, finalizar
        if self.no_hay_movimiento(self.tiempo_sin_movimiento_fin):
            return False

        return False
