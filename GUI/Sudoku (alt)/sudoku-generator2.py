# -*- coding: utf-8 -*-
import math

n = 4
klFeld = math.sqrt(n)

hamiltonianMatrix = []
for y in range(n*n*n):
	hamiltonianMatrix.append([])
	for x in range(n*n*n):
		hamiltonianMatrix[y].append(0)
		
gegeben = []
gegeben.append([0,0,0])
gegeben.append([1,0,2])
gegeben.append([3,0,3])
gegeben.append([0,1,3])
gegeben.append([2,1,0])
gegeben.append([1,2,3])
gegeben.append([1,3,0])
gegeben.append([2,3,3])
gegeben.append([3,3,1])

#stelle Matrix auf
for x1 in range(n):
	for y1 in range(n):    
		for num1 in range(n):
			for x2 in range(n):
				for y2 in range(n):
					for num2 in range(n):
						hamX = min(x1*n*n+y1*n+num1, x2*n*n+y2*n+num2)
						hamY = max(x1*n*n+y1*n+num1, x2*n*n+y2*n+num2)
						
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
						if (int(x1/klFeld)==int(x2/klFeld) and int(y1/klFeld)==int(y2/klFeld)) and num1==num2  and x1!=x2 and y1!=y2:
							hamiltonianMatrix[hamX][hamY]+=1

						#Grundbelohnung
						if x1==x2 and y1==y2 and num1==num2:
							hamiltonianMatrix[hamX][hamY]-=2

#markiere gegebene in Hamiltonian
for i in range(len(gegeben)):
	for x in range(n):
		for y in range(n):
			for num in range(n):
				hamX = x*n*n+y*n+num
				hamY = x*n*n+y*n+num
				if (x==gegeben[i][0] and y==gegeben[i][1]) or (((x==gegeben[i][0] or y==gegeben[i][1] or ((int(x/klFeld)==int(gegeben[i][0]/klFeld) and int(y/klFeld)==int(gegeben[i][1]/klFeld))))  and  num==gegeben[i][2] )):
					for x2 in range(n*n*n):
						for y2 in range(n*n*n):
							if hamX==x2:
								hamiltonianMatrix[hamX][y2]=8
							if hamY==y2:
								hamiltonianMatrix[x2][hamY]=8
#lösche markierte aus Hamiltonian
values = []
for i in range(n*n*n):
	values.append([])

for x in range(n*n*n):
	for y in range(n*n*n):
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

for i in range(len(hamiltonianMatrix)):
	print(hamiltonianMatrix[i])
