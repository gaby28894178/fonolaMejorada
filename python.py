import pygame
import os
import sys
import random
import time  # Agregado

# Inicializar Pygame y su mixer
pygame.init()
pygame.mixer.init()

# Ruta de la carpeta donde están las imágenes y sus subcarpetas
CARPETA_IMAGENES = "C:/musica"

# Configurar la ventana
ancho, alto = [1224, 680]  # Cambiar el orden para corregir las dimensiones
VENTANA = pygame.display.set_mode((ancho, alto))  # Cambiado
pygame.display.set_caption("ROKOPITHON-BG-Gabrielli")
back = pygame.image.load("8088488.jpg")
background = pygame.transform.scale(back, (ancho, alto - 22))  # Cambiado

moneda = pygame.image.load("img1.png")
moneda_creditos = pygame.transform.scale(moneda, (50, 50))

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 85)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Extensiones de imagen válidas
EXTENSIONES_VALIDAS = ('.png', '.jpg', '.jpeg')

# Extensiones válidas de música
EXTENSIONES_MUSICA = ('.mp3', '.wav', '.ogg')

# Función para obtener todas las imágenes en la carpeta y subcarpetas
def obtener_imagenes(carpeta):
    imagenes = []
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith(EXTENSIONES_VALIDAS):
                imagenes.append(os.path.join(root, file))
    return imagenes

# Función para obtener canciones de la misma carpeta
def obtener_canciones(carpeta):
    canciones = []
    for file in os.listdir(carpeta):
        if file.endswith(EXTENSIONES_MUSICA):
            canciones.append(file)
    return canciones

# Cargar todas las imágenes de la carpeta y subcarpetas
imagenes = obtener_imagenes(CARPETA_IMAGENES)

# Si no hay imágenes, salir del programa
if len(imagenes) == 0:
    print("No se encontraron imágenes en la carpeta especificada.")
    pygame.quit()
    sys.exit()

# Cargar las imágenes en Pygame
imagenes_cargadas = [pygame.image.load(img).convert() for img in imagenes]

# Index para controlar qué imagen se muestra en el centro
indice_imagen = 0

# Variable para almacenar la imagen seleccionada con "Enter"
imagen_seleccionada = None
lista_canciones = []

# Variable para controlar la selección de canciones
indice_cancion = 0

# Bucle principal
ejec = True
clock = pygame.time.Clock()

# Función para obtener cuatro imágenes de forma circular
def obtener_imagen_circular(indice):
    return [
        imagenes_cargadas[indice % len(imagenes_cargadas)],  # Imagen central
        imagenes_cargadas[(indice - 1) % len(imagenes_cargadas)],  # Imagen a la izquierda
        imagenes_cargadas[(indice - 2) % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice - 3) % len(imagenes_cargadas)],  # Imagen más a la izquierda
        imagenes_cargadas[(indice + 1) % len(imagenes_cargadas)],  # Imagen a la derecha
        imagenes_cargadas[(indice + 2) % len(imagenes_cargadas)],   # Imagen más a la derecha
        imagenes_cargadas[(indice + 3) % len(imagenes_cargadas)]   # Imagen más a la derecha
    ]

# Función para generar un color aleatorio
def color_random():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Color de borde inicial para el neón
color_neon = color_random()

# Contador para ralentizar el cambio de color
cambio_color_contador = 0

# Variable para controlar si el carrusel está activo o no
mostrar_carrusel = True

# Créditos iniciales
creditos = 1

# Lista para las canciones en cola
cola_canciones = []

# Fuente para texto de crédito 
fuente = pygame.font.Font(None, 35)

# Actualizar créditos
def actualizar_creditos(cantidad):
    global creditos
    creditos += cantidad
    print(f"Créditos: {creditos}")

# Definir la fuente
font = pygame.font.Font(None, 44)

# Función para mover la imagen
def mover_imagen(rect, intensidad=5):
    desplazamiento_x = random.randint(-intensidad, intensidad)
    desplazamiento_y = random.randint(-intensidad, intensidad)
    rect.x += desplazamiento_x
    rect.y += desplazamiento_y

