# -*- coding: utf-8 -*-

result = [1,0,1,1,1,1,1,1,0]
n=4
klFeld=2
sudokuTable = []

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

sudoku = []

#sortiere um
for x in range(n):
	sudoku.append([])
	for y in range(n):
		sudoku[x].append([])
		for num in range(n):
			besetzt=True
			for i in range(len(gegeben)):
				if (x==gegeben[i][0] and y==gegeben[i][1]) or (((x==gegeben[i][0] or y==gegeben[i][1] or ((int(x/klFeld)==int(gegeben[i][0]/klFeld) and int(y/klFeld)==int(gegeben[i][1]/klFeld))))  and  num==gegeben[i][2] )):
					besetzt=False
			if besetzt:
				sudoku[x][y].append(result[0])
				result.pop(0)
			else:
				sudoku[x][y].append(0)

#setze berechnete ein
for y in range(n):
	sudokuTable.append([])
	for x in range(n):
		besetztesFeld=0;
		for num in range(n):
			if sudoku[x][y][num] == 1:
				besetztesFeld=num+1;
		sudokuTable[y].append(besetztesFeld)

#setze Gegebene ein
for i in range(len(gegeben)):
  x = gegeben[i][0]
  y = gegeben[i][1]
  value = gegeben[i][2]+1
  sudokuTable[y][x] = value
  

print(sudokuTable)
