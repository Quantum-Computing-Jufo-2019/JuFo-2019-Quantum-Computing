import java.util.*; //<>//

int n = 8;
boolean[][] schachfeld = new boolean[n][n];
boolean[][] ausgangsposition = new boolean[n][n];
int[][] hamiltonianMatrix = new int[n*n][n*n];
ArrayList<String> simAnnGraph = new ArrayList<String>();

void setup() {
  //String []ausgangsl=loadStrings("ausgangsLösung_8.txt");
  for (int i=0; i<n; i++) {
    //String[]t=ausgangsl[i].split(" ");
    for (int j=0; j<n; j++) {
      //ausgangsposition[i][j] = (int(t[j])==1?true:false);//int(random(0, 2)) == 1
      ausgangsposition[i][j] = int(random(0, 2)) == 1;//
    }
  }
  noLoop();
}



void draw() {

  hamiltonianTermAufstellen();

  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<n*n; i++) {
    for (int j=0; j<n*n; j++) {
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
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      print((ausgangsposition[i][j]?1:0));
      print(" ");
    }
    println();
  }


  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=ausgangsposition[i][j];
    }
  }
  simulatedAnnealing();  
  exportiereGraph(simAnnGraph, "simAnn");
  println();
}



void hamiltonianTermAufstellen() {
  for (int x1 =0; x1<n; x1++) {
    for (int y1 =0; y1<n; y1++) {
      for (int x2 =0; x2<n; x2++) {
        for (int y2 =0; y2<n; y2++) {
          if (x1 == x2 && y1 == y2) {
            hamiltonianMatrix[n*x1+y1][n*x1+y1] = -2;
          } else if (x1 == x2 || y1 == y2 || abs(x1-x2) == abs(y1-y2)) {
            hamiltonianMatrix[min(n*x1+y1, n*x2+y2)][max(n*x1+y1, n*x2+y2)] = 2;
          }
          if (abs(x1-x2)*abs(y1-y2)==2) {
            hamiltonianMatrix[min(n*x1+y1, n*x2+y2)][max(n*x1+y1, n*x2+y2)]+=2;
          }
        }
      }
    }
  }
}





int kostenfunktion(boolean[][]schachfeldLocal) {
  int ergebnis=0;
  int[] vektor=new int[n*n];
  int[] vektorerg=new int[n*n];

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      vektor[i*n+j]=schachfeldLocal[i][j]==true? (1):(0);
    }
  }  

  for (int i=0; i<n*n; i++) {
    for (int j=0; j<n*n; j++) {
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}


void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<1000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten = kostenfunktion(schachfeld);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    simAnnGraph.add(durchlauf+" "+kostenfunktion(schachfeld));
    //if (kosten==n*(-2) ) {
    //  println(durchlauf+" Durchläufe");
    //  println("simAnn Schwelle: "+simAnn);
    //  break;
    //}
    simAnn*=0.99; //0.95
  }
  maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}

void maleSchachfeld(boolean[][] schachfeldLocal) {
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      print(" ");
      print(schachfeldLocal[i][j]?(1):(0));
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
  boolean[][] schachfeldRandomWalk = new boolean[n][n];
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeldRandomWalk[i][j]=true;
    }
  }
  for (int i=0; i<10000; i++) {
    int kostenOld=kostenfunktion(schachfeldRandomWalk);
    int x = int(random(n));
    int y = int(random(n));
    schachfeldRandomWalk[x][y]=!schachfeldRandomWalk[x][y];
    kostenDifferenzen.add(kostenOld-kostenfunktion(schachfeldRandomWalk));
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
