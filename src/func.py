import src.const as const
import os
from src.load_setting import *
from src.dict_prn_ppr import * 
from src.rect_item_appearance_and_action import *
from src.useful_function import *
p = DictPrnPpr()

class CalculateDifferentValue:	
	def __init__(self):		
		self.pos_x = 0
		self.pos_y = 0
		self.qrect = None


	def num_rect_in_scene(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem) -> list[int]:
		''' Количество rectitem на сцене по горизонтали и вертикали	'''
		
		if rectitem.rect().width() != 0 and rectitem.rect().height() != 0:
                
			if scene.carcase.pixmap.width() % rectitem.rect().width() :
				n_width = scene.carcase.pixmap.width() // rectitem.rect().width() + 1
			else: n_width = scene.carcase.pixmap.width() // rectitem.rect().width()
        
			if scene.carcase.pixmap.height() % rectitem.rect().height() :
				n_height = scene.carcase.pixmap.height() // rectitem.rect().height() + 1
			else: n_height = scene.carcase.pixmap.height() // rectitem.rect().height()
               
			return int (n_width), int (n_height)
			
		else:
			return 0, 0	
		
	
	def list_rect(self, scene: QGraphicsScene) -> list[QGraphicsRectItem]:
		''' Список из rectitem на сцене '''
		
		return [i for i in scene.items() if isinstance(i, QGraphicsRectItem)]
		
		#list = []
		#for i in scene.items():
		#	if isinstance(i, QGraphicsRectItem):
		#		list.append(i)
		#	else: pass
		#return list
	
	@staticmethod
	def coord_rect(num: int, total_column: int, total_row: int) -> list[int]:
		'''Возвращает список с координатами rectitem (номера столбца и строки)'''
		
		num_column  = num % total_column
		num_row = num // total_column		
		return  num_column, num_row
	
	
	@staticmethod
	def coord_rect_x_y(scene: QGraphicsScene) -> list[QPointF]:
		'''Возвращает список с координатами rectitem X и Y'''
		
		return [i.pos() for i in scene.items() if isinstance(i, QGraphicsRectItem)]
	
	
	def remove_all_rectitem(self, scene: QGraphicsScene) -> None:
		'''Удаляет все rectitem на сцене'''
		
		for i in scene.items():
			if  isinstance(i, QGraphicsRectItem):
				scene.removeItem(i)
			else: pass

	
	
	def add_one_rect(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem) -> None:
		'''Добавление одного rectitem на сцену'''
		
		self.remove_all_rectitem(scene)
		# scene.addItem(rect)
		# выдает ошибку 'QGraphicsScene::addItem: item has already been added to this scene'
		# поэтому делаем так:
		rect = RectItemAppearanceAndAction()	
		rect.setRect(rectitem.rect())
		
		scene.addItem(rect)	
		rect.setZValue(1) # прямоугольник на передний план

		scene.carcase.spinbox_number_of_pages.setValue(1)

 
	def add_certain_rect(self, scene: QGraphicsScene, rectitem: QGraphicsRectItem, num: int):
		'''Последовательное размещение произвольного количества rectitem на сцене по одному'''
		
		n_list = self.num_rect_in_scene(scene, rectitem)
		
		column = n_list[0]# возможное количество страниц по ширине(количество колонок)
		row = n_list[1] # возможное количество страниц по высоте(количество строк)
				
		_r = rectitem.rect()
		
		width_rect = _r.width()
		height_rect = _r.height()
		
		self.remove_all_rectitem(scene)
		
		for i in range(num):
			# scene.addItem(rect)
		    # выдает ошибку 'QGraphicsScene::addItem: item has already been added to this scene'
		    # поэтому делаем так:
			_rect = RectItemAppearanceAndAction()
			_rect.setRect(_r)
			_rect.setZValue(1)
			coor = CalculateDifferentValue.coord_rect(i, column, row)
				
			_rect.moveBy(self.pos_x + width_rect * coor[0],
							self.pos_y + height_rect * coor[1])               
			scene.addItem(_rect)
						
	
	def add_all_rect (self, scene: QGraphicsScene, rectitem: QGraphicsRectItem) -> None:
		'''добавление rectitem на сцену, которые полностью покрывают рисунок'''
		
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
				_rect =  RectItemAppearanceAndAction()	
				_rect.setRect(_r)			
				scene.addItem(_rect)
				_rect.setZValue(1)  # пряиоугольник на передний план			
				_rect.moveBy(j * width_rect, i * height_rect)
	
				
