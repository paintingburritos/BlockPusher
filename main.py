import pygame

from room import Room
from world import World
from leveldat import worldData
from levelSelect import levelSelect
import os

#Pygame init
pygame.init()

#Screen setup
screen = pygame.display.set_mode((640,640))
screen.fill((27, 28, 51))
pygame.display.set_caption("BlockPusher")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

#setting up the world (contains all rooms)
world1 = World(worldData)

#creating level select object
levelSel = levelSelect(world1)

def draw_menu(window): #draws and updates the menu screen
  window.blit(pygame.image.load("assets/mainMenu.png"), (0, 0))
  pygame.display.update()




#main loop
running = True
while running:
  for event in pygame.event.get():
    draw_menu(screen)
    if event.type == pygame.QUIT:
      running = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_1: # play
        flag = levelSel.loop(screen) # runs level select screen, and then takes its flag
        if flag == "main":
          draw_menu(screen)
        elif flag == "quit":
          running = False

      elif event.key == pygame.K_2: # tutorial
        pass
      elif event.key == pygame.K_3: # editor
        pass
      elif event.key == pygame.K_4: #quit
        running = False

pygame.quit()
