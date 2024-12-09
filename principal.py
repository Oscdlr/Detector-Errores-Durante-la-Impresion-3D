import tkinter as tk
import os
import sys
from tkinter import messagebox
from captura_vistas_stl import CapturaVistasSTL
from interface_inicio_impresion import muestra_interface
from interface_inicio import InterfaceDeInicio
from interface_entrada_datos import InterfaceDatos
from capturaObjetoImpreso import CapturaProceso
from estractor_gcode_info import ExtractorGcodeInfo
from procesar_contornos_vistas import ProcesarVistasSTL
from interface_modificar_gcode import InterfaceGcode

class Principal:
    def __init__(self):
        pass

    # Inicializo la interfaz de inicio del programa principal
    def interface_inicio(self):
        # Solo creamos la interfaz de inicio y la mostramos
        interface = InterfaceDeInicio(detectar_errores=self.interface_datos, modificar_gcode=self.interface_gcode)
        interface.mostrar_interfaz()

    @staticmethod
    # Funcion que ejecuto cuando el usuario pulsa continuar. Llamo a la interfaz de entrada de datos
    def interface_datos():

        interfaz = InterfaceDatos()
        ruta_stl, ruta_gcode, capas_por_captura, angulo_camara, altura_camara, correo_destino, color = interfaz.mostrar_interface_datosentrada()

        # Obtengo la altura total del objeto y la altura de capa del archivo GCODE
        altura_total, altura_capa = ExtractorGcodeInfo.extraer_datos(ruta_gcode)

        # Capturo vistas del objeto STL
        gestion_vistas = CapturaVistasSTL(
            fichero_entrada=ruta_stl,
            altura_capa=altura_capa,
            capas_entre_captura=capas_por_captura,
            altura_total=altura_total,
            angulo_camara=angulo_camara,
            altura_camara=altura_camara
        )

        lista_vistas_capturadas = gestion_vistas.iniciar()

        # Proceso los contornos de las vistas STL creando lista vacía donde insertar los contornos
        lista_contornos_stl = []

        for indice, vista in enumerate(lista_vistas_capturadas):
            if vista:
                # Proceso cada una de las vistas obteniendo los contornos y los guardo en lista contornos
                procesador_imagen = ProcesarVistasSTL(vista, 'contornos_vistas', indice)
                contorno_imagen = procesador_imagen.procesar()

                if contorno_imagen is not None:
                    lista_contornos_stl.append(contorno_imagen)
            else:
                print(f"Vista {indice + 1} no encontrada.")

        if len(lista_contornos_stl) == 0:
            print("No se han detectado contornos en las vistas.")

        # Abro la interfaz principal
        muestra_interface()

        # Inicio la captura de video y detección de contornos
        proceso_captura = CapturaProceso(lista_contornos_stl, correo_destino, color=color)
        proceso_captura.captura_video()

    @staticmethod
    def interface_gcode():
        # Inicia la interfaz que modificará el fichero Gcode
        interface_gcode = InterfaceGcode()
        interface_gcode.mostrar_interface_gcode()

# Inicio del programa
def main():
    app = Principal()
    app.interface_inicio()  # Inicio del programa abriendo la interfaz de inicio


if __name__ == "__main__":
    main()
