int n = 4;
ArrayList<PVector>points=new ArrayList<PVector>();
boolean[][]feld=new boolean[n][n];
void setup() {
  points.add(new PVector(1, 1));
  points.add(new PVector(1, 3));
  points.add(new PVector(2, 2));
  points.add(new PVector(2, 1));
  printHamiltonMatrix(createHamiltonMatrix(points));
  simulatedAnnealing(createHamiltonMatrix(points));
}

void draw() {
}

float[][] createHamiltonMatrix(ArrayList<PVector>points) {
  float[][]matrix = new float[n*n][n*n];
  float longestDistance=getlongestDistance(points);
  for (int i=0; i<matrix.length; i++) {
    for (int t=0; t<matrix.length; t++) {
      if (t<i)matrix[i][t]=0;
      else if (i==t)matrix[i][t]=-longestDistance;
      else if ((t>int(i/n)*n&&t<int(i/n)*n+n)||(i%n==t%n))matrix[i][t]=longestDistance;
      else if ((i%n!=n-1&&t%n-i%n==1)||(i%n==n-1&&t%n-i%n==-n+1))matrix[i][t]=dist(points.get(int(i/n)).x, points.get(int(i/n)).y, points.get(int(t/n)).x, points.get(int(t/n)).y);
      else matrix[i][t]=0;
    }
  }
  return matrix;
}

void printHamiltonMatrix(float[][]matrix) {
  for (int i=0; i<n*n; i++) {
    for (int j=0; j<n*n; j++) {
      if (matrix[i][j] >= 0)
        print(" ");
      print(matrix[i][j]);
    }
    println();
  }
}

float getlongestDistance(ArrayList<PVector>points) {
  float longestDistance=0;
  for (int i=0; i<points.size(); i++) {
    for (int t=0; t<points.size(); t++) {
      float distance = dist(points.get(i).x, points.get(i).y, points.get(t).x, points.get(t).y);
      longestDistance=longestDistance<distance?distance:longestDistance;
    }
  }
  return longestDistance;
}

void exportMatrix(int[][]matrix) {
}

int kostenfunktion(boolean[][]schachfeldLocal,float[][]matrix) {
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

void simulatedAnnealing(float [][]matrix) {
  println("simAnn:");
  float simAnn=100;

  for (int durchlauf=0; durchlauf<10000000; durchlauf++) {
    int alteKosten = kostenfunktion(feld,matrix);
    int x = int(random(n));
    int y = int(random(n));
    feld[x][y]=!feld[x][y];
    int kosten = kostenfunktion(feld,matrix);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      feld[x][y]=!feld[x][y];
    }
    if(durchlauf % 10000==0)
    simAnn*=0.99; //0.95
  }
  maleSchachfeld(feld);
  println("Kosten: "+kostenfunktion(feld,matrix));
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
