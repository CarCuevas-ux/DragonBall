document.addEventListener("DOMContentLoaded", () => {
    const contenedorJuego = document.getElementById("contenedor-juego");
    const personaje1 = document.getElementById("personaje1");
    const personaje2 = document.getElementById("personaje2");

    let velocidadPersonaje1 = 5; // Velocidad de movimiento de Personaje1
    let posicionPersonaje1 = 50; // Posición inicial del personaje1 (en porcentaje)
    let posicionPersonaje2 = 50; // Posición inicial del personaje2 (en porcentaje)

    // Movimiento del personaje1
    document.addEventListener("keydown", (event) => {
        if (event.key === "ArrowUp") {
            posicionPersonaje1 -= velocidadPersonaje1;
            if (posicionPersonaje1 < 0) posicionPersonaje1 = 0; // No puede salir por arriba
        } else if (event.key === "ArrowDown") {
            posicionPersonaje1 += velocidadPersonaje1;
            if (posicionPersonaje1 > 90) posicionPersonaje1 = 90; // No puede salir por abajo
        }
        personaje1.style.top = `${posicionPersonaje1}%`;
    });

    // Movimiento automático del personaje2 para perseguir al personaje1
    function moverPersonaje2() {
        const diferencia = posicionPersonaje1 - posicionPersonaje2;

        if (diferencia > 5) {
            posicionPersonaje2 += 2; // Se mueve hacia abajo
        } else if (diferencia < -5) {
            posicionPersonaje2 -= 2; // Se mueve hacia arriba
        }

        personaje2.style.top = `${posicionPersonaje2}%`;
    }
    setInterval(moverPersonaje2, 50); // Ajuste de movimiento suave cada 50ms

    // Función para que personaje2 lance poderes
    function lanzarPoder() {
        const poder = document.createElement("div");
        poder.classList.add("poder");
        poder.style.left = "20%"; // Sale desde la posición de personaje2
        poder.style.top = `${posicionPersonaje2}%`; // La posición de Personaje2
        contenedorJuego.appendChild(poder);

        let posicionPoder = 20; // Posición inicial (en porcentaje)

        const animacion = setInterval(() => {
            posicionPoder += 2; // Velocidad del poder
            poder.style.left = `${posicionPoder}%`;

            // Detectar colisión con personaje1
            const poderRect = poder.getBoundingClientRect();
            const personaje1Rect = personaje1.getBoundingClientRect();

            if (
                poderRect.left < personaje1Rect.right &&
                poderRect.right > personaje1Rect.left &&
                poderRect.top < personaje1Rect.bottom &&
                poderRect.bottom > personaje1Rect.top
            ) {
                clearInterval(animacion);
                poder.remove();
                manejarImpacto(); // Acción cuando el poder impacta al personaje1
            }

            // Eliminar el poder cuando salga de la pantalla
            if (posicionPoder > 100) {
                clearInterval(animacion);
                poder.remove();
            }
        }, 20);
    }

    // Función para manejar el impacto del poder en personaje1
    let golpes = 0;
    function manejarImpacto() {
        golpes++;
        personaje1.style.backgroundColor = golpes === 1 ? "orange" : golpes === 2 ? "red" : "black";
        if (golpes >= 3) {
            alert("¡El personaje1 ha sido derrotado!");
            location.reload(); // Reinicia el juego
        }
    }

    // Generar poderes de forma aleatoria cada 1-3 segundos
    setInterval(() => {
        lanzarPoder();
    }, Math.random() * 2000 + 1000);

    // Funciones para generar nubes y árboles
    function crearNube(id) {
        const nube = document.createElement("img");
        nube.src = `img/nube${id}.png`;
        nube.classList.add("nube");
        nube.style.top = `${Math.random() * 30 + 5}%`;
        nube.style.left = `${Math.random() * 100}%`;
        contenedorJuego.appendChild(nube);
        moverElemento(nube, "nube");
    }

    function crearArbol(id) {
        const arbol = document.createElement("img");
        arbol.src = `img/arbol${id}.png`;
        arbol.classList.add("arbol");
        arbol.style.bottom = "0";
        arbol.style.left = `${Math.random() * 100}%`;
        contenedorJuego.appendChild(arbol);

        const tiempoInicio = Math.random() * 5000; // Diferente tiempo para cada árbol
        setTimeout(() => moverElemento(arbol, "arbol"), tiempoInicio);
    }

    function moverElemento(elemento, tipo) {
        const velocidad = tipo === "nube" ? Math.random() * 10 + 15 : Math.random() * 10 + 20;
        let posicion = 100;

        const animacion = setInterval(() => {
            posicion -= 0.5;
            elemento.style.left = `${posicion}%`;

            if (posicion < -10) {
                posicion = 100;
                if (tipo === "nube") {
                    elemento.style.top = `${Math.random() * 30 + 5}%`;
                }
                elemento.style.left = "100%";
            }
        }, velocidad);
    }

    // Crear nubes y árboles
    for (let i = 1; i <= 4; i++) {
        crearNube(i);
        crearArbol(i);
    }
});
