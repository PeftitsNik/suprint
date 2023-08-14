from src.ui import *
import sys

QImageReader.setAllocationLimit(0)

if __name__ == "__main__":

	app = QApplication(sys.argv)

	window = MainWindow()

	app.exec()

