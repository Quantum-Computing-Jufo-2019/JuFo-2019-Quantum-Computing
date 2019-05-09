import java.util.*; //<>//
int queenXPosition=7;
int n = 8;
boolean diagonaleFrei = false;
boolean[][] schachfeld = new boolean[n-1][n-1];
boolean[][] ausgangsposition = new boolean[n-1][n-1];
int[][] hamiltonianMatrix = new int[n*n][n*n];



void setup() {
  //String []ausgangsl=loadStrings("ausgangsLösung_8.txt");
  for (int i=0; i<n-1; i++) {
    //String[]t=ausgangsl[i].split(" ");
    for (int j=0; j<n-1; j++) {
      //ausgangsposition[i][j] = (int(t[j])==1?true:false);//int(random(0, 2)) == 1
      ausgangsposition[i][j] = int(random(0, 2)) == 1;//
    }
  }
  noLoop();
}



void draw() {

  hamiltonianTermAufstellen();
  hamiltonianMatrix=veraendereHamiltonian(queenXPosition);
  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<hamiltonianMatrix.length; i++) {
    for (int j=0; j<hamiltonianMatrix.length; j++) {
      if (hamiltonianMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonianMatrix[i][j]);
    }
    println();
  }
  println(hamiltonianMatrix.length+" ggg");
  exportiereHamiltonianMatrix();
  //exportiereAusgangsPosition();
  println("Hamiltonian-Matrix exportiert!");
  println("ausgangslösung:");
  for (int i=0; i<n-1; i++) {
    for (int j=0; j<n-1; j++) {
      print((ausgangsposition[i][j]?1:0));
      print(" ");
    }
    println();
  }


  for (int i=0; i<n-1; i++) {
    for (int j=0; j<n-2; j++) {
      schachfeld[i][j]=ausgangsposition[i][j];
    }
  }
  simulatedAnnealing();  
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
        }
      }
    }
  }
}

int[][] veraendereHamiltonian(int queenXPosition) {
  ArrayList<Integer> deletableFields= new ArrayList<Integer>();
  ArrayList<Integer> punishableFields= new ArrayList<Integer>();
  for (int i=n; i<n*n; i++) {
    if (i%n==queenXPosition) {
      deletableFields.add(i);
    } else if ((i%(n+1)==queenXPosition%(n+1)&&i%n>queenXPosition)||(i%(n-1)==queenXPosition%(n-1)&&i%n<queenXPosition)) {//||i%(n-1)==queenXPosition%(n-1)
      punishableFields.add(i);
    }
  }
  for (int i=0; i<n; i++) {
    deletableFields.add(i);
  }
  println("Anzahl deletableFields: "+deletableFields.size());

  for (int i=0; i<n*n; i++) {
    if (punishableFields.contains(i)) {
      hamiltonianMatrix[i][i]=2;
    }
  }
  ArrayList<ArrayList> arrayListMatrix=convertArrayToArrayList(hamiltonianMatrix);
  //Zeilen löschen
  for (int i=n*n-1; i>=0; i--) {
    if (deletableFields.contains(i)) {
      arrayListMatrix.remove(i);
    }
  }

  //spalten löschen
  for (int i=n*n-1; i>=0; i--) {
    if (deletableFields.contains(i)) {
      for (int t=arrayListMatrix.size()-1; t>=0; t--) {
        arrayListMatrix.get(t).remove(i);
      }
    }
  }

  int[][] arrayMatrix=new int[arrayListMatrix.size()][arrayListMatrix.size()];
  for (int i=0; i<arrayListMatrix.size(); i++) {
    for (int t=0; t<arrayListMatrix.size(); t++) {
      arrayMatrix[i][t]=int(arrayListMatrix.get(i).get(t)+"");
    }
  }
  return arrayMatrix;
}

ArrayList<ArrayList> convertArrayToArrayList(int[][] array) {
  ArrayList<ArrayList> tList=new ArrayList<ArrayList>();
  for (int i=0; i<array.length; i++) {
    tList.add(new ArrayList<Integer>());
    for (int t=0; t<array.length; t++) {
      tList.get(i).add(array[i][t]);
    }
  }
  return tList;
}

int kostenfunktion(boolean[][]schachfeldLocal) {
  int ergebnis=0;
  int[] vektor=new int[(n-1)*(n-1)];
  int[] vektorerg=new int[(n-1)*(n-1)];

  for (int i=0; i<n-1; i++) {
    for (int j=0; j<n-1; j++) {
      vektor[i*(n-1)+j]=schachfeldLocal[i][j]==true? (1):(0);
    }
  }  

  for (int i=0; i<hamiltonianMatrix.length; i++) {
    for (int j=0; j<hamiltonianMatrix.length; j++) {
      vektorerg[i]+=hamiltonianMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<(n-1)*(n-1); i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }
  return ergebnis;
}


void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();
  for (int durchlauf=0; durchlauf<10000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    int x = int(random(n-1));
    int y = int(random(n-1));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten = kostenfunktion(schachfeld);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    if (kosten==(n-1)*(-2)) {//
      println(durchlauf+" Durchläufe");
      println("simAnn Schwelle: "+simAnn);
      break;
    }
    if (durchlauf%10000==0)
      simAnn*=0.99; //0.95
  }
  maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}



void maleSchachfeld(boolean[][] schachfeldLocal) {
  for (int i=0; i<n-1; i++) {
    for (int j=0; j<n-1; j++) {
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
    int kostenOld=kostenfunktion(schachfeldRandomWalk);
    int x = int(random(n));
    int y = int(random(n));
    schachfeldRandomWalk[x][y]=!schachfeldRandomWalk[x][y];
    kostenDifferenzen.add(kostenOld-kostenfunktion(schachfeldRandomWalk));
  }
  Collections.sort(kostenDifferenzen);
  return kostenDifferenzen.get(9900);
}

void zeichneGraph(int x, int y, color farbe) {
  fill(farbe);
  noStroke();
  ellipse(10+displayWidth/1600*(int(x/5)), displayHeight/3+-(displayHeight/300*y), 3, 3);
}

void exportiereHamiltonianMatrix() {
  String [] export=new String[n*n];
  for (int x=0; x<hamiltonianMatrix.length; x++) {
    export[x]="";
    for (int y=0; y<hamiltonianMatrix.length; y++) {
      export[x]+=hamiltonianMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrix_" + n + "_"+ (queenXPosition+1) + "vorgegeben.txt", export);
}
