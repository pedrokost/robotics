# A Map class containing walls
class Map:
    def __init__(self, canvas):
        self.walls = [];
	self.canvas = canvas

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def draw(self):
        for wall in self.walls:
            self.canvas.drawLine(wall);
