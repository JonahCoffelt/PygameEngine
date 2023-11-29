import pygame
from UI_element_handler import *
from data_handler import *
from text_handler import *
from dragable_handler import *
from displays_handler import Display
import objects_handler

class UI():
    def __init__(self):
        self.config = configs()
        self.win_size = (self.config["win_height"] * self.config["aspect_ratio"], self.config["win_height"])

        self.current_held_element = None
        self.selected_button = None
        self.selected_text = None
        
        self.mouse_pressed = False

        # Init handelers
        self.font = FontRenderer()
        self.disp = Display()
        self.drag = Dragable(self.win_size)

        # Init setup
        self.drag.define_UI_boxes(0, 0)
        self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
        self.disp.configure_displays(self.selected_button)

    def draw(self, win):
        '''
        Draws the viewframes from the Display class
        Draws the buttons from the UI_element_handler module
        '''
        self.disp.draw_displays(win)
        draw_buttons(win, self.disp.UI_elements, self.font)
        pygame.display.flip()
    
    def set_value(self, element):
        try:
            new_data = element.dtype(element.data)
            element.data = str(new_data)
            objects_handler.set_attribute(self.selected_button[0:-2], element.text, new_data)
        except ValueError:
            element.data = str(objects_handler.get_attribute(self.selected_button[0:-2], element.text))

    def UI_input(self):
        '''
        Handles mouse inputs
        Draging functions, such as the resizing of viewframes, are sent to the Dragable class
        Button functions are sent to the Display class
        '''
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        # Check for hover
        for element in self.disp.UI_elements:
            if type(self.disp.UI_elements[element]) == Button:
                bounding_box = self.disp.UI_elements[element].bounding_box
                if not self.disp.UI_elements[element].state == self.config['accent_color']:
                    if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                        self.disp.UI_elements[element].hover()
                    else:
                        self.disp.UI_elements[element].set_default()

        if pygame.mouse.get_pressed()[0]:
            if self.mouse_pressed:
                # Mouse Held
                self.drag.mouse_held(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays(self.selected_button)
            else:
                # Mouse Down
                self.mouse_pressed = True
                if self.selected_text and self.selected_text in self.disp.UI_elements:
                    self.set_value(self.disp.UI_elements[self.selected_text])
                self.drag.mouse_down(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays(self.selected_button)
        else:
            if self.mouse_pressed:
                # Mouse Released
                self.mouse_pressed = False
                update_disp = False
                for element in self.disp.UI_elements:
                    if type(self.disp.UI_elements[element]) == Button: 
                        bounding_box = self.disp.UI_elements[element].bounding_box
                        if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                            for element_other in self.disp.UI_elements:
                                if type(self.disp.UI_elements[element_other]) == Button: 
                                    self.disp.UI_elements[element_other].set_default()
                            update_disp = True
                            self.selected_button = element
                    elif type(self.disp.UI_elements[element]) == TextInput:
                        bounding_box = self.disp.UI_elements[element].bounding_box
                        if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                            for element_other in self.disp.UI_elements:
                                if type(self.disp.UI_elements[element_other]) == TextInput: 
                                    self.disp.UI_elements[element_other].deselect()
                            self.disp.UI_elements[element].select()
                            self.disp.UI_elements[element].data = ''
                            self.selected_text = element

                if update_disp:
                    self.disp.configure_displays(self.selected_button)
                    self.disp.UI_elements[self.selected_button].click()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.win_size = (event.w, event.h)
                self.drag.win_size = self.win_size
                self.drag.define_UI_boxes(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays(self.selected_button)
            if event.type == pygame.KEYDOWN: 
                if self.selected_text:
                    if self.selected_text in self.disp.UI_elements:
                        element = self.disp.UI_elements[self.selected_text]
                        if event.key == pygame.K_BACKSPACE: 
                            element.data = element.data[:-1]
                        elif event.key == 13: 
                            self.set_value(element)
                            self.selected_text = None
                            for element in self.disp.UI_elements:
                                if type(self.disp.UI_elements[element]) == TextInput: 
                                    self.disp.UI_elements[element].deselect()
                        else: 
                            element.data += event.unicode
        
        keys = pygame.key.get_pressed()