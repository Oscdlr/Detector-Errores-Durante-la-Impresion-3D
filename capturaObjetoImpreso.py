# Importacion de librerias y modulos necesarios
import cv2
import time
import os
import sys
import tkinter as tk
from tkinter import messagebox
from captura_video import ManejadorCapturaVideo
from detector_movimiento import DetectorMovimiento
from captura_imagen import CapturaImagen
from deteccion_contornos_capturas import DetectorDeContornos
from comparador_contornos import ComparadorContornos
# from gestor_errores import GestorErrores

# Modulo encargado del proceso de captura objeto impreso, procesamiento y comparacion con STL
class CapturaProceso:
    def __init__(self, lista_contornos_stl, correo_destino=None, intervalo_captura=10, color='blanco'):
        self.manejador_video = ManejadorCapturaVideo(indice_camara=0, fichero_salida='captured_video.avi')
        self.captura_imagen = CapturaImagen(carpeta_salida='capturas_objeto/capturas_camara')
        self.detector_movimiento = DetectorMovimiento(self.captura_imagen)
        self.detector_contornos = DetectorDeContornos()
        self.intervalo_captura = intervalo_captura
        self.comparador_contornos = ComparadorContornos()
        self.lista_contornos_stl = lista_contornos_stl
        self.lista_capturas = []
        self.indice_captura = 0
        self.correo_destino = correo_destino
        self.color = color
        # self.gestor_errores = GestorErrores(correo_origen = 'usuario@gmail.com', contrasena = 'xxxx xxxx xxxx xxxx')

    # Funcion que se encarga de grabar la impresion 3D y gestiona cuando es el momento de
    # capturar y de terminar de grabar.
    def captura_video(self):
        capturado_durante_pausa = False
        ultimo_tiempo_captura = None

        while True:
            imagen = self.manejador_video.obtener_imagen()
            self.manejador_video.guarda_imagen(imagen)

            if self.detector_movimiento.detecta_movimiento(imagen):
                # Si se detecta movimiento, se restablece la bandera para no capturar
                capturado_durante_pausa = False
            else:
                tiempo_actual = time.time()
                # Aquí verificamos si ha transcurrido el tiempo necesario para permitir una captura después de la pausa
                if not capturado_durante_pausa:
                    # Comprobamos que haya pasado el tiempo necesario sin movimiento
                    if ultimo_tiempo_captura is None or (tiempo_actual - ultimo_tiempo_captura) > self.intervalo_captura:
                        ultimo_tiempo_captura = tiempo_actual
                        capturado_durante_pausa = True
                        print("Captura programada tras pausa de movimiento.")

                if self.detector_movimiento.no_hay_movimiento(10):
                    print("Impresión finalizada. Terminando programa.")
                    break

            # Mostramos la imagen en tiempo real
            cv2.imshow('Monitoreo iniciado. Pulsa ESC para finalizar" ', imagen)
            self.procesa_capturas()
            # Si se pulsa EXC salir del programa
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.finalizar_proceso()

    # Este método muestra un messagebox de error y finaliza el programa.
    @staticmethod
    def mostrar_error(texto):
        # Crear una ventana de Tkinter para mostrar el messagebox
        root = tk.Tk()
        root.withdraw()  # Ocultamos la ventana principal de Tkinter
        messagebox.showerror("Error", texto)

        # Finalizamos el programa
        sys.exit()

    # Realiza la captura, detecta contorno y compara contornos entre vista STL y objeto impreso
    def procesa_capturas(self):
        ruta_captura = self.detector_movimiento.ruta_captura
        if not ruta_captura:
            # Si no detecta una ruta para la captura sale de la funcion
            return

        if ruta_captura in self.lista_capturas:
            # Si la captura esta en la lista de capturas salir de la funcion (evita duplicados)
            return

        # Agrego la nueva captura a la lista de capturas
        self.lista_capturas.append(ruta_captura)
        print(f"Captura añadida: {ruta_captura}")

        # Verifico que haya más de una captura en la lista de capturas
        if len(self.lista_capturas) <= 1:
            print("No hay suficientes capturas para comparar.")
            return

        # Compruebo que el incice de la captura no es mayor que el numero de contornos.
        if self.indice_captura >= len(self.lista_contornos_stl):
            print("Error: El índice de captura supera el tamaño de la lista de contornos STL.")
            self.mostrar_error("Error: El índice de captura supera el tamaño de la lista de contornos STL.")
            sys.exit()

        # Compruebo que el indice de la captura no es mayor que el numero de capturas.
        if self.indice_captura >= len(self.lista_capturas):
            print("Error: El índice de captura supera el tamaño de la lista de capturas.")
            self.mostrar_error("Error: El índice de captura supera el tamaño de la lista de capturas.")
            return

        # Cargo las imagenes inicial y final para detectar el contorno
        imagen_inicial = cv2.imread(self.lista_capturas[0])
        imagen_final = cv2.imread(self.lista_capturas[-1])

        # Detecto el contorno exterior de la imagen
        contorno = self.detector_contornos.detectar_contornos(imagen_inicial,
                                                              imagen_final, self.color)
        if contorno is None:
            print("Error: Contorno captura no existe.")
            self.mostrar_error("Error: Contorno captura no existe.")
            # Si no se detecta contorno, enviar correo error y salir de la funcion
            # if self.correo_destino:
                # self.gestor_errores.enviar_correo(correo_destino=self.correo_destino, coincidencia=0)
            return

        # Guardo el contorno detectado y lo comparo con el contorno de la vista STL
        directorio_salida = 'Contornos_capturas'
        os.makedirs(directorio_salida, exist_ok=True) # exist_ok evita error si directorio existe
        ruta_salida = os.path.join(directorio_salida, f'contorno_captura_{self.indice_captura + 1}.png')
        cv2.imwrite(ruta_salida, contorno)
        # print(f"Contorno guardado en: {ruta_salida}")

        if self.lista_contornos_stl[self.indice_captura] is None or contorno is None:
            print("Error: Uno de los contornos a comparar no existe.")
            self.mostrar.error("Detección de errores finalizada")
            self.finalizar_proceso()
            return

        # Comparo el contorno detectado con el contorno STL almacenado en la lista
        self.comparador_contornos.comparar(self.lista_contornos_stl[self.indice_captura], contorno, correo_destino=self.correo_destino)
        self.indice_captura += 1

    # Termina el proceso y destruye ventanas
    def finalizar_proceso(self):
        self.manejador_video.eliminar()
        cv2.destroyAllWindows()
