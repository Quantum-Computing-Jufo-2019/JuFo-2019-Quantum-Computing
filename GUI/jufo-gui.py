# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np

from functools import partial

import sys

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dwave.system import EmbeddingComposite, LazyFixedEmbeddingComposite

import neal
import dimod
import dwave_networkx as dnx
import networkx as nx
import dwave.embedding

from array import *
import thread
import math
import time
import sched
from threading import Timer
import warnings

#Vars
result = 0

min_reads = 1000
max_reads = 100000
min_annealing_time = 20
max_annealing_time = 500
min_chain_strength = 1
max_chain_strength = 40

#GUI

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(695, 595)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget_10 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setGeometry(QtCore.QRect(10, 10, 681, 581))
        self.verticalLayoutWidget_10.setObjectName(_fromUtf8("verticalLayoutWidget_10"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.stackedWidget = QtGui.QStackedWidget(self.verticalLayoutWidget_10)
        self.stackedWidget.setAcceptDrops(False)
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page_1 = QtGui.QWidget()
        self.page_1.setObjectName(_fromUtf8("page_1"))
        self.verticalLayoutWidget = QtGui.QWidget(self.page_1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_side1 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_side1.setMargin(0)
        self.verticalLayout_side1.setObjectName(_fromUtf8("verticalLayout_side1"))
        self.infos_label_1_side_1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.infos_label_1_side_1.setAcceptDrops(False)
        self.infos_label_1_side_1.setWordWrap(True)
        self.infos_label_1_side_1.setObjectName(_fromUtf8("infos_label_1_side_1"))
        self.verticalLayout_side1.addWidget(self.infos_label_1_side_1)
        self.infos_label_2_side_1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.infos_label_2_side_1.setScaledContents(False)
        self.infos_label_2_side_1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.infos_label_2_side_1.setWordWrap(True)
        self.infos_label_2_side_1.setObjectName(_fromUtf8("infos_label_2_side_1"))
        self.verticalLayout_side1.addWidget(self.infos_label_2_side_1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_side1.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.next_button_side_1 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.next_button_side_1.setObjectName(_fromUtf8("next_button_side_1"))
        self.horizontalLayout_2.addWidget(self.next_button_side_1)
        self.verticalLayout_side1.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.page_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_side_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_side_2.setMargin(0)
        self.verticalLayout_side_2.setObjectName(_fromUtf8("verticalLayout_side_2"))
        self.infos_label_1_side_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.infos_label_1_side_2.setObjectName(_fromUtf8("infos_label_1_side_2"))
        self.verticalLayout_side_2.addWidget(self.infos_label_1_side_2)
        self.infos_label_2_side_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.infos_label_2_side_2.setObjectName(_fromUtf8("infos_label_2_side_2"))
        self.verticalLayout_side_2.addWidget(self.infos_label_2_side_2)
        self.infos_label_3_side_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.infos_label_3_side_2.setObjectName(_fromUtf8("infos_label_3_side_2"))
        self.verticalLayout_side_2.addWidget(self.infos_label_3_side_2)
        self.infos_label_4_side_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.infos_label_4_side_2.setObjectName(_fromUtf8("infos_label_4_side_2"))
        self.verticalLayout_side_2.addWidget(self.infos_label_4_side_2)
        self.infos_label_5_side_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.infos_label_5_side_2.setObjectName(_fromUtf8("infos_label_5_side_2"))
        self.verticalLayout_side_2.addWidget(self.infos_label_5_side_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_side_2.addItem(spacerItem1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.back_button_side_2 = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.back_button_side_2.setObjectName(_fromUtf8("back_button_side_2"))
        self.horizontalLayout_4.addWidget(self.back_button_side_2)
        self.next_button_side_2 = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.next_button_side_2.setObjectName(_fromUtf8("next_button_side_2"))
        self.horizontalLayout_4.addWidget(self.next_button_side_2)
        self.verticalLayout_side_2.addLayout(self.horizontalLayout_4)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.page_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_side_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_side_3.setMargin(0)
        self.verticalLayout_side_3.setObjectName(_fromUtf8("verticalLayout_side_3"))
        self.headline_side_3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.headline_side_3.setFont(font)
        self.headline_side_3.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.headline_side_3.setObjectName(_fromUtf8("headline_side_3"))
        self.verticalLayout_side_3.addWidget(self.headline_side_3)
        self.solver_select = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.solver_select.setObjectName(_fromUtf8("solver_select"))
        self.verticalLayout_side_3.addWidget(self.solver_select)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_side_3.addItem(spacerItem2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.back_button_side_3 = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.back_button_side_3.setObjectName(_fromUtf8("back_button_side_3"))
        self.horizontalLayout_5.addWidget(self.back_button_side_3)
        self.next_button_side_3 = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.next_button_side_3.setObjectName(_fromUtf8("next_button_side_3"))
        self.horizontalLayout_5.addWidget(self.next_button_side_3)
        self.verticalLayout_side_3.addLayout(self.horizontalLayout_5)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.verticalLayoutWidget_9 = QtGui.QWidget(self.page_4)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget_9.setObjectName(_fromUtf8("verticalLayoutWidget_9"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.headline_side_4 = QtGui.QLabel(self.verticalLayoutWidget_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.headline_side_4.setFont(font)
        self.headline_side_4.setAlignment(QtCore.Qt.AlignCenter)
        self.headline_side_4.setObjectName(_fromUtf8("headline_side_4"))
        self.verticalLayout.addWidget(self.headline_side_4)
        self.runs_headline = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.runs_headline.setObjectName(_fromUtf8("runs_headline"))
        self.verticalLayout.addWidget(self.runs_headline)
        self.runs_slider = QtGui.QSlider(self.verticalLayoutWidget_9)
        self.runs_slider.setMinimum(1000)
        self.runs_slider.setMaximum(10000)
        self.runs_slider.setOrientation(QtCore.Qt.Horizontal)
        self.runs_slider.setObjectName(_fromUtf8("runs_slider"))
        self.verticalLayout.addWidget(self.runs_slider)
        self.horizontalLayout_runs = QtGui.QHBoxLayout()
        self.horizontalLayout_runs.setObjectName(_fromUtf8("horizontalLayout_runs"))
        self.runs_min_label = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.runs_min_label.setObjectName(_fromUtf8("runs_min_label"))
        self.horizontalLayout_runs.addWidget(self.runs_min_label)
        self.runs_label = QtGui.QLabel(self.verticalLayoutWidget_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.runs_label.setFont(font)
        self.runs_label.setAlignment(QtCore.Qt.AlignCenter)
        self.runs_label.setObjectName(_fromUtf8("runs_label"))
        self.horizontalLayout_runs.addWidget(self.runs_label)
        self.runs_max_label = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.runs_max_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.runs_max_label.setObjectName(_fromUtf8("runs_max_label"))
        self.horizontalLayout_runs.addWidget(self.runs_max_label)
        self.verticalLayout.addLayout(self.horizontalLayout_runs)
        self.annealing_time_headline = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.annealing_time_headline.setObjectName(_fromUtf8("annealing_time_headline"))
        self.verticalLayout.addWidget(self.annealing_time_headline)
        self.annealing_time_slider = QtGui.QSlider(self.verticalLayoutWidget_9)
        self.annealing_time_slider.setMinimum(20)
        self.annealing_time_slider.setMaximum(80)
        self.annealing_time_slider.setOrientation(QtCore.Qt.Horizontal)
        self.annealing_time_slider.setObjectName(_fromUtf8("annealing_time_slider"))
        self.verticalLayout.addWidget(self.annealing_time_slider)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.annealing_time_min = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.annealing_time_min.setObjectName(_fromUtf8("annealing_time_min"))
        self.horizontalLayout_3.addWidget(self.annealing_time_min)
        self.annealing_time_label = QtGui.QLabel(self.verticalLayoutWidget_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.annealing_time_label.setFont(font)
        self.annealing_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.annealing_time_label.setObjectName(_fromUtf8("annealing_time_label"))
        self.horizontalLayout_3.addWidget(self.annealing_time_label)
        self.annealing_time_max = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.annealing_time_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.annealing_time_max.setObjectName(_fromUtf8("annealing_time_max"))
        self.horizontalLayout_3.addWidget(self.annealing_time_max)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.chain_strength_headline = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.chain_strength_headline.setObjectName(_fromUtf8("chain_strength_headline"))
        self.verticalLayout.addWidget(self.chain_strength_headline)
        self.chain_strength_slider = QtGui.QSlider(self.verticalLayoutWidget_9)
        self.chain_strength_slider.setMinimum(1)
        self.chain_strength_slider.setMaximum(25)
        self.chain_strength_slider.setProperty("value", 1)
        self.chain_strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.chain_strength_slider.setObjectName(_fromUtf8("chain_strength_slider"))
        self.verticalLayout.addWidget(self.chain_strength_slider)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chain_strength_min = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.chain_strength_min.setObjectName(_fromUtf8("chain_strength_min"))
        self.horizontalLayout.addWidget(self.chain_strength_min)
        self.chain_strength_label = QtGui.QLabel(self.verticalLayoutWidget_9)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.chain_strength_label.setFont(font)
        self.chain_strength_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chain_strength_label.setObjectName(_fromUtf8("chain_strength_label"))
        self.horizontalLayout.addWidget(self.chain_strength_label)
        self.chain_strength_max = QtGui.QLabel(self.verticalLayoutWidget_9)
        self.chain_strength_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.chain_strength_max.setObjectName(_fromUtf8("chain_strength_max"))
        self.horizontalLayout.addWidget(self.chain_strength_max)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.back_button_side_4 = QtGui.QPushButton(self.verticalLayoutWidget_9)
        self.back_button_side_4.setObjectName(_fromUtf8("back_button_side_4"))
        self.horizontalLayout_6.addWidget(self.back_button_side_4)
        self.next_button_side_4 = QtGui.QPushButton(self.verticalLayoutWidget_9)
        self.next_button_side_4.setObjectName(_fromUtf8("next_button_side_4"))
        self.horizontalLayout_6.addWidget(self.next_button_side_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName(_fromUtf8("page_5"))
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.page_5)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.verticalLayout_side_5 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_side_5.setMargin(0)
        self.verticalLayout_side_5.setObjectName(_fromUtf8("verticalLayout_side_5"))
        self.headline_side_5 = QtGui.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.headline_side_5.setFont(font)
        self.headline_side_5.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.headline_side_5.setObjectName(_fromUtf8("headline_side_5"))
        self.verticalLayout_side_5.addWidget(self.headline_side_5)
        self.problem_select = QtGui.QComboBox(self.verticalLayoutWidget_4)
        self.problem_select.setObjectName(_fromUtf8("problem_select"))
        self.verticalLayout_side_5.addWidget(self.problem_select)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_side_5.addItem(spacerItem4)
        self.definition_headline = QtGui.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.definition_headline.setFont(font)
        self.definition_headline.setObjectName(_fromUtf8("definition_headline"))
        self.verticalLayout_side_5.addWidget(self.definition_headline)
        self.qubo_definition = QtGui.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.qubo_definition.setFont(font)
        self.qubo_definition.setText(_fromUtf8(""))
        self.qubo_definition.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.qubo_definition.setWordWrap(True)
        self.qubo_definition.setObjectName(_fromUtf8("qubo_definition"))
        self.verticalLayout_side_5.addWidget(self.qubo_definition)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.back_button_side_5 = QtGui.QPushButton(self.verticalLayoutWidget_4)
        self.back_button_side_5.setObjectName(_fromUtf8("back_button_side_5"))
        self.horizontalLayout_7.addWidget(self.back_button_side_5)
        self.next_button_side_5 = QtGui.QPushButton(self.verticalLayoutWidget_4)
        self.next_button_side_5.setObjectName(_fromUtf8("next_button_side_5"))
        self.horizontalLayout_7.addWidget(self.next_button_side_5)
        self.verticalLayout_side_5.addLayout(self.horizontalLayout_7)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName(_fromUtf8("page_6"))
        self.verticalLayoutWidget_5 = QtGui.QWidget(self.page_6)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 20, 681, 551))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.verticalLayout_side_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_side_6.setMargin(0)
        self.verticalLayout_side_6.setObjectName(_fromUtf8("verticalLayout_side_6"))
        self.headline_side_6 = QtGui.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.headline_side_6.setFont(font)
        self.headline_side_6.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.headline_side_6.setObjectName(_fromUtf8("headline_side_6"))
        self.verticalLayout_side_6.addWidget(self.headline_side_6)
        self.stackedWidget_2 = QtGui.QStackedWidget(self.verticalLayoutWidget_5)
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.n_queens_options_side = QtGui.QWidget()
        self.n_queens_options_side.setObjectName(_fromUtf8("n_queens_options_side"))
        self.verticalLayoutWidget_6 = QtGui.QWidget(self.n_queens_options_side)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(-1, 9, 681, 481))
        self.verticalLayoutWidget_6.setObjectName(_fromUtf8("verticalLayoutWidget_6"))
        self.verticalLayout_options_side_0 = QtGui.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_options_side_0.setMargin(0)
        self.verticalLayout_options_side_0.setObjectName(_fromUtf8("verticalLayout_options_side_0"))
        self.n_queens_options_headline = QtGui.QLabel(self.verticalLayoutWidget_6)
        self.n_queens_options_headline.setAlignment(QtCore.Qt.AlignCenter)
        self.n_queens_options_headline.setObjectName(_fromUtf8("n_queens_options_headline"))
        self.verticalLayout_options_side_0.addWidget(self.n_queens_options_headline)
        self.n_queens_n_select = QtGui.QComboBox(self.verticalLayoutWidget_6)
        self.n_queens_n_select.setObjectName(_fromUtf8("n_queens_n_select"))
        self.verticalLayout_options_side_0.addWidget(self.n_queens_n_select)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_options_side_0.addItem(spacerItem5)
        self.stackedWidget_2.addWidget(self.n_queens_options_side)
        self.knights_tour_options_side = QtGui.QWidget()
        self.knights_tour_options_side.setObjectName(_fromUtf8("knights_tour_options_side"))
        self.verticalLayoutWidget_11 = QtGui.QWidget(self.knights_tour_options_side)
        self.verticalLayoutWidget_11.setGeometry(QtCore.QRect(-1, 19, 681, 471))
        self.verticalLayoutWidget_11.setObjectName(_fromUtf8("verticalLayoutWidget_11"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.knights_tour_options_headline = QtGui.QLabel(self.verticalLayoutWidget_11)
        self.knights_tour_options_headline.setAlignment(QtCore.Qt.AlignCenter)
        self.knights_tour_options_headline.setObjectName(_fromUtf8("knights_tour_options_headline"))
        self.verticalLayout_5.addWidget(self.knights_tour_options_headline)
        self.knights_tour_no_options_label = QtGui.QLabel(self.verticalLayoutWidget_11)
        font = QtGui.QFont()
        font.setItalic(True)
        self.knights_tour_no_options_label.setFont(font)
        self.knights_tour_no_options_label.setObjectName(_fromUtf8("knights_tour_no_options_label"))
        self.verticalLayout_5.addWidget(self.knights_tour_no_options_label)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.stackedWidget_2.addWidget(self.knights_tour_options_side)
        self.sudoku_options_side = QtGui.QWidget()
        self.sudoku_options_side.setObjectName(_fromUtf8("sudoku_options_side"))
        self.verticalLayoutWidget_7 = QtGui.QWidget(self.sudoku_options_side)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(-1, 19, 681, 471))
        self.verticalLayoutWidget_7.setObjectName(_fromUtf8("verticalLayoutWidget_7"))
        self.verticalLayout_options_side_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_options_side_2.setMargin(0)
        self.verticalLayout_options_side_2.setObjectName(_fromUtf8("verticalLayout_options_side_2"))
        self.sudoku_options_headline = QtGui.QLabel(self.verticalLayoutWidget_7)
        self.sudoku_options_headline.setAlignment(QtCore.Qt.AlignCenter)
        self.sudoku_options_headline.setObjectName(_fromUtf8("sudoku_options_headline"))
        self.verticalLayout_options_side_2.addWidget(self.sudoku_options_headline)
        self.sudoku_n_select = QtGui.QComboBox(self.verticalLayoutWidget_7)
        self.sudoku_n_select.setObjectName(_fromUtf8("sudoku_n_select"))
        self.verticalLayout_options_side_2.addWidget(self.sudoku_n_select)
        self.sudoku_options_table = QtGui.QTableWidget(self.verticalLayoutWidget_7)
        self.sudoku_options_table.setRowCount(9)
        self.sudoku_options_table.setColumnCount(9)
        self.sudoku_options_table.setObjectName(_fromUtf8("sudoku_options_table"))
        self.sudoku_options_table.horizontalHeader().setVisible(False)
        self.sudoku_options_table.horizontalHeader().setDefaultSectionSize(30)
        self.sudoku_options_table.verticalHeader().setVisible(False)
        self.sudoku_options_table.verticalHeader().setHighlightSections(True)
        self.verticalLayout_options_side_2.addWidget(self.sudoku_options_table)
        self.sudoku_presets = QtGui.QComboBox(self.verticalLayoutWidget_7)
        self.sudoku_presets.setObjectName(_fromUtf8("sudoku_presets"))
        self.verticalLayout_options_side_2.addWidget(self.sudoku_presets)
        self.stackedWidget_2.addWidget(self.sudoku_options_side)
        self.amazone_options_side = QtGui.QWidget()
        self.amazone_options_side.setObjectName(_fromUtf8("amazone_options_side"))
        self.verticalLayoutWidget_12 = QtGui.QWidget(self.amazone_options_side)
        self.verticalLayoutWidget_12.setGeometry(QtCore.QRect(-1, 9, 681, 481))
        self.verticalLayoutWidget_12.setObjectName(_fromUtf8("verticalLayoutWidget_12"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.amazone_options_headline = QtGui.QLabel(self.verticalLayoutWidget_12)
        self.amazone_options_headline.setAlignment(QtCore.Qt.AlignCenter)
        self.amazone_options_headline.setObjectName(_fromUtf8("amazone_options_headline"))
        self.verticalLayout_6.addWidget(self.amazone_options_headline)
        self.amazone_n_select = QtGui.QComboBox(self.verticalLayoutWidget_12)
        self.amazone_n_select.setObjectName(_fromUtf8("amazone_n_select"))
        self.verticalLayout_6.addWidget(self.amazone_n_select)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem7)
        self.stackedWidget_2.addWidget(self.amazone_options_side)
        self.custom_hamiltonian_side = QtGui.QWidget()
        self.custom_hamiltonian_side.setObjectName(_fromUtf8("custom_hamiltonian_side"))
        self.verticalLayoutWidget_13 = QtGui.QWidget(self.custom_hamiltonian_side)
        self.verticalLayoutWidget_13.setGeometry(QtCore.QRect(-1, 9, 681, 481))
        self.verticalLayoutWidget_13.setObjectName(_fromUtf8("verticalLayoutWidget_13"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_13)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.custom_hamiltonian_label = QtGui.QLabel(self.verticalLayoutWidget_13)
        self.custom_hamiltonian_label.setAlignment(QtCore.Qt.AlignCenter)
        self.custom_hamiltonian_label.setObjectName(_fromUtf8("custom_hamiltonian_label"))
        self.verticalLayout_2.addWidget(self.custom_hamiltonian_label)
        self.custom_hamiltonian_text_field = QtGui.QPlainTextEdit(self.verticalLayoutWidget_13)
        self.custom_hamiltonian_text_field.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.custom_hamiltonian_text_field.setObjectName(_fromUtf8("custom_hamiltonian_text_field"))
        self.verticalLayout_2.addWidget(self.custom_hamiltonian_text_field)
        self.custom_hamiltonian_file_picker_button = QtGui.QPushButton(self.verticalLayoutWidget_13)
        self.custom_hamiltonian_file_picker_button.setObjectName(_fromUtf8("custom_hamiltonian_file_picker_button"))
        self.verticalLayout_2.addWidget(self.custom_hamiltonian_file_picker_button)
        self.stackedWidget_2.addWidget(self.custom_hamiltonian_side)
        self.verticalLayout_side_6.addWidget(self.stackedWidget_2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.back_button_side_6 = QtGui.QPushButton(self.verticalLayoutWidget_5)
        self.back_button_side_6.setObjectName(_fromUtf8("back_button_side_6"))
        self.horizontalLayout_8.addWidget(self.back_button_side_6)
        self.next_button_side_6 = QtGui.QPushButton(self.verticalLayoutWidget_5)
        self.next_button_side_6.setObjectName(_fromUtf8("next_button_side_6"))
        self.horizontalLayout_8.addWidget(self.next_button_side_6)
        self.verticalLayout_side_6.addLayout(self.horizontalLayout_8)
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QtGui.QWidget()
        self.page_7.setObjectName(_fromUtf8("page_7"))
        self.verticalLayoutWidget_8 = QtGui.QWidget(self.page_7)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(-1, 19, 681, 551))
        self.verticalLayoutWidget_8.setObjectName(_fromUtf8("verticalLayoutWidget_8"))
        self.verticalLayout_side_7 = QtGui.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_side_7.setMargin(0)
        self.verticalLayout_side_7.setObjectName(_fromUtf8("verticalLayout_side_7"))
        self.headline_side7 = QtGui.QLabel(self.verticalLayoutWidget_8)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.headline_side7.setFont(font)
        self.headline_side7.setAlignment(QtCore.Qt.AlignCenter)
        self.headline_side7.setObjectName(_fromUtf8("headline_side7"))
        self.verticalLayout_side_7.addWidget(self.headline_side7)
        self.result_energy = QtGui.QLabel(self.verticalLayoutWidget_8)
        self.result_energy.setObjectName(_fromUtf8("result_energy"))
        self.verticalLayout_side_7.addWidget(self.result_energy)
        self.result_best_energy = QtGui.QLabel(self.verticalLayoutWidget_8)
        self.result_best_energy.setObjectName(_fromUtf8("result_best_energy"))
        self.verticalLayout_side_7.addWidget(self.result_best_energy)
        self.number_same_results = QtGui.QLabel(self.verticalLayoutWidget_8)
        self.number_same_results.setObjectName(_fromUtf8("number_same_results"))
        self.verticalLayout_side_7.addWidget(self.number_same_results)
        self.result_requests = QtGui.QLabel(self.verticalLayoutWidget_8)
        self.result_requests.setObjectName(_fromUtf8("result_requests"))
        self.verticalLayout_side_7.addWidget(self.result_requests)
        self.request_duration = QtGui.QLabel(self.verticalLayoutWidget_8)
        self.request_duration.setObjectName(_fromUtf8("request_duration"))
        self.verticalLayout_side_7.addWidget(self.request_duration)
        self.results_table = QtGui.QTableWidget(self.verticalLayoutWidget_8)
        self.results_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.results_table.setTabKeyNavigation(False)
        self.results_table.setProperty("showDropIndicator", False)
        self.results_table.setDragDropOverwriteMode(False)
        self.results_table.setObjectName(_fromUtf8("results_table"))
        self.results_table.setColumnCount(0)
        self.results_table.setRowCount(0)
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.horizontalHeader().setDefaultSectionSize(30)
        self.results_table.verticalHeader().setVisible(False)
        self.verticalLayout_side_7.addWidget(self.results_table)
        self.request_save_to_file = QtGui.QPushButton(self.verticalLayoutWidget_8)
        self.request_save_to_file.setObjectName(_fromUtf8("request_save_to_file"))
        self.verticalLayout_side_7.addWidget(self.request_save_to_file)
        self.next_button_side_7 = QtGui.QPushButton(self.verticalLayoutWidget_8)
        self.next_button_side_7.setObjectName(_fromUtf8("next_button_side_7"))
        self.verticalLayout_side_7.addWidget(self.next_button_side_7)
        self.stackedWidget.addWidget(self.page_7)
        self.verticalLayout_4.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(4)
        self.stackedWidget_2.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Jufo Qubo", None))
        self.infos_label_1_side_1.setText(_translate("MainWindow", "Mit diesem Programm kann man Optimierungsprobleme graphisch an den Quantencomputer senden", None))
        self.infos_label_2_side_1.setText(_translate("MainWindow", "Copyright: Jonthan Treffler , Jakov D. Wallbrecher , Paul Schappert , 2019", None))
        self.next_button_side_1.setText(_translate("MainWindow", "weiter", None))
        self.infos_label_1_side_2.setText(_translate("MainWindow", "Folgendes wird als nächstes ausgeführt:", None))
        self.infos_label_2_side_2.setText(_translate("MainWindow", "1. Hamiltonian generieren", None))
        self.infos_label_3_side_2.setText(_translate("MainWindow", "2. Hamiltonian in Chimera Graph umformen", None))
        self.infos_label_4_side_2.setText(_translate("MainWindow", "3. Senden der Daten über das Internet zum Quantencomputer in Kanada", None))
        self.infos_label_5_side_2.setText(_translate("MainWindow", "4. Ergebnisse zurück übertragen und auswerten", None))
        self.back_button_side_2.setText(_translate("MainWindow", "zurück", None))
        self.next_button_side_2.setText(_translate("MainWindow", "weiter", None))
        self.headline_side_3.setText(_translate("MainWindow", "Solver auswählen", None))
        self.back_button_side_3.setText(_translate("MainWindow", "zurück", None))
        self.next_button_side_3.setText(_translate("MainWindow", "weiter", None))
        self.headline_side_4.setText(_translate("MainWindow", "Solver Parameter", None))
        self.runs_headline.setText(_translate("MainWindow", "Runs", None))
        self.runs_min_label.setText(_translate("MainWindow", "1000", None))
        self.runs_label.setText(_translate("MainWindow", "0", None))
        self.runs_max_label.setText(_translate("MainWindow", "10000", None))
        self.annealing_time_headline.setText(_translate("MainWindow", "Annealing Time", None))
        self.annealing_time_min.setText(_translate("MainWindow", "20", None))
        self.annealing_time_label.setText(_translate("MainWindow", "0", None))
        self.annealing_time_max.setText(_translate("MainWindow", "80", None))
        self.chain_strength_headline.setText(_translate("MainWindow", "Chain Strength", None))
        self.chain_strength_min.setText(_translate("MainWindow", "1", None))
        self.chain_strength_label.setText(_translate("MainWindow", "0", None))
        self.chain_strength_max.setText(_translate("MainWindow", "25", None))
        self.back_button_side_4.setText(_translate("MainWindow", "zurück", None))
        self.next_button_side_4.setText(_translate("MainWindow", "weiter", None))
        self.headline_side_5.setText(_translate("MainWindow", "Optimierungsproblem auswählen", None))
        self.definition_headline.setText(_translate("MainWindow", "Definition:", None))
        self.back_button_side_5.setText(_translate("MainWindow", "zurück", None))
        self.next_button_side_5.setText(_translate("MainWindow", "weiter", None))
        self.headline_side_6.setText(_translate("MainWindow", "Optionen für Optimierungsproblem", None))
        self.n_queens_options_headline.setText(_translate("MainWindow", "N-Damen Optionen:", None))
        self.knights_tour_options_headline.setText(_translate("MainWindow", "Knights Tour Optionen:", None))
        self.knights_tour_no_options_label.setText(_translate("MainWindow", "keine Einstellungen benötigt", None))
        self.sudoku_options_headline.setText(_translate("MainWindow", "Sudoku Optionen:", None))
        self.amazone_options_headline.setText(_translate("MainWindow", "Amazone Optionen:", None))
        self.custom_hamiltonian_label.setText(_translate("MainWindow", "Eigener Hamiltonian:", None))
        self.custom_hamiltonian_file_picker_button.setText(_translate("MainWindow", "Datei öffnen", None))
        self.back_button_side_6.setText(_translate("MainWindow", "zurück", None))
        self.next_button_side_6.setText(_translate("MainWindow", "start", None))
        self.headline_side7.setText(_translate("MainWindow", "Ergebnisse", None))
        self.result_energy.setText(_translate("MainWindow", "Energie:", None))
        self.result_best_energy.setText(_translate("MainWindow", "Beste Energie:", None))
        self.number_same_results.setText(_translate("MainWindow", "Anzahl gleicher Ergebnisse:", None))
        self.result_requests.setText(_translate("MainWindow", "Requests: ", None))
        self.request_duration.setText(_translate("MainWindow", "Dauer: ", None))
        self.request_save_to_file.setText(_translate("MainWindow", "Alle Ergebnisse in Datei speichern", None))
        self.next_button_side_7.setText(_translate("MainWindow", "zum Start", None))


def next_button():
		ui.stackedWidget.setCurrentIndex(ui.stackedWidget.currentIndex()+1)
def back_button():
		ui.stackedWidget.setCurrentIndex(ui.stackedWidget.currentIndex()-1)
def start_button():
	#try: ui.request_save_to_file.clicked.disconnect() 
	#except Exception: pass
	ui.results_table.setColumnCount(0)
	ui.results_table.setRowCount(0)
	ui.result_energy.setText(_translate("MainWindow", "Energie:", None))
	ui.result_best_energy.setText(_translate("MainWindow", "beste Energie:", None))
	ui.number_same_results.setText(_translate("MainWindow", "Anzahl gleicher Ergebnisse:", None))
	ui.result_requests.setText(_translate("MainWindow", "Requests: ", None))
	ui.request_duration.setText(_translate("MainWindow", "Dauer: ", None))
	Timer(1, start, ()).start()
	next_button()
	#start()
def switch_options_side():
	ui.stackedWidget_2.setCurrentIndex(ui.problem_select.currentIndex())
	next_button()
def custom_ui():
	ui.stackedWidget.setCurrentIndex(0)
	ui.stackedWidget_2.setCurrentIndex(0)
	ui.next_button_side_1.clicked.connect(next_button)
	ui.next_button_side_2.clicked.connect(next_button)
	ui.next_button_side_3.clicked.connect(next_button)
	ui.next_button_side_4.clicked.connect(next_button)
	ui.next_button_side_5.clicked.connect(switch_options_side)
	ui.next_button_side_6.clicked.connect(start_button)
	ui.next_button_side_7.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(0))
	
	ui.back_button_side_2.clicked.connect(back_button)
	ui.back_button_side_3.clicked.connect(back_button)
	ui.back_button_side_4.clicked.connect(back_button)
	ui.back_button_side_5.clicked.connect(back_button)
	ui.back_button_side_6.clicked.connect(back_button)
	
	ui.solver_select.addItems(solvers)
	ui.problem_select.addItems(qubo_problems)
	ui.n_queens_n_select.addItems(n_queens_options)
	ui.sudoku_n_select.addItems(sudoku_options)
	ui.amazone_n_select.addItems(amazone_options)
	
	ui.runs_slider.setMinimum(min_reads)
	ui.runs_min_label.setText(_translate("MainWindow", str(min_reads), None))
	ui.runs_slider.setMaximum(max_reads)
	ui.runs_max_label.setText(_translate("MainWindow", str(max_reads), None))
	
	ui.annealing_time_slider.setMinimum(min_annealing_time)
	ui.annealing_time_min.setText(_translate("MainWindow", str(min_annealing_time), None))
	ui.annealing_time_slider.setMaximum(max_annealing_time)
	ui.annealing_time_max.setText(_translate("MainWindow", str(max_annealing_time), None))
	
	ui.chain_strength_slider.setMinimum(min_chain_strength)
	ui.chain_strength_min.setText(_translate("MainWindow", str(min_chain_strength), None))
	ui.chain_strength_slider.setMaximum(max_chain_strength)
	ui.chain_strength_max.setText(_translate("MainWindow", str(max_chain_strength), None))
	
	ui.runs_label.setText(str(ui.runs_slider.value()))
	ui.runs_slider.valueChanged.connect(lambda: ui.runs_label.setText(str(ui.runs_slider.value())))
	
	ui.annealing_time_label.setText(str(ui.annealing_time_slider.value()))
	ui.annealing_time_slider.valueChanged.connect(lambda: ui.annealing_time_label.setText(str(ui.annealing_time_slider.value())))
	
	ui.chain_strength_label.setText(str(ui.chain_strength_slider.value()))
	ui.chain_strength_slider.valueChanged.connect(lambda: ui.chain_strength_label.setText(str(ui.chain_strength_slider.value())))
	
	ui.request_save_to_file.clicked.connect(save_results_in_file)
	
	ui.custom_hamiltonian_file_picker_button.clicked.connect(open_hamiltonian_file)
	
	ui.problem_select.currentIndexChanged.connect(lambda: ui.qubo_definition.setText(QString.fromLocal8Bit(qubo_definitions[ui.problem_select.currentIndex()])))
	ui.qubo_definition.setText(QString.fromLocal8Bit(qubo_definitions[ui.problem_select.currentIndex()]))
	
	def sudoku_n_changed():
		new_n_index = ui.sudoku_n_select.currentIndex()
		ui.sudoku_options_table.setRowCount(sudoku_options_n[new_n_index])
		ui.sudoku_options_table.setColumnCount(sudoku_options_n[new_n_index])
		ui.sudoku_presets.clear()
		ui.sudoku_presets.addItems(sudoku_preset_titles[new_n_index])
	ui.sudoku_n_select.currentIndexChanged.connect(sudoku_n_changed)
	sudoku_n_changed()
	
	def sudoku_preset_changed():
		set_table_to_array(ui.sudoku_options_table,sudoku_presets[ui.sudoku_n_select.currentIndex()][ui.sudoku_presets.currentIndex()])
	ui.sudoku_presets.currentIndexChanged.connect(sudoku_preset_changed)
	
	warnings.filterwarnings("ignore", message="The Pegasus topology produced by this generator with default parameters is one member of a large family of topologies under consideration, and may not be reflected in future products")

#Solvers
class solver:
	def solve(self,qubomatrix,runs,annealing_time,chain_strength):
		print("This schould not be called")
	def convert_to_qubo():
		print("This schould not be called")

class quantumcomputer(solver):
	def convert_to_qubo(self,qubomatrix):
		qubo = {}
		for index,value in np.ndenumerate(qubomatrix):
			if value != 0:
				qubo[index] = value
		return qubo
	def solve(self,qubomatrix,num_reads,annealing_time,chain_strength):
		qubo = self.convert_to_qubo(qubomatrix)
		responses = []
		
		progress = 0
		
		dwave_user_max_time = 900000.0
		
		if num_reads*annealing_time > dwave_user_max_time:
			self.num_reads_per_request = math.trunc(dwave_user_max_time/annealing_time)
			self.number_of_requests = int((num_reads*1.0)/self.num_reads_per_request)
		else:
			self.num_reads_per_request = num_reads;
			self.number_of_requests = 1
		
		i = 0
		for read in range(0,int(self.number_of_requests)):
			sampler = EmbeddingComposite(DWaveSampler())
			response = sampler.sample_qubo(qubo, num_reads=self.num_reads_per_request, annealing_time=annealing_time, chain_strength=chain_strength)
			responses.append(response);
		
		results = []
	
		for response in responses:
			for sample, energy, num_occurrences, cbf in response.record:
				results.append([energy,sample,num_occurrences])
				
		results = sorted(results, key=lambda x: x[0], reverse=False)
		return results

class pegasus(solver):
	def convert_to_qubo(self,qubomatrix):
		qubo = {(i,i):0.0 for i in range(len(qubomatrix))}
		for index,value in np.ndenumerate(qubomatrix):
			if value != 0:
				qubo[index] = value
		return qubo
	def solve(self,qubomatrix,num_reads,annealing_time,chain_strength):
		self.num_reads_per_request = num_reads
		self.number_of_requests = 1
		
		qubo = self.convert_to_qubo(qubomatrix)
		
		graph = dnx.pegasus_graph(16)
		simulator = neal.SimulatedAnnealingSampler()
		composite = dimod.StructureComposite(simulator, graph.nodes, graph.edges)
		sampler = LazyFixedEmbeddingComposite(composite)
		
		response = sampler.sample_qubo(qubo, num_reads=num_reads, chain_strength=chain_strength)
		
		results = []
		
		for sample, energy, num_occurrences, cbf in response.record:
				results.append([energy,sample,num_occurrences])
				
		results = sorted(results, key=lambda x: x[0], reverse=False)
		return results

#Problems
class qubo_problem():
	def get_best_energy():
		print("This schould not be called")
	def get_matrix():
		print("This schould not be called")
	def result_to_table(self,result):
		print("This schould not be called")
		
class n_queens(qubo_problem):
	def __init__(self,n,diag_free):
		self.n =n
		self.diag_free = diag_free
	def get_best_energy(self):
		return self.n*-2
	def get_matrix(self):
		if self.diag_free:
			return np.loadtxt("./Hamiltonians/n_queens/qubomatrix_"+str(self.n)+"_diagFrei.txt")
		else:
			return np.loadtxt("./Hamiltonians/n_queens/qubomatrix_"+str(self.n)+"_diagBesetzt.txt")
	def result_to_table(self,result):
		table = []
		if self.diag_free:
			table_n = self.n+1
		else:
			table_n = self.n
		for y in range(table_n):
			table.append([])
			for x in range(table_n):
				table[y].append("")
		for y in range(self.n):
			for x in range(self.n):
				table[y][x] = result[(y*self.n)+x]
		if self.diag_free:
			table[table_n-1][table_n-1] = "1"
		return table
class knights_tour(qubo_problem):
	def get_best_energy(self):
		return -14
	def get_matrix(self):
		return np.loadtxt("./Hamiltonians/knights_tour/qubomatrix_roesslesprung.txt")
	def result_to_table(self,result):
		#Wandelt in Ebenen um
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
		
		chess = []
		for i in range(9):
			chess.append([])
			for o in range(3):
				chess[i].append([])
				for p in range(3):
					chess[i][o].append(0)
				
		for i in range(len(result)):
			ebene = ((i /4) % 2)
			pos = (i % 4)
			convert_value = convert[pos][ebene]
			chess[int((i /4))][convert_value[0]-1][convert_value[1]-1] = result[i]

		#Fasst Ebenen zusammen
		spruenge = []
		
		for ebene in range(len(chess)):
			for y in range(len(chess[ebene])):
				for x in range(len(chess[ebene][y])):
					if chess[ebene][y][x] == 1:
						spruenge.append([x,y])
		
		#Bilde auf Tabelle ab
		table = []
		for i in range(3):
			table.append([])
			for o in range(3):
				table[i].append("")
		
		for sprung in range(len(spruenge)):
			x = spruenge[sprung][0]
			y = spruenge[sprung][1]
			table[x][y] = sprung+1
		return table
class amazone(qubo_problem):
	def __init__(self,n):
		self.n = n
	def get_best_energy(self):
		return self.n*-1
	def get_matrix(self):
		return np.loadtxt("./Hamiltonians/amazone/amazone_"+str(self.n)+".txt")
	def result_to_table(self,result):
		table = []
		for y in range(self.n):
			table.append([])
			for x in range(self.n):
				table[y].append(result[(y*self.n)+x])
		return table
class sudoku(qubo_problem):
	def __init__(self,n,gegeben):
		self.n = n
		self.klFeld = math.sqrt(n)
		self.gegeben = gegeben
	def get_best_energy(self):
		return (-2*(self.n*self.n))-(len(self.gegeben)*-2)
	def get_matrix(self):
		hamiltonianMatrix = []
		for y in range(self.n**3):
			hamiltonianMatrix.append([])
			for x in range(self.n**3):
				hamiltonianMatrix[y].append(0)
				
		#stelle Matrix auf
		for x1 in range(self.n):
			for y1 in range(self.n):    
				for num1 in range(self.n):
					for x2 in range(self.n):
						for y2 in range(self.n):
							for num2 in range(self.n):
								hamX = min(x1*self.n*self.n+y1*self.n+num1, x2*self.n*self.n+y2*self.n+num2)
								hamY = max(x1*self.n*self.n+y1*self.n+num1, x2*self.n*self.n+y2*self.n+num2)
								
								#pro Spalte jede Zahl nur einmal
								if x1==x2 and num1==num2  and y1!=y2:
									hamiltonianMatrix[hamX][hamY]+=1
		                
								#pro Zeile jede Zahl nur einmal
								if y1==y2 and num1==num2  and x1!=x2:
									hamiltonianMatrix[hamX][hamY]+=1
		
								#pro zelle nur eine Zahl
								if (x1==x2 and y1==y2) and num1!=num2:
									hamiltonianMatrix[hamX][hamY]+=1
		
								#pro 3x3 Feld nur eine Zahl
								if (int(x1/self.klFeld)==int(x2/self.klFeld) and int(y1/self.klFeld)==int(y2/self.klFeld)) and num1==num2  and x1!=x2 and y1!=y2:
									hamiltonianMatrix[hamX][hamY]+=1
		
								#Grundbelohnung
								if x1==x2 and y1==y2 and num1==num2:
									hamiltonianMatrix[hamX][hamY]-=2
		
		#markiere gegebene in Hamiltonian
		for i in range(len(self.gegeben)):
			for x in range(self.n):
				for y in range(self.n):
					for num in range(self.n):
						hamX = x*self.n*self.n+y*self.n+num
						hamY = x*self.n*self.n+y*self.n+num
						if (x==self.gegeben[i][0] and y==self.gegeben[i][1]) or (((x==self.gegeben[i][0] or y==self.gegeben[i][1] or ((int(x/self.klFeld)==int(self.gegeben[i][0]/self.klFeld) and int(y/self.klFeld)==int(self.gegeben[i][1]/self.klFeld))))  and  num==self.gegeben[i][2] )):
							for x2 in range(self.n**3):
								for y2 in range(self.n**3):
									if hamX==x2:
										hamiltonianMatrix[hamX][y2]=8
									if hamY==y2:
										hamiltonianMatrix[x2][hamY]=8
		#lösche markierte aus Hamiltonian
		values = []
		for i in range(self.n**3):
			values.append([])
		
		for x in range(self.n**3):
			for y in range(self.n**3):
				if hamiltonianMatrix[x][y]!=8:
					values[x].append(int(hamiltonianMatrix[x][y]))
		  
		remove_lines = []
		for i in range(len(values)-1):
			if len(values[i])==0:
				remove_lines.append(i)
		
		for i in reversed(range(len(remove_lines))):
			values.pop(remove_lines[i])
		
		hamiltonianMatrix = []
		for i in range(len(values[0])):
			hamiltonianMatrix.append([])
			for o in range(len(values[0])):
				hamiltonianMatrix[i].append(0)
		
		for x in range(len(hamiltonianMatrix)):
			for y in range(len(hamiltonianMatrix)):
				hamiltonianMatrix[x][y]=int(values[x][y])
		
		return hamiltonianMatrix
	def result_to_table(self,result):
		result = result.tolist()
		sudoku = []
		sudokuTable = []
		
		#sortiere um
		for x in range(self.n):
			sudoku.append([])
			for y in range(self.n):
				sudoku[x].append([])
				for num in range(self.n):
					besetzt=True
					for i in range(len(self.gegeben)):
						if (x==self.gegeben[i][0] and y==self.gegeben[i][1]) or (((x==self.gegeben[i][0] or y==self.gegeben[i][1] or ((int(x/self.klFeld)==int(self.gegeben[i][0]/self.klFeld) and int(y/self.klFeld)==int(self.gegeben[i][1]/self.klFeld))))  and  num==self.gegeben[i][2] )):
							besetzt=False
					if besetzt:
						sudoku[x][y].append(result[0])
						result.pop(0)
					else:
						sudoku[x][y].append(0)
		
		#setze berechnete ein
		for y in range(self.n):
			sudokuTable.append([])
			for x in range(self.n):
				besetztesFeld=0;
				for num in range(self.n):
					if sudoku[x][y][num] == 1:
						besetztesFeld=num+1;
				sudokuTable[y].append(besetztesFeld)
		
		#setze Gegebene ein
		for i in range(len(self.gegeben)):
		  x = self.gegeben[i][0]
		  y = self.gegeben[i][1]
		  value = self.gegeben[i][2]+1
		  sudokuTable[y][x] = value
		  
		return sudokuTable
class custom(qubo_problem):
	def __init__(self,hamilton_matrix):
		self.hamilton_matrix = hamilton_matrix
	def get_best_energy(self):
		return ""
	def get_matrix(self):
		return string_to_array(self.hamilton_matrix)
	def result_to_table(self,result):
		return [result]
#Functions
def open_hamiltonian_file(self):
	filename = QFileDialog.getOpenFileName(ui.centralwidget, 'Hamiltonian auswählen', '')
	if filename != '':
		with open(filename,'r') as file:
			ui.custom_hamiltonian_text_field.setPlainText(file.read())
def save_results_in_file():
	filename = QFileDialog.getSaveFileName(ui.centralwidget, 'Speicherort auswählen', 'results.txt')
	if filename != '':
		with open(filename,'w') as file:
			file.write('energy\tnum_occurrences\tsample\n')
			for response in result:
				file.write('%f\t%d\t%s' % (response[0], response[2], np.array2string(response[1], max_line_width=None).replace('\n','')))
				file.write('\n')
def string_to_array(string):
	array = []
	string = string.splitlines()
	for row in range(len(string)):
		array.append(np.fromstring(string[row],sep=' ',dtype=np.int8).tolist())
	return array
def set_table_to_array(table,array):
	ui.results_table.setRowCount(len(array))
	ui.results_table.setColumnCount(len(array[0]))
	
	for y in range(len(array)):
		for x in range(len(array[y])):
			table.setItem(y,x,QTableWidgetItem(str(array[y][x])));
def table_to_int_array(table):
	table_array = []
	for y in range(table.rowCount()):
		for x in range(table.columnCount()):
			item = table.item(y,x)
			if item is not None:
				if item.text() != "":
					table_array.append([x,y,int(item.text())-1])
	return table_array
def start():
	global result
	print("Start")
	
	start_time = time.time()
	solver = solver_classes[ui.solver_select.currentIndex()]
	if ui.problem_select.currentIndex() == 0:
		qubo_problem = n_queens_options_classes[ui.n_queens_n_select.currentIndex()]
	elif ui.problem_select.currentIndex() == 1:
		qubo_problem = knights_tour()
	elif ui.problem_select.currentIndex() == 2:
		qubo_problem = sudoku(sudoku_options_n[ui.sudoku_n_select.currentIndex()],table_to_int_array(ui.sudoku_options_table))
	elif ui.problem_select.currentIndex() == 3:
		qubo_problem = amazone_options_classes[ui.amazone_n_select.currentIndex()]
	elif ui.problem_select.currentIndex() == 4:
		qubo_problem = custom(str(ui.custom_hamiltonian_text_field.toPlainText()))
	runs = ui.runs_slider.value()
	annealing_time = ui.annealing_time_slider.value()
	chain_strength = ui.chain_strength_slider.value()
	
	result = solver.solve(qubo_problem.get_matrix(),runs,annealing_time,chain_strength)
	table = qubo_problem.result_to_table(result[0][1])
	
	end_time = time.time()
	
	set_table_to_array(ui.results_table,table)
	ui.result_energy.setText(_translate("MainWindow", "Energie: "+str(int(result[0][0])), None))
	ui.result_best_energy.setText(_translate("MainWindow", "beste Energie: "+str(qubo_problem.get_best_energy()), None))
	ui.result_requests.setText(_translate("MainWindow", "Requests: "+str(solver.number_of_requests)+"x"+str(solver.num_reads_per_request), None))
	ui.number_same_results.setText(_translate("MainWindow", "Anzahl gleicher Ergebnisse: "+str(result[0][2]), None))
	ui.request_duration.setText(_translate("MainWindow", "Dauer: "+str(end_time - start_time)+" Sekunden", None))

	
solvers = ["Quantencomputer","Pegasus Graph"]
solver_classes = [quantumcomputer(),pegasus()]
qubo_problems = ["N Damen","Knights Tour","Sudoku","N Amazonen","eigener Hamiltonian"]
qubo_definitions = [
						"Beim n-Damenproblem geht es darum n Schachdamen auf einem n mal n großen Schachfeld so zu verteilen, dass keine eine andere bedroht.",
						"Beim Knights Tour soll ein Springer einen Weg über ein n mal n großes Schachfeld finden bei dem er jedes Feld genau einmal besucht.",
						"Beim Sudoku wird ein (in diesem Fall 4 mal 4 großes) Feld in (in diesem Fall 4) kleinere Quadrate unterteilt. In jedem Quadrat , jeder Zeile und jeder Spalte darf eine Zahl nur einmal vorkommen.",
						"Beim n-Amazonenproblem sollen n Amazonen auf einem n mal n großen Feld platziert werden. Eine Amazone kann jeden Zug entscheiden ob sie wie eine Dame oder ein Springer zieht.",
						""
					]
n_queens_options = ["n=4","n=5","n=6","n=7","n=8","n=8 (mit Trick)"]
n_queens_options_classes = [n_queens(4,False),n_queens(5,False),n_queens(6,False),n_queens(7,False),n_queens(8,False),n_queens(7,True)]
sudoku_options = ["n=4"]
sudoku_options_n = [4]
sudoku_preset_titles = [["leer","9 vorgegebene"]]
sudoku_presets = [
					[
						[
							["","","",""],
							["","","",""],
							["","","",""],
							["","","",""]
						],
						[
							["1","3","","4"],
							["4","","1",""],
							["","4","",""],
							["","1","4","2"]
						]
					]
				]
amazone_options = ["n=4","n=5","n=6","n=7"]
amazone_options_classes = [amazone(4),amazone(5),amazone(6),amazone(7)]

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    custom_ui()
    sys.exit(app.exec_())
