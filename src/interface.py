class Controller_Interface:	
	def from_view_to_model(self, element_source):
		pass

	def from_model_to_view(self, element):
		pass


class Model_Interface:
	def processing(self, element):
		pass


class Element_Interface:	
	
	def set_name(self, name: str):
		self.__name = name

	def get_name(self) -> str:
		return self.__name		
	
# наблюдатель
class Observer:
	
   #изменение наблюдателя
    def update_observer():
        pass


#наблюдаемое
class Subject:	
   
    # инициализация списка наблюдателей   
	def create_list_observers(self) -> list:
		self.list_observers = []

	# сообщение наблюдателю	
	def notify(self):
		for i in self.list_observers:
			i.update_observer(self)
	
	# добавление наблюдателей
	def attach(self, observer: Observer):
		self.list_observers.append(observer)
			
	# удаление наблюдателей
	def detach(self, observer: Observer):
		self.list_observers.remove(observer)


class Carcase_Interfase:
	def create_carcase(self):
		pass

	def set_dict_lang(self):
		pass
	
	def get_dict_lang(self):
		pass

