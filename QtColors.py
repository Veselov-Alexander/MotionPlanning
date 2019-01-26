from PyQt5.QtCore import *
from PyQt5.QtGui import *

import random

def getNumber():
    return random.randint(0, 255)

def getColor():
    return QColor(getNumber(), getNumber(), getNumber())

def Color(color, opacity=1):
    color = QColor(color)
    color.setAlphaF(opacity)
    return color

def Brush(color, opacity=1, size=1):
    return QBrush(Color(color, opacity), size)

def Pen(color, opacity=1, size=1):
    return QPen(Color(color, opacity), size)

def averageColor(first, second):
    R = (first.red() + second.red()) // 2
    G = (first.green() + second.green()) // 2
    B = (first.blue() + second.blue()) // 2
    color = QColor()
    color.setRed(R)
    color.setGreen(G)
    color.setBlue(B)
    return color
