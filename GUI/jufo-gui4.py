# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np

from functools import partial

import sys

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

from array import *
import thread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

combobox_items =      ["N-Damen n=4","N-Damen n=5","N-Damen n=6","N-Damen n=7","N-Damen n=8 Diagonale Frei","N-Damen n=8","Knights Tour"]
combobox_qubo_files = ["./Hamiltonians/qubomatrix_4_diagBesetzt.txt","./Hamiltonians/qubomatrix_5_diagBesetzt.txt","./Hamiltonians/qubomatrix_6_diagBesetzt.txt","./Hamiltonians/qubomatrix_7_diagBesetzt.txt","./Hamiltonians/qubomatrix_7_diagFrei.txt","./Hamiltonians/qubomatrix_8_diagBesetzt.txt","./Hamiltonians/qubomatrix_roesslesprung.txt"]
combobox_n =          [4,5,6,7,7,8,3]
combobox_chess_n =    [4,5,6,7,8,8,3]
combobox_diag_frei =  [False,False,False,False,True,False,False]
combobox_type =       [0,0,0,0,0,0,1]
combobox_optimal =    [-8,-10,-12,-14,-14,-16,-14]
reads_per_request = 1000
max_reads = 20000
max_annealing_time = 100

def knights_tour_result_to_chess(result):
	#print("result="+str(result))
	convert = []
	for i in range(10):
		convert.append([[],[]])
	#      POS EBENE
	convert[0][0] = [1,1]
	convert[1][0] = [3,1]
	convert[2][0] = [1,3]
	convert[3][0] = [3,3]
	convert[0][1] = [2,1]
	convert[1][1] = [3,2]
	convert[2][1] = [1,2]
	convert[3][1] = [2,3]
	
	chess = [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
	#print(chess)
	result = result[1]
	#print("len="+str(len(result)))
	for i in range(len(result)):
		ebene = ((i /4) % 2)
		pos = (i % 4)
		#print("ebene %2 ="+str(ebene))
		#print("ebene ="+str((i /4)))
		#print("pos="+str(pos))
		convert_value = convert[pos][ebene]
		#print("convert_value="+str(convert_value))
		#print("result[i]"+str(result[i]))
		chess[int((i /4))][convert_value[0]-1][convert_value[1]-1] = result[i]
	return(chess)

def qubo(matrix_text_file,num_reads_times_hundred,annealing_time,n,chess_n,best_result,diag_frei,type):
	print("Berechnung gestartet")
	qubomatrix = np.loadtxt(matrix_text_file)
	print("Matrix eingelesen")

	qubo = {}
	for index,value in np.ndenumerate(qubomatrix):
	    if value != 0:
	        qubo[index] = value

	responses = []
	
	print("Sende an Quantencomputer in Kanada")
	print("0.0%")
	i = 0
	for read in range(1,num_reads_times_hundred+1):
		i = i+1
		sampler = EmbeddingComposite(DWaveSampler())
		responses.append(sampler.sample_qubo(qubo, num_reads=reads_per_request, annealing_time=annealing_time))

		print(str(((i / (num_reads_times_hundred+0.0))*100))+"%")
	ui.berechnung_lauft.setVisible(False)
	
	results = []
	
	for response in responses:
		for sample, energy, num_occurrences, cbf in response.record:
			results.append([energy,sample,num_occurrences])
	
	#results = sorted(results, key=lambda x: x[2], reverse=True)
	results = sorted(results, key=lambda x: x[0], reverse=False)
	result = results[0]
	if type == 0:
		print("result :"+str(result[1]))
		for x in range(chess_n):
			for y in range(chess_n):
				ui.results_table.setItem(y,x,QTableWidgetItem("0"));
		for x in range(n):
			for y in range(n):
				ui.results_table.setItem(y,x,QTableWidgetItem(str(result[1][x+(y*n)])));
		
		if diag_frei == True:
			print("Setze weitere Dame")
			ui.results_table.setItem(chess_n-1,chess_n-1,QTableWidgetItem("1"));
		ui.results_table.show()
	elif type == 1:
		chess = knights_tour_result_to_chess(result)
		
		spruenge = []
		
		for ebene in range(len(chess)):
			for y in range(len(chess[ebene])):
				for x in range(len(chess[ebene][y])):
					if chess[ebene][y][x] == 1:
						spruenge.append([x,y])
		print("spruenge="+str(spruenge))
		for x in range(3):
			for y in range(3):
				ui.results_table.setItem(y,x,QTableWidgetItem(""));
		
		for sprung in range(len(spruenge)):
			ui.results_table.setItem(spruenge[sprung][1],spruenge[sprung][0],QTableWidgetItem(str(sprung+1)))
	ui.results_table.show()
	print("result energy: "+str(result[0]))
	print("best result energy: "+str(best_result))
	
	switch_side_to(3)

def start():
	print("")
	hamiltonian_select_index = ui.hamiltonian_select.currentIndex()
	print("Durchläufe: "+str(ui.durchlaufe_slider.value()))
	print("Annealing Time: "+str(ui.annealing_slider.value()))
	print("Hamiltonian: "+str(combobox_items[hamiltonian_select_index]))
	print("Diagonale Frei: "+str(combobox_diag_frei[hamiltonian_select_index]))
	ui.berechnung_lauft.setVisible(True)
	ui.results_table.setRowCount(combobox_chess_n[hamiltonian_select_index])
	ui.results_table.setColumnCount(combobox_chess_n[hamiltonian_select_index])
	qubo(combobox_qubo_files[hamiltonian_select_index],(ui.durchlaufe_slider.value()/reads_per_request),ui.annealing_slider.value(),combobox_n[hamiltonian_select_index],combobox_chess_n[hamiltonian_select_index],combobox_optimal[hamiltonian_select_index],combobox_diag_frei[hamiltonian_select_index],combobox_type[hamiltonian_select_index])

def switch_side_to(show_side):
	sides = [ui.side_frame_0,ui.side_frame_1,ui.side_frame_2,ui.side_frame_4]
	i = 0
	for side in sides:
		side.setVisible(i == show_side)
		i = i+1

def switch_side_to_0():
	switch_side_to(0)

def switch_side_to_1():
	switch_side_to(1)

def switch_side_to_2():
	switch_side_to(2)

def switch_side_to_3():
	switch_side_to(3)

def do_custom_ui():
	ui.start_button.clicked.connect(start)
	ui.berechnung_lauft.setVisible(False)
	ui.hamiltonian_select.addItems(combobox_items)
	ui.button_to_side_0.clicked.connect(switch_side_to_0)
	ui.button_to_side_1.clicked.connect(switch_side_to_1)
	ui.button_to_side_2.clicked.connect(switch_side_to_2)
	ui.durchlaufe_slider.setMaximum(max_reads)
	ui.annealing_slider.setMaximum(max_annealing_time)
	ui.durchlaufe_max.setText(_translate("JufoQubo", str(max_reads), None))
	ui.annealing_max.setText(_translate("JufoQubo", str(max_annealing_time), None))
	switch_side_to(0)

class Ui_JufoQubo(object):
    def setupUi(self, JufoQubo):
        JufoQubo.setObjectName(_fromUtf8("JufoQubo"))
        JufoQubo.resize(683, 730)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("1546464-200.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        JufoQubo.setWindowIcon(icon)
        self.main = QtGui.QWidget(JufoQubo)
        self.main.setObjectName(_fromUtf8("main"))
        self.verticalLayoutWidget = QtGui.QWidget(self.main)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 695, 701))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.main_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setMargin(0)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.side_frame_0 = QtGui.QFrame(self.verticalLayoutWidget)
        self.side_frame_0.setObjectName(_fromUtf8("side_frame_0"))
        self.side_0 = QtGui.QVBoxLayout(self.side_frame_0)
        self.side_0.setObjectName(_fromUtf8("side_0"))
        self.infos_label_side_0 = QtGui.QLabel(self.side_frame_0)
        self.infos_label_side_0.setWordWrap(False)
        self.infos_label_side_0.setObjectName(_fromUtf8("infos_label_side_0"))
        self.side_0.addWidget(self.infos_label_side_0)
        self.label = QtGui.QLabel(self.side_frame_0)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.label.setObjectName(_fromUtf8("label"))
        self.side_0.addWidget(self.label)
        self.button_to_side_1 = QtGui.QPushButton(self.side_frame_0)
        self.button_to_side_1.setObjectName(_fromUtf8("button_to_side_1"))
        self.side_0.addWidget(self.button_to_side_1)
        self.main_layout.addWidget(self.side_frame_0)
        self.side_frame_1 = QtGui.QFrame(self.verticalLayoutWidget)
        self.side_frame_1.setObjectName(_fromUtf8("side_frame_1"))
        self.side_1 = QtGui.QVBoxLayout(self.side_frame_1)
        self.side_1.setObjectName(_fromUtf8("side_1"))
        self.infos_bales_side_1 = QtGui.QLabel(self.side_frame_1)
        self.infos_bales_side_1.setObjectName(_fromUtf8("infos_bales_side_1"))
        self.side_1.addWidget(self.infos_bales_side_1)
        self.label_2 = QtGui.QLabel(self.side_frame_1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.side_1.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.side_frame_1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.side_1.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.side_frame_1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.side_1.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(self.side_frame_1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.side_1.addWidget(self.label_5)
        self.button_to_side_2 = QtGui.QPushButton(self.side_frame_1)
        self.button_to_side_2.setObjectName(_fromUtf8("button_to_side_2"))
        self.side_1.addWidget(self.button_to_side_2)
        self.main_layout.addWidget(self.side_frame_1)
        self.side_frame_2 = QtGui.QFrame(self.verticalLayoutWidget)
        self.side_frame_2.setObjectName(_fromUtf8("side_frame_2"))
        self.side_2 = QtGui.QVBoxLayout(self.side_frame_2)
        self.side_2.setObjectName(_fromUtf8("side_2"))
        self.hamiltonian_select = QtGui.QComboBox(self.side_frame_2)
        self.hamiltonian_select.setObjectName(_fromUtf8("hamiltonian_select"))
        self.side_2.addWidget(self.hamiltonian_select)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.durchlaufe = QtGui.QLabel(self.side_frame_2)
        self.durchlaufe.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.durchlaufe.setObjectName(_fromUtf8("durchlaufe"))
        self.horizontalLayout_5.addWidget(self.durchlaufe)
        self.annealingTime = QtGui.QLabel(self.side_frame_2)
        self.annealingTime.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.annealingTime.setObjectName(_fromUtf8("annealingTime"))
        self.horizontalLayout_5.addWidget(self.annealingTime)
        self.side_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.durchlaufe_slider = QtGui.QSlider(self.side_frame_2)
        self.durchlaufe_slider.setMinimum(1000)
        self.durchlaufe_slider.setMaximum(10000)
        self.durchlaufe_slider.setSingleStep(100)
        self.durchlaufe_slider.setPageStep(100)
        self.durchlaufe_slider.setSliderPosition(1000)
        self.durchlaufe_slider.setOrientation(QtCore.Qt.Horizontal)
        self.durchlaufe_slider.setInvertedAppearance(False)
        self.durchlaufe_slider.setObjectName(_fromUtf8("durchlaufe_slider"))
        self.horizontalLayout_3.addWidget(self.durchlaufe_slider)
        self.annealing_slider = QtGui.QSlider(self.side_frame_2)
        self.annealing_slider.setMinimum(20)
        self.annealing_slider.setMaximum(80)
        self.annealing_slider.setOrientation(QtCore.Qt.Horizontal)
        self.annealing_slider.setObjectName(_fromUtf8("annealing_slider"))
        self.horizontalLayout_3.addWidget(self.annealing_slider)
        self.side_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.durchlaufe_min = QtGui.QLabel(self.side_frame_2)
        self.durchlaufe_min.setObjectName(_fromUtf8("durchlaufe_min"))
        self.horizontalLayout_4.addWidget(self.durchlaufe_min)
        self.durchlaufe_max = QtGui.QLabel(self.side_frame_2)
        self.durchlaufe_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.durchlaufe_max.setObjectName(_fromUtf8("durchlaufe_max"))
        self.horizontalLayout_4.addWidget(self.durchlaufe_max)
        self.annealing_min = QtGui.QLabel(self.side_frame_2)
        self.annealing_min.setObjectName(_fromUtf8("annealing_min"))
        self.horizontalLayout_4.addWidget(self.annealing_min)
        self.annealing_max = QtGui.QLabel(self.side_frame_2)
        self.annealing_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.annealing_max.setObjectName(_fromUtf8("annealing_max"))
        self.horizontalLayout_4.addWidget(self.annealing_max)
        self.side_2.addLayout(self.horizontalLayout_4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.side_2.addItem(spacerItem)
        self.berechnung_lauft = QtGui.QLabel(self.side_frame_2)
        self.berechnung_lauft.setAlignment(QtCore.Qt.AlignCenter)
        self.berechnung_lauft.setObjectName(_fromUtf8("berechnung_lauft"))
        self.side_2.addWidget(self.berechnung_lauft)
        self.start_button = QtGui.QPushButton(self.side_frame_2)
        self.start_button.setCheckable(False)
        self.start_button.setAutoDefault(False)
        self.start_button.setDefault(False)
        self.start_button.setFlat(False)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.side_2.addWidget(self.start_button)
        self.main_layout.addWidget(self.side_frame_2)
        self.side_frame_4 = QtGui.QFrame(self.verticalLayoutWidget)
        self.side_frame_4.setObjectName(_fromUtf8("side_frame_4"))
        self.side_frame_3 = QtGui.QVBoxLayout(self.side_frame_4)
        self.side_frame_3.setObjectName(_fromUtf8("side_frame_3"))
        self.results_table = QtGui.QTableWidget(self.side_frame_4)
        self.results_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.results_table.setObjectName(_fromUtf8("results_table"))
        self.results_table.setColumnCount(0)
        self.results_table.setRowCount(0)
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.horizontalHeader().setDefaultSectionSize(30)
        self.results_table.horizontalHeader().setHighlightSections(False)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setHighlightSections(False)
        self.side_frame_3.addWidget(self.results_table)
        self.button_to_side_0 = QtGui.QPushButton(self.side_frame_4)
        self.button_to_side_0.setObjectName(_fromUtf8("button_to_side_0"))
        self.side_frame_3.addWidget(self.button_to_side_0)
        self.main_layout.addWidget(self.side_frame_4)
        JufoQubo.setCentralWidget(self.main)

        self.retranslateUi(JufoQubo)
        QtCore.QMetaObject.connectSlotsByName(JufoQubo)

    def retranslateUi(self, JufoQubo):
        JufoQubo.setWindowTitle(_translate("JufoQubo", "Jufo Qubo", None))
        self.infos_label_side_0.setText(_translate("JufoQubo", "Mit diesem Programm kann man Optimierungsprobleme graphisch an den Quantencomputer senden", None))
        self.label.setText(_translate("JufoQubo", "Copyright: Jonthan Treffler , Jakov D. Wallbrecher , Paul Schappert , 2019", None))
        self.button_to_side_1.setText(_translate("JufoQubo", "weiter", None))
        self.infos_bales_side_1.setText(_translate("JufoQubo", "Folgendes wird als nächstes ausgeführt:", None))
        self.label_2.setText(_translate("JufoQubo", "1. Hamiltonian generieren (mit einem Java Programm) (nicht live)", None))
        self.label_3.setText(_translate("JufoQubo", "2. Hamiltonian in Chimera Graph umformen", None))
        self.label_4.setText(_translate("JufoQubo", "3. Senden der Daten über das Internet zum Quantencomputer in Kanada", None))
        self.label_5.setText(_translate("JufoQubo", "4. Ergebnisse zurück übertragen und auswerten", None))
        self.button_to_side_2.setText(_translate("JufoQubo", "weiter", None))
        self.durchlaufe.setText(_translate("JufoQubo", "Durchläufe", None))
        self.annealingTime.setText(_translate("JufoQubo", "Annealing Time", None))
        self.durchlaufe_min.setText(_translate("JufoQubo", "1000", None))
        self.durchlaufe_max.setText(_translate("JufoQubo", "10.000", None))
        self.annealing_min.setText(_translate("JufoQubo", "20", None))
        self.annealing_max.setText(_translate("JufoQubo", "80", None))
        self.berechnung_lauft.setText(_translate("JufoQubo", "Berechnung läuft", None))
        self.start_button.setText(_translate("JufoQubo", "Start", None))
        self.button_to_side_0.setText(_translate("JufoQubo", "fertig", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    JufoQubo = QtGui.QMainWindow()
    ui = Ui_JufoQubo()
    ui.setupUi(JufoQubo)
    JufoQubo.show()
    do_custom_ui()
    sys.exit(app.exec_())

