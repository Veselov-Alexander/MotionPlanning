import sys
import QtBuildGUI

from QtGUI import *
from QtCanvas import *
from QtButtons import *
from PyQt5.QtWidgets import *
from QtColors import averageColor

class MotionPlanningWindow(QMainWindow, Ui_MainWindow, QCanvas):
    def __init__(self):
        super().__init__()    
        self.setupUi(self)
        QCanvas.__init__(self)
        self.initModes()
        self.polygons = []
        self.minsowskiMode = 0
        self.minkowskiSum = None
        self.robot = None
        self.mapEnabled = False
        self.pathMap = None
        self.additionalMap = None
        self.movementPath = None
        self.addTestPolygons()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(10)

    def addTestPolygons(self):
        from Polygon import Polygon
        self.robot = Polygon([(-1, 0), (0, -1), (1, 0), (0, 1)])
        #self.robot = Polygon(generateCircle(100, (-4, -4)))
        self.polygons = [
            #Polygon(generateCircle(100, (4, 4))),
            #Polygon([(2, 1), (5, 1), (5, 4), (2, 4)]),
            #Polygon([(-1, 3), (1, 0), (4, 2), (2, 4)]),
            #Polygon([(3, -4), (7, -3), (5.5, -2)]),
            #Polygon([(3, 4), (6, 3), (5, 2)]),
            ]
        self.buildVisibilityMap()

    def initModes(self):
        self.modes = [
            CreatePolygonMode(self, self.createRobotButton, self.createObstacleButton),
            MovePolygonMode(self, self.moveRobotButton),
            MinsowskiMode(self, self.minsowskiButton),
            MapMode(self, self.showMapButton),
            FindPathMode(self, self.findPathMode, self.logArea),
            ExampleMode(self, self.saveButton, self.loadButton),
            ]

    def updateMinkowski(self, state=None):
        if state is None:
            state = self.minsowskiMode
        else:
            self.minsowskiMode = state
        self.minkowskiSum = []
        for polygon in self.polygons:
            self.minkowskiSum.append(self.polygonMinkowski(polygon))

    def polygonMinkowski(self, polygon):
        robot = self.robot.centered()
        points = MinkowskiSum(robot.points, polygon.points)
        return Polygon(points, averageColor(robot.color, polygon.color))

    def blockButtons(self):
        for mode in self.modes:
            mode.blockButtons()

    def unblockButtons(self):
        for mode in self.modes:
            mode.unblockButtons()

    def timerEvent(self):
        for mode in self.modes:
            mode.processTimerEvent()

    def mousePressEvent(self, event):
        for mode in self.modes:
            mode.processMousePressEvent(event)

    def mouseReleaseEvent(self, event):
        for mode in self.modes:
            mode.processMouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        for mode in self.modes:
            mode.processMouseMoveEvent(event)

    def initRobot(self, robot):
        self.robot = robot

    def buildVisibilityMap(self):
        robot = self.robot.centered()
        minsowski = []
        for polygon in self.polygons:
            minsowski.append(Polygon(MinkowskiSum(robot.points, polygon.points)))
        segmentMap = visibilityGraph(minsowski, self.getPlotRange())
        self.pathMap = segmentMap

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)

        self.drawPlot(painter)

        for mode in self.modes:
            mode.processPaintEvent(event, painter)
  
        if self.minsowskiMode == 0:
            self.paintNormal(painter)
        elif self.minsowskiMode == 1:
            self.paintMinkowski(painter)
        elif self.minsowskiMode == 2:
            self.paintNormal(painter)
            self.paintMinkowski(painter)

        if self.mapEnabled:
            self.drawMap(painter, self.pathMap, Qt.red)
            self.drawMap(painter, self.additionalMap, Qt.blue)
        self.drawPath(painter, self.movementPath)

        self.drawBorder(painter)
        painter.end()

    def paintNormal(self, painter):
        for polygon in self.polygons:
            self.drawPolygon(painter, polygon)
        if self.robot:
            self.drawPolygon(painter, self.robot, True)

    def paintMinkowski(self, painter):
        if self.minkowskiSum:
            for polygon in self.minkowskiSum:
                self.drawPolygon(painter, polygon)
        self.drawRobotPoint(painter, self.robot)

    def wheelEvent(self, event):
        self.updateScale(event)

def main():
    app = QApplication(sys.argv)
    window = MotionPlanningWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()