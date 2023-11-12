from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *
import src.i18n as i18n
from src.dict_prn_ppr import *  # в нём создается словарь, содержащий значения (имя принтера - потдерживаемые страницы),
                            # а также список потдерживаемых разрешений dpi печати 
import src.func as func
from src.rect_item_action import *
from src.interface import *
#
#
#___________________________		_______________________			________________________	
#|	Subject	(наблюдаемое)	|<-----	|Observer(наблюдатель)	|   --- |Observer(наблюдатель)	|----
#|--------------------------|		|----------------------	|   |   |----------------------	|	|		
#| виджеты  связанные		|		|	PageLayout			|   |   |	RectItem			|   |                            
#|      					|		|						|	|	|	add_objects(self,	|	|
#| с размером страницы		|		|						|   |   |	Manipulation)		|	|
#| (альбомная, портретная,	|		|-----------------------|   |   |-----------------------|	|
#| поля, А0-4, и т.д.)		|		|Subject (наблюдаемое)	|<--    |Subject (наблюдаемое)	|	|
#|__________________________|		|_______________________|<---   |_______________________|	|
#																|				^               |
#																|				|				|
#								________________________		|				|				|						
#		------------------------|Observer(наблюдатель)	|------------------------               |
#		|						|----------------------	|       |                               |
#		|						|		Scene			|       |                               |
#		|						|	add_objects(self,	|       |                               |
#       |						|Manipulation, QspinBox	|       |                               |
#       |						|	QPixmap, RectItem	|       |                               |
#		|						|_______________________|       |                               |
#		V						                                |                               |
#__________________________			              ______________|________                       |
#|	Subject	(наблюдаемое)	|<------------------  |Observer(наблюдатель)|                       |
#|--------------------------|           --------- |---------------------|                      	|
#| виджеты  связанные		|           |         |		Manipulation	|                      	|
#| с размером изображения	|           |         |						|                      	|  		
#| (растянуть, уместить,	|           |         |---------------------|                     	|  		
#| масштаб и т.д.)			|           |         |Subject (наблюдаемое)|<-----------------------	
#|__________________________|			|		  |_____________________|
# 										|		                                             	 		
#			-----------------------------												
#			V											    
#________________________                                   
#|Subject (наблюдаемое)	|                                   
#|---------------------	|                                   
#|	виджеты связанные	|                                   
#|	с количеством 		|                                   
#|  RectItem для печати	|										
#|----------------------|									
#| Observer(наблюдатель)|
#|______________________|						                                                       
# 
#____________________		
#|					|		
#| ButtonOpenFile	|
#| add_objects(self,|
#| QPixmap, Scene	|		
#| Manipulation)	|
#|__________________|		
#
#____________________
#|					 |		
#| ButtonPrint:		 |
#| __init__(self,	 |
#|Scene, Manipulation|
#|___________________|		


internationalization = i18n.ru

f_f = Fill_Forms()
d_d = DictPrnPpr()

calc_dif_value = func.CalculateDifferentValue()

class RadioButton(QRadioButton, Subject):	
	def __init__(self, name: str, parent=None):
		super().__init__(name)
		self.create_list_observers()
	
	def mousePressEvent(self, event):
		self.setChecked(True)
		self.notify()	

class RealSizeRadioButton(RadioButton):
	def __init__(self, name: str, spinbox: QSpinBox, parent=None):
		super().__init__(name)	
		self.spinbox = spinbox
		self.toggled[bool].connect(self.react_to_toggled)
	
	def react_to_toggled(self, checked: bool):
		self.spinbox.setEnabled(checked)

class ComboBoxPaperSize(QComboBox, Observer, Subject):
	def __init__(self, parent=None):
		super().__init__()
		f_f.fill_combobox_paper(self)		
		self.currentTextChanged[str].connect(self.notify)
		self.create_list_observers()
		
	def update_observer(self, subject: Subject):
		func.Func.function_for_combobox_printer[subject.get_name()](self, subject)

class ComboBoxPrinter(QComboBox, Subject):
	def __init__(self, parent=None):
		super().__init__()
		f_f.fill_combobox_printer(self)		
		self.currentTextChanged[str].connect(self.notify)
		self.create_list_observers()
		
class SpinBoxField (QSpinBox, Subject, Observer):
	def __init__(self):
		super().__init__()
		self.create_list_observers()
		self.valueChanged.connect(self.notify)		
		self.setValue(1)
		self.setFixedWidth(50)

	def update_observer(self, subject: Subject):		
		func.Func.function_for_widgets_manipulations[subject.get_name()](self, subject)	
	

