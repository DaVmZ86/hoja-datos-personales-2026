"""Genera la plantilla PDF (tamaño carta, con campos rellenables) y el archivo
js/plantilla-data.js que la incrusta en base64 para que la app funcione
incluso abriendo index.html directamente, sin servidor.

Uso:  pip install reportlab   ->   python tools/generar_plantilla.py
"""
import base64
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parent.parent
OUT = str(ROOT / "assets" / "plantilla.pdf")
LOGO = str(ROOT / "assets" / "logo-imss.png")
JS_OUT = ROOT / "js" / "plantilla-data.js"
W, H = letter  # 612 x 792

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("Hoja de Datos Personales - IMSS")
form = c.acroForm

REG, BOLD, BI = "Helvetica", "Helvetica-Bold", "Helvetica-BoldOblique"
LBL = 7.2   # tamaño de etiquetas
SUB = 6.6   # tamaño de subetiquetas


def Y(t):  # coordenada desde arriba
    return H - t


def label(x, t, text, font=REG, size=LBL):
    c.setFont(font, size)
    c.drawString(x, Y(t), text)


def line(x0, x1, t, name=None, sub=None):
    c.setLineWidth(0.6)
    c.line(x0, Y(t) - 1, x1, Y(t) - 1)
    if sub:
        c.setFont(REG, SUB)
        c.drawCentredString((x0 + x1) / 2, Y(t) - 9, sub)
    if name:
        form.textfield(name=name, x=x0 + 1, y=Y(t), width=x1 - x0 - 2, height=11,
                       borderWidth=0, fillColor=colors.white, textColor=colors.black,
                       fontName=REG, fontSize=8.5, forceBorder=False)


# ---- Marco ----
c.setLineWidth(1.3)
c.rect(36, Y(774), 540, 774 - 38)

# ---- Encabezado ----
c.drawImage(LOGO, 52, Y(93), width=40.4, height=50, mask='auto')
label(108, 78, "DIRECCIÓN DE ADMINISTRACIÓN", BOLD, 7)
c.setFont(BOLD, 7.5)
c.drawRightString(556, Y(70), "HOJA DE DATOS PERSONALES")
label(108, 100, "OOAD", BOLD, 7)
line(150, 400, 100, "ooad")

# ---- Datos generales ----
t = 136
label(52, t, "NOMBRE")
line(130, 266, t, "ap_paterno", "APELLIDO PATERNO")
line(272, 412, t, "ap_materno", "APELLIDO MATERNO")
line(418, 556, t, "nombres", "NOMBRE (S)")

t += 28
label(52, t, "MATRÍCULA")
line(130, 266, t, "matricula")
label(276, t, "CATEGORÍA")
line(326, 556, t, "categoria")

t += 24
label(52, t, "E-MAIL PARTICULAR")
line(150, 556, t, "email_particular")

t += 24
label(52, t, "E-MAIL INSTITUCIONAL")
line(150, 556, t, "email_institucional")

t += 24
label(52, t, "ESCOLARIDAD")
line(130, 380, t, "escolaridad")
label(392, t, "ESTADO CIVIL")
line(446, 556, t, "estado_civil")

t += 24
label(52, t, "LUGAR DE NACIMIENTO")
line(150, 278, t, "nac_pais", "PAÍS")
line(286, 420, t, "nac_estado", "ESTADO")
line(428, 556, t, "nac_ciudad", "CIUDAD")

t += 28
label(52, t, "ADSCRIPCIÓN")
line(130, 380, t, "adscripcion")
label(392, t, "TURNO")
line(446, 556, t, "turno")

# ---- Domicilio particular ----
t += 40
label(52, t, "DOMICILIO PARTICULAR:", BOLD, 7.5)

t += 30
label(52, t, "CALLE")
line(100, 296, t, "calle")
label(306, t, "NÚMERO EXT")
line(362, 430, t, "num_ext")
label(442, t, "NÚMERO INT")
line(494, 556, t, "num_int")

t += 30
label(52, t, "COLONIA")
line(100, 250, t, "colonia")
label(296, t, "ALCALDÍA")
line(362, 556, t, "alcaldia")

t += 30
label(52, t, "ESTADO")
line(100, 196, t, "dom_estado")
label(202, t, "CIUDAD")
line(236, 376, t, "dom_ciudad")
label(394, t, "POBLACIÓN")
line(446, 556, t, "poblacion")

t += 30
label(52, t, "C.P.")
line(100, 186, t, "cp")
label(236, t, "TELÉFONO (S)")
line(296, 556, t, "telefonos")

t += 32
label(52, t, "U.M.F.")
line(100, 376, t, "umf", "DONDE RECIBE ATENCION MEDICA")
label(394, t, "NÚMERO DE CONSULTORIO")
line(500, 556, t, "consultorio")

# ---- Contacto de emergencia ----
t += 44
label(52, t, "EN CASO DE ACCIDENTE FAVOR DE AVISAR A:", BOLD, 7.5)

t += 28
label(52, t, "NOMBRE (S)")
line(120, 556, t, "emerg_nombre")

t += 26
label(52, t, "PARENTESCO")
line(120, 320, t, "emerg_parentesco")
label(336, t, "TELÉFONO (S)")
line(398, 556, t, "emerg_telefono")

# ---- Leyenda de compromiso ----
t += 46
c.setFont(BI, 7)
for i, s in enumerate([
    "ME COMPROMETO A INFORMAR CUALQUIER CAMBIO DE LOS DATOS ANTES MENCIONADOS, ESTANDO DE",
    "ACUERDO QUE PUEDEN SER VERIFICADOS, CONOCIENDO LA SANCIÓN ADMINISTRATIVAS EN CASO DE",
    "PROPORCIONAR DATOS FALSOS",
]):
    c.drawCentredString(W / 2, Y(t + i * 10), s)

# ---- Firma ----
t = 728
c.setLineWidth(0.6)
c.line(180, Y(t), 432, Y(t))
c.setFont(BOLD, 7.5)
c.drawCentredString(W / 2, Y(t + 11), "FIRMA DE LA TRABAJADORA/TRABAJADOR")

# ---- Nota y clave ----
c.setFont(BI, 6.2)
c.drawString(44, Y(767),
             "NOTA: SE DEBE ADJUNTAR COPIA DE CREDENCIAL DE ELECTOR, COMPROBANTE DE DOMICILIO Y COMPROBANTE DE ESCOLARIDAD")
c.setFont(REG, 7)
c.drawRightString(576, Y(784), "Clave: 1A74-009-120")

c.showPage()
c.save()
b64 = base64.b64encode(Path(OUT).read_bytes()).decode("ascii")
JS_OUT.write_text(
    "// Archivo generado por tools/generar_plantilla.py. No editar a mano.\n"
    f'window.PLANTILLA_PDF_B64 = "{b64}";\n', encoding="utf-8")
print("Plantilla generada:", OUT)
print("Datos JS generados:", JS_OUT)
