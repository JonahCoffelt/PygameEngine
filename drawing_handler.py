import pygame

import objects_handler

class Draw():

    def __init__(self):
        self.grid_size = 10

    def config(self, win_size, right_margin, left_margin, top_margin, bottom_margin, cam):
        self.win_size, self.right_margin, self.left_margin, self.top_margin, self.bottom_margin, self.cam = win_size, right_margin, left_margin, top_margin, bottom_margin, cam

    def draw_grids(self, win):
        self.grid_size = (self.win_size[0] - (self.left_margin + self.right_margin) * self.win_size[0]) / self.cam.zoom
        for i in range(self.cam.zoom + 1):
            pygame.draw.line(win, (25, 25, 25), (self.grid_size * (self.cam.x - int(self.cam.x)) + self.win_size[0] * self.left_margin + i * self.grid_size, self.win_size[1] * self.top_margin), (self.grid_size * (self.cam.x - int(self.cam.x)) + self.win_size[0] * self.left_margin + i * self.grid_size, self.win_size[1] * self.top_margin + (self.win_size[1] - (self.top_margin + self.bottom_margin) * self.win_size[1])))
        for i in range(int((self.win_size[0] - (self.left_margin + self.right_margin) * self.win_size[0]) / self.grid_size) + 1):
            pygame.draw.line(win, (25, 25, 25), (self.win_size[0] * self.left_margin, self.grid_size * (self.cam.y - int(self.cam.y)) + i * self.grid_size + self.win_size[1] * self.top_margin), (self.win_size[0] - self.win_size[0] * self.right_margin, self.grid_size * (self.cam.y - int(self.cam.y)) + i * self.grid_size + self.win_size[1] * self.top_margin))

    def draw_game_objects(self, win, objects):
        for object_key in objects:
            obj = objects[object_key]
            if type(obj) == objects_handler.GameObject:
                #print(obj.x)
                pygame.draw.rect(win, obj.color, (self.left_margin * self.win_size[0] + (obj.x + self.cam.x) * self.grid_size, self.top_margin * self.win_size[1] + (-obj.y + self.cam.y) * self.grid_size, self.grid_size * obj.w, self.grid_size * obj.h))


    def draw_selection_gizmos(self, win, obj):
        pygame.draw.circle(win, (0, 150, 255), (self.left_margin * self.win_size[0] + (obj.x + self.cam.x) * self.grid_size + obj.w / 2 * self.grid_size, self.top_margin * self.win_size[1] + (-obj.y + self.cam.y) * self.grid_size + obj.h / 2 * self.grid_size), 5)
