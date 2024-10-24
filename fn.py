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
alto, ancho = [1024,680]
VENTANA = pygame.display.set_mode((alto,ancho))
pygame.display.set_caption("Carrusel Circular de Imágenes")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
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

# Función para obtener tres imágenes de forma circular
def obtener_imagen_circular(indice):
    return [
        imagenes_cargadas[indice % len(imagenes_cargadas)],  # Imagen central
        imagenes_cargadas[(indice - 1) % len(imagenes_cargadas)],  # Imagen izquierda
        imagenes_cargadas[(indice + 1) % len(imagenes_cargadas)]   # Imagen derecha
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
creditos = 1  # Puedes ajustar la cantidad inicial de créditos
credit = f"CREDITO {creditos}"

# Lista para las canciones en cola
cola_canciones = []
# Fuentes 
fuente = pygame.font.Font(None, 25)
    #Creditos Marcacion 
def actualizar_creditos(cantidad):
    global creditos  # Asegúrate de que 'creditos' es global si la variable se define fuera de esta función
    creditos += cantidad  # Actualiza el saldo de créditos
    print(f"Créditos: {creditos}")  # Imprimir el saldo actualizado

    
while ejec:
    # Renderizar y dibujar el texto de créditos
    texto_creditos = fuente.render(f"Créditos: {creditos}", True, BLANCO)
    VENTANA.blit(texto_creditos, (750, 20))
    # Mostrar los créditos actuales 
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
                creditos += 1
                actualizar_creditos(1)
                print(f"Créditos: {creditos}")

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

    if mostrar_carrusel:
        # Dibujar la imagen actual
        imagen_actual = imagenes_cargadas[indice_imagen]
        VENTANA.blit(imagen_actual, (0, 0))

        # Renderizar y dibujar el texto de créditos
        texto_creditos = fuente.render(f"Créditos: {creditos}", True, BLANCO)
        VENTANA.blit(texto_creditos, (750, 20))

        # Obtener las imágenes para mostrar (izquierda, centro, derecha)
        img_central, img_izquierda, img_derecha = obtener_imagen_circular(indice_imagen)

        # Redimensionar las imágenes si es necesario
        img_central = pygame.transform.scale(img_central, (340, 340))
        img_izquierda = pygame.transform.scale(img_izquierda, (240, 240))
        img_derecha = pygame.transform.scale(img_derecha, (240, 240))

        # Dibujar el borde de neón
        cambio_color_contador += 1
        if cambio_color_contador % 30 == 0:
            color_neon = color_random()
        pygame.draw.rect(VENTANA, color_neon, (338, 190, 341, 341), 10, border_radius=22)

        # Mostrar las imágenes en posiciones más separadas
        VENTANA.blit(img_central, (338, 190))
        VENTANA.blit(img_izquierda, (50, 180))
        VENTANA.blit(img_derecha, (750, 180))

    else:
        # Mostrar la imagen seleccionada en el centro de la pantalla
        img_seleccionada = pygame.transform.scale(imagen_seleccionada, (450, 400))
        VENTANA.blit(img_seleccionada, (350, 100))

        

        # Mostrar la lista de canciones en la parte izquierda
        fuente_canciones = pygame.font.SysFont(None, 20)
        y_pos = 50
        for i, cancion in enumerate(lista_canciones):
            if i == indice_cancion:
                texto = fuente_canciones.render(f"> {cancion}", True, AMARILLO)
            else:
                texto = fuente_canciones.render(cancion, True, BLANCO)
            VENTANA.blit(texto, (50, y_pos))
            y_pos += 25
            texto_creditos = fuente.render(f"Créditos: {creditos}", True, BLANCO)
            VENTANA.blit(texto_creditos, (750, 20))

    # Actualizar la pantalla
    pygame.display.flip()
       
    clock.tick(60)

# Finalizar Pygame
pygame.quit()