calc = CalculateDifferentValue()


######################################################################################
# в названиях функций первое имя виджета - наблюдатель, второе имя - источник
######################################################################################
class Func:
	
	#  размер бумаги при смене принтера (args[0] - Observer, args[1] - Subject)
	#										combobox_papers			combobox_printers
	def function_for_papers_from_printer (*args):
		if args[0]:
			args[0].clear()
			for key in p.dict_prn_ppr()[args[1].currentText()]:
				args[0].addItem(key)
		else: pass

	###################################################################
	########### Функции для смены картинки в label_plus_image #########
	def function_label_plus_image_portrait (*args):		
		args[0].setPixmap(QPixmap(".icons/fields_p.png"))

	def function_label_plus_image_landscape (*args):
		args[0].setPixmap(QPixmap(".icons/fields_l.png"))
	
	###################################################################
	######## функции определяющие формат страницы для QPageLayout #####
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

	###################################################################################################
	################# функции изменения содержимого Scene #############################################
		
	def function_scene_rectitem(*args):
	
		# установка макс. возможного количества rectitem (setMaximum spinbox)
		__num = calc.num_rect_in_scene(args[0], args[0].carcase.rect)[0] * calc.num_rect_in_scene(args[0], args[0].carcase.rect)[1]
		args[0].carcase.spinbox_number_of_pages.setMaximum( __num )
			
		#Func.manipulation_pixmap(args[0])	
		
		if len (calc.list_rect(args[0])) > 1:
			if args[0].carcase.print_all.isChecked():
				calc.add_all_rect(args[0], args[1])
			else:
				calc.add_certain_rect(args[0], args[1], len (calc.list_rect(args[0])))
		else:
			calc.add_one_rect(args[0], args[1])
		
		
	def function_scene_pixmap_stretch(*args):
		args[0].carcase.spinbox_number_of_pages.setDisabled(True)
		if args[0].carcase.pixmap.isNull(): pass			
		else: 
			Func.stretch_pixmap(args[0])	
			calc.add_one_rect(args[0], args[0].carcase.rect)
				
	def function_scene_pixmap_realsize(*args):
		args[0].carcase.spinbox_number_of_pages.setEnabled(True)
		if args[0].carcase.pixmap.isNull(): pass			
		else:
			Func.realsize_pixmap(args[0])
			calc.add_certain_rect(args[0], args[0].carcase.rect, args[0].carcase.spinbox_number_of_pages.value())
						
	def function_scene_pixmap_in_width(*args):
		args[0].carcase.spinbox_number_of_pages.setDisabled(True)
		if args[0].carcase.pixmap.isNull(): pass			
		else:
			Func.in_width_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].carcase.rect)
		
	def function_scene_pixmap_in_height(*args):
		args[0].carcase.spinbox_number_of_pages.setDisabled(True)
		if args[0].carcase.pixmap.isNull(): pass			
		else:
			Func.in_height_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].carcase.rect)
		
	def function_scene_pixmap_stretch_proportion(*args):
		args[0].carcase.spinbox_number_of_pages.setDisabled(True)
		if args[0].carcase.pixmap.isNull(): pass			
		else:
			Func.stretch_proportion_pixmap(args[0])
			calc.add_one_rect(args[0], args[0].carcase.rect)
			
	def function_scene_spinbox_number_of_pages(*args):
		calc.add_certain_rect(args[0], args[0].carcase.rect, args[1].value())

	def function_scene_print_all(*args):
		args[0].carcase.spinbox_number_of_pages.setDisabled(True)
		Func.realsize_pixmap(args[0])		
		calc.add_all_rect(args[0], args[0].carcase.rect)		


	###################################################################################################
	####### функция изменения Manipulation и дальнейшие действия при открытии файла ###################
	
	def function_manipulation_button_open(*args):
		# при открытии новой картинки старая удаляется
		# func.Func.remove_pixmap(self.scene)
		#
				
		fileName = QFileDialog.getOpenFileName(parent = None, caption = "Open File", 
				directory = ".", filter = "Images (*.png *.PNG *.xpm *.XPM *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.tiff *.TIFF *.webp *.WEBP *.svg *.SVG)")
			
		if fileName[0] == "":
			pass
		else :
			args[1].carcase.pixmap.load(fileName[0])
			Func.remove_pixmap(args[1].carcase.scene)	
			args[1].carcase.scene.addPixmap(args[1].carcase.pixmap)
			Func.manipulation_pixmap(args[1].carcase.scene)			
			args[0].set_dpi(args[1].carcase.pixmap.physicalDpiX())
			
			
	def function_manipulation_label_dd(*args):
		
		fileName = args[1].get_name_file()
			
		if fileName == "" or fileName == None:
			pass
		else :
			args[1].carcase.pixmap.load(fileName)
			Func.remove_pixmap(args[1].carcase.scene)	
			args[1].carcase.scene.addPixmap(args[1].carcase.pixmap)
			Func.manipulation_pixmap(args[1].carcase.scene)			
			args[0].set_dpi(args[1].carcase.pixmap.physicalDpiX())	
	
	
	
	#####################################################################################################
	################ Вспомогательные функции манипулирование картинкой и rectitem #######################
	
	def remove_pixmap(scene: QGraphicsScene): 
		for i in scene.items():
			if isinstance(i, QGraphicsPixmapItem):
				scene.removeItem(i)
			else: pass		
	
	def return_size_rectitem(scene: QGraphicsScene) -> list[int]:
		#первый элемент - ширина rectitem, второй - высота
		return int(scene.carcase.rect.rect().width()), int(scene.carcase.rect.rect().height())
	
	def stretch_pixmap(scene: QGraphicsScene):		
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.carcase.pixmap.scaled(Func.return_size_rectitem(scene)[0], Func.return_size_rectitem(scene)[1],
						transformMode = Qt.TransformationMode.FastTransformation))
		
	
	def in_width_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.carcase.pixmap.scaledToWidth(Func.return_size_rectitem(scene)[0],
                                      mode = Qt.TransformationMode.FastTransformation))
		
	def in_height_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.carcase.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1],
                                      mode = Qt.TransformationMode.FastTransformation))
                                      
	def stretch_proportion_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)		
		#  проверяем на наличие нуля в размерах
		if scene.carcase.pixmap.width() == 0 or scene.carcase.pixmap.height() == 0 or scene.carcase.rect.rect().width() == 0 or scene.carcase.rect.rect().height() == 0:
			pass
		
		else: #сравнение отношение ширины к высоте у pixmap и rectitem
		
			if (scene.carcase.pixmap.width() / scene.carcase.pixmap.height()) > (scene.carcase.rect.rect().width() / scene.carcase.rect.rect().height()):
				scene.addPixmap(scene.carcase.pixmap.scaledToWidth(Func.return_size_rectitem(scene)[0],	mode = Qt.TransformationMode.FastTransformation))
		
			elif (scene.carcase.pixmap.width() / scene.carcase.pixmap.height()) < (scene.carcase.rect.rect().width() / scene.carcase.rect.rect().height()):
				scene.addPixmap(scene.carcase.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1], mode = Qt.TransformationMode.FastTransformation))
		
			else: scene.addPixmap(scene.carcase.pixmap.scaledToHeight(Func.return_size_rectitem(scene)[1], mode = Qt.TransformationMode.FastTransformation)) 
				
	def realsize_pixmap(scene: QGraphicsScene):
		Func.remove_pixmap(scene)
		scene.addPixmap(scene.carcase.pixmap)
			
	def manipulation_pixmap(scene: QGraphicsScene):	#  вызывается при изменении rectitem и pixmap
		
		if scene.carcase.stretch.isChecked():			
			Func.stretch_pixmap(scene)
		
		elif scene.carcase.realsize.isChecked():
			Func.realsize_pixmap(scene)
			
		elif scene.carcase.in_width.isChecked():
			Func.in_width_pixmap(scene)
			
		elif scene.carcase.in_height.isChecked():
			Func.in_height_pixmap(scene)
			
		elif scene.carcase.stretch_proportion.isChecked():
			Func.stretch_proportion_pixmap(scene)

		elif scene.carcase.print_all.isChecked():
			calc.add_all_rect(scene, scene.carcase.rect)		
												
		else: pass
	
	#######################################################################################
	####################### Вспомогательные функции для печати ############################
	def rectitem_from_dpi(rectitem: QGraphicsRectItem, width: float, height: float, dpi: int):
		'''Перевод размеров в пикселях из миллиметров исходя из плотности печати точек на дюйм (25,4 mm)'''
		
		if dpi == 0 or width == 0 or height == 0: pass		
		else:			
			w = width * float(dpi) / 25.4
			h = height * float(dpi) / 25.4	
			rectitem.setRect(0, 0, w, h)
					
	####################################################################################################
	################# функции изменентя содержимого SpinBox  в зависимости от Manipulation  ############
	def function_for_spinbox_manipulations_numpages(*args):
		args[0].setValue(args[1].get_num_pages())
		
			
	######################################################################################################
	################# методы изменентя содержимого RectItem ##############################################
	def function_rectitem_pagelayout(*args): 
		# ширина = полная ширина минус левое и правое поле в mm
		width_mm = args[1].fullRect().width() - args[1].margins().left() - args[1].margins().right()
		# высота = полная высота минус верхнее и нижнее поле в mm
		height_mm = args[1].fullRect().height() - args[1].margins().top() - args[1].margins().bottom()
		
		# добавление оригинального rectItem  без пересчета dpi
		args[0].carcase.manipulation.set_orig_rect(QRectF(0,0, width_mm, height_mm))
		
		Func.rectitem_from_dpi(args[0], width_mm, height_mm, args[0].carcase.manipulation.get_dpi()[0])
		
		
	def function_rectitem_manipulation(*args):
		
		width = args[1].get_orig_rect().width() 
		height = args[1].get_orig_rect().height()
				
		Func.rectitem_from_dpi(args[0], width, height, args[1].get_dpi()[0])
	

	####################################################################
	# смена языка интерфейса (args[0] - Observer, args[1] - Subject)
	#								Carcase			combobox_lang
	
	def function_for_combobox_lang (*args):
		if args[0].get_dict_lang() != args[1].currentText() and args[0].get_dict_lang() != "":			
			# запись в файл setting выбраного в комбобоксе языка lang
			read_and_write_setting(const.FILE_SETTING, "lang", args[1].currentText()) # функция из src.useful_function
			
			######## смена языка на виджетах
			################################
			os.chdir(const.DIR_SRC)
			os.chdir(const.DIR_LANG)
			
			setting = LoadSetting()
			args[0].set_dict_lang(setting.create_dict_i18n_from_combobox(args[1].currentText()))
			os.chdir("../../")
			
			for element in args[0].get_list_element_with_text():
				if isinstance(element, QGroupBox):
					element.setTitle(args[0].get_dict_lang()[element.get_name()])
				elif isinstance(element, QTabWidget):
					_txt = args[0].get_dict_lang()[element.get_name()].split()
					element.setTabText(0, _txt[0])
					element.setTabText(1, _txt[1])
				else: element.setText(args[0].get_dict_lang()[element.get_name()])
			
		else: pass


	####################################################################
	### маштабирование картинки (args[0] - lcd, args[1] - slider) ########
	
	def function_for_view_slider(*args):
		sc = args[1].value()
		transform = QTransform()
		scale_x = sc / 100
		scale_y = sc / 100
		transform.scale(scale_x, scale_y)
		args[0].setTransform(transform)
	
	
	def function_for_lcd_slider(*args):		
		args[0].display(args[1].value())
	
	
	def function_for_slider_scale_lcd(*args):		
		sc = args[1].value()
		transform = QTransform()
		scale_x = sc / 100
		scale_y = sc / 100
		transform.scale(scale_x, scale_y)
		args[1].carcase.view.setTransform(transform)
		
		
	################################################################
	################################################################
	# количество экземпляров для печати (args[0] - Observer, args[1] - Subject)
	#								sp_num_of_copies			combobox_printers
	
	def function_for_num_of_copies_from_printers(*args):
		
		if args[1].currentText () == const.PR_PDF: # если выбрана печать в PDF
			args[0].setValue(1)
			args[0].setDisabled(True)
		else: args[0].setEnabled(True)
		
	
	################################################################
	#################### Печать картинки ###########################
				#### ags[0] и args[1] это button_print
	
	def print_pixmap_from_scene(*args):
		
		scene = args[0].carcase.scene
		rect = args[0].carcase.rect
		combobox_printers = args[0].carcase.combobox_printers
		pagelayout = args[0].carcase.pagelayout
		manipulation = args[0].carcase.manipulation
		num_copies = args[0].carcase.sp_num_of_copies.value()
				
		list_coor_rect = [i.scenePos() for i in scene.items() if isinstance (i, QGraphicsRectItem) ]
		pixmap = [i for i in scene.items() if isinstance (i, QGraphicsPixmapItem)][0].pixmap()
		
		#список из частей картинки для печати
		copy_pixmap = [pixmap.copy( int(coor.x()), int(coor.y()), int(rect.rect().width()), int(rect.rect().height()) ) for coor in list_coor_rect]
		
		if combobox_printers.currentText() == const.PR_PDF:
			file_name = QFileDialog.getSaveFileName(args[0], "Save File", ".", "PDF (*.pdf)")
			if file_name[0] == "": pass
			else: printer = QPdfWriter(file_name[0])		
		elif combobox_printers.currentText() == "":
			print("no printer selected")
		else:
			printer = QPrinter()			
			printer.setPrinterName(combobox_printers.currentText())
			printer.setCopyCount(num_copies)
		
		printer.setResolution(int(manipulation.get_dpi()[0]))
		printer.setPageLayout(pagelayout)
		
		painter = QPainter()
		painter.begin(printer)
		
		pix = copy_pixmap[::-1] ######## почему-то печатает в обратном порядке, 
		coor = list_coor_rect[::-1] ############################# поэтому так
		coor_x = 0 # координата х фрагмента картинки
		coor_y = 0 # координата у фрагмента картинки


		# #######Возможность произвольного размещения фрагмента картинки 
		# #################на листе при печати
		# если координаты рамки (rectitem) отрицательные, то смещаем координаты
		# фрагмента картинки на их абсолютное значение
		#
		# 				НА ЭКРАНЕ							НА ЛИСТЕ ПРИ ПЕЧАТИ
		#	(-x,-y)	--------------------					--------------------			
		#			|	рамка(rectitem)	|					|	рамка(rectitem)	|	
		#			|					|					|					|		
		#			|	(0,0)===========|============		|	(x,y)===========|		
		#			|		||			|			||		|		||			|
		#			|		|| фрагмент	|			||		|		|| фрагмент	|		
		#			|		|| картинки	|			||		|		|| картинки	|		
		#			|		|| для		|			||		|		|| для		|		
		#			|		|| печати	|			||		|		|| печати	|			
		#			|		||			|			||		|		||			|			
		#			|		||			|			||		|		||			|			
		#			---------------------			||		---------------------				
		# 					||						||					
		# 					||		картинка		||					
		# 					||						||						
		# 					==========================						
		# 			 
		for i in range(len(pix)):
			if coor[i].x() < 0:  
				coor_x = abs(coor[i].x()) 
			else: pass
			if coor[i].y() < 0:
				coor_y = abs(coor[i].y()) 
			else: pass
			if coor[i].x() >= 0 and coor[i].y() >= 0:
				coor_x = 0
				coor_y = 0
			else: pass

			painter.drawPixmap(int(coor_x), int(coor_y), pix[i])
			
			if i < len(pix) - 1:
				printer.newPage()
			else: pass

		painter.end()	
		
	
	#изменение brush 
	def function_brush_choice_color_rect(*args):		
		color = args[1].get_active_color()
		alpha = args[1].get_current_alpha()
		brush = args[0]
				
		# запись в файл setting выбраного цвета для rect и прозрачности alpha
		read_and_write_setting(const.FILE_SETTING, "active_color_rectangle", color.name()) # функция из src.useful_function
		read_and_write_setting(const.FILE_SETTING, "alpha", alpha)
		
		#смена цвета brush
		color.setAlpha(alpha)
		brush.setColor(color)
	
	def function_rectitem_brush(*args):
		rect =  args[0]
		brush = args[1]
		rect.setBrush(brush)
		
	def function_scene_brush(*args):
	
		scene = args[0]
		brush = args[1]
		for i in scene.items():
			if isinstance (i, QGraphicsRectItem):
				i.setBrush(brush)		
	
	function_for_element = {
		"portrait": 	{"pagelayout": function_pagelayout_portrait, "label_plus_image": function_label_plus_image_portrait},
		"landscape": 	{"pagelayout": function_pagelayout_landscape, "label_plus_image": function_label_plus_image_landscape},
		"left": 		{"pagelayout": function_pagelayout_left},
		"top": 			{"pagelayout": function_pagelayout_top},
		"right": 		{"pagelayout": function_pagelayout_right},
		"bottom": 		{"pagelayout": function_pagelayout_bottom},
		"rectitem": 	{"scene": function_scene_rectitem},
		"stretch": 		{"scene": function_scene_pixmap_stretch},
		"in_width": 	{"scene": function_scene_pixmap_in_width},
		"in_height": 	{"scene": function_scene_pixmap_in_height},
		"realsize": 	{"scene": function_scene_pixmap_realsize},
		"stretch_proportion": {"scene": function_scene_pixmap_stretch_proportion}, 
		"number_of_pages": {"scene": function_scene_spinbox_number_of_pages},
		"print_all": 	{"scene": function_scene_print_all},
		"manipulation": {"number_of_pages": function_for_spinbox_manipulations_numpages},
		"pagelayout": 	{"rectitem": function_rectitem_pagelayout},
		"manipulation": {"rectitem": function_rectitem_manipulation},
		"choise_printers": {"choise_papers": function_for_papers_from_printer, "sp_number_of_copies": function_for_num_of_copies_from_printers},
		"choise_papers": {"pagelayout": function_pagelayout_papersize},
		"choice_language": {"carcase": function_for_combobox_lang},
		"button_open": 	{"manipulation": function_manipulation_button_open},
		"label_dd":		{"manipulation": function_manipulation_label_dd},
		"button_print":	{"button_print": print_pixmap_from_scene},
		"slider": 		{"view": function_for_view_slider, "lcd": function_for_lcd_slider},
		"choice_color_rect": {"brush": function_brush_choice_color_rect},
		"brush": {"rectitem": function_rectitem_brush, "scene": function_scene_brush}
		}
