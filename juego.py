import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de vuelo")

# Cargar imágenes
fondo = pygame.image.load("assets/fondo.png")
nubes = [
    pygame.image.load(f"assets/nube{i + 1}.png") for i in range(4)
]
arboles = [
    pygame.image.load(f"assets/arbol{i + 1}.png") for i in range(4)
]
personaje_principal = pygame.image.load("assets/goku.png")
enemigo = pygame.image.load("assets/taopaipai.png")

# Escalar imágenes
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
personaje_principal = pygame.transform.scale(personaje_principal, (80, 80))
enemigo = pygame.transform.scale(enemigo, (120, 80))
nubes = [pygame.transform.scale(nube, (100, 60)) for nube in nubes]
arboles = [pygame.transform.scale(arbol, (120, 120)) for arbol in arboles]

# Configurar colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Posiciones iniciales
x_personaje = ANCHO - 100
y_personaje = ALTO // 2

x_enemigo = 50
y_enemigo = ALTO // 2

nubes_pos = [[random.randint(0, ANCHO), random.randint(0, ALTO // 2)] for _ in range(3)]
# Generar más árboles y asegurarse de que no se superpongan
arboles_pos = []
for _ in range(6):  # Ahora generamos 6 árboles
    while True:
        # Generamos una posición aleatoria
        x_arbol = random.randint(0, ANCHO)
        # Verificamos si la posición no se superpone con otro árbol
        if all(abs(x_arbol - arbol[0]) > 120 for arbol in arboles_pos):
            arboles_pos.append([x_arbol, ALTO - 120])
            break

# Lista de poderes lanzados por el enemigo
poderes = []

# Velocidades
velocidad_personaje = 8
velocidad_poderes = 7
velocidad_fondo = 2

# Barra de vida
vidas = 3
barra_ancho = 200
barra_alto = 20

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Función para mostrar "Fin del Juego"
def mostrar_fin_del_juego():
    fuente = pygame.font.SysFont(None, 100)
    texto = fuente.render("Fin del Juego", True, ROJO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Bucle principal
while True:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del personaje principal
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and y_personaje > 0:
        y_personaje -= velocidad_personaje
    if teclas[pygame.K_DOWN] and y_personaje < ALTO - personaje_principal.get_height():
        y_personaje += velocidad_personaje

    # El enemigo copia los movimientos del personaje principal
    y_enemigo += (y_personaje - y_enemigo) * 0.1  # Suaviza el movimiento

    # Lanzar poderes desde el enemigo
    if random.randint(1, 50) == 1:  # Lanzar un poder de forma aleatoria
        poderes.append([x_enemigo + 80, y_enemigo + 20])

    # Mover los poderes
    for p in poderes:
        p[0] += velocidad_poderes

    # Eliminar poderes que salen de la pantalla
    poderes = [p for p in poderes if p[0] < ANCHO]

    # Verificar colisiones entre poderes y el personaje principal
    for p in poderes:
        if x_personaje < p[0] < x_personaje + personaje_principal.get_width() and \
            y_personaje < p[1] < y_personaje + personaje_principal.get_height():
            poderes.remove(p)
            vidas -= 1

            # Efecto al ser golpeado
            for _ in range(2):
                ventana.blit(fondo, (0, 0))
                pygame.draw.circle(ventana, ROJO, (x_personaje + 40, y_personaje + 40), 40, 5)
                pygame.display.flip()
                pygame.time.delay(100)

            if vidas == 0:
                mostrar_fin_del_juego()
                pygame.quit()
                sys.exit()

    # Mover el fondo (nubes y árboles)
    for nube_pos in nubes_pos:
        nube_pos[0] -= velocidad_fondo
        if nube_pos[0] < -100:
            nube_pos[0] = ANCHO + random.randint(50, 150)
            nube_pos[1] = random.randint(0, ALTO // 2)

    for arbol_pos in arboles_pos:
        arbol_pos[0] -= velocidad_fondo
        if arbol_pos[0] < -120:
            arbol_pos[0] = ANCHO + random.randint(100, 200)

    # Dibujar todo en pantalla
    ventana.blit(fondo, (0, 0))

    # Dibujar nubes y árboles
    for i, nube_pos in enumerate(nubes_pos):
        ventana.blit(nubes[i % len(nubes)], (nube_pos[0], nube_pos[1]))
    for i, arbol_pos in enumerate(arboles_pos):
        ventana.blit(arboles[i % len(arboles)], (arbol_pos[0], arbol_pos[1]))

    # Dibujar personajes
    ventana.blit(personaje_principal, (x_personaje, y_personaje))
    ventana.blit(enemigo, (x_enemigo, y_enemigo))

    # Dibujar poderes
    for p in poderes:
        pygame.draw.circle(ventana, ROJO, (p[0], p[1]), 10)

    # Nueva posición de la barra de vida (al lado derecho del personaje principal)
    x_barra_vida = x_personaje - barra_ancho - 20  # A 20 píxeles a la izquierda del personaje
    y_barra_vida = 20  # Mantener la posición en el eje Y (en la parte superior)

    # Dibujar barra de vida
    pygame.draw.rect(ventana, NEGRO, (x_barra_vida, y_barra_vida, barra_ancho, barra_alto))  # Fondo de la barra de vida
    pygame.draw.rect(ventana, VERDE, (x_barra_vida, y_barra_vida, barra_ancho * (vidas / 3), barra_alto))  # Barra de vida (verde)

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)  # Limitar a 60 FPS
