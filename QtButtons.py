from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Polygon import *
from Algorithm import *
from PyQt5.QtWidgets import QFileDialog

import time

class Mode:
    def processMousePressEvent(self, event):
        pass

    def processPaintEvent(self, event, painter):
        pass

    def processMouseReleaseEvent(self, event):
        pass

    def processMouseMoveEvent(self, event):
        pass

    def processTimerEvent(self):
        pass

    def blockButtons(self):
        pass

    def unblockButtons(self):
        pass

class CreatePolygonMode(Mode):

    class Button:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.text = button.text()
            self.button.clicked.connect(self.processClick)

        def inverseState(self):
            self.mode.isProcessing = not self.mode.isProcessing
            return self.mode.isProcessing

        def processClick(self):           
            isProcessing = self.inverseState()
            if isProcessing:
                self.mode.polygon = Polygon()
                self.button.setText("Finish")
                self.mode.app.blockButtons()
                self.unblock()
            else:
                self.button.setText(self.text)
                self.mode.app.unblockButtons()
                self.mode.appendPolygon(self.button.text() == "Create robot")

        def block(self):
            self.button.setEnabled(False)

        def unblock(self):
            self.button.setEnabled(True)

    def __init__(self, app, createRobotButton, createObstacleButton):
        self.app = app
        self.polygon = None
        self.isProcessing = False
        self.createRobotButton = CreatePolygonMode.Button(createRobotButton, self)
        self.createObstacleButton = CreatePolygonMode.Button(createObstacleButton, self)

    def appendPolygon(self, isCreate):
        msg = checkPolygon(self.polygon)
        if msg:
            print(msg)
        else:
            if isCreate:
                self.app.initRobot(self.polygon)
            else:
                self.app.polygons.append(self.polygon)
            self.app.buildVisibilityMap()
            self.app.updateMinkowski()
        self.polygon = None
        self.app.update()

    def processMousePressEvent(self, event):
        if self.isProcessing:
            self.polygon.addPoint(self.app.scaleQPoint(event.pos()))
            self.app.update()

    def processPaintEvent(self, event, painter):
        if self.polygon:
            self.app.drawPoints(painter, self.polygon.points)
            self.app.drawPolygon(painter, self.polygon)

    def blockButtons(self):
        self.createRobotButton.block()
        self.createObstacleButton.block()

    def unblockButtons(self):
        self.createRobotButton.unblock()
        self.createObstacleButton.unblock()

class MovePolygonMode(Mode):

    class Button:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def inverseState(self):
            self.mode.isMoving = not self.mode.isMoving
            return self.mode.isMoving

        def processClick(self):           
            isMoving = self.inverseState()
            if isMoving:              
                self.button.setText("Stop drag")
                self.mode.selectedItem = self.mode.app.robot
                self.mode.app.blockButtons()
                self.unblock()    
            else:
                self.mode.app.unblockButtons()
                self.button.setText("Drag robot")
                self.mode.selectedItem = None

        def block(self):
            self.button.setEnabled(False)

        def unblock(self):
            self.button.setEnabled(True)


    def __init__(self, app, button):
        self.app = app
        self.polygon = None
        self.isMoving = False
        self.selectedItem = None
        self.button = MovePolygonMode.Button(button, self)

    def processMousePressEvent(self, event):
        if self.selectedItem:
            self.startPos = event.pos()
            self.itemStartPoints = self.selectedItem.points.copy()

    def processMouseMoveEvent(self, event):
        if self.isMoving:
            delta = event.pos() - self.startPos
            newPoints = []
            for i in range(len(self.selectedItem.points)):
                point = self.app.scaleQPoint(delta + self.app.scalePoint(self.itemStartPoints[i]))
                if not (-100 <= point[0] <= 100) or not (-100 <= point[1] <= 100):
                    return
                newPoints.append(point)
            self.selectedItem.points = newPoints
            self.app.update()

    def blockButtons(self):
        self.button.block()

    def unblockButtons(self):
        self.button.unblock()

class MinsowskiMode(Mode):

    class Button:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def inverseState(self):
            self.mode.state = (self.mode.state + 1) % 3
            return self.mode.state

        def processClick(self):           
            state = self.inverseState()
            if state == 0:              
                self.button.setText("Normal")
            elif state == 1:
                self.button.setText("Minkowski")
            elif state == 2:
                self.button.setText("Combined")
            self.mode.update()


    def __init__(self, app, button):
        self.app = app
        self.state = 0
        self.createRobotButton = MinsowskiMode.Button(button, self)

    def update(self):
        self.app.updateMinkowski(self.state)
        self.app.update()

class MapMode(Mode):

    class ShowButton:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def inverseState(self):
            self.mode.isEnabled = not self.mode.isEnabled
            return self.mode.isEnabled

        def processClick(self):           
            isEnabled = self.inverseState()
            if isEnabled:              
                self.button.setText("Hide map")
            else:
                self.button.setText("Show Map")
            self.mode.update()

    def __init__(self, app, showButton):
        self.app = app
        self.isEnabled = False
        self.showButton = MapMode.ShowButton(showButton, self)

    def build(self):
        self.app.buildVisibilityMap()
 
    def update(self):
        self.app.mapEnabled = self.isEnabled
        self.app.update()

