import java.util.*; //<>//
//TODO: Werte kommas statt punkte; Testen für n=8   ggf. Bei eigener Kostenfunktion +n*2 schreiben damit Grafik schöner ist
int n = 7;
boolean diagonaleFrei = false;
boolean[][] schachfeld = new boolean[n][n];
boolean[][] ausgangsposition = new boolean[n][n];
int[][] hamiltonianMatrix = new int[n*n][n*n];
int[][] initialMatrix = new int[n*n][n*n];
ArrayList <Summand> hamiltonianTerm = new ArrayList<Summand>();
ArrayList<String> simAnnGraph = new ArrayList<String>();
ArrayList<Float> aWerte = new ArrayList<Float>();
ArrayList<Float> bWerte = new ArrayList<Float>();
ArrayList<ArrayList> energien=new ArrayList<ArrayList>();


void setup() {
  //String []ausgangsl=loadStrings("ausgangsLösung_8.txt");
  for (int i=0; i<n; i++) {
    //String[]t=ausgangsl[i].split(" ");
    for (int j=0; j<n; j++) {
      //ausgangsposition[i][j] = (int(t[j])==1?true:false);//int(random(0, 2)) == 1
      ausgangsposition[i][j] = int(random(0, 2)) == 1;//
    }
  }
  aWerte.add(6.0);
  aWerte.add(3.1);
  aWerte.add(1.2);
  aWerte.add(0.2);
  aWerte.add(0.0);
  aWerte.add(0.0);
  bWerte.add(0.3);
  bWerte.add(1.7);
  bWerte.add(3.4);
  bWerte.add(5.8);
  bWerte.add(8.4);
  bWerte.add(12.0);
  try {
    String[]local= new String[1];
    local[0]="Diese Datei wird noch geschrieben...";
    saveStrings("energien.txt", local);
  }
  catch(NullPointerException e) {
    println("Die Datei \"energien.txt\" ist noch geöffnet! Bitte schließen!");
    exit();
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
  exportiereEnergien();
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
            hamiltonianMatrix[min(n*x1+y1, n*x2+y2)][max(n*x1+y1, n*x2+y2)] += 1;
          }
        }
      }
    }
  }
}

void initialHamiltonianAufstellen() {
  for (int x1 =0; x1<n; x1++) {
    for (int y1 =0; y1<n; y1++) {
      for (int x2 =0; x2<n; x2++) {
        for (int y2 =0; y2<n; y2++) {
          if (x1 == x2 && y1 == y2) {
            initialMatrix[n*x1+y1][n*x1+y1] = -15;
          }
          initialMatrix[min(n*x1+y1, n*x2+y2)][max(n*x1+y1, n*x2+y2)] += 2;
        }
      }
    }
  }
}


int kostenfunktion(boolean[][]schachfeldLocal, int[][]matrix) {
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
      vektorerg[i]+=matrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}


//in jedem Durchlauf werte speichern
void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();
  float a=aWerte.get(0);
  float b=bWerte.get(0);

  for (int durchlaufGesamt=0; durchlaufGesamt<aWerte.size()-1; durchlaufGesamt++) {
    for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
        schachfeld[i][j]=ausgangsposition[i][j];
      }
    }
    ArrayList<Float> localEnergies=new ArrayList<Float>();
    for (int durchlauf=0; durchlauf<700000; durchlauf++) {
      float alteKosten = ((kostenfunktion(schachfeld, initialMatrix))*a+(kostenfunktion(schachfeld, hamiltonianMatrix))*b);
      int x = int(random(n));
      int y = int(random(n));
      schachfeld[x][y]=!schachfeld[x][y];
      float kosten = ((kostenfunktion(schachfeld, initialMatrix))*a+(kostenfunktion(schachfeld, hamiltonianMatrix))*b);
      float kostenUnterschied=kosten-alteKosten;
      //((kostenfunktion(schachfeld, initialMatrix))*a+(kostenfunktion(schachfeld, hamiltonianMatrix))*b)
      if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
        schachfeld[x][y]=!schachfeld[x][y];
      }
      
      if (localEnergies.size()!=0) {
        boolean check=false;
        for (float k : localEnergies) {
          if (k==kosten) {
            check=true;
            break;
          }
        }
        if (!check) {
          localEnergies.add(kosten);
        }
      } else {
        localEnergies.add(kosten);
      }
      //simAnnGraph.add(durchlauf+" "+((kostenfunktion(schachfeld, initialMatrix))*a+(kostenfunktion(schachfeld, hamiltonianMatrix))*b)));
      //if (kosten==n*(-2) ) {
      //  println(durchlauf+" Durchläufe");
      //  println("simAnn Schwelle: "+simAnn);
      //  break;
      //}
      simAnn*=0.995; //0.95
    }
    Collections.sort(localEnergies);
    ArrayList<Float>localEnergies2=new ArrayList<Float>();
    for (int i=0; i<10&&i<localEnergies.size(); i++) {
      localEnergies2.add(localEnergies.get(i));
      println(localEnergies.get(i));
    }
    energien.add(localEnergies2);
    maleSchachfeld(schachfeld);
    println(a+"  "+b);
    println("Kosten: "+(((kostenfunktion(schachfeld, initialMatrix))*a+(kostenfunktion(schachfeld, hamiltonianMatrix))*b)));
    a=aWerte.get(durchlaufGesamt+1);    
    b=bWerte.get(durchlaufGesamt+1);
  }
  maleSchachfeld(schachfeld);
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

int randomWalkTreshold() {
  ArrayList<Integer> kostenDifferenzen=new ArrayList<Integer>();
  boolean[][] schachfeldRandomWalk = new boolean[n][n];
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeldRandomWalk[i][j]=true;
    }
  }
  for (int i=0; i<10000; i++) {
    int kostenOld=kostenfunktion(schachfeldRandomWalk, hamiltonianMatrix);
    int x = int(random(n));
    int y = int(random(n));
    schachfeldRandomWalk[x][y]=!schachfeldRandomWalk[x][y];
    kostenDifferenzen.add(kostenOld-kostenfunktion(schachfeldRandomWalk, hamiltonianMatrix));
  }
  Collections.sort(kostenDifferenzen);
  return kostenDifferenzen.get(9900);
}

void exportiereEnergien() {
  String[]toWrite=new String[energien.size()];
  for (int i=0; i<energien.size(); i++) {
    String toWrite2="";
    for (int j=0; j<energien.get(i).size(); j++) {
      toWrite2+=energien.get(i).get(j)+"0 ";
    }
    toWrite2=toWrite2.replace(".", ",");
    toWrite[i]=toWrite2;
  }
  saveStrings("energien.txt", toWrite);
}

void exportiereGraph(ArrayList <String> listToWrite, String algo) {
  String[]graphWrite= new String[listToWrite.size()];
  for (int i=0; i<listToWrite.size(); i++) {
    graphWrite[i]=listToWrite.get(i);
  }
  saveStrings("Graph_"+n+"_"+(diagonaleFrei==true?("diagFrei"):("diagBesetzt"))+"_"+algo+"ausgangs.txt", graphWrite);
}
