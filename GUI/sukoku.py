# -*- coding: utf-8 -*-

n = 4 #sudokugröße
klFeld = 2 #größe der inneren Kästchen
#int[][] hamiltonianMatrix = new int[n*n*n][n*n*n];
if_anweisung_count = 0
hamiltonianMatrix = []
for y in range(n*n*n):
	hamiltonianMatrix.append([])
	for x in range(n*n*n):
		hamiltonianMatrix[y].append(0)
#ArrayList <PVector> gegeben = new ArrayList<PVector>()
gegeben = []
#String[]gegebenStringFiles;

#Lädt gegebene Werte: Datei muss folgender maßen aufgebaut sein: 
#  0 2 0 0
#  1 0 3 4
#  0 0 1 0
#  0 3 4 2
#Also: n x n Feld: besetzte Felder die Zahl draufschreiben; nichtbesetzte Felder eine 0
#gegebenStringFiles=loadStrings("gegebeneWerte.txt");
#Füllt gegebene von der datei in eine ArrayList um 
#for (int i=0; i<gegebenStringFiles.length; i++) {
	#String[] localStrings=gegebenStringFiles[i].split(" ");
		#for (int j=0; j<localStrings.length; j++) {
			#if (int(localStrings[j])>0) {
				#gegeben.add(new PVector(j, i, int(localStrings[j])-1));
			#}
		#}
	#}
	#noLoop();
#}
gegeben.append([0,0,0])
gegeben.append([1,0,2])
gegeben.append([3,0,3])
gegeben.append([0,1,3])
gegeben.append([2,1,0])
gegeben.append([1,2,3])
gegeben.append([1,3,0])
gegeben.append([2,3,3])
gegeben.append([3,3,1])


#stellt den Standardhamiltonian auf
def hamiltonianTermAufstellen():
  #for (x1 =0; x1<n; x1++) {
  for x1 in range(n):
    #for (y1 =0; y1<n; y1++) {
    for y1 in range(n):    
      #for (num1 =0; num1<n; num1++) {
      for num1 in range(n):
        #for (x2 =0; x2<n; x2++) {
        for x2 in range(n):
          #for (y2 =0; y2<n; y2++) {
          for y2 in range(n):
            #for (num2 =0; num2<n; num2++) {
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


#setzt für jedes Qubit was "rausfliegen" soll, da der Wert gegeben ist, eine 8
def setzeGegebene():
	global if_anweisung_count
  #for (int i=0; i<gegeben.size(); i++) {
	for i in range(len(gegeben)):
	    #for (int x=0; x<n; x++) {
	    for x in range(n):
	      #for (int y=0; y<n; y++) {
	      for y in range(n):
	        #for (int num=0; num<n; num++) {
	        for num in range(n):
	          hamX = x*n*n+y*n+num
	          hamY = x*n*n+y*n+num
	          #if (((x==gegeben.get(i).x or y==gegeben.get(i).y or ((int(x/klFeld)==int(gegeben.get(i).x/klFeld) and int(y/klFeld)==int(gegeben.get(i).y/klFeld))))  and  num==gegeben.get(i).z )): #x==gegeben.get(i).x and y==gegeben.get(i).y) or 
	          if (x==gegeben[i][0] and y==gegeben[i][1]) or (((x==gegeben[i][0] or y==gegeben[i][1] or ((int(x/klFeld)==int(gegeben[i][0]/klFeld) and int(y/klFeld)==int(gegeben[i][1]/klFeld))))  and  num==gegeben[i][2] )):
	            print(str(i)+"  "+str(x)+"  "+str(y)+"  "+str(num))
	            if_anweisung_count = if_anweisung_count+1
	            #for (int x2=0; x2<n*n*n; x2++) {
	            for x2 in range(n*n*n):
	              #for (int y2=0; y2<n*n*n; y2++) {
	              for y2 in range(n*n*n):
	                if hamX==x2:
	                  hamiltonianMatrix[hamX][y2]=8
	                if hamY==y2:
	                  hamiltonianMatrix[x2][hamY]=8

#löscht alle 8ter Aus der Matrix raus
def entferneGegebene():
	global hamiltonianMatrix
  #2dim arrayList
  #ArrayList <ArrayList> values=new ArrayList <ArrayList>()
	values = []
  #initialisiere ArrayList
  #for (int i=0; i<n*n*n; i++) {
	for i in range(n*n*n):
    #values.add(new ArrayList<Integer>())
		values.append([])

  #schreibe von Matrix in ArrayList
  #for (int x=0; x<n*n*n; x++) {
	for x in range(n*n*n):
    #for (int y=0; y<n*n*n; y++) {
		for y in range(n*n*n):
			if hamiltonianMatrix[x][y]!=8:
				values[x].append(int(hamiltonianMatrix[x][y]))

  #entferne leere zeilen der Matrix
  #for (int i=0; i<values.size(); i++) {
  
	remove_lines = []
	#print("len(values) = "+str(len(values)))
	for i in range(len(values)-1):
		#print("i = "+str(i))
		if len(values[i])==0:
			#values.pop(i)
			#i = i-1
			remove_lines.append(i)

	for i in reversed(range(len(remove_lines))):
		values.pop(remove_lines[i])
  #Fülle von ArrayList in Array
  #hamiltonianMatrix = new int[values.get(0).size()][values.get(0).size()]
	hamiltonianMatrix = []
	for i in range(len(values[0])):
		hamiltonianMatrix.append([])
		for o in range(len(values[0])):
			hamiltonianMatrix[i].append(0)

  #for (int x=0; x<hamiltonianMatrix.length; x++) {
	for x in range(len(hamiltonianMatrix)):
    #for (int y=0; y<hamiltonianMatrix.length; y++) {
		for y in range(len(hamiltonianMatrix)):
			hamiltonianMatrix[x][y]=int(values[x][y])


