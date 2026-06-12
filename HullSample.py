import FreeCAD as App
# COMANDO DE IMPORTACIÓN:
# Importa el módulo principal de FreeCAD.
# Le damos el alias "App" para escribir App.Vector, App.newDocument, etc.
# Este módulo controla documentos, geometría base, vectores, recompute, unidades, etc.


import FreeCADGui as Gui
# COMANDO DE IMPORTACIÓN:
# Importa la parte visual/interfaz de FreeCAD.
# Le damos el alias "Gui".
# Sirve para controlar cámara, vista, zoom, selección, orientación visual, etc.


import Draft
# COMANDO DE IMPORTACIÓN:
# Importa el módulo Draft de FreeCAD.
# Draft permite crear líneas, BSplines, wires, objetos 2D/3D simples, etc.
# En este script lo usamos principalmente para Draft.make_bspline().


import Part
# COMANDO DE IMPORTACIÓN:
# Importa el módulo Part de FreeCAD.
# Part sirve para geometría más avanzada: superficies, lofts, sólidos, shells, faces.
# En este script todavía casi no lo usamos, pero lo dejamos listo para el próximo paso.


doc = App.newDocument("Draft_Hull_Only")
# COMANDO DE FREECAD:
# App.newDocument() crea un documento nuevo de FreeCAD.
# "Draft_Hull_Only" es el nombre del documento.
# doc es una VARIABLE que guarda ese documento para poder usarlo después.
# Conceptualmente: doc = el archivo/proyecto donde vamos a dibujar el hull.


# =========================
# BASIC HULL PARAMETERS
# Units: millimeters
# =========================
# COMENTARIO:
# Esta sección contiene los parámetros principales del casco.
# Estos valores los puedes cambiar tú a demanda.


L = 12000
# PARÁMETRO CREADO POR NOSOTROS:
# L significa Length.
# Es el largo total del casco.
# 12000 mm = 12 metros.
# Cambiar este valor hace el casco más largo o más corto.


B = 3200
# PARÁMETRO CREADO POR NOSOTROS:
# B significa Beam.
# Es la manga máxima del casco, o sea el ancho máximo.
# 3200 mm = 3.2 metros.
# Cambiar este valor hace el casco más ancho o más angosto.


D = 1400
# PARÁMETRO CREADO POR NOSOTROS:
# D significa Depth.
# Es la profundidad base del casco.
# 1400 mm = 1.4 metros.
# Cambiar este valor hace el casco más profundo o menos profundo.


stations = 13
# PARÁMETRO CREADO POR NOSOTROS:
# stations es la cantidad de secciones transversales.
# Cada station es como una “costilla” del casco.
# Más stations = más curvas azules y mejor lectura visual del casco.
# Ejemplo: 13, 20, 30, 50.


def style(obj, color=(0.2, 0.45, 0.9), width=2):
# DEFINICIÓN DE FUNCIÓN PYTHON:
# def crea una función.
# style es el nombre de la función.
# obj es un parámetro: representa el objeto de FreeCAD que vamos a pintar.
# color es un parámetro opcional con valor por defecto.
# width es otro parámetro opcional con valor por defecto.
# Esta función sirve para cambiar el color y grosor visual de una curva.

    obj.ViewObject.LineColor = color
    # COMANDO/PROPIEDAD DE FREECAD:
    # obj.ViewObject accede a la representación visual del objeto.
    # LineColor cambia el color de la línea.
    # color viene del parámetro de la función.
    # Ejemplo: (1.0, 0.1, 0.1) = rojo.

    obj.ViewObject.LineWidth = width
    # COMANDO/PROPIEDAD DE FREECAD:
    # LineWidth cambia el grosor visual de la línea.
    # width viene del parámetro de la función.
    # Ejemplo: width=4 hace una línea más gruesa.

    return obj
    # COMANDO PYTHON:
    # return devuelve algo desde la función.
    # Aquí devuelve el mismo objeto ya estilizado.
    # No es estrictamente obligatorio, pero es buena práctica.


# =========================
# HULL SHAPE FUNCTIONS
# =========================
# COMENTARIO:
# Esta sección define las funciones matemáticas que crean la forma del casco.
# Estas funciones son el “cerebro” del hull.


