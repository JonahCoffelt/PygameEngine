objects = {}

def set_attribute(obj, attrib, value):
    object = objects[obj]
    if attrib == 'x':
        object.x = value
    if attrib == 'y':
        object.y = value
    if attrib == 'z':
        object.z = value
    if attrib == 'w':
        object.w = value
    if attrib == 'h':
        object.h = value
    if attrib == 'θ':
        object.θ = value
    if attrib == 'r':
        if value > 255.0:
            value = 255.0
        if value < 0.0:
            value = 0.0
        object.color[0] = value
    if attrib == 'g':
        if value > 255.0:
            value = 255.0
        if value < 0.0:
            value = 0.0
        object.color[1] = value
    if attrib == 'b':
        if value > 255.0:
            value = 255.0
        if value < 0.0:
            value = 0.0
        object.color[2] = value

def get_attribute(obj, attrib):
    object = objects[obj]
    if attrib == 'x':
        return(object.x)
    if attrib == 'y':
        return(object.y)
    if attrib == 'z':
        return(object.z)
    if attrib == 'w':
        return(object.w)
    if attrib == 'h':
        return(object.h)
    if attrib == 'θ':
        return(object.θ)
    if attrib == 'r':
        return(object.color[0])
    if attrib == 'g':
        return(object.color[1])
    if attrib == 'b':
        return(object.color[2])

class Objects():
    def __init__(self):
        self.objects = {}

class GameObject():
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0, h=1.0, θ=0.0):
        self.attributes = ['position', 'size', 'rotation', 'color', 'components']
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.θ = θ
        self.color = [0, 0, 0]
        self.components = {}

class Camera():
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.attributes = ['position', 'target', 'components']
        self.x = x
        self.y = y
        self.z = z
        self.components = {}

class Player():
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.attributes = ['position', 'size', 'rotation', 'color', 'components']
        self.x = x
        self.y = y
        self.z = z
        self.components = {}

class TileMap():
    def __init__(self):
        self.attributes = ['map']
        self.map = []
        self.components = {}

def get_game_objects():
    return objects

def set_game_object(key, value):
    objects[key] = value