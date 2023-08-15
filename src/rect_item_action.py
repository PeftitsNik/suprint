from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import src.const #импорт констант

class RectItemAction(QGraphicsRectItem):
    
	def __init__(self, qrectf: QRectF = None):
	     
		super().__init__(qrectf)
		
		self.qrectf = qrectf
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)		
		pen = QPen()
		#self.pen1.setStyle(Qt.PenStyle.DashLine)
		pen.setColor(QColor("red"))
		
		brush = QBrush()
		color = QColor("blue")
		color.setAlpha(35)
		brush.setColor(color)
		brush.setStyle(Qt.BrushStyle.SolidPattern)
		
		space = 6
		length = 6
		width = 4
		
		dashes = [length, space]		
		pen.setDashPattern(dashes)
		pen.setWidth(width)
		self.setPen(pen)
		self.setBrush(brush)
	
					        
	def mousePressEvent(self, event):
		print("Click on Rect")
		#print(self.scenePos().x())