def beam_at(x):
# DEFINICIÓN DE FUNCIÓN PYTHON:
# beam_at significa “manga en una posición x”.
# x es una posición longitudinal a lo largo del barco.
# Esta función responde: ¿qué ancho tiene el casco en este punto del largo?

    """
    Beam distribution along length.
    0 at bow/stern, max around middle.
    """
    # DOCSTRING:
    # Esto es documentación interna de la función.
    # Explica que la manga cambia a lo largo del casco.
    # La manga será menor en los extremos y mayor en el centro.

    t = x / L
    # VARIABLE LOCAL:
    # t convierte la posición x en un porcentaje del largo total.
    # Si x = 0, entonces t = 0.
    # Si x = L/2, entonces t = 0.5.
    # Si x = L, entonces t = 1.
    # Esto facilita usar matemáticas proporcionales.

    return B * (App.Units.Quantity(1).Value) * (0.12 + 0.88 * (1 - (2*t - 1)**2))
    # RETURN PYTHON:
    # Devuelve la manga total en esa posición x.
    #
    # B es la manga máxima base que definimos arriba.
    #
    # App.Units.Quantity(1).Value:
    # Esto es de FreeCAD. Aquí realmente no es muy necesario.
    # Lo dejé como multiplicador neutro.
    # En la práctica vale 1.
    #
    # (2*t - 1):
    # Convierte t de rango 0..1 a rango -1..1.
    #
    # (2*t - 1)**2:
    # Eleva al cuadrado.
    # Esto crea una curva simétrica.
    #
    # 1 - (2*t - 1)**2:
    # Crea una parábola:
    # baja en extremos, alta en el centro.
    #
    # 0.12 + 0.88 * (...):
    # Evita que la manga llegue a cero.
    # 0.12 significa que en los extremos queda 12% de la manga.
    # 0.88 completa el resto hasta 100%.
    #
    # Conceptualmente:
    # Esta línea define cómo el casco se abre desde los extremos hacia el centro.


def depth_at(x):
# DEFINICIÓN DE FUNCIÓN PYTHON:
# depth_at significa “profundidad en una posición x”.
# Esta función responde: ¿qué profundidad tiene el casco en esta estación?

    """
    Depth distribution.
    Shallower near bow/stern, deeper midship.
    """
    # DOCSTRING:
    # Explica que el casco es menos profundo en los extremos
    # y más profundo cerca del centro.

    t = x / L
    # VARIABLE LOCAL:
    # Convierte x en porcentaje del largo.
    # Igual que en beam_at().
    # t va de 0 a 1.

    return D * (0.45 + 0.55 * (1 - (2*t - 1)**2))
    # RETURN PYTHON:
    # Devuelve la profundidad local.
    #
    # D es la profundidad base/máxima.
    #
    # 1 - (2*t - 1)**2:
    # Otra parábola.
    #
    # 0.45 + 0.55 * (...):
    # Hace que la profundidad nunca baje de 45%.
    # En el centro llega más cerca de 100%.
    #
    # Conceptualmente:
    # El casco tiene más volumen en la zona media y menos en los extremos.


def z_keel(x):
# DEFINICIÓN DE FUNCIÓN PYTHON:
# z_keel significa “posición Z de la quilla en una posición x”.
# Esta función define la línea roja de quilla.

    """
    Keel line rocker.
    Lowest near middle, higher near ends.
    """
    # DOCSTRING:
    # Explica que la quilla tiene rocker.
    # Rocker = curvatura longitudinal de la parte inferior del casco.

    t = x / L
    # VARIABLE LOCAL:
    # Convierte la posición x a porcentaje.
    # t = 0 inicio, t = 0.5 centro, t = 1 final.

    return -depth_at(x) * (0.75 + 0.25 * (1 - abs(2*t - 1)))
    # RETURN PYTHON:
    # Devuelve la altura Z de la quilla.
    #
    # depth_at(x):
    # Usa la función anterior para saber la profundidad local.
    #
    # El signo negativo "-" baja la quilla hacia abajo.
    # En FreeCAD, Z negativo significa hacia abajo en este modelo.
    #
    # abs(2*t - 1):
    # Crea una forma simétrica respecto al centro.
    #
    # 1 - abs(2*t - 1):
    # Da valor máximo en el centro y mínimo en los extremos.
    #
    # 0.75 + 0.25 * (...):
    # Controla cuánto baja la quilla.
    #
    # Conceptualmente:
    # La quilla está más baja en el centro y más alta hacia proa/popa.


# =========================
# CREATE STATIONS
# Each station is a cross-section curve
# =========================
# COMENTARIO:
# Esta sección crea las secciones transversales.
# Son las curvas azules que ves como costillas.


station_curves = []
# VARIABLE / LISTA PYTHON:
# Crea una lista vacía.
# Aquí guardaremos todas las curvas de estaciones.
# append() irá metiendo cada curva dentro de esta lista.


