from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import src.const as const #импорт констант

class RectItemAction(QGraphicsRectItem):
    
	def __init__(self):
	     
		super().__init__()
		
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)		
		
		self.other_rect_on_scene: list[RectItem] = [] # список прямоугольников на сцене, заполняется при щелчке ЛКМ на прямоугольнике
		self.delta_x = 0 # переменная, в которой накапливается значение перемещения курсора при зажатой ЛКМ, по оси Х
		self.delta_y = 0 # переменная, в которой накапливается значение перемещения курсора при зажатой ЛКМ, по оси Y        
		
		self.appearance_rect()
	
	def appearance_rect(self):
		pen = QPen()		
		pen.setColor(QColor("red"))
		
		brush = QBrush()
		color = QColor("blue")
		color.setAlpha(35)
		brush.setColor(color)
		brush.setStyle(Qt.BrushStyle.SolidPattern)
		
		space = 6
		length = 6
		width = 4
		
		#dashes = [length, space]		
		#pen.setDashPattern(dashes)
		pen.setWidth(width)
		self.setPen(pen)
		self.setBrush(brush)
	
	def add_parent_scene(self, scene: QGraphicsScene):
		self.scene = scene		
	
	def mousePressEvent(self, event):
		self.setCursor(Qt.CursorShape.SizeAllCursor)
		self.other_rect_on_scene = [i for i in self.scene().items() if isinstance(i, QGraphicsRectItem) ]
					
		self.delta_x = 0
		self.delta_y = 0

	def mouseMoveEvent(self, event):
		self.moveBy(event.pos().x() - event.lastPos().x(), event.pos().y() - event.lastPos().y())

		for i in self.other_rect_on_scene:          
			
			if i == self: continue # если прямоугольник, который двигают, сравнивается с самим собой, то продолжаем цикл 
			
            ###########  ПРИЛИПАНИЕ УГЛОВ ######################
            # при приближении двух прямоугольников
            # self  - что двигают,  i  - неподвижный
            #   ------           ------
            #  | self |    или  | self |
            #  |     ------     |      |  ------
            #  |   a| |    |    |      | |      |
            #  |    | | b  |    |      | |      |
            #   ----|-     |     ------  |      |
            #       |  i   |             |   i  |
            #        ------               ------
            #
            # Проверка границ прилипания 
			# если  углы a и b  близко друг к другу
			
			
			
		
