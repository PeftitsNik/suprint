		
def split_and_remove_symbol(string: str, separator: str) -> list:		
	''' Разбиение строки, удаление '#' и ненужных пробелов с последующим созданием списка'''
	new_list = []
	
	for line in string.split(separator):
		if line == "": # если строка пустая  пропускаем
			break
		elif line[0] == "#": # если '#' в начале строки, пропускаем
			break
		elif line.find("#") != -1: # если '#' в середине или конце строки, удаляем его и последующие символы
			s = line[0 : line.index("#")].strip()
			new_list.append(s)
			continue
		else:
			s = line.strip()
			new_list.append(s)
		
	return new_list		

