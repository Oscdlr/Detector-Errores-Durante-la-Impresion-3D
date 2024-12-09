# Importo las librerias necesarias y el modulo "seccion_captura_vista_stl
import os
from seccion_captura_vista_stl import SeccionCapturaVistaSTL


# Clase que recibe los datos que despues seran tratados para procesar el fichero STL
class CapturaVistasSTL:
    def __init__(self, fichero_entrada, altura_capa, capas_entre_captura, altura_total, angulo_camara, altura_camara):
        self.fichero_entrada = fichero_entrada
        self.altura_capa = altura_capa
        self.capas_entre_captura = capas_entre_captura
        self.altura_total = altura_total
        self.angulo_camara = angulo_camara  # Nuevo parámetro
        self.altura_camara = altura_camara  # Nuevo parámetro
        self.disenio = SeccionCapturaVistaSTL(fichero_entrada)

    def iniciar(self):
        # Inicio de la función que genera las vistas STL y las guarda
        # Comprobar que las variables no son 0
        if self.altura_capa == 0 or self.capas_entre_captura == 0:
            raise ValueError("La altura de capa y las capas entre captura no pueden ser 0.")

        # Creo carpeta donde se almacenarán las capturas de las vistas STL
        carpeta_capturas = os.path.join("capturas_objeto", "capturas_vistas")
        if not os.path.exists(carpeta_capturas):
            os.makedirs(carpeta_capturas)

        # Lista que será tratada por el programa principal para su comparación con el modelo impreso
        lista_capturas_vistas = []
        secciones_totales = int(self.altura_total // (self.altura_capa * self.capas_entre_captura))

        for indice in range(secciones_totales):
            altura_corte = round(self.altura_capa * (indice + 1) * self.capas_entre_captura, 2)
            print(f"Corte en altura: {altura_corte} mm")

            self.disenio.seccionar(altura_corte)
            self.disenio.rotar(self.angulo_camara)  # Usa el ángulo configurado

            nombre_vista = f"vista_{indice + 1}"
            self.disenio.captura_vista(carpeta_capturas, nombre_vista, self.altura_camara,
                                       altura_corte)  # Usa la altura configurada

            lista_capturas_vistas.append(os.path.join(carpeta_capturas, f"{nombre_vista}.png"))

        return lista_capturas_vistas
