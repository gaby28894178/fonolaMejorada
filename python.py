import pygame
import os
import sys
import random
import time
import subprocess  # Para comprobar dispositivos USB en Windows

pygame.init()
pygame.mixer.init()

# Ruta de la carpeta donde están las imágenes y sus subcarpetas
CARPETA_IMAGENES = r"C:/musica"
alto, ancho = [1224, 680]
VENTANA = pygame.display.set_mode((alto, ancho))
pygame.display.set_caption("ROKOPITHON-BG-Gabrielli")

# Función para verificar si el USB específico está conectado
def usb_conectado(letra_usb):
    try:
        # Comando para listar las unidades USB en Windows
        dispositivos = subprocess.check_output("wmic logicaldisk get caption, description", shell=True, text=True).strip().split('\n')
        
        # Comprobar si la letra de la unidad USB está en la lista
        for dispositivo in dispositivos:
            if letra_usb in dispositivo:
                return True
    except Exception as e:
        print(f"Error al verificar dispositivos USB: {e}")
    return False

# Letra de la unidad del USB
LETRA_USB = "E:"  # Cambia esto a la letra correcta de tu USB

# Verificar si el USB está conectado
if not usb_conectado(LETRA_USB):
    print("El USB no está conectado. El programa se cerrará.")
    pygame.quit()
    sys.exit()




# ... (continúa con el resto de tu implementación)


#! Cargo el fondo de la ventana mc
back = pygame.image.load("background.jpg")
background = pygame.transform.scale(back,(alto -22,ancho))
#! Cargo la imagen de moneda
moneda = pygame.image.load("img1.png")
moneda_creditos= pygame.transform.scale(moneda,(50,50))

#? Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 85)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
VIOLETA = (148, 0, 211)


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
                imagenes.append(os.path.normpath(os.path.join(root, file)).replace('\\', '/'))
               
    return imagenes
# Función para obtener canciones de la misma carpeta

def obtener_canciones(carpeta):
    canciones = []
    for root, dirs, files in os.walk(carpeta):  # Cambiar a os.walk para incluir subcarpetas
        for file in files:
            if file.endswith(EXTENSIONES_MUSICA):
                ruta_cancion = os.path.join(root, file)  # Construir la ruta completa
                canciones.append(os.path.normpath(ruta_cancion).replace('\\', '/'))  # Normalizar y reemplazar barras
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

# Variable para almacenar la imagen seleccionada con "Enter" y canciones 
imagen_seleccionada = None
indice_cancion = 0
lista_canciones = []

# Bucle principal
ejec = True
clock = pygame.time.Clock()

# Función para obtener cuatro imágenes de forma circular
def obtener_imagen_circular(indice):
    return [
        imagenes_cargadas[indice % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice - 1) % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice - 2) % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice - 3) % len(imagenes_cargadas)], 
        imagenes_cargadas[(indice + 1) % len(imagenes_cargadas)],  
        imagenes_cargadas[(indice + 2) % len(imagenes_cargadas)],   
        imagenes_cargadas[(indice + 3) % len(imagenes_cargadas)]   
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
# Configuración de la fuente
fuente_canciones = pygame.font.SysFont(None, 30)  # Cambia el tamaño según tu preferencia
color = color_aleatorio()




def mover_imagen(rect, intensidad=5):
    desplazamiento_x = random.randint(-intensidad, intensidad)
    desplazamiento_y = random.randint(-intensidad, intensidad)
    rect.x += desplazamiento_x
    rect.y += desplazamiento_y
running = True
mover = False
inicio_movimiento = 0
duracion_movimiento = 5  # Duración en segundos
 
# Texto a mostrar
moneda = fuente_canciones.render("Insert Money Or Coin", True, color)



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
                print(f"Créditos: {creditos}")
                
                #!borrar lista 
            elif event.key == pygame.K_l:
                cola_canciones=[]
                pygame.mixer.music.stop()
                print("Música detenida.")
                print(f"lista de canciones {cola_canciones}")
                os.system('cls')
                print("Listas Borradas")
                #!siguiente cancion de lista 
            elif event.key == pygame.K_s:
                 #! Detener la canción actual
                pygame.mixer.music.stop()
                 #? Reproducir la siguiente canción inmediatamente
                if cola_canciones:
                    pygame.mixer.music.stop()
                    print(f"Reproduciendo : {siguiente_cancion}")
                
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
                        print (len(lista_canciones))
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
        VENTANA.blit(m1, (430, 120))
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
                     #cuadrado adorno 
        pygame.draw.rect(VENTANA, color_neon,(15,60, 850,525),6,border_bottom_left_radius=53)
        
       #ventana de Vista de album 
        color = color_aleatorio()
        texto = font.render("SinFonola ", True, color)
       # Dibujar el texto en la pantalla
        VENTANA.blit(texto, (550, 10))
        
        img_seleccionada = pygame.transform.scale(imagen_seleccionada, (402, 400))
        VENTANA.blit(img_seleccionada, (588, 95))

        fuente_canciones = pygame.font.SysFont(None, 25)
        y_pos = 98
    
    # Sección de lista de canciones
    for i, ruta_cancion in enumerate(lista_canciones):
        # Extrae solo el nombre del archivo sin la ruta ni la extensión ni el nombre de artista 
        nombre_archivo = os.path.basename(ruta_cancion)
        cancion_sin_extension = nombre_archivo.replace(".mp3", "")
        
        # Divide para obtener artista y tema sin número de pista
        partes = cancion_sin_extension.split("-")
        artista_y_tema = "-".join(partes[1:]) if len(partes) > 1 else cancion_sin_extension

        # Determina si esta es la canción seleccionada
        color_texto = AMARILLO if i == indice_cancion else BLANCO
        texto = f"< [ {artista_y_tema} ] >" if i == indice_cancion else artista_y_tema

        # Renderiza el texto sin blitearlo todavía
        superficie_texto = fuente_canciones.render(texto, True, color_texto)

        # Dibuja el fondo violeta si es la canción seleccionada
        if i == indice_cancion:
            pygame.draw.rect(
                VENTANA,
                VIOLETA,
                (100 - 5, y_pos - 3, superficie_texto.get_width() + 12, superficie_texto.get_height() + 6)
            )

        # Blitea el texto encima del rectángulo
        VENTANA.blit(superficie_texto, (100, y_pos))
        y_pos += 20

        # Código adicional para los créditos
        texto_creditos = fuente.render(f" {creditos} $ ", True, BLANCO)
        VENTANA.blit(texto_creditos, (72, 620))
        VENTANA.blit(moneda_creditos, (10, 600))
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
