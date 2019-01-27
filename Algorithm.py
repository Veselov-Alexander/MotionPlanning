from decimal import *
from scipy.sparse.csgraph import shortest_path
from shapely.geometry import Point as SPoint, mapping
from shapely.ops import cascaded_union
from shapely.geometry.polygon import Polygon as SPolygon
from shapely.geometry import LineString as SLineString
from shapely.ops import triangulate
from sys import getsizeof
import numpy as np
import math
import time

getcontext().prec = 10

class Point:
    def __init__(self, x=0, y=0):
        self.x, self.y = Decimal(x), Decimal(y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, value):
        return self.y < value.y or self.y == value.y and self.x < value.x

    def toTuple(self):
        return (float(self.x), float(self.y))

def tupleToPoint(point):
    return Point(point[0], point[1])

def directConvertPoints(points):
    converted = []
    for point in points:
        converted.append(tupleToPoint(point))
    converted.append(converted[0])
    return converted

def reverseConvertPoints(points):
    converted = []
    for point in points:
        converted.append(point.toTuple())
    return converted

def indexOfMin(points):
    minIndex = 0
    for i, point in enumerate(points):
        if points[i] < points[minIndex]:
            minIndex = i
    return minIndex

def area(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - \
           (p2.y - p1.y) * (p3.x - p1.x)

def ccw(p1, p2, p3):
    return area(p1, p2, p3) >= 0

def inversedLine(line):
    p1, p2 = line[0], line[1]
    return ((-p1[0], -p1[1]), (-p2[0], -p2[1]))

def checkPolygon(polygon):
    if len(polygon.points) < 3:
        return "3 or more points are required to create a polygon."

    polygon = SPolygon(polygon.points)
    if not polygon.is_valid:
        return "Incorrect polygon."
    return None

def MinkowskiSum(first, second):
    startTime = time.time()
    n, m = len(first), len(second)
    first = SPolygon(first)
    second = SPolygon(second)

    mem = getsizeof(first) + getsizeof(second)
    fp = triangulate(first)
    sp = triangulate(second)

    mem += getsizeof(fp) + getsizeof(sp)
    fpp, spp = [], []

    for polygon in fp:
        points = list(mapping(polygon)["coordinates"][0][:-1])
        if first.contains(polygon):
            fpp.append(points)

    for polygon in sp:
        points = list(mapping(polygon)["coordinates"][0][:-1])
        if second.contains(polygon):
            spp.append(points)

    mem += getsizeof(fpp) + getsizeof(spp)
    sums = []
    for f in fpp:
        for s in spp:
            sums.append(ConvexMinkowskiSum(f, s))

    pp = []
    for polygon in sums:
        pp.append(SPolygon(polygon))

    result = cascaded_union(pp)

    mem += getsizeof(pp) + getsizeof(sums) + getsizeof(result)
    print("Minkowski sum (n={}, m={}): {:f} ms, {} bytes".format(n, m, (time.time() - startTime) * 1000, mem))
    return list(mapping(result)["coordinates"][0])[:-1]

def ConvexMinkowskiSum(first, second):
    n, m = len(first), len(second)
    p1, p2 = directConvertPoints(first), directConvertPoints(second)

    if not ccw(*p1[:3]):
        p1.reverse()
    if not ccw(*p2[:3]):
        p2.reverse() 

    i, j = indexOfMin(p1), indexOfMin(p2)
    u1, u2 = [False] * (n + 1), [False] * (m + 1)

    points = [p1[i] + p2[j]]

    while True:
        if i == n:
            i = 0
        if j == m:
            j = 0
        if u1[i] and u2[j]:
            break

        if (u1[i] or not u2[j] and (p1[i + 1].x - p1[i].x) * (p2[j + 1].y - p2[j].y) - 
                                   (p1[i + 1].y - p1[i].y) * (p2[j + 1].x - p2[j].x) < 0):
            points.append(points[-1] + (p2[j + 1] - p2[j]))
            u2[j] = True
            line = (p2[j].toTuple(), p2[j + 1].toTuple())      
            j += 1
        else:
            points.append(points[-1] + (p1[i + 1] - p1[i]))
            u1[i] = True;
            line = (p1[i].toTuple(), p1[i + 1].toTuple())
            i += 1

    return reverseConvertPoints(points)[:-1]

def dist(first, second):
    return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

def segmentOnPolygon(segment, polygon):
    segment = SLineString([segment[0], segment[1]])
    polygon = SPolygon(polygon)
    return not segment.touches(polygon) and segment.intersects(polygon)

def allIsUnited(spolygons):
    for i in range(len(spolygons)):
        for j in range(len(spolygons)):
            if i != j:
                first = spolygons[i]
                second = spolygons[j]
                if first.intersects(second):
                    spolygons.remove(first)
                    spolygons.remove(second)
                    spolygons.append(first.union(second))
                    return False
    return True

def unitePolygons(polygons):
    spolygons = []
    for polygon in polygons:
        spolygons.append(SPolygon(polygon))

    while not allIsUnited(spolygons):
        pass

    segements = []
    for polygon in spolygons:
        points = list(mapping(polygon)["coordinates"][0])
        for i in range(len(points) - 1):
            segements.append((points[i], points[i + 1]))
        segements.append((points[-1], points[0]))
    return segements

def isBlocked(segment, polygons):
    for polygon in polygons:
        if segmentOnPolygon(segment, polygon.points):
            return True
    return False

def polygonsToPoints(polygons, INF):
    points = []
    for polygon in polygons:    
        for point in polygon.points:
            points.append(point)
    points.extend([(INF, INF), (-INF, INF), (INF, -INF), (-INF, -INF),
                   (0, INF), (0, -INF), (-INF, 0), (INF, 0)])
    return points

def additionalVisibilityGraph(point, add, polygons, INF):
    points = polygonsToPoints(polygons, INF)
    points.extend([add])
    segments = []
    for i in range(len(points)):
        segment = (points[i], point)                    
        if not isBlocked(segment, polygons):
            segments.append(segment)
    return segments

def visibilityGraph(polygons, INF):
    points = polygonsToPoints(polygons, INF)
    count = len(points)
    segments = []
    for i in range(count):
        for j in range(i + 1, count):
            segment = (points[i], points[j])                    
            if not isBlocked(segment, polygons):
                segments.append(segment)
    return segments

def findInDict(dictionary, searchValue):
    for key, value in dictionary.items():
        if value == searchValue:
            return key

def isUnique(uniquePoints, point):
    EPS = 0.01
    for upoint in uniquePoints:
        if math.sqrt(dist(point, upoint)) < EPS:
            return False
    return True

def mapToPointSet(pathMap):
    uniquePoints = []
    for segment in pathMap:
        if isUnique(uniquePoints, segment[0]):
            uniquePoints.append(segment[0])
        if isUnique(uniquePoints, segment[1]):
            uniquePoints.append(segment[1])
    return uniquePoints

def Dijkstra(pathMap, src, dest):
    uniquePoints = mapToPointSet(pathMap)

    labeledPoints = dict()
    for i, point in enumerate(uniquePoints):
        labeledPoints.update({point : i})
    pointCount = len(uniquePoints)
    csgraph = [[0.0] * pointCount for _ in range(pointCount)]
    for segment in pathMap:
        first = labeledPoints[segment[0]]
        second = labeledPoints[segment[1]]
        distance = dist(segment[0], segment[1])
        csgraph[first][second] = math.sqrt(distance)
        csgraph[second][first] = math.sqrt(distance)
    csgraph = np.array(csgraph, dtype=float)   
    path, predecessors  = shortest_path(csgraph, return_predecessors=True)
    if not labeledPoints.get(src) or not labeledPoints.get(dest):
        return
    current = labeledPoints[src]
    i = labeledPoints[dest]
    path = []
    while current != -9999:
        path.append(findInDict(labeledPoints, current))
        current = predecessors[i, current]
    return path

def generateCircle(n, center=(0, 0), radius=4.0):
    points = []
    for i in range(n):
        angle = (360 / n * i + 45) * math.pi / 180
        points.append((center[0] + math.cos(angle) * radius, 
                       center[1] + math.sin(angle) * radius))
    return points
