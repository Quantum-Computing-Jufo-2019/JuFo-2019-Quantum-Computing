import java.util.*;
int tsts=0;
int n =4;
int klFeld = 2;
boolean[][][] sudoku = new boolean[n][n][n];
boolean[][][] ausgangsposition = new boolean[n][n][n];
int[][] hamiltonianMatrix = new int[n*n*n][n*n*n];
ArrayList<String> simAnnGraph = new ArrayList<String>();
ArrayList <PVector> gegeben = new ArrayList<PVector>();
String[]gegebenStringFiles;

void setup() {
  gegebenStringFiles=loadStrings("gegebeneWerte.txt");
  //String[][]sudokugegeben=new String[gegebenStringFiles.length][gegebenStringFiles.length];
  //for (int i=0; i<gegebenStringFiles.length; i++) {
  //  for (int j=0; j<gegebenStringFiles.length; j++) {
  //    sudokugegeben[i][]=
  //  }
  //}
  for (int i=0; i<gegebenStringFiles.length; i++) {
    String[] localStrings=gegebenStringFiles[i].split(" ");
    for (int j=0; j<localStrings.length; j++) {
      if (int(localStrings[j])>0)
        gegeben.add(new PVector(j, i, int(localStrings[j])-1));
    }
  }
  for (int i=0; i<gegeben.size(); i++) {
    sudoku[int(gegeben.get(i).x)][int(gegeben.get(i).y)][int(gegeben.get(i).z)]=true;
  }
  maleSudoku(sudoku);
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      for (int num=0; num<n; num++) {
        ausgangsposition[i][j][num] = int(random(0, 2)) == 1;//
      }
    }
  }
  noLoop();
}



void draw() {
  hamiltonianTermAufstellen();
  setzeGegebene();
  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<n*n*n; i++) {
    for (int j=0; j<n*n*n; j++) {
      if (hamiltonianMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonianMatrix[i][j]);
    }
    println();
  }
  entferneGegebene();
  exportiereHamiltonianMatrix();
  println(hamiltonianMatrix.length);
  //exportiereAusgangsPosition();
  println("Hamiltonian-Matrix exportiert!");
  println("ausgangslösung:");
  maleSudoku(ausgangsposition);
  println("Kosten: "+kostenfunktion(ausgangsposition));
println("tsts"+tsts);
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      for (int num=0; num<n; num++) {
        sudoku[i][j][num]=ausgangsposition[i][j][num];
      }
    }
  }
  simulatedAnnealing();  
  exportiereGraph(simAnnGraph, "simAnn");
  println();
}



void hamiltonianTermAufstellen() {
  for (int x1 =0; x1<n; x1++) {
    for (int y1 =0; y1<n; y1++) {    
      for (int num1 =0; num1<n; num1++) {
        for (int x2 =0; x2<n; x2++) {
          for (int y2 =0; y2<n; y2++) {
            for (int num2 =0; num2<n; num2++) {
              int hamX = min(x1*n*n+y1*n+num1, x2*n*n+y2*n+num2);
              int hamY = max(x1*n*n+y1*n+num1, x2*n*n+y2*n+num2);
              //pro Spalte jede Zahl nur einmal
              if (x1==x2&&num1==num2 &&y1!=y2) {
                hamiltonianMatrix[hamX][hamY]+=1;
              }
              //pro Zeile jede Zahl nur einmal
              if (y1==y2&&num1==num2 &&x1!=x2) {
                hamiltonianMatrix[hamX][hamY]+=1;
              }
              //pro zelle nur eine Zahl
              if ((x1==x2&&y1==y2)&&num1!=num2) {
                hamiltonianMatrix[hamX][hamY]+=1;
              }

              //pro 3x3 Feld nur eine Zahl
              if ((int(x1/klFeld)==int(x2/klFeld)&&int(y1/klFeld)==int(y2/klFeld))&&num1==num2 &&x1!=x2&&y1!=y2) {
                hamiltonianMatrix[hamX][hamY]+=1;
              }

              //Grundbelohnung
              if (x1==x2&&y1==y2&&num1==num2) {
                hamiltonianMatrix[hamX][hamY]-=2;
              }
            }
          }
        }
      }
    }
  }
}


