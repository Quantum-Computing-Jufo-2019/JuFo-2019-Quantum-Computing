String[] ergString;
ArrayList<Integer> ergInt=new ArrayList <Integer>();
int n=4;
int klFeld=2;
ArrayList <PVector> gegeben = new ArrayList<PVector>();
int[][][] sudoku= new int[n][n][n];
String[] gegebenStringFiles;

void setup() {
  gegebenStringFiles=loadStrings("gegebeneWerte.txt");

  for (int i=0; i<gegebenStringFiles.length; i++) {
    String[] localStrings=gegebenStringFiles[i].split(" ");
    for (int j=0; j<localStrings.length; j++) {
      if (int(localStrings[j])>0)
        gegeben.add(new PVector(j, i, int(localStrings[j])-1));
    }
  }

  ergString=loadStrings("results.txt");
  noLoop();
}

void draw() {
  ergString=ergString[0].split(" ");
  for (int i=0; i<ergString.length; i++) {
    ergInt.add(int(ergString[i]));
  }
  println(ergInt.size());
  setzeGeg();
  boolean[][][] sudokuBool=new boolean[n][n][n];
  for (int x=0; x<n; x++) {
    for (int y=0; y<n; y++) {
      for (int num=0; num<n; num++) {  
        sudokuBool[x][y][num]=sudoku[x][y][num]==1?true:false;
      }
    }
  }
  //for (int i=0; i<gegeben.size(); i++) {
  //  for (int x=0; x<n; x++) {
  //    for (int y=0; y<n; y++) {
  //      for (int num=0; num<n; num++) {  
  //        if (gegeben.get(i).x==x&&gegeben.get(i).y==y&&gegeben.get(i).z==num) {
  //          sudokuBool[x][y][num]=true;
  //        }
  //      }
  //    }
  //  }
  //}
  maleSudoku(sudokuBool);
}


void setzeGeg() {
  for (int x=0; x<n; x++) {
    for (int y=0; y<n; y++) {
      for (int num=0; num<n; num++) {
        boolean besetzt=true;
        for (int i=0; i<gegeben.size(); i++) {
          int hamX = x*n*n+y*n+num;
          int hamY = x*n*n+y*n+num;
          if ((((x==gegeben.get(i).x||y==gegeben.get(i).y||((int(x/klFeld)==int(gegeben.get(i).x/klFeld)&&
            int(y/klFeld)==int(gegeben.get(i).y/klFeld)))) && num==gegeben.get(i).z ))) {//x==gegeben.get(i).x&&y==gegeben.get(i).y)||
            besetzt=false;
            println("i");
          }
        }
        if (besetzt) {
          println(ergInt.get(0));
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
        maleSudoku(sudokuBool);
        println();
      }
    }
  }
}

void maleSudoku(boolean[][][] sudokuLocal) {
  for (int y=0; y<n; y++) {
    for (int x=0; x<n; x++) {
      int besetztesFeld=0;
      for (int num=0; num<n; num++) {
        if (sudokuLocal[x][y][num]) {
          besetztesFeld=num+1;
        }
      }
      print(besetztesFeld+" ");
    }
    println();
  }
}
