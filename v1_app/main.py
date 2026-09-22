# ---SERVIDOOOR---

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

from v1_app.database import crear_tablas, cargar_datos_iniciales, conectar

# --- Inicialización ---
app = FastAPI(title="Limbii", version="1.0.0")

# Templates HTML (Jinja2)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Archivos estáticos (CSS, JS, imágenes)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# --- Ev Arranque ---
@app.on_event("startup")
def al_iniciar():
    """Crea las tablas y carga datos iniciales si la base está vacía."""
    crear_tablas()
    cargar_datos_iniciales()


# --- Páginas principales ---
@app.get("/", response_class=HTMLResponse)
def pagina_inicio(request: Request):
    """Dashboard principal."""
    conn = conectar()

    # Datos para el panel
    total_dispositivos = conn.execute(
        "SELECT COUNT(*) FROM dispositivos"
    ).fetchone()[0]

    en_linea = conn.execute(
        "SELECT COUNT(*) FROM dispositivos WHERE en_linea = 1"
    ).fetchone()[0]

    total_perfiles = conn.execute(
        "SELECT COUNT(*) FROM perfiles"
    ).fetchone()[0]

    total_politicas = conn.execute(
        "SELECT COUNT(*) FROM politicas WHERE habilitada = 1"
    ).fetchone()[0]

    ultimos_eventos = conn.execute(
        """SELECT tipo_evento, descripcion, creado_en
           FROM eventos ORDER BY creado_en DESC LIMIT 5"""
    ).fetchall()

    dispositivos = conn.execute(
        """SELECT d.nombre_asignado, d.hostname, d.direccion_ip,
                  d.en_linea, p.nombre as perfil_nombre
           FROM dispositivos d
           LEFT JOIN perfiles p ON d.id_perfil = p.id_perfil
           ORDER BY d.en_linea DESC, d.ult_vez_visto DESC"""
    ).fetchall()

    conn.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_dispositivos": total_dispositivos,
        "en_linea": en_linea,
        "total_perfiles": total_perfiles,
        "total_politicas": total_politicas,
        "ultimos_eventos": ultimos_eventos,
        "dispositivos": dispositivos,
    })


@app.get("/dispositivos", response_class=HTMLResponse)
def pagina_dispositivos(request: Request):
    """Lista de dispositivos detectados."""
    conn = conectar()
    dispositivos = conn.execute(
        """SELECT d.*, p.nombre as perfil_nombre
           FROM dispositivos d
           LEFT JOIN perfiles p ON d.id_perfil = p.id_perfil
           ORDER BY d.en_linea DESC, d.ult_vez_visto DESC"""
    ).fetchall()
    perfiles = conn.execute("SELECT * FROM perfiles").fetchall()
    conn.close()

    return templates.TemplateResponse("dispositivos.html", {
        "request": request,
        "dispositivos": dispositivos,
        "perfiles": perfiles,
    })


@app.get("/perfiles", response_class=HTMLResponse)
def pagina_perfiles(request: Request):
    """Gestión de perfiles."""
    conn = conectar()
    perfiles = conn.execute(
        """SELECT p.*,
                  (SELECT COUNT(*) FROM dispositivos d WHERE d.id_perfil = p.id_perfil) as cant_dispositivos,
                  (SELECT COUNT(*) FROM politicas pol WHERE pol.id_perfil = p.id_perfil AND pol.habilitada = 1) as cant_politicas
           FROM perfiles p ORDER BY p.creado_en"""
    ).fetchall()
    conn.close()

    return templates.TemplateResponse("perfiles.html", {
        "request": request,
        "perfiles": perfiles,
    })


@app.get("/actividad", response_class=HTMLResponse)
def pagina_actividad(request: Request):
    """Log de eventos del sistema."""
    conn = conectar()
    eventos = conn.execute(
        """SELECT e.*, d.nombre_asignado as dispositivo_nombre, p.nombre as perfil_nombre
           FROM eventos e
           LEFT JOIN dispositivos d ON e.id_dispositivo = d.id_dispositivo
           LEFT JOIN perfiles p ON e.id_perfil = p.id_perfil
           ORDER BY e.creado_en DESC LIMIT 100"""
    ).fetchall()
    conn.close()

    return templates.TemplateResponse("actividad.html", {
        "request": request,
        "eventos": eventos,
    })


# --- API para acciones ---
@app.post("/api/perfiles")
def crear_perfil(request: Request, nombre: str, tipo: str = "menor", es_protegido: bool = True):
    """Crea un perfil nuevo."""
    from v1_app.database import registrar_evento
    conn = conectar()
    cursor = conn.execute(
        "INSERT INTO perfiles (nombre, tipo, es_protegido) VALUES (?, ?, ?)",
        (nombre, tipo, 1 if es_protegido else 0)
    )
    id_nuevo = cursor.lastrowid
    conn.commit()
    conn.close()

    registrar_evento("perfil_creado", f"Se creó el perfil '{nombre}'", id_perfil=id_nuevo)
    return {"ok": True, "id_perfil": id_nuevo}


@app.post("/api/dispositivos/{id_dispositivo}/asignar")
def asignar_dispositivo(id_dispositivo: int, id_perfil: int):
    """Asigna un dispositivo a un perfil."""
    from v1_app.database import registrar_evento
    conn = conectar()
    conn.execute(
        "UPDATE dispositivos SET id_perfil = ? WHERE id_dispositivo = ?",
        (id_perfil, id_dispositivo)
    )
    conn.commit()
    conn.close()

    registrar_evento(
        "dispositivo_asignado",
        f"Dispositivo {id_dispositivo} asignado a perfil {id_perfil}",
        id_dispositivo=id_dispositivo,
        id_perfil=id_perfil
    )
    return {"ok": True}


# --- Pto entrada ---
if __name__ == "__main__":
    uvicorn.run("v1_app.main:app", host="0.0.0.0", port=8000, reload=True)
