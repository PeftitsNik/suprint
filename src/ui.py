from src.carcase import *


class UI():
	def __init__(self, carcase: Carcase):
		self.carcase = carcase	
		self.create_ui()

	def create_ui(self):

		icon_open = QIcon(QPixmap(".icons/open.svg"))
		self.carcase.button_open.setIcon(icon_open)   ###setStyleSheet("image: url(open.png);")
		
		icon_print = QIcon(QPixmap(".icons/print.svg"))
		self.carcase.button_print.setIcon(icon_print)
		
		icon_save = QIcon(QPixmap(".icons/save.svg"))
		self.carcase.button_save_all_images.setIcon(icon_save)
		
		
		icon_print1 = QIcon(QPixmap(".icons/print1.svg"))

		icon_setting = QIcon(QPixmap(".icons/setting.svg"))

		#self.image_fields = QPixmap(".icons/fields.png")

		self.window = QWidget()
		##########################################################
		##########################################################
		###### Страница
		self.layout_paper = QHBoxLayout()
		self.layout_paper.addWidget(self.carcase.portrait, alignment=Qt.AlignmentFlag.AlignTop)
		self.layout_paper.addWidget(self.carcase.landscape, alignment=Qt.AlignmentFlag.AlignTop)
		
		###### Картинка
		self.layout_image = QVBoxLayout()
		self.layout_image.addWidget(self.carcase.stretch)
		self.layout_image.addWidget(self.carcase.in_width)
		self.layout_image.addWidget(self.carcase.in_height)
		self.layout_image.addWidget(self.carcase.stretch_proportion)
		self.layout_image.addWidget(self.carcase.realsize)
		
		self.layout_sub_image = QHBoxLayout()
		self.layout_sub_image.addStretch(1)
		self.layout_sub_image.addWidget(self.carcase.label_num_fragment)
		self.layout_sub_image.addWidget(self.carcase.spinbox_number_of_pages)
		self.layout_image.addLayout(self.layout_sub_image)
		self.layout_image.addWidget(self.carcase.print_all)
		
		##### Поля страницы
		self.layout_fields_spinbox = QVBoxLayout()		
		self.layout_fields_spinbox.addWidget(self.carcase.spinbox_left)
		self.layout_fields_spinbox.addWidget(self.carcase.spinbox_top)
		self.layout_fields_spinbox.addWidget(self.carcase.spinbox_right)
		self.layout_fields_spinbox.addWidget(self.carcase.spinbox_bottom)
		
		self.layout_fields_label = QVBoxLayout()
		self.layout_fields_label.addWidget(self.carcase.label_left)
		self.layout_fields_label.addWidget(self.carcase.label_top)
		self.layout_fields_label.addWidget(self.carcase.label_right)
		self.layout_fields_label.addWidget(self.carcase.label_bottom)
		
		self.layout_fields = QHBoxLayout()
		self.layout_fields.addLayout(self.layout_fields_spinbox)
		self.layout_fields.addLayout(self.layout_fields_label)		
		#self.label_plus_image.setScaledContents(True)
		self.layout_fields.addWidget(self.carcase.label_plus_image)
		self.layout_fields.setStretch(0,0)
		self.layout_fields.setStretch(1,0)
		self.layout_fields.setStretch(2,0)
		
		self.layout_printers = QVBoxLayout()
		self.layout_printers_1 = QVBoxLayout()
		self.layout_printers_2 = QHBoxLayout()		
		self.layout_printers.addLayout(self.layout_printers_1)
		self.layout_printers.addLayout(self.layout_printers_2)
		
		self.layout_printers_1.addWidget(self.carcase.combobox_printers)
		self.layout_printers_1.addWidget(self.carcase.combobox_papers)
		self.layout_printers_2.addWidget(self.carcase.label_num_of_copies)
		self.layout_printers_2.addWidget(self.carcase.sp_num_of_copies)
				
		_f = QFontComboBox()
		_si = _f.currentFont().pointSize()	
		_s = f"font-size: {_si*2}px"
		
		self.carcase.label_p.setStyleSheet(_s)
		self.layout_printers_2.addWidget(self.carcase.label_p, Qt.AlignmentFlag.AlignLeft)
		
		self.layout_settings_lang = QVBoxLayout()		
		self.layout_settings_lang.addWidget(self.carcase.combobox_lang)
		
		self.layout_settings_color_rect = QVBoxLayout()
		self.layout_settings_color_rect.addWidget(self.carcase.choice_color_rect )
		
		####### Группы
		
		self.carcase.group_paper.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.carcase.group_paper.setLayout(self.layout_paper)
		self.carcase.group_fields.setLayout(self.layout_fields)
		self.carcase.group_image.setLayout(self.layout_image)
		self.carcase.group_printers.setLayout(self.layout_printers)
		self.carcase.group_settings_lang.setLayout(self.layout_settings_lang)
		self.carcase.group_settings_color_rect.setLayout(self.layout_settings_color_rect)
		
		###### Левая часть
		###### Печать
		self.layout_left_print = QVBoxLayout()
		self.layout_left_print.addWidget(self.carcase.group_paper)
		self.layout_left_print.addWidget(self.carcase.group_fields)
		self.layout_left_print.addWidget(self.carcase.group_image)
		self.layout_left_print.addWidget(self.carcase.group_printers)
	
		self.layout_left_print.addSpacerItem(QSpacerItem(50,20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
		self.layout_left_print.setStretch(0,0)
		self.layout_left_print.setStretch(1,0)
		self.layout_left_print.setStretch(2,0)
		self.layout_left_print.setStretch(3,0)
		self.layout_left_print.setStretch(4,0)
		self.layout_left_print.addStretch(1)
				
		###### Левая часть
		###### Настройки
		self.layout_left_setting = QVBoxLayout()
		self.layout_left_setting.addWidget(self.carcase.group_settings_lang)
		self.layout_left_setting.addWidget(self.carcase.group_settings_color_rect)
		self.layout_left_setting.addStretch(1)
		
		
		##### Правая часть
		self.layout_right_horizontal = QHBoxLayout()
		self.layout_right_horizontal.addWidget(self.carcase.button_open)
		self.layout_right_horizontal.addWidget(self.carcase.label_dd)
		self.layout_right_horizontal.setStretch(0,0)
		self.layout_right_horizontal.setStretch(1,1)		
		
		self.layout_print_and_save = QHBoxLayout()
		self.layout_print_and_save.addWidget(self.carcase.button_print)
		self.layout_print_and_save.addWidget(self.carcase.button_save_all_images)
		
		self.layout_right = QVBoxLayout()
		self.layout_right.addLayout(self.layout_right_horizontal)
		self.layout_right.addWidget(self.carcase.view)
		self.layout_right.addLayout(self.layout_print_and_save)
		
				
		self.scale_slider_layout = QHBoxLayout()
		self.scale_slider_layout.addWidget(self.carcase.scale)
		self.scale_slider_layout.addWidget(self.carcase.slider)
		self.scale_slider_layout.addWidget(self.carcase.lcd)
		self.scale_slider_layout.addSpacerItem(QSpacerItem(10,20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
		self.scale_slider_layout.setStretch(0,0)
		self.scale_slider_layout.setStretch(1,1)
		self.scale_slider_layout.setStretch(2,0)
		self.scale_slider_layout.setStretch(3,2)
		
		self.layout_right.addLayout(self.scale_slider_layout)		
		
		#########################################
		self.tab_widget_print = QWidget()
		self.tab_widget_print.setLayout(self.layout_left_print)
		
		self.tab_widget_setting = QWidget()
		self.tab_widget_setting.setLayout(self.layout_left_setting)				
		
		self.carcase.tab.addTab(self.tab_widget_print, self.carcase.icons_tab[0], self.carcase.txt_tab[0])
		self.carcase.tab.addTab(self.tab_widget_setting, self.carcase.icons_tab[1], self.carcase.txt_tab[1])
				
		
		self.widget_image = QWidget()
		self.widget_image.setLayout(self.layout_right)
		
				
		#### Итоговое размещение
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.carcase.tab, alignment=Qt.AlignmentFlag.AlignLeft)
		self.layout.addWidget(self.widget_image)
				
		
		self.window.setLayout(self.layout)
		self.window.show()
		self.window.setMinimumWidth(800)
		self.window.setWindowTitle("Suprint")
		self.window.setWindowIcon(QIcon(".icons/suprint.png"))
		

