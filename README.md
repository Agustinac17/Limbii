# Limbii

Limbii es un prototipo web pensado para representar una plataforma simple de administración de una red doméstica.

La propuesta busca mostrar de una manera visual cómo una persona podría consultar qué dispositivos están conectados, organizarlos por perfiles, definir reglas de uso, pausar temporalmente el acceso a Internet y revisar eventos básicos de la red.

Este repositorio contiene una primera versión del prototipo desarrollada con HTML, CSS y JavaScript. Su objetivo es representar la experiencia de uso y los principales flujos de la plataforma.

Actualmente no realiza cambios reales sobre una red ni se conecta con dispositivos físicos. Las acciones, estados y datos que aparecen en pantalla son simulados para poder mostrar el funcionamiento esperado del sistema.

## Cómo abrir el prototipo

No es necesario instalar dependencias ni configurar un servidor.

1. Descargar o clonar este repositorio.
2. Abrir la carpeta `prototipo`.
3. Hacer doble clic sobre `index.html`.

El prototipo se abrirá directamente en el navegador.

También puede abrirse desde Chrome, Edge o Firefox.

## Qué se puede probar

Dentro del prototipo se pueden recorrer distintas secciones:

- Inicio y estado general de la red.
- Dispositivos conectados.
- Perfiles de usuarios.
- Reglas de acceso.
- Registro de actividad.
- Configuración general.

Algunas acciones, como pausar un dispositivo, activar reglas o crear una nueva regla, funcionan de manera simulada para facilitar la navegación del prototipo.

## Estructura

```text
prototipo/
├── index.html
├── estilos.css
└── script.js