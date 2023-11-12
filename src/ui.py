from src.carcase import *



class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("5Print")
		self.create_ui()

	def create_ui(self):
		self.manipulation = Manipulation()
		self.manipulation.set_name("manipulation")
				
		self.pixmap = QPixmap()
		
		self.scene = Scene()
		self.scene.set_name("scene")
		self.scene.addPixmap(self.pixmap)
		
		self.view = QGraphicsView()
		self.view.setScene(self.scene)
		
		self.pagelayout = PageLayout()
		self.pagelayout.set_name("pagelayout")
		
		self.port = RadioButton(internationalization["portrait"])
		self.port.setChecked(True)
		self.port.set_name("portrait")
		
		self.land = RadioButton(internationalization["landscape"])
		self.land.set_name("landscape")
		
		self.stretch = RadioButton(internationalization["stretch"])
		self.stretch.set_name("stretch")
		
		self.in_width = RadioButton(internationalization["in_width"])
		self.in_width.set_name("in_width")
		
		self.in_height = RadioButton(internationalization["in_height"])
		self.in_height.set_name("in_height")
		
		self.stretch_proportion = RadioButton(internationalization["stretch_proportion"])
		self.stretch_proportion.set_name("stretch_proportion")
		
		self.spinbox_number_of_pages = SpinBoxField()
		self.spinbox_number_of_pages.set_name("number_of_pages")
		self.spinbox_number_of_pages.setMinimum(1)
		
		self.realsize = RealSizeRadioButton(internationalization["realsize"], self.spinbox_number_of_pages)
		self.realsize.set_name("realsize")
		self.realsize.setChecked(True)
		
		self.print_all = RadioButton(internationalization["print_all"])
		self.print_all.set_name("print_all")
		
		self.paper = ComboBoxPaperSize()
		self.paper.set_name("papersize")
		
		self.printer = ComboBoxPrinter()
		self.printer.set_name("printer")
		
		self.rect = RectItem()
		self.rect.set_name("rectitem")
		
		self.spinbox_left = SpinBoxField()
		self.spinbox_left.set_name("left")
		
		self.spinbox_top = SpinBoxField()
		self.spinbox_top.set_name("top")
		
		self.spinbox_right = SpinBoxField()
		self.spinbox_right.set_name("right")
		
		self.spinbox_bottom = SpinBoxField()
		self.spinbox_bottom.set_name("bottom")
		
		self.label_num_fragment = QLabel(internationalization["num_fragment"])
		self.label_left = QLabel(internationalization["left"])
		self.label_top = QLabel(internationalization["top"])
		self.label_right = QLabel(internationalization["right"])
		self.label_bottom = QLabel(internationalization["bottom"])
		
		self.button_open = ButtonOpenFile(self.manipulation)
		self.button_open.setText(internationalization["button_open"])
		
		self.button_print = ButtonPrint(self.scene, self.manipulation)
		self.button_print.setText(internationalization["button_print"])
		
		self.scale = QLabel(internationalization["scale"])
		self.slider = Slider(self.view)	
		
		###### добавление  к виджетам других виджетов #######################
		
		self.scene.add_objects(self.manipulation, self.pixmap, self.rect, self.spinbox_number_of_pages)
		self.button_open.add_objects(self.scene, self.pixmap)		
		self.rect.add_objects(self.manipulation)
		self.rect.add_parent_scene(self.scene)
		
		######## atach() присоеденяем наблюдателей #############
		
		self.rect.attach(self.scene)
		self.pagelayout.attach(self.rect)
		self.port.attach(self.pagelayout)
		self.land.attach(self.pagelayout)
		
		self.realsize.attach(self.scene)
		self.realsize.attach(self.manipulation)
		self.stretch.attach(self.scene)
		self.stretch.attach(self.manipulation)
		self.in_width.attach(self.scene)
		self.in_width.attach(self.manipulation)
		self.in_height.attach(self.scene)
		self.in_height.attach(self.manipulation)
		self.stretch_proportion.attach(self.scene)
		self.stretch_proportion.attach(self.manipulation)
		
		self.paper.attach(self.pagelayout)
		self.printer.attach(self.paper)
		self.printer.attach(self.manipulation)
		self.spinbox_left.attach(self.pagelayout)
		self.spinbox_top.attach(self.pagelayout)
		self.spinbox_right.attach(self.pagelayout) 		
		self.spinbox_bottom.attach(self.pagelayout)
		self.spinbox_number_of_pages.attach(self.scene)
		self.spinbox_number_of_pages.attach(self.manipulation)
		self.print_all.attach(self.scene)
		self.print_all.attach(self.manipulation)
		
		self.pagelayout.attach(self.manipulation)
		self.manipulation.attach(self.rect)
				
		##### notify() посылает сигнал наблюдателям при загрузке виджета ########
		self.port.notify() 
		self.realsize.notify()
		self.paper.notify()
		self.printer.notify()
		self.spinbox_top.notify()
		self.spinbox_left.notify()
		self.spinbox_right.notify()
		self.spinbox_bottom.notify()
		##########################################################
		##########################################################
		###### Страница
		self.layout_paper = QHBoxLayout()
		#self.layout_paper.setStretch(0,0)
		#self.layout_paper.addStrut(10)
		self.layout_paper.addWidget(self.port, alignment=Qt.AlignmentFlag.AlignTop)
		self.layout_paper.addWidget(self.land, alignment=Qt.AlignmentFlag.AlignTop)
		
		###### Картинка
		self.layout_pixmap = QVBoxLayout()
		self.layout_pixmap.addWidget(self.stretch)
		self.layout_pixmap.addWidget(self.in_width)
		self.layout_pixmap.addWidget(self.in_height)
		self.layout_pixmap.addWidget(self.stretch_proportion)
		self.layout_pixmap.addWidget(self.realsize)
		
		self.layout_sub_pixmap = QHBoxLayout()
		#self.layout_sub_pixmap.addSpacing(50)
		self.layout_sub_pixmap.addStretch(1)
		self.layout_sub_pixmap.addWidget(self.label_num_fragment)
		self.layout_sub_pixmap.addWidget(self.spinbox_number_of_pages)
		self.layout_pixmap.addLayout(self.layout_sub_pixmap)
		self.layout_pixmap.addWidget(self.print_all)
		
		##### Поля страницы
		self.layout_fields_spinbox = QVBoxLayout()
		self.layout_fields_spinbox.addWidget(self.spinbox_left)
		self.layout_fields_spinbox.addWidget(self.spinbox_top)
		self.layout_fields_spinbox.addWidget(self.spinbox_right)
		self.layout_fields_spinbox.addWidget(self.spinbox_bottom)
		
		self.layout_fields_label = QVBoxLayout()
		self.layout_fields_label.addWidget(self.label_left)
		self.layout_fields_label.addWidget(self.label_top)
		self.layout_fields_label.addWidget(self.label_right)
		self.layout_fields_label.addWidget(self.label_bottom)
		
		self.layout_fields = QHBoxLayout()
		self.layout_fields.addLayout(self.layout_fields_spinbox)
		self.layout_fields.addLayout(self.layout_fields_label)
		
		self.layout_printers = QVBoxLayout()
		self.layout_printers.addWidget(self.printer)
		self.layout_printers.addWidget(self.paper)
		
		
		####### Группы
		self.group_paper = QGroupBox(internationalization["page"])
		self.group_paper.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.group_paper.setLayout(self.layout_paper)
				
		self.group_fields = QGroupBox(internationalization["fields"])
		self.group_fields.setLayout(self.layout_fields)
		
		self.group_pixmap = QGroupBox(internationalization["image"])
		self.group_pixmap.setLayout(self.layout_pixmap)
		
		self.group_printers = QGroupBox(internationalization["printers"])
		self.group_printers.setLayout(self.layout_printers)
		
		
		###### Левая часть
		self.layout_left = QVBoxLayout()
		#self.layout_left.addStretch(1)
		#self.layout_left.setStretch(0,1)
		#self.layout_left.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
		self.layout_left.addWidget(self.group_paper)
		self.layout_left.addWidget(self.group_fields)
		self.layout_left.addWidget(self.group_pixmap)
		self.layout_left.addWidget(self.group_printers)
		self.layout_left.addSpacerItem(QSpacerItem(100,200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
		self.layout_left.setStretch(0,0)
		self.layout_left.setStretch(1,0)
		self.layout_left.setStretch(2,0)
		self.layout_left.setStretch(3,0)
		self.layout_left.setStretch(4,1)
		#self.layout_left.addWidget(self.printer)
		#self.layout_left.addWidget(self.paper)
		
		##### Правая часть
		self.layout_right = QVBoxLayout()
		self.layout_right.addWidget(self.button_open)
		self.layout_right.addWidget(self.view)
		self.layout_right.addWidget(self.button_print)
		
		self.scale_slider_layout = QHBoxLayout()
		self.scale_slider_layout.addWidget(self.scale)
		self.scale_slider_layout.addWidget(self.slider)
		
		self.layout_right.addLayout(self.scale_slider_layout)
		
		#### Итоговое размещение
		self.layout = QHBoxLayout() #self.layout.setStretch(4,1)
		self.layout.addLayout(self.layout_left)
		self.layout.addLayout(self.layout_right, stretch = 1)
		
		
		self.setLayout(self.layout)
		self.show()
		self.setMinimumWidth(500)
		
