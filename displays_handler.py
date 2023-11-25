import pygame
import objects_handler
from data_handler import *
from button_handler import *

class Display():
    def __init__(self, buttons, UI_elements):
        self.config = configs()
        self.left_view = self.objects
        #self.bottom_view = self.files
        #self.right_view = self.add
        self.padding = 10
        self.buttons = buttons
        self.UI_elements = UI_elements
    
    def define_viewframes(self, left, right, bottom, top):
        self.left_viewframe = left
        self.right_viewframe = right
        self.bottom_viewframe = bottom
        self.top_viewframe = top

    def draw_displays(self, win):
        # Fill UI Sections
        pygame.draw.rect(win, self.config['primary_color'], self.right_viewframe)
        pygame.draw.rect(win, self.config['primary_color'], self.left_viewframe)
        pygame.draw.rect(win, self.config['primary_color'], self.bottom_viewframe)
        pygame.draw.rect(win, self.config['secondary_color'], self.top_viewframe)

        # Outline UI Sections
        pygame.draw.rect(win, 'black', self.right_viewframe, 1)
        pygame.draw.rect(win, 'black', self.left_viewframe, 1)
        pygame.draw.rect(win, 'black', self.bottom_viewframe, 1)
        pygame.draw.rect(win, 'black', self.top_viewframe, 1)

    def configure_displays(self):
        self.left_view(self.left_viewframe)
        #self.bottom_view(win)
        #self.right_view(win)

    def objects(self, viewframe):
        height = 25
        std_height = height
        padding = 0
        if len(objects_handler.objects) * (height + self.padding) > viewframe[3]:
            height = (viewframe[3] / len(objects_handler.objects)) - self.padding

        self.buttons['+'] = (viewframe[0] + 15, viewframe[1] + 15, std_height, std_height)
        
        for i, obj_key in enumerate(objects_handler.objects):
            self.buttons[obj_key] = (viewframe[0] + 1, viewframe[1] + (padding + height) * (i) + std_height * 2, viewframe[2] - 2, height)
            self.UI_elements[obj_key] = Button((viewframe[0] + 1, viewframe[1] + (padding + height) * (i) + std_height * 2, viewframe[2] - 2, height))
