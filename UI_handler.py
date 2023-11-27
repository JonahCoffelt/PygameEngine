import pygame
from UI_element_handler import *
from data_handler import *
from text_handler import *
from dragable_handler import *
from displays_handler import Display
from objects_handler import objects as objs

class UI():
    def __init__(self):
        self.config = configs()
        self.win_size = (self.config["win_height"] * self.config["aspect_ratio"], self.config["win_height"])

        self.current_held_element = None
        
        self.mouse_pressed = False

        # Init handelers
        self.font = FontRenderer()
        self.disp = Display()
        self.drag = Dragable(self.win_size)

        # Init setup
        self.drag.define_UI_boxes(0, 0)
        self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
        self.disp.configure_displays()

        print(help(FontRenderer.render_text))


    def draw(self, win):
        '''
        Draws the viewframes from the Display class
        Draws the buttons from the UI_element_handler module
        '''
        self.disp.draw_displays(win)
        draw_buttons(win, self.disp.UI_elements, self.font)
        pygame.display.flip()

    def UI_input(self):
        '''
        Handles mouse inputs
        Draging functions, such as the resizing of viewframes, are sent to the Dragable class
        Button functions are sent to the Display class
        '''
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        # Check for hover
        for element in self.disp.UI_elements:
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
                self.disp.configure_displays()
            else:
                # Mouse Down
                self.mouse_pressed = True
                self.drag.mouse_down(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays()
        else:
            if self.mouse_pressed:
                # Mouse Released
                self.mouse_pressed = False
                for element in self.disp.UI_elements:
                    bounding_box = self.disp.UI_elements[element].bounding_box
                    if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                        for element_other in self.disp.UI_elements:
                            self.disp.UI_elements[element_other].set_default()
                        self.disp.UI_elements[element].click()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.win_size = (event.w, event.h)
                self.drag.define_UI_boxes(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays()
        
        keys = pygame.key.get_pressed()