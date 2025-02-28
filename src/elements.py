from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *

from src.interface import *
from src.rect_item_appearance_and_action import *
from src.load_setting import *
from src.label_d_d import *
import  src.func as func

import os
import src.const as const
from src.choice_color_rect import*
from src.brush_appearance_and_action import *


class Elements:
	
	class RadioButton(QRadioButton, Element_Interface, Subject):
		def __init__(self):
			super().__init__()
			self.create_list_observers()

		def mousePressEvent(self, event):
			self.setChecked(True)
			self.notify()
					
			
	class ComboBox(QComboBox, Element_Interface, Subject, Observer):
		def __init__(self):
			super().__init__()
			self.create_list_observers()
			self.currentTextChanged[str].connect(self.notify)
		
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
		
			
	class SpinBox(QSpinBox, Element_Interface, Subject, Observer):
		def __init__(self):
			super().__init__()
			self.create_list_observers()
			self.valueChanged.connect(self.notify)
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
		
		
	class Button(QPushButton, Element_Interface, Subject, Observer):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__()
			self.carcase = carcase
			self.create_list_observers()
					
		def mousePressEvent(self, event):
			self.notify()	
		
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
	
	
	class LabelDD(LabelDragDrop, Element_Interface, Subject):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__()	
			self.carcase = carcase		
			self.create_list_observers()


	class Label(QLabel, Element_Interface):
		def __init__(self):
			super().__init__()


	class Label_Plus_Image_Fields(Label, Observer):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__()

		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			
		
	class RectItem(RectItemAppearanceAndAction, Element_Interface, Observer, Subject):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__()	
			self.carcase = carcase		
			self.create_list_observers()
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			if isinstance (subject, QBrush) != True:
				self.notify()
	
	class PageLayout(QPageLayout, Element_Interface, Observer, Subject):
		def __init__(self):
			super().__init__()	
			self.setUnits(QPageLayout.Unit.Millimeter)		
			self.create_list_observers()
		
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			self.notify()
	
	
	class Manipulation(Element_Interface, Observer, Subject):
		def __init__(self):
			self.__dpi = [0]
			self.create_list_observers()
			
		def set_orig_rect(self, rect: QRectF):
			self.__rect = rect
				
		def get_orig_rect(self) -> QRectF:
			return self.__rect
		
		def set_dpi(self, *dpi):
			self.__dpi = dpi
								
		def get_dpi(self) -> list[int]:
			return self.__dpi
		
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			self.notify()
		
	
	class Scene(QGraphicsScene, Element_Interface, Observer):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__()
			self.carcase = carcase
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
		
	
	class GraphicsView(QGraphicsView, Element_Interface, Observer):
		def __init__(self):
			super().__init__()			
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
	
	
	class Pixmap(QPixmap, Element_Interface, Observer):
		def __init__(self):
			super().__init__()			
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
	
	
	class Brush (BrushAppearanceAndAction, Element_Interface, Subject, Observer):
		def __init__(self):
			super().__init__()
			self.create_list_observers()		
			
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			self.notify()
	
	
	class GroupBox(QGroupBox, Element_Interface):
		def __init__(self):
			super().__init__()
			
		
	class Slider (QSlider, Element_Interface, Subject):
		def __init__(self, carcase: Carcase_Interfase):
			super().__init__(Qt.Orientation.Horizontal)
			self.carcase = carcase
			self.create_list_observers()
			self.valueChanged.connect(self.notify)
			
	
	class LCDNumber(QLCDNumber, Element_Interface, Observer):
		def __init__(self):
			super().__init__()
			self.display(100)
		
		def update_observer(self, subject: Subject):
			func.Func.function_for_element[subject.get_name()][self.get_name()](self, subject)
			
	
	class ChoiceColorRect (ChoiceColorWidget, Element_Interface, Subject):
		def __init__(self):
			super().__init__()
			self.create_list_observers()
			self.my_signal_change_color.connect(self.notify)
			self.my_signal_change_alpha.connect(self.notify)


	class Tab (QTabWidget, Element_Interface, Observer):
		def __init__(self):
			super().__init__()		