# Bucle principal
mover = False
inicio_movimiento = 0
duracion_movimiento = 5  # Duración en segundos

while ejec:
    # Renderizar texto de créditos
    texto_creditos = fuente.render(f"Créditos: {creditos}", True, BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejec = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and mostrar_carrusel:
                indice_imagen = (indice_imagen + 1) % len(imagenes_cargadas)
            elif event.key == pygame.K_LEFT and mostrar_carrusel:
                indice_imagen = (indice_imagen - 1) % len(imagenes_cargadas)
            elif event.key == pygame.K_RETURN and mostrar_carrusel:
                mover = True
                inicio_movimiento = time.time()  # Captura el tiempo al iniciar el movimiento
                
                # Mover la imagen si se presionó Enter y no ha pasado el tiempo de duración
                if mover:
                    if time.time() - inicio_movimiento < duracion_movimiento:
                        mover_imagen(img_central.get_rect(center=(338, 284)))  # Mover la imagen central
                    else:
                        mover = False
                
                imagen_seleccionada = imagenes_cargadas[indice_imagen]
                carpeta_seleccionada = os.path.dirname(imagenes[indice_imagen])
                lista_canciones = obtener_canciones(carpeta_seleccionada)

                mostrar_carrusel = False
            elif event.key == pygame.K_m and not mostrar_carrusel:
                mostrar_carrusel = True
                lista_canciones = []
                indice_cancion = 0                
            elif event.key == pygame.K_c:  # Créditos
                actualizar_creditos(1)
            elif not mostrar_carrusel and lista_canciones:
                if event.key == pygame.K_DOWN:
                    indice_cancion = (indice_cancion + 1) % len(lista_canciones)
                elif event.key == pygame.K_UP:
                    indice_cancion = (indice_cancion - 1) % len(lista_canciones)
                elif event.key == pygame.K_RETURN:
                    if creditos > 0:
                        cola_canciones.append(lista_canciones[indice_cancion])
                        creditos -= 1
                        print(f"Agregada a la cola: {lista_canciones[indice_cancion]} - Créditos restantes: {creditos}")
                    else:
                        print("No tienes créditos suficientes para agregar la canción.")

    # Reproducir la siguiente canción en la cola si no hay música reproduciéndose
    if not pygame.mixer.music.get_busy() and cola_canciones:
        siguiente_cancion = cola_canciones.pop(0)
        ruta_cancion = os.path.join(carpeta_seleccionada, siguiente_cancion)
        pygame.mixer.music.load(ruta_cancion)
        pygame.mixer.music.play()
        print(f"Reproduciendo: {siguiente_cancion}")

    # Dibujar la ventana
    VENTANA.fill(NEGRO)
    VENTANA.blit(background, (0, 0))

    if mostrar_carrusel:
        color = color_random()
        texto = font.render("SinFonola ", True, color)
        VENTANA.blit(texto, (550, 10))

        texto_creditos = fuente.render(f"{creditos}  $ ", True, BLANCO)
        VENTANA.blit(texto_creditos, (1120, 5))

        # Obtener imágenes para mostrar
        imagenes_a_mostrar = obtener_imagen_circular(indice_imagen)

        for i, img in enumerate(imagenes_a_mostrar):
            offset_x = (i - 3) * 100  # Offset para la disposición
            rect = img.get_rect(center=(ancho // 2 + offset_x, alto // 2))
            VENTANA.blit(img, rect)

    else:
        if imagen_seleccionada:
            img_central = imagen_seleccionada
            rect_central = img_central.get_rect(center=(ancho // 2, alto // 2))
            VENTANA.blit(img_central, rect_central)

            # Mover imagen
            if mover:
                mover_imagen(rect_central)
                
                # Controlar el tiempo de movimiento
                if time.time() - inicio_movimiento > duracion_movimiento:
                    mover = False

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
