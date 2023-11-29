import pygame
import objects_handler
from data_handler import *
from UI_element_handler import *


class Display():
    def __init__(self):
        # Load configurations from file
        self.config = configs()

        # Basic display functions
        self.left_view = self.game_objects_display
        self.bottom_view = self.game_objects_display
        self.right_view = self.inspector_display

        self.attribute_functions = {
            'position' : self.position,
            'size' : self.size,
            'rotation' : self.rotation,
            'color' : self.color,
            'components' : self.components,
            'target' : self.target
        }

        # 
        self.selected_button = None
        self.UI_elements = {}
    
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

    def configure_displays(self, selected_button):
        self.selected_button = selected_button
        self.left_view(self.left_viewframe, 'l')
        self.bottom_view(self.bottom_viewframe, 'b')
        self.right_view(self.right_viewframe, 'r')

    def game_objects_display(self, viewframe, side):
        # Basic Display Configs
        height = 25
        std_height = height
        padding = 0

        objects = objects_handler.get_game_objects()

        # Shrinks the button height if there are too many to display
        if len(objects) * (height + padding) > viewframe[3]:
            height = (viewframe[3] / len(objects)) - padding
        
        # Reads all the game objects and creates a UI element as a button for them
        for i, obj_key in enumerate(objects):
            self.UI_elements[f'{obj_key}-{side}'] = Button(f'{obj_key}', (viewframe[0] + 1, viewframe[1] + (padding + height) * (i) + std_height * 2, viewframe[2] - 2, height))

    def inspector_display(self, viewframe, side):
        title = "Inspector"
        if self.selected_button: title = self.selected_button[0:-2]
        self.UI_elements[f'inspector_title-{side}'] = Title(title, (viewframe[0] + 10, viewframe[1] + 10, viewframe[2] - 20, 50))
        if self.selected_button:
            objects = objects_handler.get_game_objects()
            self.clear_elements(side)
            attributes = objects[title].attributes
            for i, attribute in enumerate(attributes):
                self.attribute_functions[attribute](side, objects[title], viewframe[0] + 10, viewframe[1] + 70 + i  * 40, viewframe[2] - 20, 30)

    def clear_elements(self, side):
        if f'position_x-{side}' in self.UI_elements:
            self.UI_elements.pop(f'position_x-{side}')
        if f'position_y-{side}' in self.UI_elements:
            self.UI_elements.pop(f'position_y-{side}')
        if f'position_z-{side}' in self.UI_elements:
            self.UI_elements.pop(f'position_z-{side}')
        if f'size_w-{side}' in self.UI_elements:
            self.UI_elements.pop(f'size_w-{side}')
        if f'size_h-{side}' in self.UI_elements:
            self.UI_elements.pop(f'size_h-{side}')
        if f'rotation_θ-{side}' in self.UI_elements:
            self.UI_elements.pop(f'rotation_θ-{side}')
        if f'color_r-{side}' in self.UI_elements:
            self.UI_elements.pop(f'color_r-{side}')
        if f'color_g-{side}' in self.UI_elements:
            self.UI_elements.pop(f'color_g-{side}')
        if f'color_b-{side}' in self.UI_elements:
            self.UI_elements.pop(f'color_b-{side}')
        if f'Components-{side}' in self.UI_elements:
            self.UI_elements.pop(f'Components-{side}')

    def position(self, side, object, start_x, start_y, width, height):
        self.UI_elements[f'position_x-{side}'] = TextInput("x", float, object.x, bounding_box=(start_x + 2, start_y, width/3 - 4, height))
        self.UI_elements[f'position_y-{side}'] = TextInput("y", float, object.y, bounding_box=(start_x + width/3 + 2, start_y, width/3 - 4, height))
        self.UI_elements[f'position_z-{side}'] = TextInput("z", float, object.z, bounding_box=(start_x + width/3 * 2 + 2, start_y, width/3 - 4, height))
    
    def size(self, side, object, start_x, start_y, width, height):
        self.UI_elements[f'size_w-{side}'] = TextInput("w", float, object.w, bounding_box=(start_x + 2, start_y, width/2 - 4, height))
        self.UI_elements[f'size_h-{side}'] = TextInput("h", float, object.h, bounding_box=(start_x + width/2 + 2, start_y, width/2 - 4, height))
    
    def rotation(self, side, object, start_x, start_y, width, height):
        self.UI_elements[f'rotation_θ-{side}'] = TextInput("θ", float, object.θ, bounding_box=(start_x + 2, start_y, width - 4, height))
    
    def color(self, side, object, start_x, start_y, width, height):
        self.UI_elements[f'color_r-{side}'] = TextInput("r", float, object.color[0], bounding_box=(start_x + 2, start_y, width/3 - 4, height))
        self.UI_elements[f'color_g-{side}'] = TextInput("g", float, object.color[1], bounding_box=(start_x + width/3 + 2, start_y, width/3 - 4, height))
        self.UI_elements[f'color_b-{side}'] = TextInput("b", float, object.color[2], bounding_box=(start_x + width/3 * 2 + 2, start_y, width/3 - 4, height))
    
    def components(self, side, object, start_x, start_y, width, height):
        self.UI_elements[f'Components-{side}'] = Title('Components', (start_x, start_y, width, height))

    def target(self, side, object, start_x, start_y, width, height):
        pass
        #self.UI_elements[f'Components-{side}'] = Title('Components', (start_x, start_y, width/2, height))



    #def components_display()