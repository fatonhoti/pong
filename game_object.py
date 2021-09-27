class GameObject():

    def __init__(self, x, y, dx, dy):
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
    
    def step(self):
        self.x += self.dx
        self.y += self.dy
    
    def updateSpeed(self, dx, dy):
        self.dx += dx
        self.dy += dy
