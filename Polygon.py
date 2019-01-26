from QtColors import *

class Polygon:
    def __init__(self, points=None, color=None):
        if not points:
            points = []
        if not color:
            color = getColor()
        self.points = points
        self.color = Color(color, 0.75)

    def replaced(self, center):
        points = []
        for point in self.points:
            points.append((point[0] - center[0], point[1] - center[1]))
        return Polygon(points, self.color)

    def inversed(self):
        polygon = Polygon(self.points.copy())
        polygon.color = self.color
        for i in range(len(polygon.points)):
            polygon.points[i] = (-polygon.points[i][0], -polygon.points[i][1])
        return polygon

    def getSegments(self):
        segments = []
        for i in range(len(self.points) - 1):
            segments.append((self.points[i], self.points[i + 1]))
        segments.append((self.points[-1], self.points[0]))
        return segments

    def centered(self, inv=True):
        if inv:
            polygon = self.inversed()
        else:
            polygon = Polygon(self.points, self.color)
        center = polygon.center()
        return polygon.replaced(center)

    def center(self):
        x, y = 0, 0
        for point in self.points:
            x += point[0]
            y += point[1]
        return (x / len(self.points), y / len(self.points))

    def addPoint(self, point):
        self.points.append(point)

    def export(self):
        data = str(len(self.points)) + "\n"
        for point in self.points:
            data += "{} {}\n".format(*point)
        return data