for i in range(stations):
# LOOP PYTHON:
# for repite un bloque varias veces.
# range(stations) genera números desde 0 hasta stations-1.
# Si stations = 13, i será:
# 0, 1, 2, 3, ..., 12.
# Cada repetición crea una sección transversal.

    x = L * i / (stations - 1)
    # VARIABLE LOCAL:
    # Calcula la posición longitudinal de esta estación.
    #
    # L = largo total.
    # i = número actual de estación.
    # stations - 1 se usa para que la última estación caiga exactamente en L.
    #
    # Con L=12000 y stations=13:
    # x será 0, 1000, 2000, ..., 12000.
    #
    # Conceptualmente:
    # Estamos distribuyendo costillas uniformemente a lo largo del casco.

    half_beam = beam_at(x) / 2
    # VARIABLE LOCAL:
    # Calcula la mitad de la manga en esta estación.
    #
    # beam_at(x) devuelve la manga total en esa posición x.
    # Dividimos por 2 porque el casco tiene lado izquierdo y lado derecho.
    #
    # Y negativo = un lado.
    # Y positivo = el otro lado.

    depth = depth_at(x)
    # VARIABLE LOCAL:
    # Calcula la profundidad de esta estación usando la función depth_at().
    # Cada estación puede tener profundidad diferente.

    keel_z = z_keel(x)
    # VARIABLE LOCAL:
    # Calcula la altura Z de la quilla para esta estación.
    # Normalmente será un valor negativo porque baja desde la cubierta/borda.

    pts = [
    # VARIABLE / LISTA PYTHON:
    # pts será una lista de puntos 3D.
    # Estos puntos forman la sección transversal.
    # Draft.make_bspline() usará estos puntos para crear una curva suave.

        App.Vector(x, -half_beam, 0),
        # COMANDO/CLASE DE FREECAD:
        # App.Vector(x, y, z) crea un punto 3D.
        #
        # x = posición longitudinal de la estación.
        # y = -half_beam, lado izquierdo/babor.
        # z = 0, altura de borda/cubierta.
        #
        # Este es el punto superior izquierdo de la estación.

        App.Vector(x, -half_beam * 0.85, -depth * 0.20),
        # PUNTO 3D:
        # Sigue en el lado izquierdo, pero un poco más hacia adentro.
        #
        # -half_beam * 0.85:
        # 85% de la media manga.
        #
        # -depth * 0.20:
        # Baja 20% de la profundidad.
        #
        # Conceptualmente:
        # Este punto empieza a curvar la pared lateral del casco.

        App.Vector(x, -half_beam * 0.45, -depth * 0.70),
        # PUNTO 3D:
        # Más cerca del centro y bastante más abajo.
        #
        # -half_beam * 0.45:
        # 45% de media manga.
        #
        # -depth * 0.70:
        # Baja 70% de la profundidad.
        #
        # Conceptualmente:
        # Este punto forma la panza inferior del casco.

        App.Vector(x, 0, keel_z),
        # PUNTO 3D:
        # Punto central inferior de la estación.
        #
        # y = 0:
        # Centro del casco.
        #
        # z = keel_z:
        # Altura de la quilla.
        #
        # Este es el punto más bajo de la sección.

        App.Vector(x, half_beam * 0.45, -depth * 0.70),
        # PUNTO 3D:
        # Espejo del punto inferior izquierdo, ahora hacia el lado derecho.
        #
        # y positivo = otro lado del casco.
        # z mantiene la misma profundidad relativa.
        #
        # Esto ayuda a mantener simetría.

        App.Vector(x, half_beam * 0.85, -depth * 0.20),
        # PUNTO 3D:
        # Espejo del punto lateral izquierdo.
        # Sube hacia la borda derecha.

        App.Vector(x, half_beam, 0),
        # PUNTO 3D:
        # Punto superior derecho.
        #
        # y = half_beam:
        # Extremo derecho de la manga.
        #
        # z = 0:
        # Altura de borda/cubierta.
    ]

    curve = Draft.make_bspline(pts, closed=False, face=False)
    # COMANDO DE FREECAD / DRAFT:
    # Draft.make_bspline() crea una curva B-Spline.
    #
    # pts:
    # Lista de puntos que la curva usará como referencia.
    #
    # closed=False:
    # La curva NO se cierra.
    # No conecta el último punto con el primero.
    #
    # face=False:
    # No crea una cara/superficie.
    # Sólo crea una curva/línea.
    #
    # curve es una VARIABLE que guarda el objeto creado.

    curve.Label = "Station_%02d" % i
    # PROPIEDAD DE FREECAD:
    # Label cambia el nombre visible del objeto en el árbol de FreeCAD.
    #
    # "Station_%02d" % i:
    # Formatea el número con dos dígitos.
    #
    # Ejemplos:
    # i=0  -> Station_00
    # i=1  -> Station_01
    # i=12 -> Station_12

    style(curve, (0.1, 0.4, 1.0), 2)
    # LLAMADA A FUNCIÓN CREADA POR NOSOTROS:
    # Usa la función style() definida arriba.
    #
    # curve:
    # Objeto a pintar.
    #
    # (0.1, 0.4, 1.0):
    # Color RGB. Esto da azul.
    #
    # 2:
    # Grosor de línea.
    #
    # Resultado:
    # Las estaciones quedan azules.

    station_curves.append(curve)
    # COMANDO PYTHON DE LISTA:
    # append() agrega un elemento al final de una lista.
    #
    # Aquí metemos la curva dentro de station_curves.
    #
    # Conceptualmente:
    # Guardamos todas las costillas en una lista por si después queremos usarlas.


