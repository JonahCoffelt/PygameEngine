import pygame
from UI_element_handler import *
from data_handler import *
from text_handler import *
from dragable_handler import *
from displays_handler import Display
import objects_handler
from camera import EngineCamera
from drawing_handler import Draw

class UI():
    def __init__(self):
        self.config = configs()
        self.win_size = (self.config["win_height"] * self.config["aspect_ratio"], self.config["win_height"])

        self.current_held_element = None
        self.selected_button = None
        self.selected_text = None
        
        self.mouse_pressed = False
        self.mouse_held = False
        self.obj_start = None
        self.obj_width_start = None
        self.obj_height_start = None

        # Init handelers
        self.font = FontRenderer()
        self.disp = Display()
        self.drag = Dragable(self.win_size)
        self.cam = EngineCamera()
        self.drawer = Draw()

        # Init setup
        self.drag.define_UI_boxes(0, 0)
        self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
        self.disp.configure_displays(self.selected_button)
        self.drawer.config(self.win_size, self.drag.right_margin, self.drag.left_margin, self.drag.top_margin, self.drag.bottom_margin, self.cam)

    def draw(self, win):
        '''
        Draws the viewframes from the Display class
        Draws the buttons from the UI_element_handler module
        '''

        self.drawer.draw_grids(win)
        self.drawer.draw_game_objects(win, objects)
        if self.selected_button:
            if type(objects[self.selected_button[:-2]]) == GameObject:
                self.drawer.draw_selection_gizmos(win, objects[self.selected_button[:-2]])
        
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
        self.mouse_world_x, self.mouse_world_y = ((self.mouseX - self.win_size[0] * self.drag.left_margin - self.drawer.grid_size * self.cam.x) / self.drawer.grid_size, 1-(self.mouseY - self.win_size[1] * self.drag.top_margin - self.drawer.grid_size * self.cam.y) / self.drawer.grid_size)
        keys = pygame.key.get_pressed()
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
                if self.obj_start != None:
                    self.moving_obj.x = self.obj_start[0] + (int(self.mouse_world_x) - self.start[0])
                    if self.mouse_world_x < 0 and self.start[0] > 0:
                        self.moving_obj.x -= 1
                    elif self.mouse_world_x > 0 and self.start[0] < 0:
                        self.moving_obj.x += 1
                    self.moving_obj.y = self.obj_start[1] + (int(self.mouse_world_y) - self.start[1])
                    if self.mouse_world_y < 0 and self.start[1] > 0:
                        self.moving_obj.y -= 1
                    elif self.mouse_world_y > 0 and self.start[1] < 0:
                        self.moving_obj.y += 1

                if self.obj_width_start != None:
                    self.moving_obj.w = self.obj_width_start[0] + (int(self.mouse_world_x) - self.start[0])
                    if self.mouse_world_x < 0 and self.start[0] > 0:
                        self.moving_obj.w -= 1
                    elif self.mouse_world_x > 0 and self.start[0] < 0:
                        self.moving_obj.w += 1
                if self.obj_height_start != None:
                    self.moving_obj.h = self.obj_height_start[1] - (int(self.mouse_world_y) - self.start[1])
                    if self.mouse_world_y < 0 and self.start[1] > 0:
                        self.moving_obj.h -= 1
                    elif self.mouse_world_y > 0 and self.start[1] < 0:
                        self.moving_obj.h += 1
                self.mouse_held = True
                self.drag.mouse_held(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays(self.selected_button)
                self.drawer.config(self.win_size, self.drag.right_margin, self.drag.left_margin, self.drag.top_margin, self.drag.bottom_margin, self.cam)

            else:
                # Mouse Down
                self.mouse_pressed = True
                self.obj_start = None
                self.obj_width_start = None
                self.obj_height_start = None
                if not keys[pygame.K_SPACE] and self.win_size[0] * self.drag.left_margin < self.mouseX < self.win_size[0]- self.win_size[0] * self.drag.right_margin and self.win_size[1] * self.drag.top_margin < self.mouseY < self.win_size[1] - self.win_size[1] * self.drag.bottom_margin:
                    for element in objects_handler.objects:
                        obj = objects_handler.objects[element]
                        if type(obj) == GameObject:
                            if self.selected_button == element + '-l':
                                if obj.x < self.mouse_world_x < obj.x + obj.w and obj.y - obj.h + 1 < self.mouse_world_y < obj.y + 1:
                                    self.moving_obj = obj
                                    self.obj_start = (obj.x, obj.y)
                                    self.start = (int(self.mouse_world_x), int(self.mouse_world_y))
                                elif obj.x + 1 < self.mouse_world_x < obj.x + obj.w + 1 and obj.y - obj.h + 1 < self.mouse_world_y < obj.y + 1:
                                    self.moving_obj = obj
                                    self.obj_width_start = (obj.w, obj.h)
                                    self.start = (int(self.mouse_world_x), int(self.mouse_world_y))
                                elif obj.x < self.mouse_world_x < obj.x + obj.w and obj.y - obj.h < self.mouse_world_y < obj.y:
                                    self.moving_obj = obj
                                    self.obj_height_start = (obj.w, obj.h)
                                    self.start = (int(self.mouse_world_x), int(self.mouse_world_y))
                            
                if self.selected_text and self.selected_text in self.disp.UI_elements:
                    self.set_value(self.disp.UI_elements[self.selected_text])
                self.drag.mouse_down(self.mouseX, self.mouseY)
                self.disp.define_viewframes(self.drag.left_box, self.drag.right_box, self.drag.bottom_box, self.drag.top_box)
                self.disp.configure_displays(self.selected_button)
        else:
            if self.mouse_pressed:
                # Mouse Released
                self.mouse_pressed = False
                self.mouse_held = False
                update_disp = False
                config_disp = False
                if not keys[pygame.K_SPACE] and self.win_size[0] * self.drag.left_margin < self.mouseX < self.win_size[0]- self.win_size[0] * self.drag.right_margin and self.win_size[1] * self.drag.top_margin < self.mouseY < self.win_size[1] - self.win_size[1] * self.drag.bottom_margin:
                    for element in objects_handler.objects:
                        obj = objects_handler.objects[element]
                        if type(obj) == GameObject:
                            if obj.x < self.mouse_world_x < obj.x + obj.w and obj.y - obj.h + 1 < self.mouse_world_y < obj.y + 1:
                                self.selected_button = element + '-l'
                                self.disp.right_view = self.disp.inspector_display
                                self.disp.configure_displays(self.selected_button)
                                self.disp.UI_elements[self.selected_button].click()
                else:
                    for element in self.disp.UI_elements:
                        if type(self.disp.UI_elements[element]) == Button: 
                            bounding_box = self.disp.UI_elements[element].bounding_box
                            if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                                for element_other in self.disp.UI_elements:
                                    if type(self.disp.UI_elements[element_other]) == Button: 
                                        self.disp.UI_elements[element_other].set_default()
                                if self.disp.UI_elements[element].function == "Selectable":
                                    update_disp = True
                                    self.selected_button = element
                                else:
                                    self.disp.UI_elements[element].function(self.disp)
                                    config_disp = True

                        elif type(self.disp.UI_elements[element]) == TextInput:
                            bounding_box = self.disp.UI_elements[element].bounding_box
                            if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                                for element_other in self.disp.UI_elements:
                                    if type(self.disp.UI_elements[element_other]) == TextInput: 
                                        self.disp.UI_elements[element_other].deselect()
                                self.disp.UI_elements[element].select()
                                self.disp.UI_elements[element].data = ''
                                self.selected_text = element

                    if config_disp:
                        self.disp.configure_displays(self.selected_button)

                    if update_disp:
                        self.disp.right_view = self.disp.inspector_display
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
                self.drawer.config(self.win_size, self.drag.right_margin, self.drag.left_margin, self.drag.top_margin, self.drag.bottom_margin, self.cam)
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
            if event.type == pygame.MOUSEWHEEL:
                if self.win_size[0] * self.drag.left_margin < self.mouseX < self.win_size[0]- self.win_size[0] * self.drag.right_margin and self.win_size[1] * self.drag.top_margin < self.mouseY < self.win_size[1] - self.win_size[1] * self.drag.bottom_margin:
                    self.cam.zoom += event.y
        
        if self.win_size[0] * self.drag.left_margin < self.mouseX < self.win_size[0]- self.win_size[0] * self.drag.right_margin and self.win_size[1] * self.drag.top_margin < self.mouseY < self.win_size[1] - self.win_size[1] * self.drag.bottom_margin:
            if keys[pygame.K_SPACE]:
                if self.mouse_pressed:
                    if self.mouse_held == False:
                        self.camera_start = (self.cam.x, self.cam.y)
                        self.start = (self.mouseX, self.mouseY)
                    else:
                        self.cam.x = self.camera_start[0] + (self.mouseX - self.start[0]) / self.drawer.grid_size
                        self.cam.y = self.camera_start[1] + (self.mouseY - self.start[1]) / self.drawer.grid_size
