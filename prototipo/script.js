/* Limbii */

document.addEventListener("DOMContentLoaded", () => {

    const menuItems = document.querySelectorAll(".menu-item");
    const secciones = document.querySelectorAll(".seccion");
    const enlacesInternos = document.querySelectorAll("[data-ir]");

    const notificacion = document.getElementById("notificacion");

    const botonPausarInternet = document.getElementById("botonPausarInternet");

    const botonesPausa = document.querySelectorAll(".boton-pausa");

    const buscarDispositivo = document.getElementById("buscarDispositivo");
    const dispositivosBuscables = document.querySelectorAll(".dispositivo-buscable");

    const modalRegla = document.getElementById("modalRegla");
    const nuevaRegla = document.getElementById("nuevaRegla");
    const cerrarModal = document.getElementById("cerrarModal");
    const cancelarModal = document.getElementById("cancelarModal");
    const formRegla = document.getElementById("formRegla");

    let internetPausado = false;


    /* NAV */

    function mostrarSeccion(idSeccion) {

        secciones.forEach((seccion) => {
            seccion.classList.remove("activa");
        });

        menuItems.forEach((item) => {
            item.classList.remove("activo");
        });

        const seccionSeleccionada = document.getElementById(idSeccion);

        if (seccionSeleccionada) {
            seccionSeleccionada.classList.add("activa");
        }

        const menuSeleccionado = document.querySelector(
            `.menu-item[data-seccion="${idSeccion}"]`
        );

        if (menuSeleccionado) {
            menuSeleccionado.classList.add("activo");
        }

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }


    menuItems.forEach((item) => {

        item.addEventListener("click", () => {

            const seccion = item.dataset.seccion;

            mostrarSeccion(seccion);

        });

    });


    enlacesInternos.forEach((enlace) => {

        enlace.addEventListener("click", () => {

            const destino = enlace.dataset.ir;

            mostrarSeccion(destino);

        });

    });


    /* NOTIF */

    function mostrarNotificacion(mensaje) {

        notificacion.textContent = mensaje;
        notificacion.classList.add("visible");

        setTimeout(() => {

            notificacion.classList.remove("visible");

        }, 2500);

    }


    /* PAUSAR INTERNET GENERAL */

    botonPausarInternet.addEventListener("click", () => {

        internetPausado = !internetPausado;

        const estadoSistema = document.querySelector(".estado-sistema");
        const puntoEstado = estadoSistema.querySelector(".estado-punto");

        const estadoRedTitulo = document.querySelector(".estado-red h3");
        const estadoRedTexto = document.querySelector(".estado-red p");

        const estadoConexion = document.querySelector(".estado-red-dato strong");


        if (internetPausado) {

            botonPausarInternet.textContent = "Reanudar Internet";

            estadoSistema.childNodes[2].textContent = " Internet pausado";

            puntoEstado.style.background = "#b86b6b";

            estadoRedTitulo.textContent = "Internet está pausado";

            estadoRedTexto.textContent =
                "El acceso a Internet fue detenido temporalmente para los dispositivos de la casa.";

            estadoConexion.textContent = "Pausada";

            mostrarNotificacion("Internet pausado temporalmente");

        } else {

            botonPausarInternet.textContent = "Pausar Internet";

            estadoSistema.childNodes[2].textContent = " Sistema activo";

            puntoEstado.style.background = "";

            estadoRedTitulo.textContent = "Tu casa está conectada";

            estadoRedTexto.textContent =
                "8 dispositivos están usando Internet en este momento. No se detectaron problemas.";

            estadoConexion.textContent = "Activa";

            mostrarNotificacion("Internet reanudado");

        }

    });


    /* PAUSAR DISPOSITIVOS */

    botonesPausa.forEach((boton) => {

        if (boton.disabled) {
            return;
        }

        boton.addEventListener("click", () => {

            const fila = boton.closest(".tabla-fila");

            const nombreDispositivo =
                fila.querySelector("strong").textContent;

            const estado =
                fila.querySelector(".estado-en-linea, .estado-desconectado");


            if (boton.classList.contains("pausado")) {

                boton.classList.remove("pausado");

                boton.textContent = "Pausar";

                estado.textContent = "En línea";
                estado.className = "estado-en-linea";

                mostrarNotificacion(
                    `${nombreDispositivo}: acceso restaurado`
                );

            } else {

                boton.classList.add("pausado");

                boton.textContent = "Reanudar";

                estado.textContent = "Pausado";
                estado.className = "estado-desconectado";

                mostrarNotificacion(
                    `${nombreDispositivo}: acceso pausado`
                );

            }

        });

    });


    /* BUSCADOR DE DISP */

    buscarDispositivo.addEventListener("input", () => {

        const busqueda =
            buscarDispositivo.value.toLowerCase().trim();


        dispositivosBuscables.forEach((dispositivo) => {

            const texto =
                dispositivo.textContent.toLowerCase();


            if (texto.includes(busqueda)) {

                dispositivo.style.display = "";

            } else {

                dispositivo.style.display = "none";

            }

        });

    });


    /* MODAL NUEVA REGLA */

    function abrirModal() {

        modalRegla.classList.add("visible");

    }


    function cerrarModalRegla() {

        modalRegla.classList.remove("visible");

    }


    nuevaRegla.addEventListener("click", abrirModal);

    cerrarModal.addEventListener("click", cerrarModalRegla);

    cancelarModal.addEventListener("click", cerrarModalRegla);


    modalRegla.addEventListener("click", (evento) => {

        if (evento.target === modalRegla) {

            cerrarModalRegla();

        }

    });


    /* CREAR REGLA */

    formRegla.addEventListener("submit", (evento) => {

        evento.preventDefault();

        const nombre = formRegla.querySelector(
            'input[type="text"]'
        ).value;

        const selects = formRegla.querySelectorAll("select");

        const perfil = selects[0].value;
        const tipo = selects[1].value;

        const panelReglas = document.querySelector(
            "#reglas .panel"
        );


        const nuevaReglaElemento =
            document.createElement("div");

        nuevaReglaElemento.classList.add("regla");


        nuevaReglaElemento.innerHTML = `
            <div>
                <span class="regla-tipo">
                    ${tipo.toUpperCase()}
                </span>

                <h3>${nombre}</h3>

                <p>
                    ${perfil} · Regla creada desde el prototipo.
                </p>
            </div>

            <label class="interruptor">
                <input type="checkbox" checked>
                <span></span>
            </label>
        `;


        panelReglas.appendChild(nuevaReglaElemento);

        formRegla.reset();

        cerrarModalRegla();

        mostrarNotificacion("Nueva regla creada");

    });


    /* INTERRUPTORES */

    const interruptores =
        document.querySelectorAll(".interruptor input");


    interruptores.forEach((interruptor) => {

        interruptor.addEventListener("change", () => {

            if (interruptor.checked) {

                mostrarNotificacion("Configuración activada");

            } else {

                mostrarNotificacion("Configuración desactivada");

            }

        });

    });


    /* BOTONES*/

    const botonesPrincipales =
        document.querySelectorAll(".boton-principal");


    botonesPrincipales.forEach((boton) => {

        const texto =
            boton.textContent.trim().toLowerCase();


        if (texto === "agregar dispositivo") {

            boton.addEventListener("click", () => {

                mostrarNotificacion(
                    "Función representada en el prototipo"
                );

            });

        }


        if (texto === "crear perfil") {

            boton.addEventListener("click", () => {

                mostrarNotificacion(
                    "Creación de perfiles simulada"
                );

            });

        }

    });


    const botonesAdministrar =
        document.querySelectorAll(".perfil .boton-secundario");


    botonesAdministrar.forEach((boton) => {

        boton.addEventListener("click", () => {

            const perfil =
                boton.closest(".perfil").querySelector("h3").textContent;

            mostrarNotificacion(
                `Administración del perfil ${perfil}`
            );

        });

    });


    /* MENSAJE */

    console.log(
        "Limbii - Prototipo académico v0"
    );

    console.log(
        "Los datos y acciones representados son simulados."
    );

});