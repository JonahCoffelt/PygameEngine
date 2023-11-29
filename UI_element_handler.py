import pygame
from data_handler import *

class Button():
    def __init__(self, text, bounding_box=(0, 0, 0, 0)):
        self.config = configs()

        self.function = None

        self.bounding_box = bounding_box
        self.state = self.config['primary_color']
        self.text = text

    def draw(self, win, font):
        '''
        Draws the box of the button and any text
        Args:
            win::pygame.Surface
                This is the drawing location of the button
            font::text_handler.FontRenderer
                An instance of a font renderer class is needed to used the render_text function. Allows for quicker and easier text rendering
        '''
        pygame.draw.rect(win, self.state, self.bounding_box)
        font.render_text(win, (self.bounding_box[0] + 15, self.bounding_box[1] + self.bounding_box[3] / 2), self.text, size=0)

    def hover(self):
        self.state = self.config['hover_color']
    def click(self):
        self.state = self.config['accent_color']
    def set_default(self):
        self.state = self.config['primary_color']

    def game_object_func(self):
        pass

class TextInput():
    def __init__(self, text, dtype, data, bounding_box=(0, 0, 0, 0)) -> None:
        self.config = configs()

        self.text = text
        self.data = str(data)
        self.dtype = dtype
        self.bounding_box = bounding_box
        self.state = self.config['hover_color']

    def deselect(self):
        self.state = self.config['hover_color']
    def select(self):
        self.state = self.config['accent_color']

    def draw(self, win, font):
        '''
        Draws the box of the title and text
        Args:
            win::pygame.Surface
                This is the drawing location of the button
            font::text_handler.FontRenderer
                An instance of a font renderer class is needed to used the render_text function. Allows for quicker and easier text rendering
        '''
        pygame.draw.rect(win, self.state, self.bounding_box)
        font.render_text(win, (self.bounding_box[0] + 15, self.bounding_box[1] + self.bounding_box[3] / 2), self.text + ': '+str(self.data), size=0)
    

class Title():
    def __init__(self, text, bounding_box=(0, 0, 0, 0)) -> None:
        self.config = configs()

        self.text = text
        self.bounding_box = bounding_box

    def draw(self, win, font):
        '''
        Draws the box of the title and text
        Args:
            win::pygame.Surface
                This is the drawing location of the button
            font::text_handler.FontRenderer
                An instance of a font renderer class is needed to used the render_text function. Allows for quicker and easier text rendering
        '''
        pygame.draw.rect(win, self.config['hover_color'], self.bounding_box)
        font.render_text(win, (self.bounding_box[0] + 15, self.bounding_box[1] + self.bounding_box[3] / 2), self.text, size=1)


def draw_buttons(win, UI_elements, font):
    '''
    Draws the buttons in the UI elements. This function is subject to change with the implamentation of new UI element types
    Args:
        win::pygame.Surface
            This is sent to the Button.draw function. See help(Button.draw) for more info
        UI_elements::dict
            Constains all UI elements to be drawn.
        font::text_handler.FontRenderer
            This is sent to the Button.draw function. See help(Button.draw) for more info
    '''
    for element in UI_elements:
        UI_elements[element].draw(win, font)