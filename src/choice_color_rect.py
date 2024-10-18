from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import math
from src.load_setting import *


class DifSize:
		RECT_SIZE_F = QRectF(0,0,24,24)
		WIDTH_PEN_DEFAULT = 1
		WIDTH_PEN_ACTIVE = 4
		DISTANCE_RECT = 4
		NUM_RECT_IN_ROW = 2


class RectSample (QGraphicsRectItem):
	def __init__(self):
		super().__init__()
				
	def mouseMoveEvent(self, event):		
		self.moveBy(event.pos().x() - event.lastPos().x(), event.pos().y() - event.lastPos().y())
		
	def mousePressEvent(self, event):
		pass
		
	
class RectColor (QGraphicsRectItem):
	def __init__(self, parent = None, color: QColor = QColor("blue"), alpha: int = 255):
		super().__init__()
		self.parent = parent
		self.color = color
		self.alpha = alpha
		self.color.setAlpha(self.alpha)
		self.brush = QBrush()
		self.brush.setColor(self.color)
		self.brush.setStyle(Qt.BrushStyle.SolidPattern)
		self.setBrush(self.brush)
		self.setRect(DifSize.RECT_SIZE_F)
		
		self.pen = QPen()
		self.set_pen(DifSize.WIDTH_PEN_DEFAULT)
	
	def set_pen(self, width: int):
		self.pen.setWidth(width)
		self.setPen(self.pen)
				
	def get_color_rect(self) -> QColor:
		return self.color

	def mousePressEvent(self, event):
		self.parent.set_color_rect_sample (self.get_color_rect())
		for i in self.scene().items():
			if isinstance(i, RectColor):
				i.set_pen(DifSize.WIDTH_PEN_DEFAULT)
			else: pass
			
		self.set_pen(DifSize.WIDTH_PEN_ACTIVE)
		self.parent.set_active_color(self.get_color_rect())
		

