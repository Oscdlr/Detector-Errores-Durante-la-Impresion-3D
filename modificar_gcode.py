# Importo las librerias necesarias
import os

# Modulo donde modifico el Gcode para que realice pausas programadas cada n capas
class ModificadorGcode:
    def __init__(self, ruta_archivo, altura_capa, capas_entre_pausa):
        self.ruta_archivo = ruta_archivo
        self.altura_capa = altura_capa
        self.capas_entre_pausa = capas_entre_pausa
        self.altura_total = 0
        self.gcode_modificado = []
        self.capas_para_pausa = []
        self.mesh_detectado = False

    # Modifico el gcode siguendo secuencialmente estas ordenes
    def modificar(self):
        self.leer_archivo()
        self.calcular_capas_para_pausa()
        self.procesar_lineas()
        self.guardar_archivo_modificado()

    # Leo el archivo para encontrar la altura total
    def leer_archivo(self):
        with open(self.ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        # Busco la altura total del objeto
        for linea in lineas:
            if linea.startswith(";MAXZ:"):
                self.altura_total = float(linea.split(":")[1].strip())
                break

    # Calculo en que capas se debe pausar el gcode y guardo el numero de capa en lista
    def calcular_capas_para_pausa(self):
        num_capas = int(self.altura_total / self.altura_capa)
        for i in range(1, num_capas + 1):
            if i % self.capas_entre_pausa == 0:
                self.capas_para_pausa.append(i)

    # Leo el fichero linea a linea
    def procesar_lineas(self):
        capa_actual = 0
        with open(self.ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        # Compruebo cada linea para encontrar donde debe hacer las pausas
        for linea in lineas:
            # Pausa inicial despues del Mesh para hacer la captura base
            if linea.startswith(";MESH:") and not self.mesh_detectado:
                self.gcode_modificado.append(linea)
                self.gcode_modificado.append("G0 X0 Y220 ; Mover a la posición X0 Y220\n")
                self.gcode_modificado.append("G4 S3 ; Pausar por 3 segundos\n")
                self.gcode_modificado.append("; --- Fin de la pausa inicial ---\n")
                self.mesh_detectado = True
                continue

            # Pausa cada n capas. Compruebo cada vez que inicia una capa nueva si esta en lista de capas
            # en las que debe haber pausa. Si esta en la lista incorporo las ordenes de pausa.
            if linea.startswith("G0") and " Z" in linea:
                capa_actual += 1
                if capa_actual in self.capas_para_pausa:
                    altura_capa_actual = capa_actual * self.altura_capa
                    # self.gcode_modificado.append("G0 E-1 F1800 ; Retracción del filamento antes del movimiento\n")
                    self.gcode_modificado.append("G0 X0 Y220 ; Mover a la esquina superior izquierda\n")
                    self.gcode_modificado.append("G4 S3 ; Pausar por 3 segundos\n")
                    self.gcode_modificado.append("G0 X110 Y110 ; Mover al centro\n")
                    # self.gcode_modificado.append("G0 E1 F1800 ; Restaurar el filamento retraído\n")
                    self.gcode_modificado.append(f"G0 Z{altura_capa_actual}  ; Volver a la altura de la capa\n")

            # Añado la linea leida al fichero
            self.gcode_modificado.append(linea)

    # Guardo el archivo modificado en la misma carpeta renombrando
    def guardar_archivo_modificado(self):
        nombre_archivo_modificado = 'modificado_' + os.path.basename(self.ruta_archivo)


        with open(nombre_archivo_modificado, 'w') as archivo:
            archivo.writelines(self.gcode_modificado)

        # print(f"Altura total del objeto: {self.altura_total} mm")
        # print(f"Archivo modificado guardado en: {nombre_archivo_modificado}")
        return nombre_archivo_modificado


if __name__ == "__main__":
    pass