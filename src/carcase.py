from src.elements import *
from src.interface import *
from src.load_setting import *
from src.dict_prn_ppr import *
import  src.func as func
import os
import locale

#___________________________________________________
#|													|
#|			Carcase									|
#|													|
#|этот класс содержит в себе все нижеперечисленные,	|
#|некоторые из которых содержат ссылку на Carcase	|
#|для доступа к другим классам						|
#| 													|
#|__________________________________________________|
#
#
#___________________________		_______________________			________________________	
#|	Subject	(наблюдаемое)	|<-----	|Observer(наблюдатель)	|   --- |Observer(наблюдатель)	|----
#|--------------------------|		|----------------------	|   |   |----------------------	|	|
#| виджеты  связанные		|		|	PageLayout			|   |   |	RectItem		 	|   |                    
#|      					|		|						|	|	|						|	|
#| с размером страницы		|		|						|   |   |						|	|
#| (альбомная, портретная,	|		|-----------------------|   |   |-----------------------|	|
#| поля, А0-4, и т.д.)		|		|Subject (наблюдаемое)	|<--    |Subject (наблюдаемое)	|	|
#|__________________________|		|_______________________|<---   |_______________________|	|
#																|				^               |
#																|				|				|
#								________________________		|				|				|						
#		------------------------|Observer(наблюдатель)	|------------------------               |
#		|						|----------------------	|       |                               |
#		|						|		Scene			|       |                               |
#		|						|						|       |                               |
#       |						|						|       |                               |
#       |						|						|       |                               |
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
#
#________________________
#|Subject (наблюдаемое)	|
#|---------------------	|		
#|						| button_print наблюдает сам за собой для удобства доступа
#| Button				| к методу печати из класса Func 
#| 						|
#| 						|	
#| 						|
#|----------------------|
#| Observer(наблюдатель)|
#|______________________|
# 
#
#
#

