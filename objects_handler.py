class Objects():
    def __init__(self):
        self.objects = {}

class GameObject():
    def __init__(self, x=0, y=0):
        self.attributes = ['possition', 'size', 'rotation', 'color', 'components']
        self.x = x
        self.y = y
        self.components = {}

class Camera():
    def __init__(self, x=0, y=0):
        self.attributes = ['possition', 'target', 'components']
        self.x = x
        self.y = y
        self.components = {}

class Player():
    def __init__(self, x=0, y=0):
        self.attributes = ['possition', 'size', 'rotation', 'color', 'components']
        self.x = x
        self.y = y
        self.components = {}

class TileMap():
    def __init__(self):
        self.attributes = ['map']
        self.map = []
        self.components = {}

objects = {}