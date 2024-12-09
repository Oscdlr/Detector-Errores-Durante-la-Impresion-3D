# Importo librerías necesarias
import vtk
import os

# Clase que recibe como entrada el fichero STL y lo procesa haciendo seccion, giro y guardado de vista STL
class SeccionCapturaVistaSTL:
    def __init__(self, entrada_stl):
        self.entrada_stl = entrada_stl
        self.datos_stl = None

    # Seccion del fichero STL a altura determinada
    def seccionar(self, altura):
        # Lectura fichero STL
        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.entrada_stl)

        # Plano de corte del objeto STL. Este plano secciona el objeto a cierta altura.
        plano = vtk.vtkPlane()
        plano.SetOrigin(0, 0, altura)
        plano.SetNormal(0, 0, 1)

        # Seccionador recorta la maya STL usando el plano
        seccionador = vtk.vtkClipPolyData()
        seccionador.SetClipFunction(plano)
        # InsideOutOn se usa para conservar el objeto. Si no se incluyera se conservaria la seccion del Objeto.
        seccionador.InsideOutOn()
        # No generar valores escalares adicionales
        seccionador.GenerateClipScalarsOff()
        # Para que pueda ser utilizado por el reader
        seccionador.SetInputConnection(reader.GetOutputPort())
        # Aplica la seccion
        seccionador.Update()

        self.datos_stl = seccionador.GetOutput()
        return self.datos_stl

    # Función que rota el fichero STL un número de grados indicado
    def rotar(self, angulo):
        if self.datos_stl is None:
            raise ValueError("Los datos STL no se han cargado correctamente.")

        # vtkTransform se usa para rotar, transladar o escalar objetos. En este caso rota archivo STL
        transformar = vtk.vtkTransform()
        # Rotación en el eje Z. "RotateZ"
        transformar.RotateZ(angulo)
        # Crea un filtro para aplicar la transformación (rotación)
        transformar_filter = vtk.vtkTransformPolyDataFilter()
        transformar_filter.SetTransform(transformar)
        transformar_filter.SetInputData(self.datos_stl)
        # Aplica la transformación
        transformar_filter.Update()
        # Obtengo el objeto transformado
        self.datos_stl = transformar_filter.GetOutput()
        return self.datos_stl

    # Función que guarda el objeto STL seccionado, sin utilizar, solo usada para pruebas.
    def guardar(self, fichero_salida):
        if self.datos_stl is None:
            raise ValueError("No hay datos STL para guardar. Por favor, corta el STL a una altura primero.")

        archivador = vtk.vtkSTLWriter()
        archivador.SetFileName(fichero_salida)
        archivador.SetInputData(self.datos_stl)
        archivador.Write()

    # Función que captura vista STL con la camara configurada a cierta altura.
    # Se tiene en cuenta la altura de la seccion para que el objeto aparezca dentro de los margenes.
    def captura_vista(self, carpeta_salida, nombre_vista, altura_cam, altura_seccion):

        if self.datos_stl is None:
            raise ValueError("No hay datos en el fichero STL")

        # Creo la carpeta si no existe
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        # Creo el mapeador de los datos STL para que sea entendido y renderizado
        mapeador = vtk.vtkPolyDataMapper()
        mapeador.SetInputData(self.datos_stl)

        # Creo objeto actor (objeto 3D)
        actor = vtk.vtkActor()
        actor.SetMapper(mapeador)
        # Muestro solo el "wireframe", son los bordes sin relleno (esqueleto del objeto)
        actor.GetProperty().SetRepresentationToWireframe()
        # Establezco color en blanco
        actor.GetProperty().SetColor(1.0, 1.0, 1.0)

        # Creo el renderizador encargado de la visualización de objetos en la escena
        renderizador = vtk.vtkRenderer()
        renderizador.AddActor(actor)
        renderizador.SetBackground(0.1, 0.1, 0.1)

        # Crear la ventana de renderizado donde se visualiza el renderizado
        ventana_rend = vtk.vtkRenderWindow()
        ventana_rend.SetOffScreenRendering(1)  # Para que no se abra ventana gráfica al usuario
        ventana_rend.AddRenderer(renderizador)  # Para que el objeto se visualice en la ventana
        ventana_rend.SetSize(800, 600) # Tamanio de ventana

        # Obtengo los limites del objeto en el eje X, Y y Z para ajustar la vista.
        bounds = self.datos_stl.GetBounds()
        altura_min, altura_max = bounds[4], bounds[5]
        alzado_min, alzado_max = bounds[0], bounds[1]
        perfil_min, perfil_max = bounds[2], bounds[3]

        # Calculo la anchura y la altura del objeto
        anchura_obj = max(alzado_max - alzado_min, perfil_max - perfil_min)
        altura_obj = max(altura_seccion, altura_max) - altura_min

        # Creo la camara para mantener la vista centrada
        camera = vtk.vtkCamera()
        camera.SetPosition(0, -220, altura_cam)  # Indico la posicion de la camara. Distancia 22cms.
        camera.SetFocalPoint(0, 0, altura_min)  # Apunto a la base del objeto
        camera.SetViewUp(0, 0, 1)  # Indico la posicion del eje Z hacia arriba
        camera.SetViewAngle(45)  # Para ampliar el angulo de vista en perspectiva

        # Calculo el centro del objeto para mantenerlo centrado
        centro_objeto_z = (altura_min + altura_max) / 2
        camera.SetFocalPoint(0, 0, centro_objeto_z)  # Mantengo el objeto centrado en la vista

        # Ajusto el ParallelScale para que el objeto no se salga de la ventana a medida que crece
        escala_vista = max(anchura_obj, altura_obj) / 2
        camera.SetParallelScale(escala_vista * 3)  # Ajusto la escala

        # Activo la camara diciendoselo al renderizador
        renderizador.SetActiveCamera(camera)

        # Capturo la imagen
        imagen_capturada = vtk.vtkWindowToImageFilter()
        imagen_capturada.SetInput(ventana_rend)
        imagen_capturada.ReadFrontBufferOff()
        imagen_capturada.Update()

        # Guardo la imagen capturada en la carpeta de salida
        guardado = vtk.vtkPNGWriter()
        guardado.SetFileName(f"{carpeta_salida}/{nombre_vista}.png")
        guardado.SetInputConnection(imagen_capturada.GetOutputPort())
        guardado.Write()

        # Finalizo
        ventana_rend.Finalize()
