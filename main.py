from src.ui import *
import sys


QImageReader.setAllocationLimit(0) # снимаем ограничение на размер изображения

if __name__ == "__main__":

	app = QApplication(sys.argv)
	
	elements = Elements()
	
	carcase = Carcase(elements)
	carcase.set_dict_lang(carcase.setting.create_dict_i18n_from_file())
	carcase.create_carcase()
	
	ui = UI(carcase)
	

	app.exec()
	
