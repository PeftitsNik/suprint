from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import itertools

class PosFigure:
	######### Для прямоугольников ################
	def pos_rect(self, rect: QGraphicsRectItem) -> tuple:
		''' Создание кортежа из координат углов прямоугольника  в виде QPointF'''
		
		#	1---2
		#	|	|
		#	4---3
		
		
		point_rect = (
		rect.scenePos(),
		QPointF(rect.scenePos().x() + rect.rect().width(), rect.scenePos().y()),
		QPointF(rect.scenePos().x() + rect.rect().width(), rect.scenePos().y() + rect.rect().height()),
		QPointF(rect.scenePos().x(), rect.scenePos().y() + rect.rect().height())
		)
				
		return point_rect
		
	def pos_substraction_reсt_angle(self, rect1: QGraphicsRectItem, rect2: QGraphicsRectItem, border: int) -> tuple:
		''' Создание результата вычитания координат углов прямоугольников на расстоянии меньше border,
			который представляет собой смещение x и y координат'''
		p = (0, 0)
		
		point_rect1 = self.pos_rect(rect1)
		point_rect2 = self.pos_rect(rect2)
				
		for p1, p2 in itertools.product(point_rect1, point_rect2):
			if abs((p1 - p2).x()) < border and abs((p1 - p2).y()) < border:
				p = ((p1 - p2).x(), (p1 - p2).y())
				break
			else: pass
	
		return p
	
	#def dist_move_line(lines1: tuple,  lines2: tuple) -> tuple:
	#	''' Расстояние на которое надо сдвинуть линию (dx,dy), при условии, что
	#	check_parallel_lines() == True'''	
	#	pass
	
	
	def delta_parallel_lines(self, lines1: tuple,  lines2: tuple, border: int) -> tuple:
		'''Проверка параллельности двух отрезков lines1 (QPointF, QPointF) 
		и lines2 (QPointF, QPointF) на расстоянии меньше border с определением
		велечины необходимого смещения линии delta на dx, dy'''
		
		delta = (0,0)
		
		# уравнение прямой y = kx + b
		# прямые параллельны при равенстве k
		# k = (y1 - y2) / (x1 - x2), x1 - x2 != 0 
		
		k1 = (lines1[0].y() - lines1[1].y()) / (lines1[0].x() - lines1[1].x()) if lines1[0].x() - lines1[1].x() != 0 else 0
		k2 = (lines2[0].y() - lines2[1].y()) / (lines2[0].x() - lines2[1].x()) if lines2[0].x() - lines2[1].x() != 0 else 0
		
		# если параллельны 
		if k1 == k2:
			
			# если их проекции на одну из осей частично совмещаются
			# тут на ось Х, аналогично и на Y
			#	   |			lines1
			#	x12|-----------	/
			#	   |		   /		lines2
			#	x22|--------- /--------/
			#	   |		 /		  /
			#	x11|--------/		 /
			#	   |				/
			#	x21|---------------/	
			#	   |
			#	   |______________________________________
			
			# размер проекции lines1 на оси X и Y
			lin1_x = abs(lines1[0].x() - lines1[1].x())
			lin1_y = abs(lines1[0].y() - lines1[1].y())
			
			#размер проекции lines2 а оси X и Y
			lin2_x = abs(lines2[0].x() - lines2[1].x())
			lin2_y = abs(lines2[0].y() - lines2[1].y())
		
			# если их проекции на оси частично совмещаются
			# на ось X
			#		x21				x11				x22					x21				x12				x22
			if (lines2[0].x() <= lines1[0].x() >= lines2[1].x()) or (lines2[0].x() <= lines1[1].x() >= lines2[1].x()):
				# и между отрезками мешьше border по оси Х
				if abs(lines1[0].x() - lines2[0].x()) < border:
					delta = (lines1[0].x() - lines2[0].x(), 0)
				else: pass
			# или по оси Y\
			elif (lines2[0].y() <= lines1[0].y() >= lines2[1].y()) or (lines2[0].y() <= lines1[1].y() >= lines2[1].y()):
				if abs(lines1[0].y() - lines2[0].y()) < border:
					delta = (0, lines1[0].y() - lines2[0].y())					
				else: pass
				
			else: pass
			
		else: pass
		
		return delta
			
	def move_reсt(self, rect1: QGraphicsRectItem, rect2: QGraphicsRectItem, border: int):
		''' Создание кортежа из результата вычитания координат параллельных сторон прямоугольников из двух
			наборов rect на расстоянии меньше border, который представляет собой смещение x и y координат'''
		p = (0, 0)
		
		point_rect1 = self.pos_rect(rect1)
		point_rect2 = self.pos_rect(rect2)
				
		#	  __1___	
		#	 |		|	
		#	4|		|2
		#	 |______|	
		#		3
						
		line1_1 = (point_rect1[0], point_rect1[1])
		line1_2 = (point_rect1[1], point_rect1[2])
		line1_3 = (point_rect1[2], point_rect1[3])
		line1_4 = (point_rect1[3], point_rect1[0])
		lines1 = (line1_1, line1_2, line1_3, line1_4)
		
		line2_1 = (point_rect2[0], point_rect2[1])
		line2_2 = (point_rect2[1], point_rect2[2])
		line2_3 = (point_rect2[2], point_rect2[3])
		line2_4 = (point_rect2[3], point_rect2[0])
		lines2 = (line2_1, line2_2, line2_3, line2_4)
	
		for l1, l2 in itertools.product(lines1, lines2):
			
			dx = self.delta_parallel_lines(l1,  l2, border)[0]
			dy = self.delta_parallel_lines(l1,  l2, border)[1]
			
			
			if dx !=0 or dy !=0: 
				p = (dx, dy)
				break
		
		return p