doc.recompute()
# COMANDO DE FREECAD:
# Recalcula/actualiza el documento.
# FreeCAD no siempre actualiza todo automáticamente.
# recompute() fuerza a FreeCAD a construir y mostrar la geometría recién creada.


# =========================
# CREATE LONGITUDINAL GUIDE CURVES
# These make the hull easier to understand visually
# =========================
# COMENTARIO:
# Ahora vamos a crear líneas longitudinales.
# Estas líneas recorren el casco desde punta a punta.
# Sirven para leer mejor la forma del hull.


keel_pts = []
# LISTA PYTHON:
# Guardará puntos de la línea de quilla.
# Luego se convertirá en una BSpline roja.


port_sheer_pts = []
# LISTA PYTHON:
# Guardará puntos de la borda de babor.
# “Sheer line” = línea superior/lateral del casco.


starboard_sheer_pts = []
# LISTA PYTHON:
# Guardará puntos de la borda de estribor.


port_chine_pts = []
# LISTA PYTHON:
# Guardará puntos de una guía lateral inferior de babor.
# En este draft es una línea visual, no un chine estructural real todavía.


starboard_chine_pts = []
# LISTA PYTHON:
# Guardará puntos de una guía lateral inferior de estribor.


for i in range(stations):
# LOOP PYTHON:
# Recorre las mismas estaciones.
# Pero ahora no crea costillas.
# Ahora extrae puntos clave para crear líneas longitudinales.

    x = L * i / (stations - 1)
    # VARIABLE LOCAL:
    # Calcula la misma posición x de cada estación.
    # Esto asegura que las líneas longitudinales coincidan con las costillas.

    half_beam = beam_at(x) / 2
    # VARIABLE LOCAL:
    # Calcula media manga en esa posición x.

    depth = depth_at(x)
    # VARIABLE LOCAL:
    # Calcula profundidad local.

    keel_zv = z_keel(x)
    # VARIABLE LOCAL:
    # Calcula altura Z de la quilla.
    #
    # Uso keel_zv en vez de keel_z sólo para distinguir el nombre.
    # Podría llamarse keel_z también.

    keel_pts.append(App.Vector(x, 0, keel_zv))
    # APPEND A LISTA:
    # Agrega un punto a la lista keel_pts.
    #
    # x = posición longitudinal.
    # y = 0, centro del casco.
    # z = keel_zv, altura de quilla.
    #
    # Estos puntos formarán la línea roja de quilla.

    port_sheer_pts.append(App.Vector(x, -half_beam, 0))
    # APPEND A LISTA:
    # Agrega un punto a la línea de borda izquierda/babor.
    #
    # y = -half_beam.
    # z = 0.
    #
    # Estos puntos formarán una línea verde.

    starboard_sheer_pts.append(App.Vector(x, half_beam, 0))
    # APPEND A LISTA:
    # Agrega un punto a la línea de borda derecha/estribor.
    #
    # y = half_beam.
    # z = 0.
    #
    # Estos puntos formarán la otra línea verde.

    port_chine_pts.append(App.Vector(x, -half_beam * 0.55, -depth * 0.65))
    # APPEND A LISTA:
    # Agrega un punto a la guía lateral inferior izquierda.
    #
    # y = -half_beam * 0.55:
    # Punto lateral a 55% de la media manga.
    #
    # z = -depth * 0.65:
    # Punto bajo, a 65% de la profundidad.
    #
    # Conceptualmente:
    # Esta línea ayuda a ver cómo corre la panza lateral del casco.

    starboard_chine_pts.append(App.Vector(x, half_beam * 0.55, -depth * 0.65))
    # APPEND A LISTA:
    # Agrega punto equivalente para el lado derecho.
    # Es el espejo del port_chine.


