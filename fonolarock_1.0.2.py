import pygame # type: ignore
import os
import sys
import random
# from color.colores import *
import color.colores as colores 



# ========== INICIALIZACIÓN ==========
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Configuración de ventana
ANCHO, ALTO = 1224, 780
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("ROKOPITHON-BG-Gabrielli-Tel 11-2167-4227")

# Rutas y extensiones
CARPETA_IMAGENES = "C:/musica"
EXTENSIONES_VALIDAS = ('.png', '.jpg', '.jpeg')
EXTENSIONES_MUSICA = ('.mp3', '.wav', '.ogg')

# Configuración de grid
GRID_COLS = 4
GRID_ROWS = 3
ITEMS_PER_PAGE = GRID_COLS * GRID_ROWS

# ========== CLASE DE ESTADO ==========
class EstadoApp:
    def __init__(self):
        # Configuración de interfaz
        self.imagen_seleccionada = None
        self.lista_canciones = []
        self.indice_cancion = 0
        self.cancion_actual = None
        self.indice_imagen = None
        self.reproduciendo = False
        self.ejecucion = True
        self.mostrar_grid = True
        self.mostrar_creditos = True
        self.scroll_canciones = 0
        self.creditos = 6
        self.creditos_activos = True
        
        # Para la cola de reproducción
        self.playlist = []
        self.current_playlist_index = 0
        self.en_cola = False
        self.playlist_visible = True
        
        # Temporizador de inactividad
        self.tiempo_inicio_inactividad = pygame.time.get_ticks()
        self.tiempo_limite_inactividad = 10000  # 20 segundos en milisegundos
        self.temporizador_activo = True
        
        # Información de vista
        self.vista_actual = "Principal"
        self.vistas_cargadas = []

    def reiniciar_temporizador(self):
        """Reinicia el temporizador de inactividad"""
        self.tiempo_inicio_inactividad = pygame.time.get_ticks()
    
    def verificar_inactividad(self):
        """Verifica si ha pasado el tiempo límite de inactividad"""
        if not self.temporizador_activo:
            return False
            
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_inactividad
        
        return tiempo_transcurrido >= self.tiempo_limite_inactividad
    
    def volver_a_principal(self):
        """Regresa a la vista principal y resetea el estado"""
        self.mostrar_grid = True
        self.vista_actual = "Principal"
        self.reiniciar_temporizador()
        print("Regresando a la vista principal por inactividad...")

# ========== FUNCIONES DE CARGA DE RECURSOS ==========
def cargar_fondo():
    """Carga la imagen de fondo o crea una por defecto"""
    try:
        back = pygame.image.load("background.jpg")
        fondo = pygame.transform.scale(back, (ANCHO, ALTO))
        return fondo, fondo.copy()
    except Exception as e:
        print(f"Error al cargar fondo: {e}")
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill(NEGRO)
        return fondo, fondo.copy()

def cargar_icono_moneda():
    """Carga el icono de moneda para créditos"""
    try:
        moneda = pygame.image.load("img1.png")
        return pygame.transform.scale(moneda, (40, 40))
    except Exception as e:
        print(f"Error al cargar icono: {e}")
        return None

def obtener_imagenes(carpeta):
    """Obtiene todas las imágenes válidas de la carpeta y subcarpetas"""
    imagenes = []
    try:
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.lower().endswith(EXTENSIONES_VALIDAS):
                    imagenes.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error al buscar imágenes: {e}")
    return imagenes

def obtener_canciones(carpeta):
    """Obtiene las canciones de una carpeta específica"""
    canciones = []
    try:
        for file in os.listdir(carpeta):
            if file.lower().endswith(EXTENSIONES_MUSICA):
                canciones.append(file)
    except Exception as e:
        print(f"No se pudo acceder a {carpeta}: {e}")
    return canciones

def cargar_imagenes(imagenes):
    """Carga las imágenes o crea placeholders si falla"""
    imagenes_cargadas = []
    for img_path in imagenes:
        try:
            img = pygame.image.load(img_path).convert()
            imagenes_cargadas.append(img)
        except Exception as e:
            print(f"Error al cargar {img_path}: {e}")
            placeholder = pygame.Surface((200, 200))
            placeholder.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            imagenes_cargadas.append(placeholder)
    return imagenes_cargadas

