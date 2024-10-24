import pygame
import os
import sys

# Inicializar Pygame
pygame.init()

# Ruta de la carpeta donde están las imágenes
CARPETA_IMAGENES = "C:/musica"

# Configurar la ventana
VENTANA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Carrusel de Imágenes")

# Colores
BLANCO = (255, 255, 255)

# Cargar todas las imágenes de la carpeta
imagenes = [os.path.join(CARPETA_IMAGENES, archivo) for archivo in os.listdir(CARPETA_IMAGENES) if archivo.endswith(('.png', '.jpg', '.jpeg'))]

# Si no hay imágenes, salir del programa
if len(imagenes) == 0:
    print("No se encontraron imágenes en la carpeta especificada.")
    pygame.quit()
    sys.exit()

# Cargar las imágenes en Pygame
imagenes_cargadas = [pygame.image.load(img).convert() for img in imagenes]

# Index para controlar qué imagen se muestra
indice_imagen = 0

# Bucle principal
ejec = True
clock = pygame.time.Clock()

while ejec:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejec = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                indice_imagen = (indice_imagen + 1) % len(imagenes_cargadas)  # Avanzar a la siguiente imagen
            elif event.key == pygame.K_LEFT:
                indice_imagen = (indice_imagen - 1) % len(imagenes_cargadas)  # Retroceder a la imagen anterior

    # Dibujar la ventana
    VENTANA.fill(BLANCO)

    # Obtener la imagen actual y redimensionarla si es necesario
    imagen_actual = imagenes_cargadas[indice_imagen]
    imagen_redimensionada = pygame.transform.scale(imagen_actual, (800, 600))

    # Mostrar la imagen
    VENTANA.blit(imagen_redimensionada, (0, 0))

    # Actualizar la ventana
    pygame.display.flip()
    
    # Controlar la velocidad del bucle
    clock.tick(30)

# Cerrar Pygame
pygame.quit()
sys.exit()
