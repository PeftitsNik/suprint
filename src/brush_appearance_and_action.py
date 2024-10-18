from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.load_setting import *

class BrushAppearanceAndAction(QBrush):
    
	def __init__(self):
	     
		super().__init__()
		self.appearance_brush()
		
	
	def appearance_brush(self):	
		setting = LoadSetting()
		self.color = QColor(setting.get_active_color_rect())
		self.color_alpha = setting.get_current_alpha()
		self.color.setAlpha(self.color_alpha)
		self.setColor(self.color)
		self.setStyle(Qt.BrushStyle.SolidPattern)	
	
