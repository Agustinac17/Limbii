import sqlite3
import os
from datetime import datetime

# Ruta de la base de datos (mismo directorio raíz del proyecto)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "limbii.db")


def conectar():
    """Abre una conexión a la base de datos con claves foráneas activadas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # para acceder por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON") # activar integridad referencial
    return conn


def crear_tablas():
    """Crea todas las tablas si no existen."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS perfiles (
        id_perfil         INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre            TEXT    NOT NULL,
        tipo              TEXT    NOT NULL DEFAULT 'menor',
        es_protegido      INTEGER NOT NULL DEFAULT 1,
        creado_en         TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS dispositivos (
        id_dispositivo    INTEGER PRIMARY KEY AUTOINCREMENT,
        direccion_mac     TEXT    NOT NULL UNIQUE,
        direccion_ip      TEXT,
        hostname          TEXT,
        nombre_asignado   TEXT,
        id_perfil         INTEGER,
        prim_vez_visto    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
        ult_vez_visto     TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
        en_linea          INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
    );

    CREATE TABLE IF NOT EXISTS listas_de_dominio (
        id_lista          INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre            TEXT    NOT NULL,
        url_origen        TEXT,
        descripcion       TEXT,
        es_personalizada  INTEGER NOT NULL DEFAULT 0,
        actualizada_en    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS dominios (
        id_dominio        INTEGER PRIMARY KEY AUTOINCREMENT,
        id_lista          INTEGER NOT NULL,
        dominio           TEXT    NOT NULL,
        FOREIGN KEY (id_lista) REFERENCES listas_de_dominio(id_lista)
    );

    CREATE TABLE IF NOT EXISTS politicas (
        id_politica       INTEGER PRIMARY KEY AUTOINCREMENT,
        id_perfil         INTEGER NOT NULL,
        tipo_politica     TEXT    NOT NULL DEFAULT 'filtrado',
        id_lista          INTEGER,
        horario_inicio    TEXT,
        horario_fin       TEXT,
        dias_activos      TEXT    NOT NULL DEFAULT 'lun,mar,mie,jue,vie,sab,dom',
        habilitada        INTEGER NOT NULL DEFAULT 1,
        creada_en         TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil),
        FOREIGN KEY (id_lista) REFERENCES listas_de_dominio(id_lista)
    );

    CREATE TABLE IF NOT EXISTS eventos (
        id_evento         INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_evento       TEXT    NOT NULL,
        id_dispositivo    INTEGER,
        id_perfil         INTEGER,
        descripcion       TEXT    NOT NULL,
        detalle           TEXT,
        creado_en         TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo),
        FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
    );

    """)

    conn.commit()
    conn.close()


def registrar_evento(tipo_evento: str, descripcion: str,
                     id_dispositivo: int = None, id_perfil: int = None,
                     detalle: str = None):
    """Registra un evento en el log del sistema."""
    conn = conectar()
    conn.execute(
        """INSERT INTO eventos (tipo_evento, id_dispositivo, id_perfil, descripcion, detalle)
           VALUES (?, ?, ?, ?, ?)""",
        (tipo_evento, id_dispositivo, id_perfil, descripcion, detalle)
    )
    conn.commit()
    conn.close()


def cargar_datos_iniciales():
    """Carga perfiles y listas por defecto si la base está vacía."""
    conn = conectar()
    cursor = conn.cursor()

    # Solo cargar si no hay perfiles
    cursor.execute("SELECT COUNT(*) FROM perfiles")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Perfiles prueba
    cursor.executemany(
        "INSERT INTO perfiles (nombre, tipo, es_protegido) VALUES (?, ?, ?)",
        [
            ("Adultos",  "adulto", 0),
            ("Casa",     "compartido", 0),
        ]
    )

    # Lista de pureba: redes sociales
    cursor.execute(
        """INSERT INTO listas_de_dominio (nombre, descripcion, es_personalizada)
           VALUES (?, ?, ?)""",
        ("Redes sociales", "Dominios de redes sociales populares", 1)
    )
    id_lista = cursor.lastrowid

    dominios_ejemplo = [
        "facebook.com", "instagram.com", "tiktok.com",
        "twitter.com", "snapchat.com", "reddit.com"
    ]
    cursor.executemany(
        "INSERT INTO dominios (id_lista, dominio) VALUES (?, ?)",
        [(id_lista, d) for d in dominios_ejemplo]
    )

    cursor.execute(
        """INSERT INTO eventos (tipo_evento, descripcion)
           VALUES (?, ?)""",
        ("sistema_iniciado", "Base de datos creada con datos iniciales")
    )

    conn.commit()
    conn.close()


# --- PRUEBA ---
if __name__ == "__main__":
    crear_tablas()
    cargar_datos_iniciales()
    print(f"Base de datos creada en: {DB_PATH}")

    # Verificación rápida
    conn = conectar()
    for tabla in ["perfiles", "dispositivos", "listas_de_dominio",
                  "dominios", "politicas", "eventos"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        print(f"  {tabla}: {count} registros")
    conn.close()