void setzeGegebene() {
  for (int i=0; i<gegeben.size(); i++) {

    for (int x=0; x<n; x++) {
      for (int y=0; y<n; y++) {
        for (int num=0; num<n; num++) {
          int hamX = x*n*n+y*n+num;
          int hamY = x*n*n+y*n+num;
          if ((x==gegeben.get(i).x&&y==gegeben.get(i).y)||(x==gegeben.get(i).x||y==gegeben.get(i).y||((int(x/klFeld)==int(gegeben.get(i).x/klFeld)&&
            int(y/klFeld)==int(gegeben.get(i).y/klFeld)))) && num==gegeben.get(i).z ) {//x==gegeben.get(i).x&&y==gegeben.get(i).y)||
            println(i+"  "+x+"  "+y+"  "+num);
            for (int x2=0; x2<n*n*n; x2++) {
              for (int y2=0; y2<n*n*n; y2++) {
                if (hamX==x2) {
                  hamiltonianMatrix[hamX][y2]=8;
                }
                if (hamY==y2) {
                  hamiltonianMatrix[x2][hamY]=8;
                }
              }
            }
          }
        }
      }
    }
  }
}

void entferneGegebene() {
  ArrayList <ArrayList> values=new ArrayList <ArrayList>();
  //initialisiere ArrayList
  for (int i=0; i<n*n*n; i++) {
    values.add(new ArrayList<Integer>());
  }
  //schreibe von Matrix in ArrayList
  for (int x=0; x<n*n*n; x++) {
    for (int y=0; y<n*n*n; y++) {
      if (hamiltonianMatrix[x][y]!=8) {
        values.get(x).add(int(hamiltonianMatrix[x][y]));
      }
    }
  }
  //entferne leere zeilen der Matrix
  for (int i=0; i<values.size(); i++) {
    if (values.get(i).size()==0) {
      values.remove(i);
      i--;
    }
  }
  //Fülle von ArrayList in Array
  hamiltonianMatrix = new int[values.get(0).size()][values.get(0).size()];
  for (int x=0; x<hamiltonianMatrix.length; x++) {
    for (int y=0; y<hamiltonianMatrix.length; y++) {
      hamiltonianMatrix[x][y]=int(values.get(x).get(y).toString());
    }
  }
  //Ausgeben der neuen Matrix
  for (int i=0; i<hamiltonianMatrix.length; i++) {
    for (int j=0; j<hamiltonianMatrix.length; j++) {
      if (hamiltonianMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonianMatrix[i][j]);
    }
    println();
  }
}



