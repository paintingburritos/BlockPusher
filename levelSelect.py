import pygame
import copy
pygame.init()

#levelSelcect Manages the world object
#It is easier to have the world object deal with formating the data, and levelSelect for choosing the levels

class levelSelect:
  def __init__(self, world):
    self.currentWorld = 0
    self.world = copy.deepcopy(world)

  def change(self, n): #increments currentWorld counter by n
    if (self.currentWorld + n < 0) or (self.currentWorld + n > len(self.world.rooms) - 1): # if the new world be out of index range for our worlds room list
      pass
    else:
      self.currentWorld += n

  def draw(self, window):
    window.fill((79,103,129))
    #minimap display
    tilemap = self.world.rooms[self.currentWorld].tile()
    for i, layer in enumerate(tilemap):
      for j, ele in enumerate(layer):
        window.blit(pygame.image.load("assets/levelSelect/miniTiles/spriteMini" + str(ele) + ".png"), ((j * 16 + 304), (i * 16 + 304)))
    
    #drawing main level screen ontop
    window.blit(pygame.image.load("assets/levelSelect/levelSelect.png"), (0, 0))
    
    # level counter
    levelN = self.currentWorld + 1
    levelN = str(levelN)
    #blanks if it is a one digit number
    if len(levelN) == 1:
      levelN = "B" + levelN
    
    window.blit(pygame.image.load("assets/levelSelect/numbers/num" + str(levelN[0]) + ".png"), (416,236))
    window.blit(pygame.image.load("assets/levelSelect/numbers/num" + str(levelN[1]) + ".png"), (432,236))

    #dev score counter

    devScore = str(self.world.rooms[self.currentWorld].devScore)

    if len(devScore) == 1:
      devScore = "00" + devScore
    elif len(devScore) == 2:
      devScore = "0" + devScore

    window.blit(pygame.image.load("assets/levelSelect/numbers/num" + str(devScore[0]) + ".png"), (452, 492))
    window.blit(pygame.image.load("assets/levelSelect/numbers/num" + str(devScore[1]) + ".png"), (468, 492))
    window.blit(pygame.image.load("assets/levelSelect/numbers/num" + str(devScore[2]) + ".png"), (484, 492))


    #(452,492) 
     
      

  def loop(self, window): # main loop which controls all of the actions
    running = True
    self.draw(window)
    pygame.display.update()
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit game
          return "quit"
      
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE: # back to main menu
            return "main"
          
          elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: # enter level
            self.world.load(self.currentWorld)
            flag = self.world.play(window) # run the game and save the returned flag
            if flag == "quit":
              return "quit"
            
            elif flag == "levelSelect": # if the player chooses to return to level select
              self.world.pass_action("r") # resets view on screen as tile() returns the tempMap not the reset map

              self.draw(window)
              pygame.display.update()
            
          #changes selected level and redraws it
          elif event.key == pygame.K_RIGHT:
            self.change(1)
            self.draw(window)
            pygame.display.update()
          elif event.key == pygame.K_LEFT:
            self.change(-1)
            self.draw(window)
            pygame.display.update()
        