keel = Draft.make_bspline(keel_pts, closed=False, face=False)
# COMANDO DE FREECAD / DRAFT:
# Crea una BSpline usando los puntos de quilla.
# Esta será la línea longitudinal central inferior del casco.
#
# keel es una VARIABLE que guarda esa curva.


keel.Label = "Keel_Line"
# PROPIEDAD DE FREECAD:
# Cambia el nombre visible de la curva a Keel_Line.


style(keel, (1.0, 0.1, 0.1), 4)
# LLAMADA A FUNCIÓN CREADA POR NOSOTROS:
# Pinta la línea de quilla.
#
# (1.0, 0.1, 0.1) = rojo.
# 4 = línea gruesa.


port_sheer = Draft.make_bspline(port_sheer_pts, closed=False, face=False)
# COMANDO DE FREECAD / DRAFT:
# Crea la BSpline de la borda de babor.
# Usa los puntos guardados en port_sheer_pts.


port_sheer.Label = "Port_Sheer_Line"
# PROPIEDAD DE FREECAD:
# Nombre visible del objeto.


style(port_sheer, (0.0, 0.7, 0.2), 3)
# LLAMADA A FUNCIÓN:
# Pinta la línea de babor en verde.
# Grosor 3.


starboard_sheer = Draft.make_bspline(starboard_sheer_pts, closed=False, face=False)
# COMANDO DE FREECAD / DRAFT:
# Crea la BSpline de la borda de estribor.


starboard_sheer.Label = "Starboard_Sheer_Line"
# PROPIEDAD DE FREECAD:
# Nombre visible en el árbol de FreeCAD.


style(starboard_sheer, (0.0, 0.7, 0.2), 3)
# LLAMADA A FUNCIÓN:
# Pinta la línea de estribor en verde.
# Grosor 3.


port_chine = Draft.make_bspline(port_chine_pts, closed=False, face=False)
# COMANDO DE FREECAD / DRAFT:
# Crea la guía longitudinal inferior de babor.
# Usa los puntos port_chine_pts.


port_chine.Label = "Port_Chine_Guide"
# PROPIEDAD DE FREECAD:
# Nombre visible del objeto.


style(port_chine, (0.9, 0.6, 0.0), 2)
# LLAMADA A FUNCIÓN:
# Pinta esta guía en amarillo/naranja.
# Grosor 2.


starboard_chine = Draft.make_bspline(starboard_chine_pts, closed=False, face=False)
# COMANDO DE FREECAD / DRAFT:
# Crea la guía longitudinal inferior de estribor.


starboard_chine.Label = "Starboard_Chine_Guide"
# PROPIEDAD DE FREECAD:
# Nombre visible del objeto.


style(starboard_chine, (0.9, 0.6, 0.0), 2)
# LLAMADA A FUNCIÓN:
# Pinta la guía de estribor amarillo/naranja.
# Grosor 2.


doc.recompute()
# COMANDO DE FREECAD:
# Recalcula el documento otra vez.
# Esto asegura que todas las curvas longitudinales se vean correctamente.


# =========================
# VIEW SETUP
# =========================
# COMENTARIO:
# Esta sección sólo controla la vista.
# No cambia la geometría del casco.


Gui.ActiveDocument.ActiveView.viewAxometric()
# COMANDO DE FREECAD GUI:
# Cambia la cámara a vista axonométrica/isométrica.
# Sirve para ver el casco en 3D.


Gui.SendMsgToActiveView("ViewFit")
# COMANDO DE FREECAD GUI:
# Ajusta el zoom para que todo el modelo entre en la pantalla.
# Es como “zoom extents” o “fit all”.


print("Draft hull created.")
# COMANDO PYTHON:
# Imprime un mensaje en la consola.
# No crea geometría.


print("Length:", L, "mm")
# COMANDO PYTHON:
# Imprime el largo usado.
# L es la variable de largo definida arriba.


print("Beam:", B, "mm")
# COMANDO PYTHON:
# Imprime la manga usada.
# B es la variable de manga.


print("Depth:", D, "mm")
# COMANDO PYTHON:
# Imprime la profundidad usada.
# D es la variable de profundidad.
