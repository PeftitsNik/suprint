from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *
from PyQt6.QtWidgets import *
import src.const as const

import sys

class DictPrnPpr():
	def __init__(self):
        
		self.prn = QPrinterInfo.availablePrinterNames() # создаём список поддерживаемых принтеров

    ########################################################################################################################
    #  Создаёт словарь, содержащий ключ - имя принтера и значения - другой словарь, ключ которого имя потдерживаемой принтером страницы,  
    #  а значение - соответствующий класс QPageSize.PageSizeId,
    #         dict1
    #          |
    #   { имя принтера : dict2 }
    #                      |
    #            { наименование страницы : QPageSize.PageSizeId }


	def dict_prn_ppr (self): # Создаёт словарь dict1
       
		dict1 = {}
        
		for p in self.prn:
			p_low = p.lower()
			if p_low.find('pdf') != -1: # если среди доступных есть экспорт в PDF, 
				continue                # то его пропускаем, чтобы потом создать свой
            
			dict1[p] = self.dict2(p)
        
        
        
		dict1[const.PR_PDF] = {QPageSize(QPageSize.PageSizeId.A0).name(): QPageSize(QPageSize.PageSizeId.A0), #добавляем печать в PDF
                           QPageSize(QPageSize.PageSizeId.A1).name(): QPageSize(QPageSize.PageSizeId.A1),
                           QPageSize(QPageSize.PageSizeId.A2).name(): QPageSize(QPageSize.PageSizeId.A2),
                           QPageSize(QPageSize.PageSizeId.A3).name(): QPageSize(QPageSize.PageSizeId.A3),
                           QPageSize(QPageSize.PageSizeId.A4).name(): QPageSize(QPageSize.PageSizeId.A4)}
		return dict1
    
    
	def dict2(self, printer): # Создаёт словарь dict2
        
		d2 = {}
		for s in QPrinterInfo.supportedPageSizes(QPrinterInfo.printerInfo(printer)):
			d2[s.name()] = s
            
		return d2
     
     #создание списка, содержащего поддерживаемое принтером разрешение
     #printer - строка название принтера
	def list_prn_dpi(self, printer: str) -> list[int]:
		l = []
        
		if printer == "":
			pass
		
		else:			
			p = QPrinter(QPrinterInfo.printerInfo(printer)) #создание объекта QPrinter из строки название принтера
			l.append(str(p.resolution()))
		       
		return l 
		
     #-словарь, содержащий имя_страницы:PageSizeId    
	def dict_support_pages(self): 
		l = {}
		d = self.dict_prn_ppr()
		for k1, v1 in d.items():
			for k2, v2 in v1.items():
				if k2 in l: continue
				else: l[k2] = v2
				
		return l
	
class Fill_Forms():
	def __init__(self):
		self.prn_ppr = DictPrnPpr()
		self.dict_p_p = self.prn_ppr.dict_prn_ppr()
		
		if QPrinterInfo.defaultPrinterName():			
			self.default_printer = QPrinterInfo.defaultPrinterName() # принтер по умолчанию
		else: self.default_printer = const.PR_PDF
		
		
	def fill_combobox_printer(self, combobox: QComboBox):
		combobox.addItem(self.default_printer) #добавление принтера по умолчанию
		for key in self.dict_p_p:
			if key == self.default_printer: continue
			else: combobox.addItem(key)
		 
	def fill_combobox_paper(self, combobox: QComboBox):
		for s in self.dict_p_p[self.default_printer]: # бумага для принтера
			combobox.addItem(s)
 
     
######################### TEST ###############################       
#app = QApplication(sys.argv)
#pr = QPrinter()
#pr.setPrinterName(QPrinterInfo.defaultPrinterName())
#margins = QMarginsF(5.0,5.0,10.0,10.0)
#pr.setPageMargins(margins)

#dpr =  DictPrnPpr()
#d = dpr.dict_support_pages()

#pl = QPageLayout()
#pl.setUnits(QPageLayout.Unit.Millimeter)
#pl.setPageSize(d["A4"])

#pr.setPageLayout(pl)
#print(pr.pageLayout().minimumMargins().left())
#print(pr.pageLayout().minimumMargins().top())
#print(pr.pageLayout().margins().left())

#print(d["A4"])
#print(QPrinterInfo.defaultPrinterName())




#d = dpr.dict_support_pages()
#print(d["A4"])

#pl = QPageLayout()
#pl.setPageSize(d["A4"])
#print(pl.minimumMargins().top())

#d = Fill_Forms()
#print(d.dict_p_p)
#print(d.default_printer)

#for key, val in d.items():
    
#    print(key, "-->", val)

#print(d["A3"])           
#app.exec()
