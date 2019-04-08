String[]matrixString;
int[][]matrixInt;
int[] loesung;
int n;

void setup() {
  matrixString=loadStrings("qubomatrix.txt");
  noLoop();
}


void draw() {

  matrixInt=new int[matrixString.length][matrixString.length];
  for (int i=0; i<matrixString.length; i++) {
    String[] matrixReihe=new String[matrixString.length];
    matrixReihe=matrixString[i].split(" ");
    for (int j=0; j<matrixString.length; j++) {
      matrixInt[i][j]=int(matrixReihe[j]);
    }
  }
  n=matrixInt.length;
  loesung = new int[n];
  simulatedAnnealing();
  println();
  for (int i=0; i<n; i++) {
    print(loesung[i]+" ");
  }
}

int kostenfunktion(int[]vektor) {
  int ergebnis=0;
  int[] vektorerg=new int[vektor.length];

  for (int i=0; i<vektor.length; i++) {
    for (int j=0; j<vektor.length; j++) {
      vektorerg[i]+=matrixInt[i][j]*vektor[j];
    }
  }

  for (int i=0; i<vektor.length; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}

void simulatedAnnealing() {
  float simAnn=700;
  for (int durchlauf=0; durchlauf<100000; durchlauf++) {
    int alteKosten = kostenfunktion(loesung);
    int x = int(random(n));
    loesung[x]=loesung[x]==1?0:1;
    int kosten = kostenfunktion(loesung);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      loesung[x]=loesung[x]==1?0:1;
    }

    simAnn*=0.9; //0.99
  }
  println("Kosten: "+kostenfunktion(loesung));
}
