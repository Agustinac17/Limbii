# Limbii

Limbii es un proyecto orientado a facilitar la administración de una red doméstica desde una interfaz simple y centralizada.

La propuesta busca representar cómo una persona puede consultar los dispositivos conectados, organizarlos por perfiles, definir reglas de uso, pausar accesos y revisar eventos básicos de la red.

Este repositorio reúne el prototipo, la documentación de trabajo, el relevamiento, los análisis realizados y las entregas correspondientes al Proyecto Integrador Final.

## Prototipo

El prototipo fue desarrollado con HTML, CSS y JavaScript.

Actualmente funciona como una maqueta navegable con datos simulados. No realiza cambios reales sobre una red ni se conecta con dispositivos físicos.

Permite recorrer las principales secciones previstas para Limbii:

- Inicio
- Dispositivos
- Perfiles
- Reglas
- Actividad
- Configuración

También incluye algunas interacciones simuladas, como pausar dispositivos, activar o desactivar reglas y crear nuevas reglas.

## Cómo abrir el prototipo

No es necesario instalar dependencias ni configurar un servidor.

1. Descargar o clonar este repositorio.
2. Abrir la carpeta `src/prototipo`.
3. Hacer doble clic sobre el archivo `index.html`.

El prototipo se abrirá directamente en el navegador.

Puede utilizarse con Chrome, Edge o Firefox.

## Estructura del repositorio

```text
Limbii/
├── 00-gestion/
├── 01-relevamiento/
├── 02-analisis/
├── 03-requisitos/
├── 04-diseno/
├── 05-entregas/
├── src/
│   └── prototipo/
│       ├── index.html
│       ├── estilos.css
│       └── script.js
└── README.md