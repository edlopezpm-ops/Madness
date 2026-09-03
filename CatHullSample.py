import FreeCAD as App
import Draft
import Part

try:
    import FreeCADGui as Gui
except Exception:
    Gui = None


doc = App.newDocument("Draft_Catamaran_Hull_Lines")


# =========================
# BASIC CATAMARAN PARAMETERS
# Units: millimeters
# =========================

L = 12000
# Largo total del catamarán: 12 metros.

hull_beam = 1200
# Manga de CADA casco individual.
# No es la manga total del catamarán.

overall_beam = 6000
# Manga total aproximada del catamarán.
# Distancia total de lado exterior a lado exterior.

D = 1200
# Profundidad de cada casco.

stations = 15
# Cantidad de secciones transversales por casco.

hull_spacing = overall_beam - hull_beam
# Distancia entre centros de los dos cascos.
# Si overall_beam = 6000 y hull_beam = 1200,
# entonces los centros quedan separados por 4800 mm.

port_hull_y = -hull_spacing / 2
# Centro del casco de babor.
# Y negativo = lado izquierdo.

starboard_hull_y = hull_spacing / 2
# Centro del casco de estribor.
# Y positivo = lado derecho.


# =========================
# VISUAL STYLE FUNCTION
# =========================

def style(obj, color=(0.2, 0.45, 0.9), width=2):
    if Gui is not None and getattr(obj, "ViewObject", None) is not None:
        obj.ViewObject.LineColor = color
        obj.ViewObject.LineWidth = width
    return obj


# =========================
# HULL SHAPE FUNCTIONS
# =========================

def beam_at(x):
    """
    Manga local de cada casco individual.
    Más delgado en proa/popa, más ancho al centro.
    """
    t = x / L
    return hull_beam * (0.10 + 0.90 * (1 - (2*t - 1)**2))


def depth_at(x):
    """
    Profundidad local de cada casco.
    Menos profundo en extremos, más profundo al centro.
    """
    t = x / L
    return D * (0.40 + 0.60 * (1 - (2*t - 1)**2))


def z_keel(x):
    """
    Línea de quilla / rocker de cada casco.
    Z negativo significa hacia abajo.
    """
    t = x / L
    return -depth_at(x) * (0.70 + 0.30 * (1 - abs(2*t - 1)))


# =========================
# FUNCTION TO CREATE ONE HULL
# =========================

def create_single_hull(center_y, name_prefix):
    """
    Crea las líneas de UN casco.
    Luego llamamos esta función dos veces:
    una para babor y otra para estribor.
    """

    station_curves = []

    keel_pts = []
    port_sheer_pts = []
    starboard_sheer_pts = []
    port_chine_pts = []
    starboard_chine_pts = []

    for i in range(stations):
        x = L * i / (stations - 1)

        half_beam = beam_at(x) / 2
        depth = depth_at(x)
        keel_z = z_keel(x)

        # =========================
        # CROSS SECTION POINTS
        # =========================
        # Esta sección crea una costilla transversal del casco.
        # La diferencia con el monohull es que todo está desplazado
        # alrededor de center_y.

        pts = [
            App.Vector(x, center_y - half_beam, 0),
            App.Vector(x, center_y - half_beam * 0.80, -depth * 0.20),
            App.Vector(x, center_y - half_beam * 0.40, -depth * 0.70),
            App.Vector(x, center_y, keel_z),
            App.Vector(x, center_y + half_beam * 0.40, -depth * 0.70),
            App.Vector(x, center_y + half_beam * 0.80, -depth * 0.20),
            App.Vector(x, center_y + half_beam, 0),
        ]

        curve = Draft.make_bspline(pts, closed=False, face=False)
        curve.Label = "%s_Station_%02d" % (name_prefix, i)
        style(curve, (0.1, 0.4, 1.0), 2)
        station_curves.append(curve)

        # =========================
        # LONGITUDINAL GUIDE POINTS
        # =========================

        keel_pts.append(App.Vector(x, center_y, keel_z))

        port_sheer_pts.append(App.Vector(x, center_y - half_beam, 0))

        starboard_sheer_pts.append(App.Vector(x, center_y + half_beam, 0))

        port_chine_pts.append(App.Vector(x, center_y - half_beam * 0.50, -depth * 0.65))

        starboard_chine_pts.append(App.Vector(x, center_y + half_beam * 0.50, -depth * 0.65))

    # =========================
    # CREATE LONGITUDINAL CURVES
    # =========================

    keel = Draft.make_bspline(keel_pts, closed=False, face=False)
    keel.Label = "%s_Keel_Line" % name_prefix
    style(keel, (1.0, 0.1, 0.1), 4)

    port_sheer = Draft.make_bspline(port_sheer_pts, closed=False, face=False)
    port_sheer.Label = "%s_Port_Sheer_Line" % name_prefix
    style(port_sheer, (0.0, 0.7, 0.2), 3)

    starboard_sheer = Draft.make_bspline(starboard_sheer_pts, closed=False, face=False)
    starboard_sheer.Label = "%s_Starboard_Sheer_Line" % name_prefix
    style(starboard_sheer, (0.0, 0.7, 0.2), 3)

    port_chine = Draft.make_bspline(port_chine_pts, closed=False, face=False)
    port_chine.Label = "%s_Port_Chine_Guide" % name_prefix
    style(port_chine, (0.9, 0.6, 0.0), 2)

    starboard_chine = Draft.make_bspline(starboard_chine_pts, closed=False, face=False)
    starboard_chine.Label = "%s_Starboard_Chine_Guide" % name_prefix
    style(starboard_chine, (0.9, 0.6, 0.0), 2)

    return station_curves


# =========================
# CREATE BOTH CATAMARAN HULLS
# =========================

port_hull = create_single_hull(port_hull_y, "Port_Hull")

starboard_hull = create_single_hull(starboard_hull_y, "Starboard_Hull")


# =========================
# OPTIONAL DECK / BRIDGE GUIDE LINES
# These are only visual reference lines
# =========================

deck_z = 500
# Altura visual del puente/cubierta sobre los cascos.

bridge_station_indexes = [3, 7, 11]
# Estaciones donde dibujaremos líneas transversales entre ambos cascos.

for idx in bridge_station_indexes:
    x = L * idx / (stations - 1)

    bridge_pts = [
        App.Vector(x, port_hull_y, deck_z),
        App.Vector(x, starboard_hull_y, deck_z),
    ]

    bridge_line = Draft.make_bspline(bridge_pts, closed=False, face=False)
    bridge_line.Label = "Bridge_Deck_Guide_%02d" % idx
    style(bridge_line, (0.8, 0.2, 0.8), 2)


# =========================
# CENTERLINE REFERENCE
# =========================

centerline_pts = [
    App.Vector(0, 0, deck_z),
    App.Vector(L, 0, deck_z),
]

centerline = Draft.make_bspline(centerline_pts, closed=False, face=False)
centerline.Label = "Catamaran_Centerline_Reference"
style(centerline, (0.5, 0.5, 0.5), 1)


# =========================
# UPDATE DOCUMENT AND VIEW
# =========================

doc.recompute()

if Gui is not None and getattr(Gui, "ActiveDocument", None) is not None:
    Gui.ActiveDocument.ActiveView.viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")


print("Draft catamaran hull lines created.")
print("Length:", L, "mm")
print("Single hull beam:", hull_beam, "mm")
print("Overall beam:", overall_beam, "mm")
print("Hull depth:", D, "mm")
print("Stations per hull:", stations)