def cargar_tecla(ruta, tamaño=(40, 40)):
    """Carga una imagen de tecla o devuelve None si falla"""
    try:
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, tamaño)
    except Exception as e:
        print(f"Error al cargar tecla {ruta}: {e}")
        superficie = pygame.Surface(tamaño, pygame.SRCALPHA)
        pygame.draw.rect(superficie, GRIS_CLARO, (0, 0, tamaño[0], tamaño[1]), 1)
        return superficie

# ========== FUNCIONES DE REPRODUCCIÓN DE MÚSICA ==========
def reproducir_cancion(ruta_cancion, estado):
    """Reproduce una canción y maneja los créditos"""
    try:
        pygame.mixer.music.load(ruta_cancion)
        pygame.mixer.music.play()
        estado.reproduciendo = True
        estado.cancion_actual = os.path.basename(ruta_cancion)
        # NO descontar crédito aquí, ya se descontó al seleccionar
        # Configurar evento para cuando termine la canción
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
    except Exception as e:
        print(f"Error al reproducir {ruta_cancion}: {e}")

def agregar_a_playlist(ruta_cancion, estado):
    """Agrega una canción a la playlist"""
    # Si la canción ya está en la playlist, no la agregamos de nuevo
    if ruta_cancion in estado.playlist:
        return
    
    estado.playlist.append(ruta_cancion)
    if not estado.en_cola:
        estado.current_playlist_index = len(estado.playlist) - 1
        reproducir_cancion(ruta_cancion, estado)
        estado.en_cola = True
    else:
        # Mostrar mensaje de que la canción fue agregada a la cola
        print(f"Canción agregada a la cola: {os.path.basename(ruta_cancion)}")

def manejar_fin_cancion(estado):
    """Maneja el evento de fin de canción para la cola de reproducción"""
    if estado.playlist:
        estado.current_playlist_index += 1
        if estado.current_playlist_index < len(estado.playlist):
            reproducir_cancion(estado.playlist[estado.current_playlist_index], estado)
        else:
            estado.reproduciendo = False
            estado.en_cola = False
            estado.playlist = []
            estado.current_playlist_index = 0

# !========== FUNCIONES DE INTERFAZ GRÁFICA ==========

