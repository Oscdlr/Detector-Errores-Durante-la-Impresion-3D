# importo librerias necesarias
import tkinter as tk
from tkinter import messagebox

# Interface de inicio de impresion 3D
class InterfaceInicioImpresion:
    # creo la ventana con titulo y tamanio
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Detección de Errores - 3D Print")
        self.ventana.geometry("600x250")

        # Texto para orientar a usuario
        etiqueta = tk.Label(self.ventana, text="Pulse iniciar cuando comience la impresion 3D.", font=("Arial", 14))
        etiqueta.pack(pady=20)

        # Creo boton de inicio
        self.boton_inicio = tk.Button(self.ventana, text="Iniciar", command=self.iniciar_programa, width=15)
        self.boton_inicio.pack(side=tk.LEFT, padx=50, pady=50)

        # Creo boton de cancelacion
        self.boton_cancelacion = tk.Button(self.ventana, text="Cancelar", command=self.cancelar_programa, width=15)
        self.boton_cancelacion.pack(side=tk.RIGHT, padx=50, pady=50)

    # Inicio el programa
    def iniciar_programa(self):
        # Cierro la ventana para que continue la ejecucion del programa principal
        self.ventana.destroy()

    # Cancelo el programa
    def cancelar_programa(self):
        # Cierro la ventana sin continuar la ejecucion en el programa principal
        self.ventana.destroy()
        messagebox.showinfo("Cancelar", "El programa ha sido cancelado.")
        # Finaliza el programa
        exit()

    # inicio la interface
    def iniciar_interface(self):
        self.ventana.mainloop()

# Llamada para iniciar la interfaz
def muestra_interface():
    interface = InterfaceInicioImpresion()
    interface.iniciar_interface()
