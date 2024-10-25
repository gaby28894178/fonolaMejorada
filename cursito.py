import pygame
import sys
from pygame.locals import *


pygame.init()
fps = 18
fpsClock = pygame.time.Clock()

#ventana creacion
ventana = pygame.display.set_mode((400,300),0,32)
pygame.display.set_caption("ventana1")


color = (255,255,255)

imagen = pygame.image.load("n.png")
imagenx = 0
imageny= 0
direction = "right"


while True:
    ventana.fill((0,0,0))
    if direction == "right":
        imagenx +=15
        if imagenx >= 280:
            direction = 'down'
            
    elif direction == "down":
        imageny += 25
        if imageny >=120:
            direction ="left"
            
    elif direction == "left":
        imagenx -= 8
        if imagenx <= 10:
            direction = "up"
            
    elif direction == "up":
        imageny -=5
        if imageny <= 10:
            direction = "right"
    ventana.blit(imagen,(imagenx,imageny))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(fps)






    
            
    



        
