from room import Room
import copy
import pygame
pygame.init()


class World:
  def __init__(self, rooms):
    self.rooms = rooms
    self.lastStates = []

    self.current = 0
  
  def load(self, level):
    self.current = level
    self.rooms[self.current].reset()
    self.lastStates = []
  
  #reverts to last state in puzzle
  def undo(self):
    if len(self.lastStates) != 0:
      self.rooms[self.current] = copy.deepcopy(self.lastStates[-1])
      del self.lastStates[-1]
    else:
      pass
  
  #gets the current room and returns its state
  def get_current(self):
    return self.rooms[self.current]
  
  #passes an action through and stores last state into undo list
  def pass_action(self,action):
    if action == "r":
      self.lastStates = []
      self.rooms[self.current].action(action)
    else:
      oldRoom = copy.deepcopy(self.rooms[self.current])

      if self.rooms[self.current].action(action): # if the action goes through in the Room() object
        self.lastStates.append(oldRoom)
        self.rooms[self.current].moves += 1

  def win(self, window): # returns level select after showing win screen
    window.blit(pygame.image.load("assets/win/winScreen.png"), (0, 0)) #drawing win screen
    
    #Displaying number of moves for solution
    moves = str(self.get_current().moves)
    if len(moves) == 1:
      moves = "00" + moves
    elif len(moves) == 2:
      moves = "0" + moves
    
    window.blit(pygame.image.load("assets/win/win" + moves[0] + ".png"), (336, 268))
    window.blit(pygame.image.load("assets/win/win" + moves[1] + ".png"), (352, 268))
    window.blit(pygame.image.load("assets/win/win" + moves[2] + ".png"), (368, 268))


    pygame.display.update()
    while True: # infinite loop until an option is selected
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return "quit"
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RIGHT:
            return "next"
          elif event.key == pygame.K_BACKSPACE:
            return "levelSelect"
          elif event.key == pygame.K_r:
            return "reset"

  #Plays the current room and draws to a given window
  def play(self, window): 
    #inital drawing
    window.fill((79, 103, 129))
    self.get_current().draw_tiles(window)
    self.get_current().draw_teleports(window)
    pygame.display.update()

    #main loops for games
    paused = False
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return "quit"
      
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            paused = not paused
            if paused:
              window.blit(pygame.image.load("assets/text/pause.png"), (0,0))
              pygame.display.update()
          
          if not paused:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
              self.pass_action("a")
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
              self.pass_action("w")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
              self.pass_action("d")
            elif event.key == pygame.K_c:
              self.pass_action("c")
            elif event.key == pygame.K_r:
              self.pass_action("r")
            elif event.key == pygame.K_z:
              self.undo()

            self.get_current().check()

            window.fill((79, 103, 129))
            self.get_current().draw_tiles(window)
            self.get_current().draw_teleports(window)
            pygame.display.update()
          else: # if in paused state
            if event.key == pygame.K_BACKSPACE:
              self.pass_action("r")
              return "levelSelect"

          if self.get_current().objectives == 0: # win condition
            
            
            winFlag = self.win(window)
            if winFlag == "reset":
              self.pass_action("r")
              
              #resets screen
              window.fill((79, 103, 129))
              self.get_current().draw_tiles(window)
              self.get_current().draw_teleports(window)
              pygame.display.update()

            elif winFlag == "levelSelect":
              return "levelSelect"
            
            elif winFlag == "quit":
              return "quit"

            elif winFlag == "next":
              if self.current == len(self.rooms) - 1: # if there is no next level
                return "levelSelect"
              else: # if there is a next level
                self.get_current().reset()
                
                self.current += 1
                self.load(self.current)
                
                #resets screen
                window.fill((79, 103, 129))
                self.get_current().draw_tiles(window)
                self.get_current().draw_teleports(window)
                pygame.display.update()

              
              