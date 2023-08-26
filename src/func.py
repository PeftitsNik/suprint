from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *
from src.rect_item_action import *
import copy

from src.dict_prn_ppr import *  # в нём создается словарь, содержащий значения (имя принтера - потдерживаемые страницы),
                        	# а также список потдерживаемых разрешений dpi печати 

import src.const #импорт констант

p = DictPrnPpr()

class RectItem(QGraphicsRectItem):		####
	pass								#
class PixmapManipulation:					## определены в carcase.py
	pass								#
										###


class CalculateDifferentValue:	
	def __init__(self):		
		self.pos_x = 0
		self.pos_y = 0
		self.qrect = None
			
	# количество rectitem на сцене по горизонтали и вертикали	
	def num_rect_in_scene(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem) -> list[int]:
		
		if rectitem.rect().width() != 0 and rectitem.rect().height() != 0:
                
			if scene.pixmap.width() % rectitem.rect().width() :
				n_width = scene.pixmap.width() // rectitem.rect().width() + 1
			else: n_width = scene.pixmap.width() // rectitem.rect().width()
        
			if scene.pixmap.height() % rectitem.rect().height() :
				n_height = scene.pixmap.height() // rectitem.rect().height() + 1
			else: n_height = scene.pixmap.height() // rectitem.rect().height()
               
			return int (n_width), int (n_height)
			
		else:
			return 0, 0	
		
	
	# список rectitem на сцене
	def list_rect(self, scene: QGraphicsScene) -> list[QGraphicsRectItem]:
		list = []
		for i in scene.items():
			if isinstance(i, QGraphicsRectItem):
				list.append(i)
			else: pass
		return list
	
	#возвращает список с координатами rectitem (номера столбца и строки)
	@staticmethod
	def coord_rect(num: int, total_column: int, total_row: int) -> list[int]: 
		num_column  = num % total_column
		num_row = num // total_column		
		return  num_column, num_row
	
	#удаляет все rectitem на сцене	
	def remove_all_rectitem(self, scene: QGraphicsScene):
		for i in scene.items():
			if  isinstance(i, QGraphicsRectItem):
				scene.removeItem(i)
			else: pass

	#проверяет значение SpinBox  и максимально возможное количество rectitem на картинке
	def verification_num_spinbox(self, scene: QGraphicsScene):
		__num_rect = self.num_rect_in_scene(scene, scene.rectitem)[0] * self.num_rect_in_scene(scene, scene.rectitem)[1]
		if  __num_rect < scene.spinbox.value():
			scene.spinbox.setValue(__num_rect)
			scene.spinbox.notify()
		else: pass
		

	# добавление одного rectitem на сцену
	def add_one_rect(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem):
		self.remove_all_rectitem(scene)
		# scene.addItem(rect)
		# выдает ошибку 'QGraphicsScene::addItem: item has already been added to this scene'
		# поэтому делаем так:
		rect = RectItemAction()	
		rect.setRect(rectitem.rect())
		
		scene.addItem(rect)	
		rect.setZValue(1) # пряиоугольник на передний план	


	# последовательное размещение произвольного количества rectitem на сцене по одному
	def add_certain_rect(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem, num: int):		
		n_list = self.num_rect_in_scene(scene, rectitem)
		column = n_list[0]# возможное количество страниц по ширине(количество колонок)
		row = n_list[1] # возможное количество страниц по высоте(количество строк)
		
		width_rect = rectitem.rect().width()
		height_rect = rectitem.rect().height()
		
		if (num - len( self.list_rect(scene)) ) != 0: 
			self.remove_all_rectitem(scene)
			for i in range(num):
				# scene.addItem(rect)
		        # выдает ошибку 'QGraphicsScene::addItem: item has already been added to this scene'
		        # поэтому делаем так:
				rect = RectItemAction()
				rect.setRect(rectitem.rect())
				rect.setZValue(1)
				coor = CalculateDifferentValue.coord_rect(i, column, row)
				
				rect.moveBy(self.pos_x + width_rect * coor[0],
							self.pos_y + height_rect * coor[1])               
				scene.addItem(rect)
		else: pass		
				
	# добавление rectitem на сцену, которые полностью покрывают рисунок
	def add_all_rect (self, scene: QGraphicsScene, rectitem: QGraphicsRectItem):
		_r = rectitem.rect()	
		width_rect = _r.width()
		height_rect = _r.height()
		
		num_x = self.num_rect_in_scene(scene, rectitem)[0]  # количество rectitem  по оси х (горизонтали)
		num_y = self.num_rect_in_scene(scene, rectitem)[1]  # количество rectitem  по оси у (вертикали)
				
		self.remove_all_rectitem(scene) # удаляем предыдущие rectitem
				
		for i in range(0, num_y):	
			for j in range(0, num_x):
				#scene.addItem(rect)
		        # выдает ошибку 'QGraphicsScene::addItem: item has already been added to this scene'
		        # поэтому делаем так:
				_rect =  RectItemAction()	
				_rect.setRect(_r)			
				scene.addItem(_rect)
				_rect.setZValue(1)  # пряиоугольник на передний план			
				_rect.moveBy(j * width_rect, i * height_rect)
	
			
				
