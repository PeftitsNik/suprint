from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import src.const as const
from src.pos_f import *
from src.brush_appearance_and_action import *

class RectItemAppearanceAndAction(QGraphicsRectItem):
    
	def __init__(self):
	     
		super().__init__()
		
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
		self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)		
		
		self.other_rect_on_scene: list[RectItem] = [] # список прямоугольников на сцене, заполняется при щелчке ЛКМ на прямоугольнике
		self.delta_x = 0 # переменная, в которой накапливается значение перемещения курсора при зажатой ЛКМ, по оси Х
		self.delta_y = 0 # переменная, в которой накапливается значение перемещения курсора при зажатой ЛКМ, по оси Y        
		
		self.appearance_rect()
		
		self.pos_figure = PosFigure()
	
	def appearance_rect(self):		
				
		brush = BrushAppearanceAndAction()
		self.setBrush(brush)
		
		space = 6
		length = 6
		width = 4
		
	def set_color_rect(self, color: QColor):
		self.color = color
	
	def add_parent_scene(self, scene: QGraphicsScene):
		self.scene = scene		
	
	def mousePressEvent(self, event):
		self.setCursor(Qt.CursorShape.SizeAllCursor)
		#список rectitem на сцене
		self.other_rect_on_scene = [i for i in self.scene().items() if isinstance(i, RectItemAppearanceAndAction) ]
							
		self.delta_x = 0
		self.delta_y = 0
		
		

	def mouseMoveEvent(self, event):
		self.moveBy(event.pos().x() - event.lastPos().x(), event.pos().y() - event.lastPos().y())

		for i in self.other_rect_on_scene:          
			pos = self.pos_figure.pos_substraction_reсt_angle(self, i, const.BORDER)
			move = self.pos_figure.move_reсt(self, i, const.BORDER)	# сдвиг на dx, dy
			
			if i == self: continue # если прямоугольник, который двигают, сравнивается с самим собой, то продолжаем цикл 
			
			###########  ПРИЛИПАНИЕ УГЛОВ ######################
			# при приближении двух углов
			# прямоугольник self  - что двигают,  i  - неподвижный
			#
			#		-------------
			#		|			|
			#		|	self	|
			#		|			|
			#		|			|
			#		|		----|-------
			#		|		|	|		|
			#		--------|---		|
			#				|			|
			#				|			|
			#				|	i		|
			#				-------------

			
			elif pos[0] != 0 or pos[1] != 0:
				self.moveBy(-pos[0], -pos[1]) # минус, потому что вычитаем из прямоугольника, который двигаем 
			
				self.delta_x = self.delta_x + event.pos().x() - event.lastPos().x()
				self.delta_y = self.delta_y + event.pos().y() - event.lastPos().y()

				#сли накопленное значение больше BORDER передмещаем двигаемый прямоугольник к позиции курсора
				if abs(self.delta_x) > const.BORDER:
					self.moveBy(self.delta_x, event.pos().y() - event.lastPos().y())
					self.delta_x = 0
					self.delta_y = 0
					break
				elif abs(self.delta_y) > const.BORDER:
					self.moveBy(event.pos().x() - event.lastPos().x(), self.delta_y)
					self.delta_x = 0
					self.delta_y = 0
					break
				else:  break
			
			         
			elif move[0] != 0 or move[1] != 0:
				self.moveBy(-move[0], -move[1])
				
				self.delta_x = self.delta_x + event.pos().x() - event.lastPos().x()
				self.delta_y = self.delta_y + event.pos().y() - event.lastPos().y()

				#сли накопленное значение больше BORDER передмещаем двигаемый прямоугольник к позиции курсора
				if abs(self.delta_x) > const.BORDER:
					self.moveBy(self.delta_x, event.pos().y() - event.lastPos().y())
					self.delta_x = 0
					self.delta_y = 0
					break
				elif abs(self.delta_y) > const.BORDER:
					self.moveBy(event.pos().x() - event.lastPos().x(), self.delta_y)
					self.delta_x = 0
					self.delta_y = 0
					break
				else:  break
			

	def mouseReleaseEvent(self, event):
		self.setCursor(Qt.CursorShape.ArrowCursor)
