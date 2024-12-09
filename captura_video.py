# Importar libreria cv2
import cv2
import tkinter as tk
from tkinter import messagebox
import sys

#Clase que maneja la captura de video
class ManejadorCapturaVideo:
    def __init__(self, indice_camara=0, fichero_salida='salida.avi'):
        self.captura = cv2.VideoCapture(indice_camara)
        if not self.captura.isOpened():
            self.mostrar_error("Error: No se puede acceder a la cámara. Verifique la conexion.")
        self.anchura_imagen = int(self.captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.altura_imagen = int(self.captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # self.video = cv2.VideoWriter(fichero_salida, cv2.VideoWriter_fourcc(*'XVID'), 25,
        #                              (self.anchura_imagen, self.altura_imagen))
        # para guardar el video descomentar


    # Método para mostrar un mensaje de error y finalizar el programa
    @ staticmethod
    def mostrar_error(mensaje):
        # Crear una ventana para mostrar el messagebox
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        messagebox.showerror("Error", mensaje)
        sys.exit()

    # Obtengo la imagen
    def obtener_imagen(self):

        ret, imagen = self.captura.read()
        if not ret:
            print("Error: No se puede capturar la imagen.")

            return None
        return imagen

    # Guardo la imagen
    @staticmethod
    def guarda_imagen(imagen):
        #
        if imagen is not None:
            # self.video.write(imagen)
            # para guardar video descomentar
            pass
        else:
            print("Error: La imagen no existe, no se puede guardar")

    # Libero la camara
    def eliminar(self):
        # Eliminamos la captura de video
        self.captura.release()
        # Liberamos el video si existe
        if hasattr(self, 'video'):
            self.video.release()
