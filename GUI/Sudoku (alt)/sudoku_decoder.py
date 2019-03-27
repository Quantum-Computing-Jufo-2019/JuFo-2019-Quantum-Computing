# -*- coding: utf-8 -*-

ergString = "1 0 1 1 1 1 1 1 0"
#ArrayList<Integer> ergInt=new ArrayList <Integer>();
ergInt = []
n=4
klFeld=2
gegeben = []
#int[][][] sudoku= new int[n][n][n];
sudoku = []
for i in range(n):
	sudoku.append([])
	for o in range(n):
		sudoku[i].append([])
		for p in range(n):
			sudoku[i][o].append(0)

gegeben.append([0,0,0])
gegeben.append([1,0,2])
gegeben.append([3,0,3])
gegeben.append([0,1,3])
gegeben.append([2,1,0])
gegeben.append([1,2,3])
gegeben.append([1,3,0])
gegeben.append([2,3,3])
gegeben.append([3,3,1])

ergString = ergString.split(" ")
#for (int i=0; i<ergString.length; i++) {
for i in range(len(ergString)):
	ergInt.append(int(ergString[i]))

#Das ist das eigentliche Programm, das kannst du so übernehmen
def setzeGeg():
  #for (int x=0; x<n; x++) {
	for x in range(n):
		#for (int y=0; y<n; y++) {
		for y in range(n):
			#for (int num=0; num<n; num++) {
			for num in range(n):
				besetzt=True
				#for (int i=0; i<gegeben.size(); i++) {
				for i in range(len(gegeben)):
					if (x==gegeben[i][0] and y==gegeben[i][1]) or (((x==gegeben[i][0] or y==gegeben[i][1] or ((int(x/klFeld)==int(gegeben[i][0]/klFeld) and int(y/klFeld)==int(gegeben[i][1]/klFeld))))  and  num==gegeben[i][2] )):
						besetzt=False
						#print("i")
				if besetzt:
					sudoku[x][y][num]=ergInt[0]
					ergInt.pop(0)
				#boolean[][][] sudokuBool=new boolean[n][n][n];
				sudokuBool = []
				for i in range(n):
					sudokuBool.append([])
					for o in range(n):
						sudokuBool[i].append([])
						for p in range(n):
							sudokuBool[i][o].append(False)
					
				#for (int a=0; a<n; a++) {
				for a in range(n):
					#for (int b=0; b<n; b++) {
					for b in range(n):
						#for (int c=0; c<n; c++) {  
						for c in range(n):
							sudokuBool[a][b][c]=sudoku[a][b][c]==1

def get_table(sudokuLocal):
  #for (int y=0; y<n; y++) {
  sudokuTable = []
  for y in range(n):
    #for (int x=0; x<n; x++) {
    sudokuTable.append([])
    for x in range(n):
      besetztesFeld=0;
      #for (int num=0; num<n; num++) {
      for num in range(n):
        if sudokuLocal[x][y][num] == 1:
          besetztesFeld=num+1;
      sudokuTable[y].append(besetztesFeld)
  for i in range(len(gegeben)):
	  x = gegeben[i][0]
	  y = gegeben[i][1]
	  value = gegeben[i][2]+1
	  sudokuTable[y][x] = value
  return sudokuTable

setzeGeg()
#Hier wird nur Das 3d sudoku von ints (0 oder 1) zu bool (false oder true) umgefüllt
#boolean[][][] sudokuBool=new boolean[n][n][n];
sudokuBool = []
for i in range(n):
	sudokuBool.append([])
	for o in range(n):
		sudokuBool[i].append([])
		for p in range(n):
			sudokuBool[i][o].append(False)
#for (int x=0; x<n; x++) {
for x in range(n):
	#for (int y=0; y<n; y++) {
    for y in range(n):
		#for (int num=0; num<n; num++) {
		for num in range(n):
			sudokuBool[x][y][num] = sudoku[x][y][num]==1

print(get_table(sudoku))
