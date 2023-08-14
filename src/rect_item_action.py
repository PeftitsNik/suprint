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
		pen1 = QPen()
		#self.pen1.setStyle(Qt.PenStyle.DashLine)
		pen1.setColor(QColor("red"))
		
		space = 6
		length = 6
		width = 4
		
		dashes = [length, space]		
		pen1.setDashPattern(dashes)
		pen1.setWidth(width)
		self.setPen(pen1)	
		
		#self.rect_inside = QGraphicsRectItem(self)
		#self.rect_inside.setPen(QColor("white"))
		#self.rect_inside.setRect(self.qrectf.x()-1, self.qrectf.y()-1, self.qrectf.width()-2, self.qrectf.height()-2)
        
	def mousePressEvent(self, event):
		print("Click on Rect")
		
	
       
