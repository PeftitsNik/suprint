# наблюдатель
class Observer:
    #имя 
    def set_name(self, name: str):
        self.__name = name
        
    def get_name(self) -> str:
        return self.__name

    def update_observer():
        pass


#наблюдаемое
class Subject:	
    #имя 
	def set_name(self, name: str):
		self.__name = name
	
	def get_name(self) -> str:
		return self.__name

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