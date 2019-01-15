int n = 3;
boolean[][][] schachfeld = new boolean[n*n][n][n];
int[][] hamiltonianMatrix = new int[n*n*n*n][n*n*n*n];
ArrayList<String> simAnnGraph = new ArrayList<String>();

void setup() {
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        schachfeld[l][i][j] = int(random(0, 2)) == 1;
      }
    }
  }
  noLoop();
}



void draw() {

  hamiltonianTermAufstellen();

  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<n*n*n*n; i++) {
    for (int j=0; j<n*n*n*n; j++) {
      if (hamiltonianMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonianMatrix[i][j]);
    }
    println();
  }
  println("ausgangslösung:");
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        if (schachfeld[l][i][j]==true)
          println("<"+l+", "+i+", "+j+">");
      }
    }
  }
  exportiereHamiltonianMatrix();
  simulatedAnnealing();  
  exportiereGraph(simAnnGraph, "simAnn");
  println();
}



void hamiltonianTermAufstellen() {
  for (int l=0; l<n*n; l++) {
    for (int x=0; x<n; x++) {
      for (int y=0; y<n; y++) {
        for (int m=0; m<n*n; m++) {
          for (int a=0; a<n; a++) {
            for (int b=0; b<n; b++) {
              int i = l*n*n+y*n+x;
              int j = m*n*n+b*n+a;
              //übereinander keine Springer
              if (x==a && y==b && m!=l) {
                hamiltonianMatrix[(i<=j)?i:j][(i<=j)?j:i]+=2;
              }
              //auf der feldebene keine springer
              if (l==m && !(x==a && y==b)) {
                hamiltonianMatrix[(i<=j)?i:j][(i<=j)?j:i]+=1;
              }
              if (abs(l-m)==1) {
                if (abs(x-a)*abs(b-y)==2) {
                  hamiltonianMatrix[(i<=j)?i:j][(i<=j)?j:i]-=1;
                } else {
                  hamiltonianMatrix[(i<=j)?i:j][(i<=j)?j:i]+=1;
                }
              }
            }
          }
        }
      }
    }
  }
}


int kostenfunktion(boolean[][][]schachfeldLocal) {
  int ergebnis=0;
  int[] vektor=new int[n*n*n*n];
  int[] vektorerg=new int[n*n*n*n];

  for (int l=0; l<n*n; l++) {
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        vektor[l*n*n+i*n+j]=schachfeldLocal[l][i][j]==true? (1):(0);
      }
    }
  }

  for (int i=0; i<n*n*n*n; i++) {
    for (int j=0; j<n*n*n*n; j++) {
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n*n*n; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}


void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=kostenfunktion(schachfeld)-5;

  for (int durchlauf=0; durchlauf<50000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    if (durchlauf%100==0) {
      print("#");
    }
    if (durchlauf%10000==0) {
      println();
      println(alteKosten);
      maleSchachfeld(schachfeld);
      println();
    }

    int x = int(random(n));
    int y = int(random(n));
    int l = int(random(n*n));
    schachfeld[l][x][y]=!schachfeld[l][x][y];
    int kosten = kostenfunktion(schachfeld);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>=0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      schachfeld[l][x][y]=!schachfeld[l][x][y];
    }
    simAnnGraph.add(durchlauf+" "+kostenfunktion(schachfeld));
    //if (kosten==n*(-2) ) {
    //  println(durchlauf+" Durchläufe");
    //  println("simAnn Schwelle: "+simAnn);
    //  break;
    //}
    simAnn*=0.99999; //0.95
  }
  
  maleSchachfeld(schachfeld);
  println("simAnn: "+simAnn);
  println("Kosten: "+kostenfunktion(schachfeld));
}


void maleSchachfeld(boolean[][][] schachfeldLocal) {
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        if (schachfeldLocal[l][i][j]==true)
          println("<"+l+", "+i+", "+j+">");
      }
    }
  }
}

void exportiereGraph(ArrayList <String> listToWrite, String algo) {
  String[]graphWrite= new String[listToWrite.size()];
  for (int i=0; i<listToWrite.size(); i++) {
    graphWrite[i]=listToWrite.get(i);
  }
  saveStrings("Graphroesslesprung_"+n+"_"+algo+".txt", graphWrite);
}

void exportiereHamiltonianMatrix() {
  String [] export=new String[n*n*n*n];
  for (int x=0; x<n*n*n*n; x++) {
    export[x]="";
    for (int y=0; y<n*n*n*n; y++) {
      export[x]+=hamiltonianMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrixroesslesprung_" + n +".txt", export);
}