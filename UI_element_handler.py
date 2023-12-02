import pygame
from data_handler import *
from objects_handler import *

functions = {'Window'}

class Button():
    def __init__(self, text, bounding_box=(0, 0, 0, 0), function='None', icon=False):
        self.config = configs()

        self.functions = {
            'None' : "Selectable",
            'Window_Add' : self.window_add,
            'Add_Game_Object' : self.add_game_object
            }

        self.function = self.functions[function]
        self.icon = icon

        self.bounding_box = bounding_box
        self.state = self.config['primary_color']
        self.text = text

    def draw(self, win, font, padding=15):
        '''
        Draws the box of the button and any text
        Args:
            win::pygame.Surface
                This is the drawing location of the button
            font::text_handler.FontRenderer
                An instance of a font renderer class is needed to used the render_text function. Allows for quicker and easier text rendering
        '''
        pygame.draw.rect(win, self.state, self.bounding_box)
        if self.icon:
            font.render_text(win, (self.bounding_box[0] + self.bounding_box[2] / 2, self.bounding_box[1] + self.bounding_box[3] / 2), self.text, size=2, center_width=True)
        else:
            font.render_text(win, (self.bounding_box[0] + padding, self.bounding_box[1] + self.bounding_box[3] / 2), self.text, size=0)

    def hover(self):
        self.state = self.config['hover_color']
    def click(self):
        self.state = self.config['accent_color']
    def set_default(self):
        self.state = self.config['primary_color']

    def window_add(self, disp):
        disp.right_view = disp.add_display
    def add_game_object(self, disp):
        objects[f'GameObject {len(objects)}'] = GameObject()

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