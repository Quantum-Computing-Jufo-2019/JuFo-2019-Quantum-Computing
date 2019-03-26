ergString = "1 0 1 1 1 1 1 1 0";
ArrayList<Integer> ergInt=new ArrayList <Integer>();
n=4;
klFeld=2;
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

ergString=ergString.split(" ")
#for (int i=0; i<ergString.length; i++) {
for i in range(len(ergString)):
	ergInt.add(int(ergString[i]));
  
 setzeGeg();
  //Hier wird nur Das 3d sudoku von ints (0 oder 1) zu bool (false oder true) umgefüllt
  boolean[][][] sudokuBool=new boolean[n][n][n];
  for (int x=0; x<n; x++) {
    for (int y=0; y<n; y++) {
      for (int num=0; num<n; num++) {  
        sudokuBool[x][y][num]=sudoku[x][y][num]==1?true:false;
      }
    }
  }
}

//Das ist das eigentliche Programm, das kannst du so übernehmen
def setzeGeg() {
  for (int x=0; x<n; x++) {
    for (int y=0; y<n; y++) {
      for (int num=0; num<n; num++) {
        boolean besetzt=true;
        for (int i=0; i<gegeben.size(); i++) {
          if ((x==gegeben.get(i).x&&y==gegeben.get(i).y)||(((x==gegeben.get(i).x||y==gegeben.get(i).y||((int(x/klFeld)==int(gegeben.get(i).x/klFeld)&&
            int(y/klFeld)==int(gegeben.get(i).y/klFeld)))) && num==gegeben.get(i).z ))) {//x==gegeben.get(i).x&&y==gegeben.get(i).y)||
            besetzt=false;
            println("i");
          }
        }
        if (besetzt) {
          sudoku[x][y][num]=ergInt.get(0);
          ergInt.remove(0);
        }  
        boolean[][][] sudokuBool=new boolean[n][n][n];
        for (int a=0; a<n; a++) {
          for (int b=0; b<n; b++) {
            for (int c=0; c<n; c++) {  
              sudokuBool[a][b][c]=sudoku[a][b][c]==1?true:false;
            }
          }
        }
      }
    }
  }
}