class PageLayout(QPageLayout, Observer, Subject):
	def __init__(self):
		super().__init__()
		self.setUnits(QPageLayout.Unit.Millimeter)
		self.create_list_observers()	
		
	def update_observer(self, subject: Subject):		
		func.Func.function_for_pagelayout[subject.get_name()](self, subject)
		self.notify()				

class RectItem(RectItemAction, Observer, Subject):
	def __init__(self):
		super().__init__()			
		self.create_list_observers()	
	
	def add_objects(self, manipulation):
		self.manipulation = manipulation
	
	def update_observer(self, subject: Subject):		
		func.Func.function_for_rectitem[subject.get_name()](self, subject)
		self.notify()
			
	
#  в Manipulation хранятся состояния различных виджетов и классов
class Manipulation(Observer, Subject):
	def __init__(self):
		self.__status_image = ["", ""] 	# 1 элемент - размер картинки (реальный, растянутый и т.п)
									# 2 элемент - тип печать (распечатать всё, отдельные фрагменты)
		self.__num = 1		
		self.__dpi = [0]
		self.create_list_observers()
							
	def set_status_image(self, status1: str, status2: str): # состояние картинки: растянутая, нормальная, маштаб и т.д
		self.__status_image = [status1, status2]
		
	def get_status_image(self) -> list[str]:
		return self.__status_image
	
	def set_num_pages(self, num: int): # количество rectitem на картинке
		self.__num = num
		
	def get_num_pages(self) -> int:
		return self.__num
		
	def set_orig_rect(self, rect: QRectF):
		self.__rect = rect
	
	def get_orig_rect(self) -> QRectF:
		return self.__rect
	
	def set_dpi(self, *dpi):
		self.__dpi = dpi
		self.notify()
					
	def get_dpi(self) -> list[int]:
		return self.__dpi
	
	def set_pagelayout(self, page: QPageLayout):
		self.__page = page
	
	def get_pagelayout(self) -> QPageLayout:
		return self.__page
		
	def set_name_printer(self, printer: str):
		self.printer = printer
		
	def get_name_printer(self) -> str:
		return self.printer	
	
	def update_observer(self, subject: Subject):		
		func.Func.function_for_manipulation[subject.get_name()](self, subject)
		#self.notify()	
		
class Scene(QGraphicsScene, Observer):
	def __init__(self):
		super().__init__()		
	
	def add_objects(self, manipulation: Manipulation, pixmap: QPixmap,
					rectitem: RectItem, spinbox: QSpinBox):
		self.manipulation = manipulation
		self.pixmap = pixmap
		self.rectitem = rectitem	
		self.spinbox = spinbox
		
	def update_observer(self, subject: Subject):				
		func.Func.function_for_scene[subject.get_name()](self, subject)
	
	
class ButtonOpenFile(QPushButton):
	def __init__(self, manipulation: Manipulation):		
		super().__init__()
		self.manipulation = manipulation
		self.clicked.connect(self.open_pix)
				
	def add_objects(self, scene: Scene, pixmap: QPixmap):
		self.pixmap = pixmap
		self.scene = scene
	
	@pyqtSlot()			
	def open_pix(self):
		# при открытии новой картинки старая удаляется
		# func.Func.remove_pixmap(self.scene)
		
		self.fileName = QFileDialog.getOpenFileName(self, "Open File", ".", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.tiff *.webp)")
			
		if self.fileName[0] == "":
			pass
		else :
			self.pixmap.load(self.fileName[0])
			func.Func.remove_pixmap(self.scene)			
			self.scene.addPixmap(self.pixmap)
			func.Func.manipulation_pixmap(self.scene)
			self.manipulation.set_dpi(self.pixmap.physicalDpiX())

			__list__num = calc_dif_value.num_rect_in_scene(self.scene, self.scene.rectitem)
			__num = __list__num[0] * __list__num[1]
			self.scene.spinbox.setMaximum(__num)
			
			
class ButtonPrint(QPushButton):
	def __init__(self, scene: Scene, manipulation: Manipulation):		
		super().__init__()	
		self.scene = scene
		self.manipulation = manipulation
		self.clicked.connect(self.print_pix)
	
	@pyqtSlot()
	def print_pix(self):
		scene = Scene()
		func.Func.print_pixmap_from_scene(self, self.scene, self.manipulation)
		
class Slider (QSlider):
	def __init__(self, view: QGraphicsView):
		super().__init__(Qt.Orientation.Horizontal)
		self.view = view
		self.setRange(10, 200)
		self.setValue(100)
		self.valueChanged.connect(self.slider_event)
		
	@pyqtSlot()
	def slider_event(self):
		sc = self.value()
		transform = QTransform()
		scale_x = sc / 100
		scale_y = sc / 100
		transform.scale(scale_x, scale_y)
		self.view.setTransform(transform)	
		
		
##################################################################
