from src.i18n import *
import src.const as const
import os
from src.useful_function import *

class LoadSetting:
	
	#def __init__(self):
	#	print(os.getcwd())
						
	def get_i18n (self, file_name : str) -> dict:
		return i18n | self.get_dict_setting(file_name)
		
	def get_dict_setting(self, file_name: str) -> dict:
		new_dict = {}
		
		with open(file_name, encoding='utf-8', mode='r') as f:			
			for line in f: # для каждой строки из файла
				s = split_and_remove_symbol(line, ":")
				if len(s) == 0: pass
				elif s[0] and s[1]:
					new_dict[s[0]] = s[1]
				else: pass
		
		return new_dict
		
	def create_dict_i18n_from_file(self):
		
		lang = self.get_dict_setting(const.FILE_SETTING)["lang"]
		
		os.chdir(const.DIR_SRC)
		os.chdir(const.DIR_LANG)
		
		dict_i18n = self.get_i18n(lang)
		
		os.chdir("../../")
				
		return dict_i18n
		
	def create_dict_i18n_from_combobox(self, lang: str) -> dict:
		dict_i18n = self.get_i18n(lang)
		
		return dict_i18n
		
	def get_available_lang(self) -> list:
		l = []
		for line in self.get_dict_setting(const.FILE_SETTING)["available_lang"].split(","):
			l.append(line.strip())
		return l
		
	def get_current_lang(self) -> str:		
		return self.get_dict_setting(const.FILE_SETTING)["lang"]					

