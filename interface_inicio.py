# Importo librerias necesarias
import tkinter as tk

class InterfaceDeInicio:
    # Creo ventana con titulo
    def __init__(self, detectar_errores=None, modificar_gcode=None):
        self.detectar_errores = detectar_errores
        self.modificar_gcode = modificar_gcode
        self.ventana = tk.Tk()
        self.ventana.title("Inicio")
        self.ventana.geometry("500x250")  # Configuro tamanio de la ventana

        # Creo los botones de la interfaz "modificar Gcode" y "Detector Errores"
        self.modificar_boton_gcode = tk.Button(self.ventana, text="Modificar Gcode", command=self.abrir_modificar_gcode)
        self.modificar_boton_gcode.pack(side=tk.LEFT, expand=True, padx=20, pady=20)

        self.boton_detector_errores = tk.Button(self.ventana, text="Detector Errores", command=self.abrir_detector_errores)
        self.boton_detector_errores.pack(side=tk.RIGHT, expand=True, padx=20, pady=20)

    # Abro la interface modificar Gcode
    def abrir_modificar_gcode(self):
        # Oculto la ventana principal
        self.ventana.withdraw()
        if self.modificar_gcode:
            # Abro la interfaz para modifiar el Gcode
            self.modificar_gcode()
        # Vuelvo a mostrar la ventana principal despues de cerrar la interfaz modificar Gcode
        self.ventana.deiconify()

    # Abro la interface de deteccion de errores
    def abrir_detector_errores(self):
        # Cierro la ventana principal y abro la interfaz detector de errores
        self.ventana.destroy()
        if self.detectar_errores:
            self.detectar_errores()

    # Abro la interface de inicio
    def mostrar_interfaz(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    def detecta_errores():
        print("Detectando errores...")

    def modifica_gcode():
        print("Modificando Gcode...")

    interface = InterfaceDeInicio(detectar_errores=detecta_errores(), modificar_gcode=modifica_gcode())
    interface.mostrar_interfaz()
