import pygame
from data_handler import *

class Button():
    def __init__(self, bounding_box=()):
        self.config = configs()
        self.bounding_box = bounding_box
        self.state = self.config['primary_color']
        self.text = 'asdasd'

    def draw(self, win, font):
        pygame.draw.rect(win, self.state, self.bounding_box)
        font.render_text(win, (self.bounding_box[0] + 15, self.bounding_box[1] + self.bounding_box[3] / 2), self.text, size=0)

    def set_hover(self):
        self.state = self.config['hover_color']
    def set_selected(self):
        self.state = self.config['accent_color']
    def set_default(self):
        self.state = self.config['primary_color']

def draw_buttons(win, UI_elements, config, UI_button_elements, current_seletion, current_hover, font):
    for element in UI_elements:
        UI_elements[element].draw(win, font)