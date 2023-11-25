import pygame
from button_handler import *
from data_handler import *
from text_handler import *
from displays_handler import Display
from objects_handler import objects as objs

class UI():
    def __init__(self):
        self.config = configs()

        self.UI_hold_elements = {}
        self.UI_button_elements = {}
        self.UI_elements = {}
        self.mouse_pressed = False
        self.current_seletion = None

        self.font = FontRenderer()
        self.disp = Display(self.UI_button_elements, self.UI_elements)

        self.left_margin = .25
        self.right_margin = .20
        self.bottom_margin = .35
        self.top_margin = .065

        self.define_UI_boxes((self.config["win_height"] * self.config["aspect_ratio"], self.config["win_height"]))
        self.disp.configure_displays()
        self.current_held_element = None
    
    def define_UI_boxes(self, win_size):
        self.win_size = win_size
        self.right_box = (win_size[0] - win_size[0] * self.right_margin, win_size[1] * self.top_margin, win_size[0] * self.right_margin, win_size[1] - win_size[1] * self.top_margin)
        self.left_box = (0, win_size[1] * self.top_margin, win_size[0] * self.left_margin, win_size[1] - win_size[1] * self.bottom_margin - win_size[1] * self.top_margin)
        self.bottom_box = (0, win_size[1] - win_size[1] * self.bottom_margin, win_size[0] - win_size[0] * self.right_margin, win_size[1] * self.bottom_margin)
        self.top_box = (0, 0, win_size[0], win_size[1] * self.top_margin)

        hold_box_margin = 16
        self.UI_hold_elements[self.drag_right_bar] = (self.right_box[0] - hold_box_margin/2, self.right_box[1], hold_box_margin, self.right_box[3])
        self.UI_hold_elements[self.drag_left_bar] = (self.left_box[2] - hold_box_margin/2, self.left_box[1], hold_box_margin, self.left_box[3])
        self.UI_hold_elements[self.drag_bottom_bar] = (0, self.bottom_box[1] - hold_box_margin/2, self.bottom_box[2], hold_box_margin)

        self.disp.define_viewframes(self.left_box, self.right_box, self.bottom_box, self.top_box)
        self.disp.configure_displays()

    def draw(self, win):
        self.disp.draw_displays(win)
        draw_buttons(win, self.UI_elements, self.config, self.UI_button_elements, self.current_seletion, 0, self.font)
        pygame.display.flip()
        

    def UI_input(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        for element in self.UI_elements:
            bounding_box = self.UI_elements[element].bounding_box
            if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                self.UI_elements[element].set_hover()
            else:
                self.UI_elements[element].set_default()

        if pygame.mouse.get_pressed()[0]:
            if self.mouse_pressed:
                # Mouse Held
                if self.current_held_element:
                    self.current_held_element()
            else:
                # Mouse Mouse Down
                self.mouse_pressed = True
                self.current_held_element = None
                for element in self.UI_hold_elements:
                    bounding_box = self.UI_hold_elements[element]
                    if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                        self.current_held_element = element
                        self.startX, self.startY = self.mouseX, self.mouseY
                        self.org_pos = self.right_margin
        else:
            if self.mouse_pressed:
                # Mouse Released
                self.mouse_pressed = False
                for element in self.UI_elements:
                    bounding_box = self.UI_elements[element].bounding_box
                    if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                        self.UI_elements[element].set_selected()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.define_UI_boxes((event.w, event.h))
        
        keys = pygame.key.get_pressed()
    
    def drag_right_bar(self):
        new_pos = 1 - self.mouseX / self.win_size[0]
        if new_pos > .02:
            self.right_margin = new_pos
            self.define_UI_boxes(self.win_size)
    def drag_left_bar(self):
        new_pos = self.mouseX / self.win_size[0]
        if new_pos > .02:
            self.left_margin = new_pos
            self.define_UI_boxes(self.win_size)
    def drag_bottom_bar(self):
        new_pos = 1 - self.mouseY / self.win_size[1]
        if new_pos > .02:
            self.bottom_margin = new_pos
            self.define_UI_boxes(self.win_size)
