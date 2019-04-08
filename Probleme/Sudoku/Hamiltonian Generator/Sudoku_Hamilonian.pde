// TODO: for schleifen überarbeiten: n ersetzen durch nxnxn oder nxn/3
//       Matrix einfüllen: bisher nur die Bestrafungsbedingungen

import java.util.*;

int n = 9;
boolean[][] sudoku = new boolean[n*n/3][n*n/3];
boolean[][] ausgangsposition = new boolean[n*n/3][n*n/3];
int[][] hamiltonianMatrix = new int[n*n*n][n*n*n];
ArrayList<String> simAnnGraph = new ArrayList<String>();

void setup() {
  for (int i=0; i<n*n/3; i++) {
    for (int j=0; j<n*n/3; j++) {
      ausgangsposition[i][j] = int(random(0, 2)) == 1;//
    }
  }
  noLoop();
}



void draw() {

  hamiltonianTermAufstellen();

  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<n*n*n; i++) {
    for (int j=0; j<n*n*n; j++) {
      if (hamiltonianMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonianMatrix[i][j]);
    }
    println();
  }
  exportiereHamiltonianMatrix();
  //exportiereAusgangsPosition();
  println("Hamiltonian-Matrix exportiert!");
  println("ausgangslösung:");
  for (int i=0; i<n*n/3; i++) {
    for (int j=0; j<n*n/3; j++) {
      print((ausgangsposition[i][j]?1:0));
      print(" ");
    }
    println();
  }


  for (int i=0; i<n*n/3; i++) {
    for (int j=0; j<n*n/3; j++) {
      sudoku[i][j]=ausgangsposition[i][j];
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
              //pro Spalte jede Zahl nur einmal
              if (x1==x2&&num1==num2) {
              }
              //pro Zeile jede Zahl nur einmal
              if (y1==y2&&num1==num2) {
              }
              //pro zelle nur eine Zahl
              if ((x1==x2&&y1==y2)&&num1!=num2) {
              }

              //pro 3x3 Feld nur eine Zahl
              if ((int(x1/3)==int(x2/3)&&int(y1/3)==int(y2/3))&&num1==num2) {
              }
            }
          }
        }
      }
    }
  }
}



int kostenfunktion(boolean[][]sudokuLocal) {
  int ergebnis=0;
  int[] vektor=new int[n*n*n];
  int[] vektorerg=new int[n*n*n];

  for (int i=0; i<n*n/3; i++) {
    for (int j=0; j<n*n/3; j++) {
      vektor[i*n+j]=sudokuLocal[i][j]==true? (1):(0);
    }
  }  

  for (int i=0; i<n*n*n; i++) {
    for (int j=0; j<n*n*n; j++) {
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n*n; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}


void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<1000000; durchlauf++) {
    int alteKosten = kostenfunktion(sudoku);
    int x = int(random(n));
    int y = int(random(n));
    sudoku[x][y]=!sudoku[x][y];
    int kosten = kostenfunktion(sudoku);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      sudoku[x][y]=!sudoku[x][y];
    }
    simAnnGraph.add(durchlauf+" "+kostenfunktion(sudoku));
    //if (kosten==n*(-2) ) {
    //  println(durchlauf+" Durchläufe");
    //  println("simAnn Schwelle: "+simAnn);
    //  break;
    //}
    simAnn*=0.99; //0.95
  }
  malesudoku(sudoku);
  println("Kosten: "+kostenfunktion(sudoku));
}

void malesudoku(boolean[][] sudokuLocal) {
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      print(" ");
      print(sudokuLocal[i][j]?(1):(0));
    }
    println();
  }
}


void exportiereHamiltonianMatrix() {
  String [] export=new String[n*n];
  for (int x=0; x<n*n; x++) {
    export[x]="";
    for (int y=0; y<n*n; y++) {
      export[x]+=hamiltonianMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrix_" + n  + ".txt", export);
}


int randomWalkTreshold() {
  ArrayList<Integer> kostenDifferenzen=new ArrayList<Integer>();
  boolean[][] sudokuRandomWalk = new boolean[n][n];
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      sudokuRandomWalk[i][j]=true;
    }
  }
  for (int i=0; i<10000; i++) {
    int kostenOld=kostenfunktion(sudokuRandomWalk);
    int x = int(random(n));
    int y = int(random(n));
    sudokuRandomWalk[x][y]=!sudokuRandomWalk[x][y];
    kostenDifferenzen.add(kostenOld-kostenfunktion(sudokuRandomWalk));
  }
  Collections.sort(kostenDifferenzen);
  return kostenDifferenzen.get(9900);
}

void exportiereAusgangsPosition() {
  String [] export=new String[n];
  for (int x=0; x<n; x++) {
    export[x]="";
    for (int y=0; y<n; y++) {
      export[x]+=(ausgangsposition[x][y]?1:0)+" ";
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
