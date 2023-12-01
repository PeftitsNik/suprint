from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import itertools

class PosFigure:
	def pos_rect(self, rect: QGraphicsRectItem) -> tuple:
		point_rect = (
		rect.scenePos(),
		QPointF(rect.scenePos().x() + rect.rect().width(), rect.scenePos().y()),
		QPointF(rect.scenePos().x() + rect.rect().width(), rect.scenePos().y() + rect.rect().height()),
		QPointF(rect.scenePos().x(), rect.scenePos().y() + rect.rect().height())
		)				
		return point_rect
		
	def pos_substraction_reсt(self, rect1: QGraphicsRectItem, rect2: QGraphicsRectItem, border: int):
		point_rect1 = self.pos_rect(rect1)
		point_rect2 = self.pos_rect(rect2)
		p = (0, 0)
		i = 0
		
		for p1, p2 in itertools.product(point_rect1, point_rect2):
			if abs((p1 - p2).x()) < border and abs((p1 - p2).y()) < border:
				p = ((p1 - p2).x(), (p1 - p2).y())
				break
			else: i = i + 1
		
		
		return p
