# Modulo que extrae la informacion que necesitamos del fichero Gcode
class ExtractorGcodeInfo:
    @staticmethod
    def extraer_datos(ruta_gcode):
        altura_total = 0
        altura_capa = 0
        try:
            with open(ruta_gcode, 'r') as gcode:
                for linea in gcode:
                    # Extraigo la altura total y altura de capa
                    if linea.startswith(";MAXZ:"):
                        altura_total = float(linea.split(":")[1])
                    if linea.startswith(";Layer height:"):
                        altura_capa = float(linea.split(":")[1])
                    if altura_total > 0 and altura_capa > 0:
                        break
        except Exception as e:
            print(f"Error al leer el archivo GCODE: {e}")

        return altura_total, altura_capa