class FindPathMode(Mode):

    class Button:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def inverseState(self):
            self.mode.state = not self.mode.state
            return self.mode.state

        def block(self):
            self.button.setEnabled(False)

        def unblock(self):
            self.button.setEnabled(True)

        def processClick(self):           
            state = self.inverseState()
            if state:
                self.mode.app.blockButtons()
                self.unblock()        
                self.button.setText("Disable path finding")
            else:
                self.mode.app.unblockButtons()
                self.mode.app.additionalMap
                self.mode.app.movementPath = None
                self.mode.shift = 0
                self.mode.lastPoint = None
                self.button.setText("Enable path finding")
            self.mode.update()


    def __init__(self, app, button, logArea):
        self.app = app
        self.state = False
        self.button = FindPathMode.Button(button, self)
        self.logArea = logArea
        self.shift = 0
        self.lastPoint = None

    def pathLength(self, path):
        length = 0.0
        for i in range(len(path) - 1):
            length += math.sqrt(dist(path[i], path[i + 1]))
        return round(length, 5)

    def processMousePressEvent(self, event):
        if self.state and self.app.movementPath is None:
            dest = self.app.scaleQPoint(event.pos())
            src = self.app.robot.center()
            dest = (round(dest[0], 2), round(dest[1], 2))
            src = (round(src[0], 2), round(src[1], 2))
            INF = self.app.getPlotRange()
            robot = self.app.robot.centered()
            minsowski = []
            for polygon in self.app.polygons:
                minsowski.append(Polygon(MinkowskiSum(robot.points, polygon.points)))
            graph = additionalVisibilityGraph(dest, src, minsowski, INF)
            graph.extend(additionalVisibilityGraph(src, dest, minsowski, INF))
            self.app.additionalMap = graph
            minsowskiSegment = unitePolygons([polygon.points for polygon in minsowski])
            path = Dijkstra(self.app.pathMap + 
                            self.app.additionalMap + 
                            minsowskiSegment, 
                            src, dest)

            self.app.movementPath = path
            if path:
                length = self.pathLength(path)
                self.logArea.append("Path found!\nLength: " + str(length))
                self.lastPoint = (-path[-1][0],-path[-1][1])
            else:
                self.app.additionalMap = None
                self.app.movementPath = None
                self.logArea.append("Wrong destination.")
        self.update()

    def update(self):
        self.app.update()

    def blockButtons(self):
        self.button.block()

    def unblockButtons(self):
        self.button.unblock()

    def aff(self, p1, p2, t):
        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])
        return (-x, -y)

    def processTimerEvent(self):
        if self.state:
            path = self.app.movementPath
            robot = self.app.robot
            if path:
                point = None
                if (len(path) > 1):
                    if self.shift >= 0.999:
                        self.shift = 0
                        path.pop(0)
                        point = robot.inversed().center()
                    else:
                        point = self.aff(path[0], path[1], self.shift)
                        self.shift += 0.1 / math.sqrt(dist(path[0], path[1]))
                if point:
                    self.app.robot = robot.centered(False).replaced(point)
                elif self.lastPoint:
                    self.app.additionalMap = None
                    self.app.movementPath = None
                    self.app.robot = robot.centered(False).replaced(self.lastPoint)
                    self.lastPoint = None
            self.update()

    
class ExampleMode(Mode):
    class SaveButton:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def save(self):
             fileName = QFileDialog().getSaveFileName(self.mode.app, "Save file", "test")[0]
             if not fileName:
                 return
             polygons = self.mode.app.polygons
             lines = self.mode.app.robot.export()
             lines += str(len(polygons)) + "\n"
             for polygon in polygons:
                 lines += polygon.export()
             open(fileName, "w").writelines(lines)

        def processClick(self):
            self.save()
            self.mode.update()

        def block(self):
            self.button.setEnabled(False)

        def unblock(self):
            self.button.setEnabled(True)

    class LoadButton:
        def __init__(self, button, mode):
            self.button = button
            self.mode = mode
            self.button.clicked.connect(self.processClick)

        def load(self):
            try:
                fileName = QFileDialog().getOpenFileName(self.mode.app, "Open file", "test")[0]
                if not fileName:
                     return
                self.lines = open(fileName, "r").readlines()
                self.readIndex = 0
                self.mode.app.robot = self.readPolygon()
                polygonCount = int(self.read())
                self.mode.app.polygons.clear()
                for i in range(polygonCount):
                    self.mode.app.polygons.append(self.readPolygon())
                self.mode.app.buildVisibilityMap()
            except:
                print("Wrong file.")

        def read(self):
            data = self.lines[self.readIndex].rstrip()
            self.readIndex += 1
            return data

        def readPolygon(self):
            pointCount = int(self.read())
            points = []
            for i in range(pointCount):
                line = self.read().split()
                x, y = float(line[0]), float(line[1])
                points.append((x, y))
            return Polygon(points)

        def processClick(self):
            self.load()
            self.mode.update()

        def block(self):
            self.button.setEnabled(False)

        def unblock(self):
            self.button.setEnabled(True)


    def __init__(self, app, saveButton, loadButton):
        self.app = app
        self.saveButton = ExampleMode.SaveButton(saveButton, self)
        self.loadButton = ExampleMode.LoadButton(loadButton, self)
 
    def update(self):
        self.app.update()

    def blockButtons(self):
        self.saveButton.block()
        self.loadButton.block()

    def unblockButtons(self):
        self.saveButton.unblock()
        self.loadButton.unblock()