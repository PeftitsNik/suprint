def split_and_remove_symbol(string: str, separator: str) -> list[str]:	
	
	''' Разбиение строки, удаление '#' и ненужных пробелов с последующим созданием списка'''
	new_list = []
	for line in string.split(separator):		
		if line == "": # если строка пустая  пропускаем
			break
		elif line[0] == "#": # если '#' в начале строки, пропускаем
			break
		#elif line.find("#") != -1: # если '#' в середине или конце строки, удаляем его и последующие символы
		#	s = line[0 : line.index("#")].strip()
		#	new_list.append(s)
		#	continue
		else:
			s = line.strip()
			new_list.append(s)	
	return new_list

def read_and_write_setting(file_name: str, setting_name: str, new_value: str) -> None:
	''' Чтение из файла настроек параметра и запись нового значения'''
	
	new_setting_list = []
	
	with open(file_name, encoding='utf-8', mode='r') as f:
		for line in f:
			if line[0 : len(setting_name)] == setting_name:
				new_setting_list.append(f"{setting_name}: {new_value}\n")
			else: new_setting_list.append(line)	
					
	with open(file_name, encoding='utf-8', mode='w') as f:	
		f.write("".join(new_setting_list))
