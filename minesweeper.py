import pygame                                           
from pygame.constants import (                          
    QUIT, KEYDOWN, K_q, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
)
import os
import random


class Settings(object):    
    def __init__(self): 
        self.brick_width = 16
        self.brick_height = 16
        self.width = 640
        self.height = 320
        self.fps = 60       
        self.title = "Minesweeper" 
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.file_path, "images")
        self.map_path = os.path.join(self.file_path, "map")

    def get_dim(self):
        return (self.width, self.height)

class Game(object): 
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()
        self.bombs = 25
        self.done = False
        self.bricks = {}
        self.place_bricks()
        self.place_base()
        self.placeBombs()
        self.place_bombs()

    def run(self):  
        while not self.done:                            
            self.clock.tick(self.settings.fps)          
            for event in self.pygame.event.get():       
                if event.type == QUIT:                 
                    self.done = True 
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        self.done = True   
            self.draw()

    def place_base(self):
        map = []
        firstline = True
        with  open(os.path.join(self.settings.map_path, "base.map"), "r") as file:
            for line in file:
                if firstline:
                    self.columns = int(line.split(" ")[0])
                    self.rows = int(line.split(" ")[1])
                    firstline = False
                else:
                    map.append(line.split((" ")))
        self.base = map

    def place_bricks(self):
        self.bricks.clear()
        base = self.pygame.image.load(os.path.join(self.settings.image_path, "leer_voll.jpg")).convert()
        bomb = self.pygame.image.load(os.path.join(self.settings.image_path, "miene.jpg")).convert()
        self.bricks[1] = base
        self.bricks[2] = bomb

    def draw_base(self):
        for i in range(self.rows):
            for y in range(self.columns):
                self.screen.blit(self.bricks[1],(y*self.settings.brick_width,i*self.settings.brick_height))

    def placeBombs(self):
        self.bombsY = []
        self.bombsX = []
        oldColumn = 0
        oldRow = 0
        bombplace = self.bombs
        while bombplace > 0:
            row = random.randint(0,(self.rows -1))
            column = random.randint(0,(self.columns - 1))
            if oldColumn != column and oldRow != row:
                self.bombsX.append(column)
                self.bombsY.append(row)
                oldColumn = column
                oldRow = row
                bombplace -= 1
        print(self.bombsX, self.bombsY)

    def place_bombs(self):
        x = 0
        y = 0
        for i in range (len(self.bombsX)):
            x += 1
            y += 1
            for j in range (len(self.bombsY)):               
                self.screen.blit(self.bricks[2], (self.bombsX[x - 1]*self.settings.brick_width, self.bombsY[y -1]*self.settings.brick_height))

    def draw(self):
        self.draw_base()
        self.place_bombs()
        self.pygame.display.flip()



    #def restart():
      #  game()
      #  restart = input("Would you like to play again? Please enter '1' for YES or '2' for NO: ")
        #while restart == 1:
        #    game()
         #   print restart
       # else:
            #print "Thanks for playing!"



if __name__ == '__main__':     
    settings = Settings()
    pygame.init()              
    game = Game(pygame, settings)
    game.run()  
    pygame.quit()              

