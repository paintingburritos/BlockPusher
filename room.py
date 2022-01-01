import copy # required to deepcopy nested arrays
import pygame
pygame.init()

# floorMap codes:
# 0 = Nothing
# 1 = Wall (inmoveable)
# 2 = Standard Pushable Block
# 3 = Objective Pushable Block
# 4 = Objective Goal (Solid)
# 5 = Objective Goal Completed (Solid) 
# 6 = Player teleport/spawn
# 7 = Player

#Note the player cannot move down

#Contains all floor data and player data (such as remain teleports)
class Room:
  def __init__(self, floorMap, devScore = 0):
    self.resetMap = copy.deepcopy(floorMap)
    
    
    #The number of remaining teleports
    self.teleports = 1

    #Spawn cords (0 incase none are found for debugging)
    self.spawnY = 0
    self.spawnX = 0
    #Player cords for simplicity
    self.playerY = 0
    self.playerX = 0

    #move counter
    self.moves = 0 # this value is incremented in world.py file


    #best by creator of the level (zero if no score is set)
    self.devScore = devScore

    #Find teleport spawn cordinates
    for i in range(len(self.resetMap)):
      for j in range(len(self.resetMap[0])):
        if self.resetMap[i][j] == 6:
          self.resetMap[i][j] = 7
          self.spawnY = i
          self.spawnX = j
          self.playerY = i
          self.playerX = j
    
    #creates the tempmap in which the player actually moves
    self.tempMap = copy.deepcopy(self.resetMap)

    #The number of remaining objectives (note same code as check(), but does not calculate teleports)
    self.objectives = 0
    for layer in self.tempMap:
      for e in layer:
        if e == 4:
          self.objectives += 1
    
  #Temporary draw function for debugging purposes
  def draw(self):
    for layer in self.tempMap:
      print(layer)
  
  #Updates the number of remaining objectives
  def check(self):
    initial = self.objectives
    self.objectives = 0
    for layer in self.tempMap:
      for e in layer:
        if e == 4:
          self.objectives += 1
    
    self.teleports += (initial - self.objectives)
    
  
  #Resets the room
  def reset(self):
    self.tempMap = copy.deepcopy(self.resetMap) #Resets map
    
    #Reset player cords
    self.playerX = self.spawnX
    self.playerY = self.spawnY
    
    self.check() # Resets objective count
    self.teleports = 1 # reset teleports
    self.moves = 0 #reset moves

  #Tries to pass a player action through, will do nothing if not possible
  def action(self, key):
    if key == "c": # teleport
      return self.teleport()
    elif key == "w": # up
      return self.moveUp()
    elif key == "d": # right
      return self.moveRight()
    elif key == "a": # left
      return self.moveLeft()
    elif key == "r": # reset
      self.reset()
    else:
      print("Invalid Input")

  #teleports player to start
  def teleport(self):
    if self.teleports > 0:  
      self.tempMap[self.playerY][self.playerX] = 0
      
      self.playerY = self.spawnY
      self.playerX = self.spawnX

      self.tempMap[self.playerY][self.playerX] = 7

      self.teleports -= 1
      return True
    else:
      return False
    
  def moveUp(self):
    if self.playerY == 0: # border
      return False
    
    tileUp = self.tempMap[self.playerY - 1][self.playerX]

    if tileUp == 0 or tileUp == 6: # if nothing solid above
      self.tempMap[self.playerY][self.playerX] = 0
      self.playerY -= 1
      self.tempMap[self.playerY][self.playerX] = 7
      return True
    elif tileUp == 1 or tileUp == 4 or tileUp == 5: # if immovable object
      return False
    
    elif tileUp == 2 or tileUp == 3: # if pushable object
      if self.playerY == 1: # if the block will hit the top wall
        return False
    

    if tileUp == 2: # standard block
      if self.tempMap[self.playerY - 2][self.playerX] == 0:
        self.tempMap[self.playerY - 2][self.playerX] = 2
        self.tempMap[self.playerY - 1][self.playerX] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerY -= 1

        return True
      
    elif tileUp == 3: # objective block
      if self.tempMap[self.playerY - 2][self.playerX] == 0: # if nothing
        self.tempMap[self.playerY - 2][self.playerX] = 3
        self.tempMap[self.playerY - 1][self.playerX] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerY -= 1

        return True
      elif self.tempMap[self.playerY - 2][self.playerX] == 4: # if objective block
        self.tempMap[self.playerY - 2][self.playerX] = 5
        self.tempMap[self.playerY - 1][self.playerX] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerY -= 1

        return True

  def moveRight(self):
    if self.playerX == len(self.tempMap[0]) - 1:
      return False

    tileRight = self.tempMap[self.playerY][self.playerX + 1]
    
    if tileRight == 0 or tileRight == 6: # blanks
      self.tempMap[self.playerY][self.playerX] = 0
      self.playerX += 1
      self.tempMap[self.playerY][self.playerX] = 7
      return True
    elif tileRight == 1 or tileRight == 4 or tileRight == 5: #immovables
      return False
    elif tileRight == 2 or tileRight == 3: #moveables
      if self.playerX == len(self.tempMap[0]) - 2: #if block will hit right wall
        return False

    if tileRight == 2: #standard block
      if self.tempMap[self.playerY][self.playerX + 2] == 0:
        self.tempMap[self.playerY][self.playerX + 2] = 2
        self.tempMap[self.playerY][self.playerX + 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX += 1
        return True
      
    elif tileRight == 3: # objective block
      if self.tempMap[self.playerY][self.playerX + 2] == 0: # if nothing
        self.tempMap[self.playerY][self.playerX + 2] = 3
        self.tempMap[self.playerY][self.playerX + 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX += 1
        
        return True
      elif self.tempMap[self.playerY][self.playerX + 2] == 4: # if objective block
        self.tempMap[self.playerY][self.playerX + 2] = 5
        self.tempMap[self.playerY][self.playerX + 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX += 1
        return True

  def moveLeft(self):
    if self.playerX == 0: # border
      return False
    tileLeft = self.tempMap[self.playerY][self.playerX - 1]
    
    if tileLeft == 0 or tileLeft == 6: # blanks
      self.tempMap[self.playerY][self.playerX] = 0
      self.playerX -= 1
      self.tempMap[self.playerY][self.playerX] = 7
      return True
    elif tileLeft == 1 or tileLeft == 4 or tileLeft == 5: #immovables
      return False
    elif tileLeft == 2 or tileLeft == 3: #moveables
      if self.playerX == 1: #if block will hit left wall
        return False

    if tileLeft == 2: #standard block
      if self.tempMap[self.playerY][self.playerX - 2] == 0:
        self.tempMap[self.playerY][self.playerX - 2] = 2
        self.tempMap[self.playerY][self.playerX - 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX -= 1

        return True
      
    elif tileLeft == 3: # objective block
      if self.tempMap[self.playerY][self.playerX - 2] == 0: # if nothing
        self.tempMap[self.playerY][self.playerX - 2] = 3
        self.tempMap[self.playerY][self.playerX - 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX -= 1

        return True
      elif self.tempMap[self.playerY][self.playerX - 2] == 4: # if objective block
        self.tempMap[self.playerY][self.playerX - 2] = 5
        self.tempMap[self.playerY][self.playerX - 1] = 7
        self.tempMap[self.playerY][self.playerX] = 0

        self.playerX -= 1

        return True

  #Returns a tilemap which refers to tile numbers in assets/tiles/sprite(n).png (needed to place spawns on maps)
  def tile(self):
    tilemap = copy.deepcopy(self.tempMap)
    
    if tilemap[self.spawnY][self.spawnX] == 7:
      tilemap[self.spawnY][self.spawnX] = 8
    else:
      tilemap[self.spawnY][self.spawnX] = 6
    
    return tilemap

  #Drawing code below this
  def draw_tiles(self, window):
    for i, layer in enumerate(self.tile()):
      for j, ele in enumerate(layer):
        window.blit(pygame.image.load("assets/tiles/sprite" + str(ele) + ".png"), (j * 64, i * 64))

  def draw_teleports(self,window): # draws teleports, and other text below
    window.blit(pygame.image.load("assets/text/teleport.png"),(0, 576))
    
    #drawing teleport number
    teleports = str(self.teleports)
    if len(teleports) == 1:
      teleports = "0" + teleports

    window.blit(pygame.image.load("assets/text/number" + teleports[0] + ".png"), (316, 580))
    window.blit(pygame.image.load("assets/text/number" + teleports[1] + ".png"), (332, 580))

    #drawing move number
    moves = str(self.moves)
    if len(moves) == 1:
      moves = "00" + moves
    elif len(moves) == 2:
      moves = "0" + moves

    window.blit(pygame.image.load("assets/text/number" + moves[0] + ".png"), (300, 608))
    window.blit(pygame.image.load("assets/text/number" + moves[1] + ".png"), (316, 608))
    window.blit(pygame.image.load("assets/text/number" + moves[2] + ".png"), (332, 608))


    #drawing dev score
    devScore = str(self.devScore)

    if len(devScore) == 1:
      devScore = "00" + devScore
    elif len(devScore) == 2:
      devScore = "0" + devScore
    
    window.blit(pygame.image.load("assets/text/number" + devScore[0] + ".png"), (572, 580))
    window.blit(pygame.image.load("assets/text/number" + devScore[1] + ".png"), (588, 580))
    window.blit(pygame.image.load("assets/text/number" + devScore[2] + ".png"), (604, 580))
    
  



