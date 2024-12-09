# Importo las librerias y modulos necesarios
import tkinter as tk
from tkinter import filedialog, messagebox
from modificar_gcode import ModificadorGcode
import os

# Interface que recibe un fichero Gcode, altura de Capa y capas entre pausa y modifica el Gcode
# Incluyendo paradas programadas en la impresion
class InterfaceGcode:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Modificar GCODE")
        self.ventana.geometry("600x300")

        # Variables para almacenar los valores introducidos por el usuario
        self.gcode = None
        self.altura_capa = None
        self.capas_entre_pausa = None

        # Configuro los elementos de la interfaz
        self.configurar_elementos()

    # Creo las etiquetas y entradas de la interface de usuario
    def configurar_elementos(self):
        # Etiqueta Ruta al archivo Gcode
        tk.Label(self.ventana, text="Ruta al archivo GCODE:").grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")
        self.gcode = tk.Entry(self.ventana, width=40)
        self.gcode.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Boton seleccionar Gcode
        sel_gcode_button = tk.Button(self.ventana, text="Seleccionar GCODE", command=self.seleccionar_gcode)
        sel_gcode_button.grid(row=0, column=2, padx=10, pady=10)

        # Etiqueta altura de capa
        tk.Label(self.ventana, text="Altura de la capa (mm):").grid(row=1, column=0, padx=(10, 5), pady=10, sticky="e")
        self.altura_capa = tk.Entry(self.ventana, width=10)
        self.altura_capa.grid(row=1, column=1, padx=(5, 10), pady=10)

        # Etiqueta Capas entre pausa
        tk.Label(self.ventana, text="Capas entre pausas:").grid(row=2, column=0, padx=(10, 5), pady=10, sticky="e")
        self.capas_entre_pausa = tk.Entry(self.ventana, width=10)
        self.capas_entre_pausa.grid(row=2, column=1, padx=(5, 10), pady=10)

        # Botones centrados en una fila
        marco_boton = tk.Frame(self.ventana)
        marco_boton.grid(row=3, column=0, columnspan=3, pady=20)

        # Boton para modificar de la interface
        boton_modificar = tk.Button(marco_boton, text="Modificar", command=self.modificar)
        boton_modificar.pack(side=tk.LEFT, padx=20)

        # Boton para cancelar de la interface
        boton_cancelar = tk.Button(marco_boton, text="Cancelar", command=self.cancelar)
        boton_cancelar.pack(side=tk.LEFT, padx=20)

    # Funcion donde se abre explorador para selecciona fichero Gcode
    def seleccionar_gcode(self):

        try:
            print("Abriendo el explorador de archivos...")
            ruta_gcode = filedialog.askopenfilename(filetypes=[("GCODE Files", "*.gcode")])

            # Verifico que la ruta no sea vacia
            if ruta_gcode:
                # Convierto a ruta absoluta
                ruta_relativa = os.path.relpath(ruta_gcode)
                print(f"Archivo seleccionado: {ruta_relativa}")
                self.gcode.delete(0, tk.END)  # Elimino texto anterior escrito
                self.gcode.insert(0, ruta_relativa)  # Muestro la ruta en la entrada
            else:
                print("No se seleccionó ningún archivo.")

        except Exception as e:
            print(f"Error al seleccionar el archivo: {e}")
            messagebox.showerror("Error", f"Hubo un error al intentar seleccionar el archivo: {e}")

    # Funcion que valida y modifica el archivo Gcode con los parametros introducidos por usuario
    def modificar(self):
        ruta_gcode = self.gcode.get()

        # Compruebo que la ruta no este vacia y que exista
        if not ruta_gcode or not os.path.exists(ruta_gcode):
            messagebox.showerror("Error", f"No se ha encontrado el fichero G-code")
            return

        altura_capa = None

        try:
            altura_capa = float(self.altura_capa.get())
            if altura_capa <=0:
                messagebox.showerror("Error", "La altura de capa debe ser positiva")
                return
        except ValueError:
            messagebox.showerror("Error", "La altura de capa no es válida")

        try:
            capas_entre_pausa = int(self.capas_entre_pausa.get())
            if capas_entre_pausa <= 0:
                messagebox.showerror("Error", "Las capas entre pausa debe ser valor positivo")
                return
        except ValueError:
            messagebox.showerror("Error", "El valor de capas entre pausa no es válido")
            return

        try:
            # Creo instancia de ModificadorGcode y modifico el Gcode
            modificador_gcode = ModificadorGcode(ruta_gcode, altura_capa, capas_entre_pausa)
            modificador_gcode.modificar()

            # Cierro la ventana y el programa
            self.ventana.quit()

        except ValueError as e:
            messagebox.showerror("Error", f"La entrada de datos no es valida: {e}")

    # Funcion que cancela la interface y cierra la ventana
    def cancelar(self):
        self.ventana.quit()

    # Funcion para iniciar la interface Gcode
    def mostrar_interface_gcode(self):
        self.ventana.mainloop()
        # Se elimina la ventana principal al cerrar el programa
        self.ventana.destroy()


# Punto de entrada del programa
if __name__ == "__main__":
    interface = InterfaceGcode()
    interface.mostrar_interface_gcode()
