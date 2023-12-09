from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class LabelDragDrop (QLabel):
	def __init__(self):
		super().__init__()
		self.setStyleSheet("background-color: #E0E0E0;"
							"border: 2px solid green;")
		self.setAcceptDrops(True)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
	def get_name_file(self) -> str:
		return self.files[0]
	
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		self.files = [u.toLocalFile() for u in event.mimeData().urls()]
		for f in self.files:
			print(f)
		self.notify() # метод из interface.py (оповещение наблюдателей)