class Carcase(Carcase_Interfase, Element_Interface, Observer):
			
	def __init__(self, elements: Elements):
		self.elements = elements
		self._dict_lang = {}
		self.setting = LoadSetting()	
		self.list_element_with_text = []
		self.fill_forms_prn_ppr = Fill_Forms()
		self.set_name("carcase")
		
	def update_observer(self, subject: Subject):		
		func.function_for_element[subject.get_name()][self.get_name()](self, subject)
	
	def set_dict_lang(self, dict_lang: dict):
		self._dict_lang = dict_lang
	
	def get_dict_lang(self):
		return self._dict_lang	
	
	def get_list_element_with_text(self) -> list:
		return self.list_element_with_text
		
	def create_carcase(self):
		self.manipulation = self.elements.Manipulation()
		self.manipulation.set_name("manipulation")
		
		self.pixmap = self.elements.Pixmap()
		self.pixmap.set_name("pixmap")
		
		self.scene = self.elements.Scene(self)
		self.scene.set_name("scene")
		self.scene.addPixmap(self.pixmap)
		
		self.view = self.elements.GraphicsView()
		self.view.set_name("view")
		self.view.setScene(self.scene)
		
		self.pagelayout = self.elements.PageLayout()
		self.pagelayout.set_name("pagelayout")
		
		self.portrait = self.elements.RadioButton()
		self.portrait.setChecked(True)
		self.portrait.setText(self.get_dict_lang()["portrait"])
		self.portrait.set_name("portrait")
		self.list_element_with_text.append(self.portrait)
		
		self.landscape = self.elements.RadioButton()
		self.landscape.setText(self.get_dict_lang()["landscape"])
		self.landscape.set_name("landscape")
		self.list_element_with_text.append(self.landscape)
		
		self.stretch = self.elements.RadioButton()
		self.stretch.set_name("stretch")
		self.list_element_with_text.append(self.stretch)
		
		self.in_width = self.elements.RadioButton()
		self.in_width.set_name("in_width")
		self.list_element_with_text.append(self.in_width)
		
		self.in_height = self.elements.RadioButton()
		self.in_height.set_name("in_height")
		self.list_element_with_text.append(self.in_height)
		
		self.stretch_proportion = self.elements.RadioButton()
		self.stretch_proportion.set_name("stretch_proportion")
		self.list_element_with_text.append(self.stretch_proportion)
				
		self.spinbox_number_of_pages = self.elements.SpinBox()
		self.spinbox_number_of_pages.set_name("number_of_pages")
		self.spinbox_number_of_pages.setValue(1)
		self.spinbox_number_of_pages.setMinimum(1)
						
		self.realsize = self.elements.RadioButton()
		self.realsize.set_name("realsize")
		self.realsize.setChecked(True)
		self.list_element_with_text.append(self.realsize)
		
		self.print_all = self.elements.RadioButton()
		self.print_all.set_name("print_all")
		self.list_element_with_text.append(self.print_all)
		
		self.brush = self.elements.Brush()
		self.brush.set_name("brush")
		
		self.rect = self.elements.RectItem(self)
		self.rect.set_name("rectitem")
		self.rect.setBrush(self.brush)
				
		self.spinbox_left = self.elements.SpinBox()
		self.spinbox_left.set_name("left")
		
		self.spinbox_top = self.elements.SpinBox()
		self.spinbox_top.set_name("top")
		
		self.spinbox_right = self.elements.SpinBox()
		self.spinbox_right.set_name("right")
		
		self.spinbox_bottom = self.elements.SpinBox()
		self.spinbox_bottom.set_name("bottom")
		
		self.label_num_fragment = self.elements.Label()
		self.label_num_fragment.set_name("num_fragment")
		self.list_element_with_text.append(self.label_num_fragment)
				
		self.label_left = self.elements.Label()
		self.label_left.set_name("left")
		self.list_element_with_text.append(self.label_left)
		
		self.label_top = self.elements.Label()
		self.label_top.set_name("top")
		self.list_element_with_text.append(self.label_top)
		
		self.label_right = self.elements.Label()
		self.label_right.set_name("right")
		self.list_element_with_text.append(self.label_right)
		
		self.label_bottom = self.elements.Label()
		self.label_bottom.set_name("bottom")
		self.list_element_with_text.append(self.label_bottom)

		self.label_plus_image = self.elements.Label_Plus_Image_Fields(self)
		self.label_plus_image.set_name("label_plus_image")
		
		self.label_language = self.elements.Label()
		self.label_language.set_name("language")
		self.list_element_with_text.append(self.label_language)
				
		self.button_open = self.elements.Button(self)
		self.button_open.set_name("button_open")
		self.list_element_with_text.append(self.button_open)
		
		self.label_dd = self.elements.LabelDD(self)
		self.label_dd.set_name("label_dd")		
		self.list_element_with_text.append(self.label_dd)
		
		self.button_print = self.elements.Button(self)
		self.button_print.set_name("button_print")
		self.list_element_with_text.append(self.button_print)
			
		self.scale = self.elements.Label()
		self.scale.set_name("scale")
		self.list_element_with_text.append(self.scale)		
		
		self.lcd = self.elements.LCDNumber()
		self.lcd.set_name("lcd")
		self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
		
		self.slider = self.elements.Slider(self)	
		self.slider.set_name("slider")
		self.slider.setRange(10, 200)
		self.slider.setValue(100)
						
		self.combobox_printers = self.elements.ComboBox()
		self.combobox_printers.set_name("choise_printers")
		self.fill_forms_prn_ppr.fill_combobox_printer(self.combobox_printers)
		
		self.combobox_papers = self.elements.ComboBox()
		self.combobox_papers.set_name("choise_papers")
		self.fill_forms_prn_ppr.fill_combobox_paper(self.combobox_papers)
		
		self.combobox_printers.attach(self.combobox_papers)
		
		##########################################################################################
		self.sp_num_of_copies = self.elements.SpinBox()
		self.sp_num_of_copies.set_name("sp_number_of_copies")
		self.sp_num_of_copies.setValue(1)
		
		self.label_num_of_copies = self.elements.Label()
		self.label_num_of_copies.set_name("label_number_of_copies")
		self.list_element_with_text.append(self.label_num_of_copies)
		############################################################################################
				
		self.radiobutton_portrait = self.elements.RadioButton()
		self.radiobutton_portrait.setText(self.get_dict_lang()["portrait"])
		self.radiobutton_portrait.set_name("portrait")
		self.list_element_with_text.append(self.radiobutton_portrait)
		
		self.radiobutton_landscape = self.elements.RadioButton()
		self.radiobutton_landscape.setText(self.get_dict_lang()["landscape"])
		self.radiobutton_landscape.set_name("landscape")
		self.list_element_with_text.append(self.radiobutton_landscape)
		
		self.combobox_lang = self.elements.ComboBox()
		self.combobox_lang.set_name("choice_language")
		self.combobox_lang.attach(self)
		self.combobox_lang.addItem(self.setting.get_current_lang())
			
		for _lang in self.setting.get_available_lang():
			if _lang != self.combobox_lang.currentText():
				self.combobox_lang.addItem(_lang)
			else: pass		
		
		self.choice_color_rect = self.elements.ChoiceColorRect()
		self.choice_color_rect.set_name("choice_color_rect")
		
		
		self.group_paper = self.elements.GroupBox()	
		self.group_paper.set_name("paper")
		self.group_paper.setTitle(self.get_dict_lang()["paper"])
		self.list_element_with_text.append(self.group_paper)
				
		self.group_fields = self.elements.GroupBox()
		self.group_fields.set_name("fields")
		self.group_fields.setTitle(self.get_dict_lang()["fields"])
		self.list_element_with_text.append(self.group_fields)
		
		self.group_image = self.elements.GroupBox()
		self.group_image.set_name("image")
		self.group_image.setTitle(self.get_dict_lang()["image"])
		self.list_element_with_text.append(self.group_image)
		
		self.group_printers = self.elements.GroupBox()
		self.group_printers.set_name("printers")
		self.group_printers.setTitle(self.get_dict_lang()["printers"])
		self.list_element_with_text.append(self.group_printers)
		
		self.group_settings_lang = self.elements.GroupBox()
		self.group_settings_lang.set_name("settings_lang")
		self.group_settings_lang.setTitle(self.get_dict_lang()["settings_lang"])
		self.list_element_with_text.append(self.group_settings_lang)
		
		self.group_settings_color_rect = self.elements.GroupBox()
		self.group_settings_color_rect.set_name("settings_color_rect")
		self.group_settings_color_rect.setTitle(self.get_dict_lang()["settings_color_rect"])
		self.list_element_with_text.append(self.group_settings_color_rect)
		
		
		self.tab = self.elements.Tab()
		self.tab.set_name("tab_setting")
		self.list_element_with_text.append(self.tab)
		
		
		self.icons_tab = [QIcon(QPixmap(".icons/print1.svg")), QIcon(QPixmap(".icons/setting.svg"))]
		self.txt_tab = (self.get_dict_lang()["tab_setting"]).split()
		
	
		
		#####################################################
		self.rect.add_parent_scene(self.scene)
		
		
		######## atach() присоеденяем наблюдателей #############
		
		self.rect.attach(self.scene)		
		self.pagelayout.attach(self.rect)
		self.portrait.attach(self.pagelayout)
		self.portrait.attach(self.label_plus_image)
		self.landscape.attach(self.pagelayout)
		self.landscape.attach(self.label_plus_image)
		
		self.realsize.attach(self.scene)
		self.stretch.attach(self.scene)
		self.in_width.attach(self.scene)
		self.in_height.attach(self.scene)
		self.stretch_proportion.attach(self.scene)
				
		self.combobox_papers.attach(self.pagelayout)		
		self.spinbox_left.attach(self.pagelayout)
		self.spinbox_top.attach(self.pagelayout)
		self.spinbox_right.attach(self.pagelayout) 		
		self.spinbox_bottom.attach(self.pagelayout)
		self.spinbox_number_of_pages.attach(self.scene)
		self.print_all.attach(self.scene)
		
		self.button_open.attach(self.manipulation)
		self.label_dd.attach(self.manipulation)
		self.button_print.attach(self.button_print)
						
		self.manipulation.attach(self.rect)
		self.slider.attach(self.lcd)
		self.slider.attach(self.view)
		
		self.combobox_printers.attach(self.sp_num_of_copies)
		
		self.choice_color_rect.attach(self.brush)
		self.brush.attach(self.rect)
		self.brush.attach(self.scene)
		
		##### notify() посылает сигнал наблюдателям при загрузке виджета ########
		
		self.portrait.notify() 
		self.realsize.notify()
		self.combobox_papers.notify()
		self.combobox_printers.notify()
		self.spinbox_top.notify()
		self.spinbox_left.notify()
		self.spinbox_right.notify()
		self.spinbox_bottom.notify()
		
