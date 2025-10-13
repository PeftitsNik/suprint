from src.i18n import *
import src.const as const
import os
import src.useful_function as us_fn

class LoadSetting:

	def get_dict_setting(self, file_name: str) -> dict[str]:
		''' Создание словаря из файла настроек setting'''
		
		new_dict = {}
		
		with open(file_name, encoding='utf-8', mode='r') as f:			
			for line in f: # для каждой строки из файла
				s = us_fn.split_and_remove_symbol(line, ":")
				if len(s) == 0: pass
				elif s[0] and s[1]:
					new_dict[s[0]] = s[1].replace("\\n", "\n")
				else: pass
		
		return new_dict					
	
	def get_i18n (self, file_name : str) -> dict[str]:		
		return i18n | self.get_dict_setting(file_name)
	
	def create_dict_i18n_from_file(self):
		
		lang = self.get_dict_setting(const.FILE_SETTING)["lang"]
		
		os.chdir(const.DIR_SRC)
		os.chdir(const.DIR_LANG)
		
		dict_i18n = self.get_i18n(lang)
		
		os.chdir("../../")
	
		return dict_i18n
		
	def create_dict_i18n_from_combobox(self, file: str) -> dict[str]:
		dict_i18n = self.get_i18n(file)
		return dict_i18n
		
	def get_available_lang(self) -> list[str]:
		l = []
		for line in self.get_dict_setting(const.FILE_SETTING)["available_lang"].split(","):
			l.append(line.strip())
		return l
		
	def get_current_lang(self) -> str:		
		return self.get_dict_setting(const.FILE_SETTING)["lang"]					

	def get_active_color_rect(self) -> str:		
		return self.get_dict_setting(const.FILE_SETTING)["active_color_rectangle"]
		
	def get_current_alpha(self) -> int:
		return int(self.get_dict_setting(const.FILE_SETTING)["alpha"])
