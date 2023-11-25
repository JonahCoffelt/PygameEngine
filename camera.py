class EngineCamera():
    def __init__(self):
        self.x = 0
        self.y = 0

        self.speed = 1
        self.view = 1
    
    def move(self, dt, delta_x, delta_y):
        self.x += delta_x * self.speed * dt
        self.y += delta_y * self.speed * dt

class PlayerCamera():
    def __init__(self, target):
        self.target = target
        self.x = target.x
        self.y = target.y

        self.speed = 1
        self.view = 1