class ChoiceColorWidget(QWidget):
	
	my_signal_change_color = pyqtSignal()
	my_signal_change_alpha = pyqtSignal()

	def __init__(self):		
		super().__init__()
		
		pixmap = QPixmap(".icons/image_.png")
		pix = pixmap.scaledToHeight(int(DifSize.RECT_SIZE_F.height()) * 4 + DifSize.DISTANCE_RECT * 4)
		
		self.setting = LoadSetting()
		_color_name = self.setting.get_active_color_rect()
		_color_alpha = self.setting.get_current_alpha()
		
		if QColor(_color_name):
			self.set_active_color(QColor(_color_name))
		else: self.set_active_color(QColor("blue"))
	
		color = QColor(_color_name)
		color.setAlpha(_color_alpha)
		
		self.current_alpha = 0
		
		self.scene_rect = QGraphicsScene()
		self.view_rect = QGraphicsView()
		self.view_rect.setFrameShape(QFrame.Shape.NoFrame)
			
		#Rect с цветами по умолчанию
		self.rect_color =  [RectColor(self, QColor("blue")), RectColor(self, QColor("turquoise")),
						RectColor(self, QColor("green")),	RectColor(self, QColor("lime")),
						RectColor(self, QColor("orange")), RectColor(self, QColor("pink")),
						RectColor(self, QColor("red")), RectColor(self, QColor("sienna"))]
		
		self.view_rect.setScene(self.scene_rect)
				
		self.scene_sample = QGraphicsScene()
		self.scene_sample.addPixmap(pix)	
		self.view_sample = QGraphicsView()	
		self.view_sample.setHorizontalScrollBarPolicy (Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.view_sample.setVerticalScrollBarPolicy (Qt.ScrollBarPolicy.ScrollBarAlwaysOff)	
		self.view_sample.setFrameShape(QFrame.Shape.NoFrame)
		self.rect_sample = RectSample()
		self.rect_sample.setRect(0, 0, DifSize.RECT_SIZE_F.width() * 2.2, DifSize.RECT_SIZE_F.height() * 3 )
		self.rect_sample.setZValue(1)
		self.scene_sample.addItem(self.rect_sample)		
		self.view_sample.setScene(self.scene_sample)
		self.rect_sample.setBrush(QBrush(color))
		self.view_sample.setMaximumSize(pixmap.size().width(), pixmap.size().height())
		self.view_rect.setMaximumSize( int((DifSize.RECT_SIZE_F.width() + DifSize.DISTANCE_RECT) * DifSize.NUM_RECT_IN_ROW),
										int ((DifSize.RECT_SIZE_F.height() + DifSize.DISTANCE_RECT) * 
										math.ceil(len(self.rect_color) / DifSize.NUM_RECT_IN_ROW))) # количество рядов
			
		self.layout_rect = QHBoxLayout()
		self.layout_rect.addWidget(self.view_sample)
		self.layout_rect.addWidget(self.view_rect)
		
		self.placement_rect()
			
		################################
		
		self.slider = QSlider(Qt.Orientation.Horizontal)
		self.slider.setMaximum(255)
		self.slider.setMinimum(0)
		
		self.spinbox = QSpinBox()
		self.spinbox.setMaximum(255)
		self.spinbox.setMinimum(0)
		
		self.layout_transparency = QHBoxLayout()
		self.layout_transparency.addWidget(self.spinbox)
		self.layout_transparency.addWidget(self.slider)
				
		######################################
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.layout_rect)
		self.layout.addLayout(self.layout_transparency)
		self.setLayout(self.layout)
		
		self.slider.valueChanged.connect(self.spinbox.setValue)
		self.spinbox.valueChanged.connect(self.slider.setValue)
		self.spinbox.valueChanged.connect(self.set_current_alpha)
		self.spinbox.setValue(_color_alpha)
									
	def set_active_color(self, color: QColor) -> None:
		self.active_color = color
		self.my_signal_change_color.emit()
		
	def get_active_color(self) -> QColor:
		return self.active_color		
								
	def set_color_rect_sample (self, color: QColor) -> None:
		color.setAlpha(self.get_current_alpha())
		self.rect_sample.setBrush(QBrush(color))
	
	def set_current_alpha(self, alpha: int) -> None:
		self.current_alpha = alpha
		self.my_signal_change_alpha.emit()
		color = self.get_active_color()
		color.setAlpha(alpha)
		self.rect_sample.setBrush(QBrush(color))
		
	def get_current_alpha(self) -> int:
		return self.current_alpha
	
	def add_rect_color(self, rect_color: RectColor):
		self.rect_color.append(rect_color)		
	
	def get_rect_color(self) -> list[RectColor]:
		return self.rect_color
		

	def coord_rect(self, num: int, total_column: int, total_row: int) -> list[int]:
		'''Возвращает список с координатами rectitem (номера столбца и строки)'''
		
		num_column  = num % total_column
		num_row = num // total_column
		return  num_column, num_row
	
	def placement_rect(self) -> None:
		'''Размещение на сцене rect выбора цветов'''		
		
		num_row = math.ceil(len(self.rect_color) / DifSize.NUM_RECT_IN_ROW) # количество рядов 
																		# math.ceil - округление до большего
		num_column = DifSize.NUM_RECT_IN_ROW
		
		for i in range (len(self.rect_color)):
			self.scene_rect.addItem(self.rect_color[i])
			_xy = self.coord_rect(i, num_column, num_row)		
			_x = _xy[0] * (DifSize.RECT_SIZE_F.width() + DifSize.DISTANCE_RECT) + 2 * DifSize.RECT_SIZE_F.width() + DifSize.DISTANCE_RECT * 2
			_y = _xy[1] * (DifSize.RECT_SIZE_F.height() + DifSize.DISTANCE_RECT)
			
			self.rect_color[i].moveBy(_x, _y)
	
	
