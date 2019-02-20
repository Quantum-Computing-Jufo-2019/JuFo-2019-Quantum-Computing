# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Jufo.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import numpy as np

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

from array import *
import thread

combobox_items =      ["N-Damen n=4","N-Damen n=5","N-Damen n=6","N-Damen n=7","N-Damen n=8","Knights Tour"]
combobox_qubo_files = ["./Hamiltonians/qubomatrix_4_diagBesetzt.txt","./Hamiltonians/qubomatrix_5_diagBesetzt.txt","./Hamiltonians/qubomatrix_6_diagBesetzt.txt","./Hamiltonians/qubomatrix_7_diagBesetzt.txt","./Hamiltonians/qubomatrix_8_diagBesetzt.txt"]

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
def qubo(matrix_text_file,num_reads_times_hundred,annealing_time):
	qubomatrix = np.loadtxt(matrix_text_file)
	print('Loaded matrix:\n', qubomatrix, '\n')

	qubo = {}
	for index,value in np.ndenumerate(qubomatrix):
	    if value != 0:
	        qubo[index] = value

	responses = []

	reads_per_request = 100

	i = 0
	for read in range(1,num_reads_times_hundred+1):
		i = i+1
		#ui.progressBar.setProperty("value", ((read*reads_per_request / (num_reads_times_hundred*reads_per_request))*100))
		qubo_progress = ((read*reads_per_request / (num_reads_times_hundred*reads_per_request))*100)
		sampler = EmbeddingComposite(DWaveSampler())
		responses.append(sampler.sample_qubo(qubo, num_reads=reads_per_request, annealing_time=annealing_time))

		print('Saved result from request ',read,' in results.txt','   ',((i / (num_reads_times_hundred+0.0))*100))
def update_progress_bar():
	if qubo_progress != 100:
		print(qubo_progress)
		#ui.progressBar.setValue(qubo_progress)
		app.processEvents()
		update_progress_bar()
	
def start():
	print("Durchläufe: "+str(ui.durchlaufe_slider.value()))
	print("Annealing Time: "+str(ui.annealing_slider.value()))
	print("Hamiltonian: "+str(combobox_items[ui.comboBox_2.currentIndex()]))
	#ui.progressBar.setVisible(True)
	ui.progressLabel.setVisible(True)
	thread.start_new_thread(qubo,(combobox_qubo_files[ui.comboBox_2.currentIndex()],(ui.durchlaufe_slider.value()/100),ui.annealing_slider.value()))
	#update_progress_bar()

