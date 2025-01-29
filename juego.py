import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego
ANCHO, ALTO = 800, 600  # Dimensiones de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tao Pai Pai Vs Goku")  # Título de la ventana

# Cargar imágenes del juego
fondo = pygame.image.load("assets/fondo.png")  # Imagen de fondo
nubes = [pygame.image.load(f"assets/nube{i + 1}.png") for i in range(4)]  # Imágenes de nubes
arboles = [pygame.image.load(f"assets/arbol{i + 1}.png") for i in range(12)]  # Imágenes de 12 árboles
personaje_principal = pygame.image.load("assets/goku.png")  # Imagen de Goku
enemigo = pygame.image.load("assets/taopaipai.png")  # Imagen de Tao pai pai

# Escalar imágenes para que encajen bien en el juego
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajustar el fondo al tamaño de la ventana
personaje_principal = pygame.transform.scale(personaje_principal, (80, 80))  # Escalar a Goku
enemigo = pygame.transform.scale(enemigo, (120, 80))  # Escalar a Tao pai pai
nubes = [pygame.transform.scale(nube, (100, 60)) for nube in nubes]  # Escalar nubes
arboles = [pygame.transform.scale(arbol, (120, 120)) for arbol in arboles]  # Escalar árboles

# Definir colores (en formato RGB)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Posiciones iniciales de los personajes
x_personaje = ANCHO - 100  # Posición inicial de Goku (derecha)
y_personaje = ALTO // 2  # Centrado verticalmente

x_enemigo = 50  # Posición inicial de Tao pai pai (izquierda)
y_enemigo = ALTO // 2  # Centrado verticalmente

# Posiciones iniciales de las nubes (al azar)
nubes_pos = [[random.randint(0, ANCHO), random.randint(0, ALTO // 2)] for _ in range(3)]

# Posiciones iniciales de los árboles (distribuidos uniformemente para evitar superposición)
arboles_pos = [[ANCHO + i * 150, ALTO - 120] for i in range(12)]

# Lista para almacenar los poderes que lanza Tao pai pai
poderes = []

# Configuración de velocidades
velocidad_personaje = 8  # Velocidad de movimiento de Goku
velocidad_poderes = 7  # Velocidad a la que se mueven los poderes
velocidad_fondo = 2  # Velocidad de desplazamiento de nubes
velocidad_arboles = 4  # Velocidad de desplazamiento de los árboles (más rápida)

# Configuración de la barra de vida
vidas = 3  # Vidas iniciales del personaje principal
barra_ancho = 200  # Ancho de la barra de vida
barra_alto = 20  # Alto de la barra de vida

# Controlador de FPS
reloj = pygame.time.Clock()

# Función para mostrar el mensaje "game over" cuando las vidas se acaben
def mostrar_fin_del_juego():
    fuente = pygame.font.SysFont(None, 100)  # Fuente de texto
    texto = fuente.render("GAME OVER", True, ROJO)  # Generar el texto
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))  # Centrarlo
    pygame.display.flip()  # Actualizar la pantalla para mostrar el mensaje
    pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar el juego

# Bucle principal del juego
while True:
    # Manejo de eventos (teclas y cierre de ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Si el jugador cierra la ventana
            pygame.quit()
            sys.exit()

    # Movimiento del personaje principal con teclas
    teclas = pygame.key.get_pressed()  # Detectar teclas presionadas
    if teclas[pygame.K_UP] and y_personaje > 0:  # Mover hacia arriba
        y_personaje -= velocidad_personaje
    if teclas[pygame.K_DOWN] and y_personaje < ALTO - personaje_principal.get_height():  # Mover hacia abajo
        y_personaje += velocidad_personaje

    # Movimiento del enemigo (sigue a goku)
    y_enemigo += (y_personaje - y_enemigo) * 0.1  # Movimiento suave hacia gaku

    # Lógica para lanzar poderes desde el enemigo
    if random.randint(1, 50) == 1:  # Probabilidad de lanzar un poder
        poderes.append([x_enemigo + 80, y_enemigo + 20])  # Añadir poder a la lista

    # Movimiento de los poderes
    for p in poderes:
        p[0] += velocidad_poderes  # Mover los poderes hacia la derecha

    # Eliminar poderes que salgan de la pantalla
    poderes = [p for p in poderes if p[0] < ANCHO]

    # Verificar colisiones entre poderes y goku
    for p in poderes:
        if x_personaje < p[0] < x_personaje + personaje_principal.get_width() and \
            y_personaje < p[1] < y_personaje + personaje_principal.get_height():
            poderes.remove(p)  # Eliminar el poder
            vidas -= 1  # Restar una vida

            # Mostrar efecto visual cuando el personaje es golpeado
            for _ in range(2):
                ventana.blit(fondo, (0, 0))
                pygame.draw.circle(ventana, ROJO, (x_personaje + 40, y_personaje + 40), 40, 5)
                pygame.display.flip()
                pygame.time.delay(100)

            if vidas == 0:  # Si las vidas llegan a 0, termina el juego
                mostrar_fin_del_juego()
                pygame.quit()
                sys.exit()

    # Movimiento del fondo (nubes)
    for nube_pos in nubes_pos:
        nube_pos[0] -= velocidad_fondo  # Mover nubes hacia la izquierda
        if nube_pos[0] < -100:  # Si salen de la pantalla, reaparecen al final
            nube_pos[0] = ANCHO + random.randint(50, 150)
            nube_pos[1] = random.randint(0, ALTO // 2)

    # Movimiento de los árboles
    for arbol_pos in arboles_pos:
        arbol_pos[0] -= velocidad_arboles  # Mover árboles hacia la izquierda
        if arbol_pos[0] < -120:  # Si salen de la pantalla, reaparecen al final
            arbol_pos[0] = ANCHO + random.randint(100, 200)

    # Dibujar todo en la pantalla
    ventana.blit(fondo, (0, 0))  # Dibujar el fondo

    # Dibujar nubes
    for i, nube_pos in enumerate(nubes_pos):
        ventana.blit(nubes[i % len(nubes)], (nube_pos[0], nube_pos[1]))

    # Dibujar árboles
    for i, arbol_pos in enumerate(arboles_pos):
        ventana.blit(arboles[i % len(arboles)], (arbol_pos[0], arbol_pos[1]))

    # Dibujar personajes
    ventana.blit(personaje_principal, (x_personaje, y_personaje))  # Personaje principal (goku)
    ventana.blit(enemigo, (x_enemigo, y_enemigo))  # Enemigo (tao pai pai)

    # Dibujar poderes
    for p in poderes:
        pygame.draw.circle(ventana, ROJO, (p[0], p[1]), 10)  # Dibujar los poderes como círculos

    # Dibujar barra de vida (al lado derecho del personaje principal)
    x_barra_vida = x_personaje - barra_ancho - 20  # Posición X de la barra
    y_barra_vida = 20  # Posición Y de la barra
    pygame.draw.rect(ventana, NEGRO, (x_barra_vida, y_barra_vida, barra_ancho, barra_alto))  # Fondo negro
    pygame.draw.rect(ventana, VERDE, (x_barra_vida, y_barra_vida, barra_ancho * (vidas / 3), barra_alto))  # Barra verde

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)  # Limitar a 60 FPS