calc = CalculateDifferentValue()

class Func:
	
	
	######################################################################################
	# в названиях функций первое имя виджета - наблюдатель, второе имя - источник
	######################################################################################
	
	#######################################################################################	
	################# методы определяющие формат страницы для QPageLayout #################
	def function_pagelayout_portrait (*args):
		args[0].setOrientation(QPageLayout.Orientation.Portrait)
						
	def function_pagelayout_landscape(*args):
		args[0].setOrientation(QPageLayout.Orientation.Landscape)
					
	def function_pagelayout_papersize(*args):
		if args[1].currentText() == "": pass # проверяем на пустую строку, т.к. при очистке списка посылается сигнал наблюдателю
		else:
			args[0].setPageSize(QPageSize(p.dict_support_pages()[args[1].currentText()]))
						
	def function_pagelayout_left(*args):		
		args[0].setLeftMargin(args[1].value())
							
	def function_pagelayout_top(*args):		
		args[0].setTopMargin(args[1].value())
							
	def function_pagelayout_right(*args):	
		args[0].setRightMargin(args[1].value())
					
	def function_pagelayout_bottom(*args):	
		args[0].setBottomMargin(args[1].value())
				
	
	function_for_pagelayout = {
		"portrait": function_pagelayout_portrait,
		"landscape": function_pagelayout_landscape,
		"papersize": function_pagelayout_papersize,
		"left": function_pagelayout_left,
		"top": function_pagelayout_top,
		"right": function_pagelayout_right,
		"bottom": function_pagelayout_bottom
		}
	
	#######################################################################################
	################# методы на клик по выбору принтера ComboBoxPrinter ###################
	def function_choise_printer(*args):
		args[0].clear()
		for key in p.dict_prn_ppr()[args[1].currentText()]:
			args[0].addItem(key)
				
		
	function_for_combobox_printer = {
		"printer": function_choise_printer
		}
	
	###################################################################################################
	################# методы изменентя содержимого Scene ##############################################
		
	def function_scene_rectitem(*args):
		Func.manipulation_pixmap(args[0])
		if len (calc.list_rect(args[0])) > 1:
			if args[0].manipulation.get_status_image()[1] == "print_all":
				calc.add_all_rect(args[0], args[1])
			else: calc.add_certain_rect(args[0], args[1], len (calc.list_rect(args[0])))
		else:
			calc.add_one_rect(args[0], args[1])
								
	def function_scene_pixmap_stretch(*args):
		if args[0].pixmap.isNull(): pass			
		else: 
			Func.stretch_pixmap(args[0])	
			calc.add_one_rect(args[0], args[0].rectitem)	
	
	def function_scene_pixmap_realsize(*args):
		if args[0].pixmap.isNull(): pass			
		else:
			Func.realsize_pixmap(args[0])		
			calc.add_certain_rect(args[0], args[0].rectitem, args[0].spinbox.value())
		
	def function_scene_pixmap_in_width(*args):
		if args[0].pixmap.isNull(): pass			
		else:
			Func.in_width_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].rectitem)
		
	def function_scene_pixmap_in_height(*args):
		if args[0].pixmap.isNull(): pass			
		else:
			Func.in_height_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].rectitem)
		
	def function_scene_pixmap_stretch_proportion(*args):
		if args[0].pixmap.isNull(): pass			
		else:
			Func.stretch_proportion_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].rectitem)
			
	def function_scene_spinbox_number_of_pages(*args):
		calc.add_certain_rect(args[0], args[0].rectitem, args[1].value())
	
	def function_scene_print_all(*args):
		Func.realsize_pixmap(args[0])		
		calc.add_all_rect(args[0], args[0].rectitem)
		args[0].spinbox.setValue( len(calc.list_rect(args[0])) )
		
	function_for_scene = {
		"rectitem": function_scene_rectitem,
		"stretch": function_scene_pixmap_stretch,
		"in_width": function_scene_pixmap_in_width,
		"in_height": function_scene_pixmap_in_height,
		"realsize": function_scene_pixmap_realsize,
		"stretch_proportion": function_scene_pixmap_stretch_proportion, 
		"number_of_pages": function_scene_spinbox_number_of_pages,
		"print_all": function_scene_print_all
		}
	
	
	
	#####################################################################################################
	################ Вспомогательные функции манипулирование картинкой и rectitem #######################
	
	def remove_pixmap(scene: QGraphicsScene): 
		for i in scene.items():
			if isinstance(i, QGraphicsPixmapItem):
				scene.removeItem(i)
			else: pass		
	
	def return_size_rectitem(scene: QGraphicsScene) -> list[int]:
		#первый элемент - ширина rectitem, второй - высота
		return int(scene.rectitem.rect().width()), int(scene.rectitem.rect().height())
	
	def stretch_pixmap(scene: QGraphicsScene):		
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.pixmap.scaled(Func.return_size_rectitem(scene)[0], Func.return_size_rectitem(scene)[1],
						transformMode = Qt.TransformationMode.FastTransformation))
		
	
	def in_width_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.pixmap.scaledToWidth(Func.return_size_rectitem(scene)[0],
                                      mode = Qt.TransformationMode.FastTransformation))
		
	def in_height_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1],
                                      mode = Qt.TransformationMode.FastTransformation))
                                      
	def stretch_proportion_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)		
		#  проверяем на наличие нуля в размерах
		if scene.pixmap.width() == 0 or scene.pixmap.height() == 0 or scene.rectitem.rect().width() == 0 or scene.rectitem.rect().height() == 0:
			pass
		
		else: #сравнение отношение ширины к высоте у pixmap и rectitem
		
			if (scene.pixmap.width() / scene.pixmap.height()) > (scene.rectitem.rect().width() / scene.rectitem.rect().height()):
				scene.addPixmap(scene.pixmap.scaledToWidth(Func.return_size_rectitem(scene)[0],	mode = Qt.TransformationMode.FastTransformation))
		
			elif (scene.pixmap.width() / scene.pixmap.height()) < (scene.rectitem.rect().width() / scene.rectitem.rect().height()):
				scene.addPixmap(scene.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1], mode = Qt.TransformationMode.FastTransformation))
		
			else: scene.addPixmap(scene.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1], mode = Qt.TransformationMode.FastTransformation)) 
					
				
	def realsize_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.pixmap)
			
	def manipulation_pixmap(scene: QGraphicsScene):	#  вызывается при изменении rectitem и pixmap
		if scene.manipulation.get_status_image()[0] == "stretch":
			Func.stretch_pixmap(scene)
									
		elif scene.manipulation.get_status_image()[0] == "realsize":				
			Func.realsize_pixmap(scene)
						
		elif scene.manipulation.get_status_image()[0] == "in_width":
			Func.in_width_pixmap(scene)
			
		elif scene.manipulation.get_status_image()[0] == "in_height":
			Func.in_height_pixmap(scene)
			
		elif scene.manipulation.get_status_image()[0] == "stretch_proportion":
			Func.stretch_proportion_pixmap(scene)
				
		else: pass
		
		if scene.manipulation.get_status_image()[0] == "realsize" and scene.manipulation.get_status_image()[1] == "print_all":
			calc.add_all_rect(scene, scene.rectitem)
		
		elif scene.manipulation.get_status_image()[0] == "realsize" and scene.manipulation.get_status_image()[1] == "number_of_pages":
			
			__num = calc.num_rect_in_scene(scene, scene.rectitem)[0] * calc.num_rect_in_scene(scene, scene.rectitem)[1]
			
			if __num == 1:
				calc.remove_all_rectitem(scene)
				calc.add_one_rect(scene, scene.rectitem)
				scene.spinbox.setValue(1)
				
			elif __num > 1:				
				calc.remove_all_rectitem(scene)
				#scene.spinbox.setValue(__num) ############################### если в спинбоксе число rectitem больше чем вмещается на картинку
				scene.spinbox.notify()
				
			else: pass
												
		else: pass
	
	#######################################################################################
	####################### Вспомогательные функции для печати ############################
	def rectitem_from_dpi(rectitem: QGraphicsRectItem, width: float, height: float, dpi: int):
		#перевод размеров в пикселях из миллиметров исходя из плотности печати точек на дюйм (25,4 mm)
		if dpi == 0 or width == 0 or height == 0: pass		
		else:			
			w = width * float(dpi) / 25.4
			h = height * float(dpi) / 25.4	
			rectitem.setRect(0, 0, w, h)
					
	####################################################################################################
	################# методы изменентя содержимого SpinBox  в зависимости от Manipulation  #############
	def function_for_spinbox_manipulations_numpages(*args):
		args[0].setValue(args[1].get_num_pages())
		
	function_for_widgets_manipulations = {
		"manipulation": function_for_spinbox_manipulations_numpages
	}
		
	######################################################################################################
	################# методы изменентя содержимого RectItem ##############################################
	def function_rectitem_pagelayout(*args): 
		# ширина = полная ширина минус левое и правое поле в mm
		width_mm = args[1].fullRect().width() - args[1].margins().left() - args[1].margins().right()
		# высота = полная высота минус верхнее и нижнее поле в mm
		height_mm = args[1].fullRect().height() - args[1].margins().top() - args[1].margins().bottom()
		
		# добавление оригинаоьного rectItem  без пересчета dpi
		args[0].manipulation.set_orig_rect(QRectF(0,0, width_mm, height_mm))
		
		Func.rectitem_from_dpi(args[0], width_mm, height_mm, args[0].manipulation.get_dpi()[0])
		
				
	def function_rectitem_manipulation(*args): ###############!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		width = args[0].manipulation.get_orig_rect().width() 
		height = args[0].manipulation.get_orig_rect().height()
				
		Func.rectitem_from_dpi(args[0], width, height, args[1].get_dpi()[0])
		
				
	function_for_rectitem = {
		"pagelayout": function_rectitem_pagelayout,
		"manipulation": function_rectitem_manipulation
		}
	
	
	################# методы изменентя содержимого Manipulation #####################################
	def function_manipulation_stretch(*args):
		args[0].set_status_image(args[1].get_name(), "")
						
	def function_manipulation_realsize(*args):
		args[0].set_status_image(args[1].get_name(), "")
		
	def function_manipulation_in_width(*args):
		args[0].set_status_image(args[1].get_name(), "")
		
	def function_manipulation_in_height(*args):
		args[0].set_status_image(args[1].get_name(), "")
		
	def function_manipulation_stretch_proportion(*args):
		args[0].set_status_image(args[1].get_name(), "")	
							
	def function_manipulation_print_all(*args):
		args[0].set_status_image("realsize", args[1].get_name())
		
	def function_manipulation_number_of_pages(*args):
		args[0].set_status_image("realsize", args[1].get_name())
	
	def function_manipulation_printer(*args):
		args[0].set_dpi(*p.list_prn_dpi(args[1].currentText()))
		args[0].set_name_printer(args[1].currentText())
		
			
	def function_manipulation_pagelayout(*args):
		args[0].set_pagelayout(args[1])
																		
	function_for_manipulation = {
		"stretch": function_manipulation_stretch,
		"realsize": function_manipulation_realsize,
		"print_all": function_manipulation_print_all,
		"in_width": function_manipulation_in_width,
		"in_height": function_manipulation_in_height,
		"stretch_proportion": function_manipulation_stretch_proportion,
		"number_of_pages": function_manipulation_number_of_pages,
		"printer": function_manipulation_printer,
		"pagelayout": function_manipulation_pagelayout
		}

	################################################################
	#################### Печать картинки ###########################
	@staticmethod
	def print_pixmap_from_scene(button: QPushButton, scene: QGraphicsScene, manipulation):
		list_coor_rect = [i.scenePos() for i in scene.items() if isinstance (i, QGraphicsRectItem) ]
		pixmap = [i for i in scene.items() if isinstance (i, QGraphicsPixmapItem)][0].pixmap()
		
		#print("physicalDpiX ", pixmap.physicalDpiX())
		#print("physicalDpiY", pixmap.physicalDpiY())
		#print("logicalDpiX", pixmap.logicalDpiX())
		#print("logicalDpiY", pixmap.logicalDpiY())
		
		#список из частей картинки для печати
		copy_pixmap = [pixmap.copy( int(coor.x()), int(coor.y()), int(scene.rectitem.rect().width()), int(scene.rectitem.rect().height()) )
																												for coor in list_coor_rect]
		
		if manipulation.get_name_printer() == const.PR_PDF: # если выбрана печать "to PDF"
			file_name = QFileDialog.getSaveFileName(button, "Save File", ".", "PDF (*.pdf)")
			if file_name[0] == "": pass
			else: printer = QPdfWriter(file_name[0])
		elif manipulation.get_name_printer() == "":
			print("no printer selected")
		else:
			printer = QPrinter()
			printer.setPrinterName(manipulation.get_name_printer())
		
		printer.setResolution(int(manipulation.get_dpi()[0]))
				
		printer.setPageLayout(manipulation.get_pagelayout())
		#printer.setOutputFileName("test.pdf")
		painter = QPainter()
		painter.begin(printer)
		
		pix = copy_pixmap[::-1] ################################# печатает в обратном порядке, поэтому так 
		for p in pix:    
			painter.drawPixmap(0,0, p)
			if pix.index(p) < len(pix) - 1:
				printer.newPage()
			else: pass
		painter.end()	
		
