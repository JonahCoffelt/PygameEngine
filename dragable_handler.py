

class Dragable():
    def __init__(self, win_size):
        # Basic viewframe bounds
        self.left_margin = .20
        self.right_margin = .30
        self.bottom_margin = .35
        self.top_margin = .065

        self.win_size = win_size
        self.UI_drag_elements = {}

        self.current_held_element = None
    
    def mouse_held(self, mouseX, mouseY):
        self.mouseX, self.mouseY = mouseX, mouseY

        if self.current_held_element:
            self.current_held_element()
    
    def mouse_down(self, mouseX, mouseY):
        self.mouseX, self.mouseY = mouseX, mouseY
        self.current_held_element = None

        for element in self.UI_drag_elements:
            bounding_box = self.UI_drag_elements[element]
            if bounding_box[0] < self.mouseX < bounding_box[0] + bounding_box[2] and bounding_box[1] < self.mouseY < bounding_box[1] + bounding_box[3]:
                self.current_held_element = element
                self.startX, self.startY = self.mouseX, self.mouseY
                self.org_pos = self.right_margin

    def define_UI_boxes(self, mouseX, mouseY):
        self.mouseX, self.mouseY = mouseX, mouseY

        self.right_box = (self.win_size[0] - self.win_size[0] * self.right_margin, self.win_size[1] * self.top_margin, self.win_size[0] * self.right_margin, self.win_size[1] - self.win_size[1] * self.top_margin)
        self.left_box = (0, self.win_size[1] * self.top_margin, self.win_size[0] * self.left_margin, self.win_size[1] - self.win_size[1] * self.bottom_margin - self.win_size[1] * self.top_margin)
        self.bottom_box = (0, self.win_size[1] - self.win_size[1] * self.bottom_margin, self.win_size[0] - self.win_size[0] * self.right_margin, self.win_size[1] * self.bottom_margin)
        self.top_box = (0, 0, self.win_size[0], self.win_size[1] * self.top_margin)

        drag_box_margin = 16
        self.UI_drag_elements[self.drag_right_bar] = (self.right_box[0] - drag_box_margin/2, self.right_box[1], drag_box_margin, self.right_box[3])
        self.UI_drag_elements[self.drag_left_bar] = (self.left_box[2] - drag_box_margin/2, self.left_box[1], drag_box_margin, self.left_box[3])
        self.UI_drag_elements[self.drag_bottom_bar] = (0, self.bottom_box[1] - drag_box_margin/2, self.bottom_box[2], drag_box_margin)
    
    def drag_right_bar(self):
        new_pos = 1 - self.mouseX / self.win_size[0]
        if new_pos > .02:
            self.right_margin = new_pos
            self.define_UI_boxes(self.mouseX, self.mouseY)
    def drag_left_bar(self):
        new_pos = self.mouseX / self.win_size[0]
        if new_pos > .02:
            self.left_margin = new_pos
            self.define_UI_boxes(self.mouseX, self.mouseY)
    def drag_bottom_bar(self):
        new_pos = 1 - self.mouseY / self.win_size[1]
        if new_pos > .02:
            self.bottom_margin = new_pos
            self.define_UI_boxes(self.mouseX, self.mouseY)