def dibujar_tecla_con_texto(x, y, tecla_img, texto, fuente, ventana):
    """Dibuja una tecla con su texto descriptivo"""
    if tecla_img:
        ventana.blit(tecla_img, (x, y))
    txt_surf = fuente.render(texto, True, colores.BLANCO)
    ventana.blit(txt_surf, (x + (tecla_img.get_width() if tecla_img else 0) + 5, 
                 y + ((tecla_img.get_height() - txt_surf.get_height()) // 2 if tecla_img else 0)))

def dibujar_panel_teclas(ventana, teclas, fuente_canciones):
    """Dibuja el panel inferior con los controles"""
    panel_y = ALTO - 47
    ancho_panel = ANCHO - 10
    #!teclas  dibujar
    pygame.draw.rect(ventana,colores.NEGRO, (6, panel_y, ancho_panel, 45), 0)
    pygame.draw.rect(ventana, colores.ROJO, (6, panel_y, ancho_panel, 45), 2)
    
    # Teclas de navegación
    x_pos = 100
    for tecla, texto in [('left', ""), ('right', ""), 
                         ('up', ""), ('down', "")]:
        dibujar_tecla_con_texto(x_pos, panel_y + 5, teclas.get(tecla), texto, fuente_canciones, ventana)
        x_pos += 150
    
    # Teclas de acciones
    x_pos = ANCHO - 500
    for tecla, texto in [('', "Selecr"), ('', "Menú"), ('', "Créditos")]:
        dibujar_tecla_con_texto(x_pos, panel_y + 5, teclas.get(tecla), texto, fuente_canciones, ventana)
        x_pos += 150

def dibujar_cola_reproduccion(ventana, estado, fuente_canciones):
    """Dibuja la cola de reproducción en la parte derecha"""
    if not estado.playlist_visible or not estado.playlist:
        return
    
    ancho_cola = 300
    margen = 20
    
    # Panel de la cola
    pygame.draw.rect(ventana, colores.GRIS_OSCURO, (ANCHO - ancho_cola - margen, 100, ancho_cola, ALTO - 200))
    pygame.draw.rect(ventana, colores.AZUL_CLARO, (ANCHO - ancho_cola - margen, 100, ancho_cola, ALTO - 200), 2)
    
    # Título
    titulo = fuente_canciones.render("COLA DE REPRODUCCIÓN", True, colores.AZUL_CLARO)
    ventana.blit(titulo, (ANCHO - ancho_cola - margen + 10, 110))
    
    # Lista de canciones en cola
    for i, cancion in enumerate(estado.playlist):
        y_pos = 140 + i * 25
        nombre = os.path.basename(cancion)[:30]
        
        # Resaltar la canción actual
        if i == estado.current_playlist_index and estado.reproduciendo:
            color = colores.AMARILLO
            pygame.draw.rect(ventana,colores.GRIS_CLARO, (ANCHO - ancho_cola - margen + 5, y_pos - 2, ancho_cola - 20, 20))
        else:
            color = colores.BLANCO
        
        texto = fuente_canciones.render(f"{i+1}. {nombre}", True, color)
        ventana.blit(texto, (ANCHO - ancho_cola - margen + 10, y_pos))

def dibujar_indicador_tiempo(ventana, estado, fuente_canciones):
    """Dibuja un indicador del tiempo restante antes de volver al menú principal"""
    if not estado.temporizador_activo or estado.mostrar_grid:
        return
    
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - estado.tiempo_inicio_inactividad
    tiempo_restante = max(0, estado.tiempo_limite_inactividad - tiempo_transcurrido)
    segundos_restantes = tiempo_restante // 1000
    
    # Solo mostrar cuando quedan menos de 5 segundos
    if segundos_restantes <= 5:
        texto = f"Regresando al menu en {segundos_restantes}s"
        superficie_texto = fuente_canciones.render(texto, True, colores.ROJO)
        x = ANCHO // 2 - superficie_texto.get_width() // 2
        y = 20
        
        # Fondo semi-transparente
        pygame.draw.rect(ventana, (0, 0, 0, 128), (x - 10, y - 5, superficie_texto.get_width() + 20, superficie_texto.get_height() + 10))
        ventana.blit(superficie_texto, (x, y))

def dibujar_grid(ventana, imagenes_cargadas, current_page, selected_index, estado, 
                fuente_principal, fuente_titulo, fuente_creditos, moneda_creditos, teclas):
    """Dibuja el grid de imágenes"""
    start_idx = current_page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, len(imagenes_cargadas))
    cover_w, cover_h = 200, 200
    margin_x, margin_y = 50, 50
    texto_pagina = fuente_principal.render(f"Página", True, colores.BLANCO)
    
    
    for i in range(start_idx, end_idx):
        pos_rel = i - start_idx
        row, col = pos_rel // GRID_COLS, pos_rel % GRID_COLS
        x = margin_x + col * (cover_w + 30)
        y = margin_y + row * (cover_h + 30)
        
        cover = pygame.transform.scale(imagenes_cargadas[i], (cover_w, cover_h))
        ventana.blit(cover, (x, y))
        #!Rectangulo selector 
        if pos_rel == selected_index:
            pygame.draw.rect(ventana,colores.AZUL , (x-5, y-5, cover_w+10, cover_h+10), 3)
        
        if pos_rel == selected_index:
            pygame.draw.rect(ventana,colores.VIOLETA_ELECTRICO  , (x-2, y-7, cover_w+3, cover_h+16), 3)

    # Información de página
    total_pages = max(1, (len(imagenes_cargadas) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    texto_pagina = fuente_principal.render(f"Página {current_page+1}/{total_pages}", True, colores.BLANCO)
    ventana.blit(texto_pagina, (ANCHO//2 + 430 , 110))
    
    # Título principal
    texto_titulo = fuente_titulo.render("Selecciona un Álbum", True, colores.BLANCO)
    ventana.blit(texto_titulo, (ANCHO//2 - 60, 20))
    
    # Mostrar créditos
    if estado.creditos_activos:
        dibujar_label_creditos(ventana, estado, fuente_creditos, moneda_creditos)
    
    fuente_canciones = pygame.font.SysFont(None, 24)
    dibujar_panel_teclas(ventana, teclas, fuente_canciones)

def dibujar_lista_canciones(ventana, estado, imagenes, fuente_principal, fuente_titulo, 
                          fuente_canciones, fuente_creditos, moneda_creditos, teclas):
    """Dibuja la lista de canciones con scroll"""
    # Panel principal
    # pygame.draw.rect(ventana, colores.GRIS_OSCURO, (50, 50, 350, ALTO - 150), 0)
    pygame.draw.rect(ventana, colores.VERDE, (50, 50, 350, ALTO - 149), 2)
    
    # Título del álbum
    if estado.indice_imagen is not None and estado.indice_imagen < len(imagenes):
        titulo = os.path.basename(os.path.dirname(imagenes[estado.indice_imagen]))[:30]
    else:
        titulo = "Álbum desconocido"
    #! titulo de lista
    texto_titulo = fuente_titulo.render(titulo, True, colores.BLANCO)
    ventana.blit(texto_titulo, (60, 60))
    
    # Área de canciones con scroll
    area_canciones = pygame.Rect(60, 90, 330, ALTO - 228)
    # pygame.draw.rect(ventana,"" , area_canciones)
    
    # Calcular canciones visibles
    max_visibles = area_canciones.height // 25
    inicio = max(0, min(estado.scroll_canciones, len(estado.lista_canciones) - max_visibles))
    fin = min(inicio + max_visibles, len(estado.lista_canciones))
    
    # Dibujar canciones visibles
    for i in range(inicio, fin):
        y_pos = 90 + (i - inicio) * 25
        color = colores.VIOLETA_MEDIO if i == estado.indice_cancion else colores.BLANCO
        nombre = estado.lista_canciones[i][:25] if i < len(estado.lista_canciones) else "Canción desconocida"
        texto = fuente_canciones.render(nombre, True, color)
        ventana.blit(texto, (70, y_pos))
    
    # Barra de scroll
    if len(estado.lista_canciones) > max_visibles:
        altura_barra = max(20, (max_visibles / len(estado.lista_canciones)) * area_canciones.height)
        pos_barra = (estado.scroll_canciones / len(estado.lista_canciones)) * (area_canciones.height - altura_barra)
        pygame.draw.rect(ventana, colores.GRIS_CLARO, (area_canciones.right - 10, area_canciones.top + pos_barra, 8, altura_barra))
    
    # Estado de reproducción
    estado_texto = "Reproduciendo" if estado.reproduciendo else "Pausado"
    texto_estado = fuente_principal.render(f"Estado: {estado_texto}", True, colores.BLANCO)
    ventana.blit(texto_estado, (96, ALTO - 210))
    
    # Canción actual
    if estado.cancion_actual:
        texto_cancion = fuente_principal.render(f"Canción: {estado.cancion_actual[:3]}", True, colores.BLANCO)
        ventana.blit(texto_cancion, (96, ALTO - 180))
    
    # Indicador de modo
    texto_modo = fuente_titulo.render("Modo: Lista de Canciones", True, colores.AMARILLO)
    ventana.blit(texto_modo, (400, 60))
    
    # Mostrar créditos
    if estado.creditos_activos:
        dibujar_label_creditos(ventana, estado, fuente_creditos, moneda_creditos)
    
    # Mostrar cola de reproducción
    dibujar_cola_reproduccion(ventana, estado, fuente_canciones)
    
    # Mostrar indicador de tiempo
    dibujar_indicador_tiempo(ventana, estado, fuente_canciones)
    
    dibujar_panel_teclas(ventana, teclas, fuente_canciones)

def dibujar_label_creditos(ventana, estado, fuente_creditos, moneda_creditos):
    """Dibuja el label de créditos que se actualiza dinámicamente"""
    ancho_panel = 200
    alto_panel = 60
    margen = 20
    
    panel_x = ANCHO - ancho_panel - margen
    panel_y = margen
    
    pygame.draw.rect(ventana, colores.GRIS_OSCURO, (panel_x, panel_y, ancho_panel, alto_panel))
    pygame.draw.rect(ventana, colores.AMARILLO, (panel_x, panel_y, ancho_panel, alto_panel), 2)
    
    if moneda_creditos:
        ventana.blit(moneda_creditos, (panel_x + 10, panel_y + 10))
    
    texto_creditos = fuente_creditos.render(f"Créditos: {estado.creditos}", True, colores.AMARILLO)
    ventana.blit(texto_creditos, (panel_x + 60, panel_y + 20))

# ========== FUNCIÓN PRINCIPAL ==========
def main():
    # Cargar recursos
    background, default_background = cargar_fondo()
    moneda_creditos = cargar_icono_moneda()
    
    # Fuentes
    fuente_principal = pygame.font.Font(None, 35)
    fuente_canciones = pygame.font.SysFont(None, 24)
    fuente_titulo = pygame.font.SysFont(None, 30, bold=True)
    fuente_creditos = pygame.font.SysFont(None, 24)
    
    # Cargar imágenes
    imagenes = obtener_imagenes(CARPETA_IMAGENES)
    if not imagenes:
        print("No se encontraron imágenes. Saliendo...")
        pygame.quit()
        sys.exit()
    
    imagenes_cargadas = cargar_imagenes(imagenes)
    
    # Cargar teclas
    teclas = {
        'up': cargar_tecla("teclas/5.png"),
        'down': cargar_tecla("teclas/4.png"),
        'left': cargar_tecla("teclas/3.png"),
        'right': cargar_tecla("teclas/2.png"),
        'enter': cargar_tecla("teclas/1.png"),
        'm': cargar_tecla("teclas/Retornar.png"),
        'pageup': cargar_tecla("teclas/pageup.png"),
        'pagedown': cargar_tecla("teclas/pagedow.png"),
        'c': cargar_tecla("teclas/moneda.png"),
        
    }
    
    # Estado de la aplicación
    estado = EstadoApp()
    current_page = 0
    selected_index = 0
    
    # Bucle principal
    while estado.ejecucion:
        # Verificar inactividad
        if estado.verificar_inactividad() and not estado.mostrar_grid:
            estado.volver_a_principal()
            current_page = 0
            selected_index = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado.ejecucion = False
            
            # Manejar fin de canción
            elif event.type == pygame.USEREVENT:
                manejar_fin_cancion(estado)
            
            # Manejo de teclado
            elif event.type == pygame.KEYDOWN:
                # Reiniciar temporizador cuando hay actividad
                estado.reiniciar_temporizador()
                
                if event.key == pygame.K_ESCAPE:
                    estado.ejecucion = False
                
                if estado.mostrar_grid:
                    # Navegación en el grid
                    if event.key == pygame.K_LEFT:
                        selected_index = max(0, selected_index - 1)
                    elif event.key == pygame.K_RIGHT:
                        selected_index = min(ITEMS_PER_PAGE - 1, selected_index + 1)
                    elif event.key == pygame.K_UP:
                        selected_index = max(0, selected_index - GRID_COLS)
                    elif event.key == pygame.K_DOWN:
                        selected_index = min(ITEMS_PER_PAGE - 1, selected_index + GRID_COLS)
                    elif event.key == pygame.K_RETURN:
                        # Seleccionar imagen/carpeta
                        if current_page * ITEMS_PER_PAGE + selected_index < len(imagenes):
                            estado.indice_imagen = current_page * ITEMS_PER_PAGE + selected_index
                            carpeta = os.path.dirname(imagenes[estado.indice_imagen])
                            estado.lista_canciones = obtener_canciones(carpeta)
                            if estado.lista_canciones:
                                estado.mostrar_grid = False
                                estado.vista_actual = "Lista_Canciones"
                                estado.reiniciar_temporizador()  # Reiniciar al cambiar vista
                    elif event.key == pygame.K_PAGEUP:
                        current_page = max(0, current_page - 1)
                        selected_index = 0
                    elif event.key == pygame.K_PAGEDOWN:
                        current_page = min((len(imagenes_cargadas) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE - 1, current_page + 1)
                        selected_index = 0
                
                else:  # Modo lista de canciones
                    if event.key == pygame.K_UP:
                        estado.indice_cancion = max(0, estado.indice_cancion - 1)
                        if estado.indice_cancion < estado.scroll_canciones:
                            estado.scroll_canciones = estado.indice_cancion
                    elif event.key == pygame.K_DOWN:
                        estado.indice_cancion = min(len(estado.lista_canciones) - 1, estado.indice_cancion + 1)
                        max_visibles = (ALTO - 220 - 90) // 25
                        if estado.indice_cancion >= estado.scroll_canciones + max_visibles:
                            estado.scroll_canciones = estado.indice_cancion - max_visibles + 1
                    elif event.key == pygame.K_s:
                        pygame.mixer.music.stop()
                        estado.reproduciendo = False
                        estado.en_cola = False
                        estado.playlist = []
                        estado.current_playlist_index = 0
                        print("Música detenida y cola limpiada.")
                    elif event.key == pygame.K_RETURN:
                        if estado.creditos > 0:
                            if estado.indice_cancion < len(estado.lista_canciones):
                                ruta_cancion = os.path.join(
                                    os.path.dirname(imagenes[estado.indice_imagen]), 
                                    estado.lista_canciones[estado.indice_cancion])
                                # Descontar crédito ANTES de agregar a playlist
                                estado.creditos = max(0, estado.creditos - 1)
                                agregar_a_playlist(ruta_cancion, estado)
                                print(f"Crédito descontado. Créditos restantes: {estado.creditos}")
                        else:
                            print("No tienes créditos suficientes para reproducir la canción.")
                    elif event.key == pygame.K_SPACE:
                        # Pausar/reanudar
                        if estado.reproduciendo:
                            pygame.mixer.music.pause()
                            estado.reproduciendo = False
                        else:
                            pygame.mixer.music.unpause()
                            estado.reproduciendo = True
                    elif event.key == pygame.K_n:
                        # Siguiente canción
                        if estado.playlist and estado.current_playlist_index < len(estado.playlist) - 1:
                            estado.current_playlist_index += 1
                            reproducir_cancion(estado.playlist[estado.current_playlist_index], estado)
                    elif event.key == pygame.K_b:
                        # Canción anterior
                        if estado.playlist and estado.current_playlist_index > 0:
                            estado.current_playlist_index -= 1
                            reproducir_cancion(estado.playlist[estado.current_playlist_index], estado)
                    elif event.key == pygame.K_h:
                        pygame.mixer.music.stop()
                
                # Teclas globales
                if event.key == pygame.K_m:
                    estado.mostrar_grid = True
                    estado.vista_actual = "Principal"
                    estado.reiniciar_temporizador()
                elif event.key == pygame.K_c:
                    estado.creditos += 1
                    estado.mostrar_creditos = not estado.mostrar_creditos
                # elif event.key == pygame.K_q:
                    # estado.playlist_visible = not estado.playlist_visible
            
            # Reiniciar temporizador también con eventos de mouse
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                estado.reiniciar_temporizador()
        
        # Dibujar la escena
        VENTANA.blit(background, (0, 0))
        
        if estado.mostrar_grid:
            dibujar_grid(VENTANA, imagenes_cargadas, current_page, selected_index, estado,
                        fuente_principal, fuente_titulo, fuente_creditos, moneda_creditos, teclas)
        else:
            dibujar_lista_canciones(VENTANA, estado, imagenes, fuente_principal, fuente_titulo,
                                  fuente_canciones, fuente_creditos, moneda_creditos, teclas)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()