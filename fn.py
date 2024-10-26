import pygame
import os
import sys
import random

# Inicializar Pygame y su mixer
pygame.init()
pygame.mixer.init()

# Ruta de la carpeta donde están las imágenes y sus subcarpetas
CARPETA_IMAGENES = "C:/musica"

# Configurar la ventana
alto, ancho = [1224,680]
VENTANA = pygame.display.set_mode((alto,ancho))
pygame.display.set_caption("ROKOPITHON-BG-Gabrielli")
back = pygame.image.load("8088488.jpg")
background = pygame.transform.scale(back,(alto -22,ancho))

moneda = pygame.image.load("img1.png")
moneda_creditos= pygame.transform.scale(moneda,(50,50))
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
        imagenes_cargadas[(indice - 1) % len(imagenes_cargadas)],  # Imagen más derecha
        imagenes_cargadas[(indice - 2) % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice - 3) % len(imagenes_cargadas)], # Imagen izquierda
        imagenes_cargadas[(indice + 1) % len(imagenes_cargadas)],  # Imagen derecha
        imagenes_cargadas[(indice + 2) % len(imagenes_cargadas)],   # Imagen más derecha
        imagenes_cargadas[(indice + 3) % len(imagenes_cargadas)]   # Imagen más derecha
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

# Fuente para texto cont credito 
fuente = pygame.font.Font(None, 35)

# Actualizar créditos
def actualizar_creditos(cantidad):
    global creditos
    creditos += cantidad
    print(f"Créditos: {creditos}")
#cambiar color moneda insertion 


# Definir la fuente
font = pygame.font.Font(None, 44)

# Función para generar un color RGB aleatorio
def color_aleatorio():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))




while ejec:
    # Renderizar texto de créditos
    texto_creditos = fuente.render(f"Créditos: {creditos}", True, BLANCO)
    # VENTANA.blit(texto_creditos, (750, 20))
    # VENTANA.blit(moneda_creditos,(750,20))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejec = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and mostrar_carrusel:
                indice_imagen = (indice_imagen + 1) % len(imagenes_cargadas)
            elif event.key == pygame.K_LEFT and mostrar_carrusel:
                indice_imagen = (indice_imagen - 1) % len(imagenes_cargadas)
            elif event.key == pygame.K_RETURN and mostrar_carrusel:
                imagen_seleccionada = imagenes_cargadas[indice_imagen]
                carpeta_seleccionada = os.path.dirname(imagenes[indice_imagen])
                lista_canciones = obtener_canciones(carpeta_seleccionada)
                mostrar_carrusel = False
            elif event.key == pygame.K_m and not mostrar_carrusel:
                mostrar_carrusel = True
                lista_canciones = []
                indice_cancion = 0                
            elif event.key == pygame.K_c:  # Creditos
                actualizar_creditos(1)
                # print(f"Créditos: {creditos}")
            elif not mostrar_carrusel and lista_canciones:
                if event.key == pygame.K_DOWN:
                    indice_cancion = (indice_cancion + 1) % len(lista_canciones)
                elif event.key == pygame.K_UP:
                    indice_cancion = (indice_cancion - 1) % len(lista_canciones)
                elif event.key == pygame.K_RETURN:
                    if creditos > 0:
                        cola_canciones.append(lista_canciones[indice_cancion])
                        creditos -= 1
                        # print(f"Agregada a la cola: {lista_canciones[indice_cancion]} - Créditos restantes: {creditos}")
                    else:
                     pass

    # Reproducir la siguiente canción en la cola si no hay música reproduciéndose
    if not pygame.mixer.music.get_busy() and cola_canciones:
        siguiente_cancion = cola_canciones.pop(0)
        ruta_cancion = os.path.join(carpeta_seleccionada, siguiente_cancion)
        pygame.mixer.music.load(ruta_cancion)
        pygame.mixer.music.play()
        # print(f"Reproduciendo: {siguiente_cancion}")

    # Dibujar la ventana
    VENTANA.fill(NEGRO)
    VENTANA.blit(background,(10,-390))

    if mostrar_carrusel:
          
        color = color_aleatorio()
        texto = font.render("SinFonola ", True, color)
            # Dibujar el texto en la pantalla
        VENTANA.blit(texto, (550, 10))
        
        texto_creditos = fuente.render(f"{creditos}  $ ", True, BLANCO)
        VENTANA.blit(texto_creditos, (72, 620))
        VENTANA.blit(moneda_creditos,(10,600))

        # Obtener imágenes
        img_central,m1,m2,m3,p1,p2,p3 = obtener_imagen_circular(indice_imagen)

        # Redimensionar imágenes
        img_central = pygame.transform.scale(img_central, (340, 340))

        m1 = pygame.transform.scale(m1, (260, 260))
        m2 = pygame.transform.scale(m2, (260, 260))
        m3 = pygame.transform.scale(m3, (260, 260))
        
        p1 = pygame.transform.scale(p1, (290, 290))
        p2 = pygame.transform.scale(p2, (260, 260))
        p3 = pygame.transform.scale(p3, (260, 260))
        
        
          # Mostrar imágenes
        VENTANA.blit(m1, (110, 10))
        VENTANA.blit(m2, (660, 160))
        VENTANA.blit(m1, (580, 262))
        VENTANA.blit(p3, (230, 160))
        VENTANA.blit(p2, (140, 225))
        VENTANA.blit(p1, (218, 262))
        VENTANA.blit(img_central, (338, 284))
        # Mostrar imágenes en forma circular


        # Dibujar el borde de neón
        cambio_color_contador += 1
        if cambio_color_contador % 30 == 0:
            color_neon = color_random()
        pygame.draw.rect(VENTANA, color_neon, (330, 275, 358, 358), 5, border_radius=2)

    else:
       
        VENTANA.fill(NEGRO)
        
        color = color_aleatorio()
        texto = font.render("SinFonola ", True, color)
            # Dibujar el texto en la pantalla
        VENTANA.blit(texto, (550, 10))

        
        
        img_seleccionada = pygame.transform.scale(imagen_seleccionada, (380, 300))
        VENTANA.blit(img_seleccionada, (450, 100))

        fuente_canciones = pygame.font.SysFont(None, 20)
        y_pos = 98
        for i, cancion in enumerate(lista_canciones):
            texto = fuente_canciones.render(f"> {cancion}" if i == indice_cancion else cancion, True, AMARILLO if i == indice_cancion else BLANCO)
            VENTANA.blit(texto, (123, y_pos))
            y_pos += 25
            texto_creditos = fuente.render(f" {creditos} $ ", True, BLANCO)
            VENTANA.blit(texto_creditos, (72, 620))
            VENTANA.blit(moneda_creditos,(10,600))
            
            # Renderizar el texto con un color aleatorio
            color = color_aleatorio()
            texto = font.render("Insertion Money Or Coint", True, color)
            # Dibujar el texto en la pantalla
            VENTANA.blit(texto, (125 , 618))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
