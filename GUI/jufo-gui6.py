
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

#Vars
#num_reads_per_request = 1000
progress = 0

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
			num_reads_per_request = math.trunc(dwave_user_max_time/annealing_time)
			number_of_requests = number_of_requests = int((num_reads*1.0)/num_reads_per_request)
		else:
			num_reads_per_request = num_reads;
			number_of_requests = 1
		
		print(num_reads_per_request)
		print(number_of_requests)
		
		i = 0
		for read in range(0,int(number_of_requests)):
			sampler = EmbeddingComposite(DWaveSampler())
			response = sampler.sample_qubo(qubo, num_reads=num_reads_per_request, annealing_time=annealing_time, chain_strength=chain_strength)
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
	def set_options(self,n,diag_free):
		print("This schould not be called")
	def get_max_energy():
		print("This schould not be called")
	def get_matrix():
		print("This schould not be called")
		
class n_queens(qubo_problem):
	def set_options(self,n,diag_free):
		self.n =n
		self.diag_free = diag_free
	def get_max_energy(self):
		return self.n*-2
	def get_matrix(self):
		if self.diag_free:
			return np.loadtxt("./Hamiltonians/qubomatrix_"+str(self.n)+"_diagFrei.txt")
		else:
			return np.loadtxt("./Hamiltonians/qubomatrix_"+str(self.n)+"_diagBesetzt.txt")
	def result_to_table(self,result):
		print(result)
		table = []
		for y in range(self.n):
			table.append([])
			for x in range(self.n):
				table[y].append(result[(y*self.n)+x])
		return table
class knights_tour(qubo_problem):
	def get_max_energy(self):
		return -14
	def get_matrix(self):
		return np.loadtxt("./Hamiltonians/qubomatrix_roesslesprung.txt")
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

solver = quantumcomputer()
problem = knights_tour()
#problem.set_options(4,False)
print(problem.result_to_table(solver.solve(problem.get_matrix(),1000,40,7)[0][1]))