int kostenfunktion(boolean[][][]sudokuLocal) {
  int ergebnis=0;
  int[] vektor=new int[n*n*n];
  int[] vektorerg;

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      for (int num=0; num<n; num++) {
        vektor[i*n*n+j*n+num]=sudokuLocal[i][j][num]==true? (1):(0);
      }
    }
  }
  //umfüllen vektor[] zu vectors außer denen, die schon vorgegeben sind
  ArrayList <Integer> vectors=new ArrayList <Integer>();

  for (int x=0; x<n; x++) {
    for (int y=0; y<n; y++) {
      for (int num=0; num<n; num++) {
        int hamX = x*n*n+y*n+num;
        int hamY = x*n*n+y*n+num;
        boolean check=true;          

        for (int i=0; i<gegeben.size(); i++) {
          if ((x==gegeben.get(i).x&&y==gegeben.get(i).y)||(( (x==gegeben.get(i).x||y==gegeben.get(i).y||((int(x/klFeld)==int(gegeben.get(i).x/klFeld)&&int(y/klFeld)==int(gegeben.get(i).y/klFeld)))) && num==gegeben.get(i).z))) {//x==gegeben.get(i).x&&y==gegeben.get(i).y)||
              tsts++;
            for (int x2=0; x2<n*n*n; x2++) {
              for (int y2=0; y2<n*n*n; y2++) {
                if (hamX==x2) {
                  check=false;
                }
                if (hamY==y2) {
                  check=false;
                }
              }
            }
          }
        }
        if (check) {
          vectors.add(vektor[hamX]);
        }
      }
    }
  }
  vektor = new int[vectors.size()];
  for (int i=0; i<vectors.size(); i++) {
    vektor[i]=vectors.get(i);
    //println(vektor[i]);
  }
  //println(vektor.length);
  //exit();
  vektorerg=new int[vektor.length];
  for (int i=0; i<vektor.length; i++) {
    for (int j=0; j<hamiltonianMatrix.length; j++) {
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<vektor.length; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}


void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<700000; durchlauf++) {
    int alteKosten = kostenfunktion(sudoku);
    int x = int(random(n));
    int y = int(random(n));
    int num = int(random(n));
    sudoku[x][y][num]=!sudoku[x][y][num];
    int kosten = kostenfunktion(sudoku);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      sudoku[x][y][num]=!sudoku[x][y][num];
    }
    for (int i=0; i<gegeben.size(); i++) {
      for (int numb=0; numb<n; numb++) {
        sudoku[int(gegeben.get(i).x)][int(gegeben.get(i).y)][numb]=false;
      }
    }
    kosten=kostenfunktion(sudoku);
    simAnnGraph.add(durchlauf+" "+kosten);

    //if (kosten==n*n*(-2)) {
    //  println(durchlauf+" Durchläufe");
    //  println("simAnn Schwelle: "+simAnn);
    //  break;
    //}

    simAnn*=0.99; //0.99
  }
  maleSudoku(sudoku);
  println("Kosten: "+kostenfunktion(sudoku));
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


void exportiereHamiltonianMatrix() {
  String [] export=new String[hamiltonianMatrix.length];
  for (int x=0; x<hamiltonianMatrix.length; x++) {
    export[x]="";
    for (int y=0; y<hamiltonianMatrix.length; y++) {
      export[x]+=hamiltonianMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrix_" + n + ".txt", export);
}


int randomWalkTreshold() {
  ArrayList<Integer> kostenDifferenzen=new ArrayList<Integer>();
  boolean[][][] sudokuRandomWalk = new boolean[n][n][n];
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      for (int num=0; num<n; num++) {
        sudokuRandomWalk[i][j][num]=true;
      }
    }
  }
  for (int i=0; i<10000; i++) {
    int kostenOld=kostenfunktion(sudokuRandomWalk);
    int x = int(random(n));
    int y = int(random(n));
    int num = int(random(n));
    sudokuRandomWalk[x][y][num]=!sudokuRandomWalk[x][y][num];
    kostenDifferenzen.add(kostenOld-kostenfunktion(sudokuRandomWalk));
  }
  Collections.sort(kostenDifferenzen);
  return kostenDifferenzen.get(9900);
}

void exportiereAusgangsPosition() {
  String [] export=new String[n*n];
  for (int y=0; y<n; y++) {
    export[y]="";
    for (int x=0; x<n; x++) {
      int besetztesFeld=0;
      for (int num=0; num<n; num++) {
        if (ausgangsposition[x][y][num]) {
          besetztesFeld=num+1;
        }
      }
      export[x]+=besetztesFeld;
    }
  }
  saveStrings("ausgangsLösung_" + n+".txt", export);
}

void exportiereGraph(ArrayList <String> listToWrite, String algo) {
  String[]graphWrite= new String[listToWrite.size()];
  for (int i=0; i<listToWrite.size(); i++) {
    graphWrite[i]=listToWrite.get(i);
  }
  saveStrings("Graph_"+n+"_"+algo+"ausgangs.txt", graphWrite);
}
