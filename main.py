import pygame
from pygame import font
from UI_handler import *
from sprite_sheets import *
from data_handler import *
import objects_handler

class Engine():
    def __init__(self):
        '''
        Creates classes and pygame instances
        '''
        self.config = configs()
        self.sprites = generate_sprite_sheets(self.config['tile_size'])
        
        self.win = pygame.display.set_mode((self.config["win_height"] * self.config["aspect_ratio"], self.config["win_height"]), pygame.RESIZABLE)
        pygame.display.set_caption("2D Engine")
        self.clock = pygame.time.Clock()     
        
        for i in range(10):
            objects_handler.objects[f'GameObject {i}'] = objects_handler.GameObject()

        self.UI = UI()

    def update(self):
        '''
        Clears the screen and draws all UI
        '''
        self.win.fill((100, 100, 100))
        self.UI.draw(self.win)
        pygame.display.flip()

    def start_app(self):
        '''
        Starts the engine
        Currently, this starts the runtime loop
        FPS is locked at 60 (Subject to future change)
        '''
        self.run = True
        while self.run:
            self.dt = self.clock.tick(60) / 1000
            self.UI.UI_input()
            self.update()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    engine = Engine()
    engine.start_app()