#berechnet die Kosten: eig nur bei Opt verfahren nötig
#WICHTIG: Diese Kostenfunktion funktioniert anders als eine normale, da die gegebenen Werte vorher noch hinzugefügt werden müssen
def kostenfunktion(sudokuLocal):
  ergebnis=0
  #vektor=new int[n*n*n]
  vektor = []
  for i in range(n*n*n):
	  vektor.append()
  vektorerg = []

  #for (int i=0; i<n; i++) {
  for i in range(n):
    #for (int j=0; j<n; j++) {
    for j in range(n):
      #for (int num=0; num<n; num++) {
      for num in range(n):
        #vektor[i*n*n+j*n+num]=sudokuLocal[i][j][num]==true? (1):(0)
		if sudokuLocal[i][j][num]==true:
			vektor[i*n*n+j*n+num]= 1
		else:
			vektor[i*n*n+j*n+num]= 0
  #umfüllen vektor[] zu vectors außer denen, die schon vorgegeben sind
  #ArrayList <Integer> vectors=new ArrayList <Integer>()
  vectors = []

  #for (int x=0; x<n; x++) {
  for x in range(n):
    #for (int y=0; y<n; y++) {
    for y in range(n):
      #for (int num=0; num<n; num++) {
      for num in range(n):
        hamX = x*n*n+y*n+num
        hamY = x*n*n+y*n+num
        check = True          

        #for (int i=0; i<gegeben.size(); i++) {
        for i in range(len(gegeben)):
          #if (( (x==gegeben.get(i).x or y==gegeben.get(i).y or ((int(x/klFeld)==int(gegeben.get(i).x/klFeld) and int(y/klFeld)==int(gegeben.get(i).y/klFeld))))  and  num==gegeben.get(i).z)): #x==gegeben.get(i).x and y==gegeben.get(i).y) or 
          if (x==gegeben[i][0] and y==gegeben[i][1]) or (((x==gegeben[i][0] or y==gegeben[i][1] or ((int(x/klFeld)==int(gegeben[i][0]/klFeld) and int(y/klFeld)==int(gegeben[i][1]/klFeld))))  and  num==gegeben[i][2] )):
            #for (int x2=0; x2<n*n*n; x2++) {
            for x2 in range(n*n*n):
              #for (int y2=0; y2<n*n*n; y2++) {
              for y2 in range(n*n*n):
                if hamX==x2:
                  check=false
                if hamY==y2:
                  check=false
        if check:
          vectors.add(vektor[hamX])

  #vektor = new int[vectors.size()]
  vektor = []
  #for (int i=0; i<vectors.size(); i++) {
  for i in range(len(vectors)):
    #vektor[i]=vectors.get(i)
    vektor.append(vectors[i])
    
  #vektorerg=new int[vektor.length]
  vektorerg = []
  for i in range(len(vektor)):
	  vektorerg.append()
  #for (int i=0; i<vektor.length; i++) {
  for i in range(len(vektor)):
    #for (int j=0; j<hamiltonianMatrix.length; j++) {
    for j in range(len(hamiltonianMatrix)):
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j]

  #for (int i=0; i<vektor.length; i++) {
  for i in range(len(vektor)):
    ergebnis+=vektor[i]*vektorerg[i]

  return ergebnis

def exportiereHamiltonianMatrix():
  #String [] export=new String[hamiltonianMatrix.length]
  export = []
  for i in range(len(hamiltonianMatrix)):
	  export.append("")

  #for (int x=0; x<hamiltonianMatrix.length; x++) {
  for x in range(len(hamiltonianMatrix)):
    export[x]=""
    #for (int y=0; y<hamiltonianMatrix.length; y++) {
    for y in range(len(hamiltonianMatrix)):
      export[x]+=str(hamiltonianMatrix[x][y])+" "

  #saveStrings("qubomatrix_" + n + ".txt", export)
  for i in range(len(export)):
	print(export[i])
	
  print("Matrix Höhe: "+str(len(export)))

hamiltonianTermAufstellen()
setzeGegebene()
entferneGegebene()
exportiereHamiltonianMatrix()
print(if_anweisung_count)
