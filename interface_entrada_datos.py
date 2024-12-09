# Importacion de librerias necesarias para la creacion de la interface
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Interface para la introduccion y guardado de datos de entrada
class InterfaceDatos:
    def __init__(self):
        self.datos = {}  # Diccionario para almacenar los datos del usuario

        # Creo la ventana principal "Configuracion entrada de Datos"
        self.ventana = tk.Tk()
        self.ventana.title("Configuracion entrada de Datos")

        # Configuro el tamanio de la ventana
        self.ventana.geometry("600x450")

        # Creo el marco donde aparece el formulario
        self.marco = tk.Frame(self.ventana)
        self.marco.pack(expand=True)

        # Obtengo la carpeta donde se ejecuta el programa
        if getattr(sys, 'frozen', False):
            # Si el programa se ejecuta desde el .exe uso carpeta del ejecutable
            carpeta_actual = os.path.dirname(sys.executable)
        else:
            # Uso la carpeta donde se encuentra el proyecto
            carpeta_actual = os.path.dirname(os.path.abspath(__file__))

        self.carpeta_actual = carpeta_actual

        # Inicializo los valores de los atributos de entrada de la interfaz de entrada de datos
        self.fichero_stl = None
        self.fichero_gcode = None
        self.capas_entrada = None
        self.angulo_camara = None
        self.altura_camara = None
        self.correo_destino = None
        self.marco_botones = None
        self.color_filamento = None

        # Creo elementos de la ventana de entrada de datos: etiquetas, entradas y botones
        self.crear_etiquetas()

    def crear_etiquetas(self):
        # Función para que el usuario seleccione el fichero STL
        def seleccionar_stl():
            ruta_stl = filedialog.askopenfilename(filetypes=[("STL Files", "*.stl")])
            if ruta_stl:
                ruta_stl_relativa = os.path.relpath(ruta_stl, self.carpeta_actual)
                self.fichero_stl.delete(0, tk.END)
                self.fichero_stl.insert(0, ruta_stl_relativa)

        # Funcion para que el usuario seleccione el fichero GCODE
        def seleccionar_gcode():
            ruta_gcode = filedialog.askopenfilename(filetypes=[("GCODE Files", "*.gcode")])
            if ruta_gcode:
                ruta_gcode_relativa = os.path.relpath(ruta_gcode, self.carpeta_actual)
                self.fichero_gcode.delete(0, tk.END)
                self.fichero_gcode.insert(0, ruta_gcode_relativa)

        # Creo etiquetas y entradas de la ventana para introducir datos de usuario
        # Ruta al archivo STL
        tk.Label(self.marco, text="Ruta al archivo STL:").grid(row=0, column=0, padx=10, pady=10)
        self.fichero_stl = tk.Entry(self.marco, width=40)
        self.fichero_stl.grid(row=0, column=1, padx=10, pady=10)
        self.fichero_stl.insert(0, "archivo.stl") # Valor por defecto
        seleccionar_boton_stl = tk.Button(self.marco, text="Seleccionar STL", command=seleccionar_stl)
        seleccionar_boton_stl.grid(row=0, column=2, padx=10, pady=10)

        # Ruta al archivo Gcode
        tk.Label(self.marco, text="Ruta al archivo GCODE:").grid(row=1, column=0, padx=10, pady=10)
        self.fichero_gcode = tk.Entry(self.marco, width=40)
        self.fichero_gcode.grid(row=1, column=1, padx=10, pady=10)
        self.fichero_gcode.insert(0, "modificado_archivo.gcode") # Valor por defecto
        seleccionar_boton_gcode = tk.Button(self.marco, text="Seleccionar GCODE", command=seleccionar_gcode)
        seleccionar_boton_gcode.grid(row=1, column=2, padx=10, pady=10)

        # Capas por captura
        tk.Label(self.marco, text="Capas por captura:").grid(row=2, column=0, padx=10, pady=10)
        self.capas_entrada = tk.Entry(self.marco, width=10)
        self.capas_entrada.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.capas_entrada.insert(0, "10") # Valor por defecto

        # Angulo de la camara
        tk.Label(self.marco, text="Ángulo de la cámara (°):").grid(row=3, column=0, padx=10, pady=10)
        self.angulo_camara = tk.Entry(self.marco, width=10)
        self.angulo_camara.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.angulo_camara.insert(0, "90")  # Valor por defecto

        # Altura de la camara
        tk.Label(self.marco, text="Altura de la cámara (mm):").grid(row=4, column=0, padx=10, pady=10)
        self.altura_camara = tk.Entry(self.marco, width=10)
        self.altura_camara.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        self.altura_camara.insert(0, "30")  # Valor por defecto

        # Entrada para el correo de destino
        tk.Label(self.marco, text="Correo de destino:").grid(row=5, column=0, padx=10, pady=10)
        self.correo_destino = tk.Entry(self.marco, width=40)
        self.correo_destino.grid(row=5, column=1, padx=10, pady=10)
        self.correo_destino.insert(0, "usuario@gmail.com")  # Valor por defecto

        # Color del filamento
        tk.Label(self.marco, text="Color del filamento:").grid(row=6, column=0, padx=10, pady=10)
        colores = ['blanco', 'negro', 'rojo', 'verde', 'azul', 'amarillo', 'gris', 'otro color']
        self.color_filamento = tk.StringVar(self.ventana)
        self.color_filamento.set(colores[0]) # color blanco por defecto
        menu_color = tk.OptionMenu(self.marco, self.color_filamento, *colores)
        menu_color.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        # Creo el marco para los botones
        self.marco_botones = tk.Frame(self.ventana)
        self.marco_botones.pack(pady=20)

        # Creo los botones "continuar" y "cancelar"
        boton_continuar = tk.Button(self.marco_botones, text="Continuar", command=self.validar_datos)
        boton_continuar.pack(side=tk.LEFT, padx=10)

        boton_cancelar = tk.Button(self.marco_botones, text="Cancelar", command=self.cancelar)
        boton_cancelar.pack(side=tk.LEFT, padx=10)

    # Funcion que valida los datos del formulario y los guarda
    def validar_datos(self):
        ruta_stl = self.fichero_stl.get()
        ruta_gcode = self.fichero_gcode.get()
        correo_destino = self.correo_destino.get()
        color_seleccionado = self.color_filamento.get()
        try:
            # Compruebo que las capas, el ángulo y la altura son enteros.
            capas_valor = int(self.capas_entrada.get())
            angulo_camara_valor = int(self.angulo_camara.get())
            altura_camara_valor = int(self.altura_camara.get())
            #
            if capas_valor <= 0:
                raise ValueError("El número de capas por captura debe ser mayor que 0")
            if altura_camara_valor <= 0:
                raise ValueError("La altura de la cámara debe ser mayor que 0.")
            if angulo_camara_valor < -360 or angulo_camara_valor > 360:
                raise ValueError("El ángulo debe ser mayor que -360º y menor de 360º")
            if not os.path.exists(ruta_stl):
                raise FileNotFoundError(f"El archivo STL no existe: {ruta_stl}")
            if not os.path.exists(ruta_gcode):
                raise FileNotFoundError(f"El archivo STL no existe: {ruta_gcode}")
            if not correo_destino:
                raise ValueError("No se ha introducido un correo de destino")

        except ValueError as e:
            # Captura de errores en los valores introducidos
            messagebox.showerror("Error en los datos", f"Valor no válido: {e}")
            return
        except FileNotFoundError as e:
            # Captura de errores en las rutas
            messagebox.showerror("Error de archivo", f"Archivo no encontrado: {e}")
            return
        # Captura del resto de errores inesperados.
        except Exception as e:
            messagebox.showerror("Error", f"Valor no válido: {e}")
            return

        # Guardar los datos en el diccionario
        self.datos['stl'] = ruta_stl
        self.datos['gcode'] = ruta_gcode
        self.datos['capas'] = capas_valor
        self.datos['angulo_camara'] = angulo_camara_valor
        self.datos['altura_camara'] = altura_camara_valor
        self.datos['correo'] = correo_destino
        self.datos['color'] = color_seleccionado
        self.ventana.destroy()

    # Funcion que cancela la interface
    def cancelar(self):
        self.ventana.destroy()
        sys.exit(0)

    # Funcion que ejecuta la interface y devuelve los datos obtenidos
    def mostrar_interface_datosentrada(self):
        self.ventana.mainloop()
        return (self.datos.get('stl'), self.datos.get('gcode'),
                self.datos.get('capas'), self.datos.get('angulo_camara'),
                self.datos.get('altura_camara'), self.datos.get('correo'),
                self.datos.get('color'))


if __name__ == "__main__":
    interfaz = InterfaceDatos()
    stl, gcode, capas, angulo_camara, altura_camara, correo, color = interfaz.mostrar_interface_datosentrada()
    print(f"STL: {stl}, GCODE: {gcode}, Capas: {capas}, Ángulo: {angulo_camara}, Altura: {altura_camara}, Correo: {correo}")

