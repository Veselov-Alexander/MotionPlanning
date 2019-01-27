from PyQt5.QtCore import *
from PyQt5.QtGui import *
from QtColors import *
from Algorithm import *
from Polygon import *

WINDOW_SIZE = float(600)

class QCanvas:   
    def __init__(self):
        self.scale = 0.05
        self.plot_size = 200.0

    def getPlotRange(self):
        return round(self.plot_size * self.scale, 1)

    def scaleQPoint(self, point):
        plotRange = self.getPlotRange()
        x = point.x() * 2 * plotRange / WINDOW_SIZE - plotRange
        y = -(point.y() * 2 * plotRange / WINDOW_SIZE - plotRange)
        return (x, y)

    def scalePoint(self, point):
        plotRange = self.getPlotRange()
        x = point[0] / (2 * plotRange) * WINDOW_SIZE + WINDOW_SIZE / 2
        y = -(point[1] / (2 * plotRange) * WINDOW_SIZE - WINDOW_SIZE / 2)
        return QPoint(x, y)

    def updateScale(self, event):
        plotRange = self.getPlotRange()
        if event.angleDelta().y() > 0:
            if plotRange > 11:
                self.scale -= 0.05
        else:
            if plotRange < 99:
                self.scale += 0.05
        self.update()

    def drawPlot(self, painter):
        painter.drawRect(0, 0, WINDOW_SIZE, WINDOW_SIZE)        
        self.drawPlotRange(painter)

        return     
        painter.drawLine(QLine(WINDOW_SIZE / 2, 0,
                               WINDOW_SIZE / 2, WINDOW_SIZE)) # vertical line

        painter.drawLine(QLine(0, WINDOW_SIZE / 2,
                               WINDOW_SIZE, WINDOW_SIZE / 2)) # horisontal line
        self.drawArrows(painter)

    def drawArrows(self, painter):
        
        dx, dy = 5, 15
        upArrow = QPolygonF([
            QPoint(WINDOW_SIZE / 2, 0),
            QPoint(WINDOW_SIZE / 2 + dx, dy),
            QPoint(WINDOW_SIZE / 2 - dx, dy),
            ])

        rightArrow = QPolygonF([
            QPoint(WINDOW_SIZE, WINDOW_SIZE / 2),
            QPoint(WINDOW_SIZE - dy, WINDOW_SIZE / 2 + dx),
            QPoint(WINDOW_SIZE - dy, WINDOW_SIZE / 2 - dx),
            ])

        self.drawFilledPolygon(painter, upArrow)
        self.drawFilledPolygon(painter, rightArrow)

    def drawPlotRange(self, painter):
        plotRange = self.getPlotRange()
        painter.drawText(10, WINDOW_SIZE - 10,
                        "Plot range: [{}, {}]".format(-plotRange, plotRange))

    def drawPolygon(self, painter, polygon, isRobot=False):
        polygonF = QPolygonF()
        brush = Brush(polygon.color, 0.6)
        if isRobot:
            brush.setStyle(Qt.Dense2Pattern)
        painter.setBrush(brush)
        for point in polygon.points:
            polygonF.append(self.scalePoint(point))
        self.drawFilledPolygon(painter, polygonF, brush)

    def drawFilledPolygon(self, painter, polygon, brush=Qt.black):
        path = QPainterPath()
        path.addPolygon(polygon)
        painter.fillPath(path, brush)

    def drawPoints(self, painter, points):
        painter.setPen(Pen(Qt.black, 0.8))
        painter.setBrush(Brush(Qt.black, 0.8))
        for point in points:
            painter.drawEllipse(self.scalePoint(point), 3, 3)

    def drawBorder(self, painter):
        painter.setPen(Pen(Qt.lightGray, 1, 1))
        painter.setBrush(Brush(Qt.lightGray, 1))
        painter.drawRect(WINDOW_SIZE, 0, WINDOW_SIZE, WINDOW_SIZE)

    def drawRobotPoint(self, painter, robot):
        painter.setPen(Pen(Qt.black, 1, 1))
        painter.setBrush(Brush(Qt.black, 1))
        point = self.scalePoint(robot.center())
        r = 4
        painter.drawEllipse(QRect(point - QPoint(r, r), QSize(2 * r, 2 * r)))

    def drawMap(self, painter, pathMap, color):
        painter.setPen(Pen(color, 0.6, 1))
        painter.setBrush(Brush(color, 0.6))
        if pathMap:
            for segment in pathMap:
                start = self.scalePoint(segment[0])
                end = self.scalePoint(segment[1])
                painter.drawLine(QLine(start, end))

    def drawPath(self, painter, movementPath):
        painter.setPen(Pen(Qt.black, 0.6, 2))
        if movementPath:
            for i in range(len(movementPath) - 1):
                start = self.scalePoint(movementPath[i])
                end = self.scalePoint(movementPath[i + 1])
                painter.drawLine(QLine(start, end))