class Ui_JufoQubo(object):
    def setupUi(self, JufoQubo):
        JufoQubo.setObjectName(_fromUtf8("JufoQubo"))
        JufoQubo.resize(685, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("1546464-200.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        JufoQubo.setWindowIcon(icon)
        self.main = QtGui.QWidget(JufoQubo)
        self.main.setObjectName(_fromUtf8("main"))
        self.verticalLayoutWidget = QtGui.QWidget(self.main)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 661, 531))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.comboBox_2 = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItems(combobox_items)
        self.verticalLayout_3.addWidget(self.comboBox_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.durchlaufe = QtGui.QLabel(self.verticalLayoutWidget)
        self.durchlaufe.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.durchlaufe.setObjectName(_fromUtf8("durchlaufe"))
        self.horizontalLayout_5.addWidget(self.durchlaufe)
        self.annealingTime = QtGui.QLabel(self.verticalLayoutWidget)
        self.annealingTime.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.annealingTime.setObjectName(_fromUtf8("annealingTime"))
        self.horizontalLayout_5.addWidget(self.annealingTime)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.durchlaufe_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.durchlaufe_slider.setOrientation(QtCore.Qt.Horizontal)
        self.durchlaufe_slider.setInvertedAppearance(False)
        self.durchlaufe_slider.setMinimum(1000)
        self.durchlaufe_slider.setMaximum(10000)
        self.durchlaufe_slider.setTickInterval(1000)
        self.durchlaufe_slider.setTickPosition(2)
        self.durchlaufe_slider.setSingleStep(1000)
        self.durchlaufe_slider.setPageStep(1000)
        self.durchlaufe_slider.setObjectName(_fromUtf8("durchlaufe_slider"))
        self.horizontalLayout_3.addWidget(self.durchlaufe_slider)
        self.annealing_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.annealing_slider.setMinimum(20)
        self.annealing_slider.setMaximum(80)
        self.annealing_slider.setOrientation(QtCore.Qt.Horizontal)
        self.annealing_slider.setObjectName(_fromUtf8("annealing_slider"))
        self.horizontalLayout_3.addWidget(self.annealing_slider)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.durchlaufe_min = QtGui.QLabel(self.verticalLayoutWidget)
        self.durchlaufe_min.setObjectName(_fromUtf8("durchlaufe_min"))
        self.horizontalLayout_4.addWidget(self.durchlaufe_min)
        self.durchlaufe_max = QtGui.QLabel(self.verticalLayoutWidget)
        self.durchlaufe_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.durchlaufe_max.setObjectName(_fromUtf8("durchlaufe_max"))
        self.horizontalLayout_4.addWidget(self.durchlaufe_max)
        self.annealing_min = QtGui.QLabel(self.verticalLayoutWidget)
        self.annealing_min.setObjectName(_fromUtf8("annealing_min"))
        self.horizontalLayout_4.addWidget(self.annealing_min)
        self.annealing_max = QtGui.QLabel(self.verticalLayoutWidget)
        self.annealing_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.annealing_max.setObjectName(_fromUtf8("annealing_max"))
        self.horizontalLayout_4.addWidget(self.annealing_max)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        
		self.progressLabel = QtGui.QLabel(self.verticalLayoutWidget)
		self.progressLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
		self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.progressLabel.setVisible(False)
        self.verticalLayout_3.addWidget(self.progressLabel)
        
        #self.progressBar = QtGui.QProgressBar(self.verticalLayoutWidget)
        #self.progressBar.setProperty("value", 0)
        #self.progressBar.setObjectName(_fromUtf8("progressBar"))
        #self.progressBar.setVisible(False)
        #self.verticalLayout_3.addWidget(self.progressBar)
        self.Start = QtGui.QPushButton(self.verticalLayoutWidget)
        self.Start.setCheckable(False)
        self.Start.setAutoDefault(False)
        self.Start.setDefault(False)
        self.Start.setFlat(False)
        self.Start.setObjectName(_fromUtf8("Start"))
        self.Start.clicked.connect(start)
        self.verticalLayout_3.addWidget(self.Start)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        JufoQubo.setCentralWidget(self.main)

        self.retranslateUi(JufoQubo)
        QtCore.QMetaObject.connectSlotsByName(JufoQubo)

    def retranslateUi(self, JufoQubo):
        JufoQubo.setWindowTitle(_translate("JufoQubo", "Jufo Qubo", None))
        self.progressLabel.setText(_translate("JufoQubo", "Berechnung läuft", None))
        self.durchlaufe.setText(_translate("JufoQubo", "Durchläufe", None))
        self.annealingTime.setText(_translate("JufoQubo", "Annealing Time", None))
        self.durchlaufe_min.setText(_translate("JufoQubo", "1000", None))
        self.durchlaufe_max.setText(_translate("JufoQubo", "10.000", None))
        self.annealing_min.setText(_translate("JufoQubo", "20", None))
        self.annealing_max.setText(_translate("JufoQubo", "80", None))
        self.Start.setText(_translate("JufoQubo", "Start", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    JufoQubo = QtGui.QMainWindow()
    ui = Ui_JufoQubo()
    ui.setupUi(JufoQubo)
    JufoQubo.show()
    sys.exit(app.exec_())
	
qubo_progress = 0
	
		#for response in responses:
			#for sample, energy, num_occurrences, cbf in response.record:
				#file.write('%f\t%d\t%s' % (energy, num_occurrences, np.array2string(sample, max_line_width=None).replace('\n','')))
				#file.write('\n')

	#return(responses)
