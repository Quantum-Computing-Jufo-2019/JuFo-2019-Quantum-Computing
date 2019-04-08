import java.util.*; //<>//

int n = 4;
boolean diagonaleFrei = true;
boolean[][] schachfeld = new boolean[n][n];
boolean[][] ausgangsposition = new boolean[n][n];
int[][] hamiltonianMatrix = new int[n*n][n*n];
ArrayList <Summand> hamiltonianTerm = new ArrayList<Summand>();
ArrayList<String> greedyGraph = new ArrayList<String>();
ArrayList<String> simAnnGraph = new ArrayList<String>();
ArrayList<String> thresholdGraph = new ArrayList<String>();
ArrayList<String> greatDelugeGraph = new ArrayList<String>();

//char[] alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'};


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
  erstelleHamiltonianMatrix(hamiltonianTerm);
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
  greedy();
  exportiereGraph(greedyGraph, "greedy");
  println();

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=ausgangsposition[i][j];
    }
  }
  simulatedAnnealing();  
  exportiereGraph(simAnnGraph, "simAnn");
  println();

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=ausgangsposition[i][j];
    }
  }

  greatDeluge();
  exportiereGraph(greatDelugeGraph, "greatDeluge");
  println();

  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=ausgangsposition[i][j];
    }
  }
  thresholdAccepting();  
  exportiereGraph(thresholdGraph, "threshold");
}



void hamiltonianTermAufstellen() {
  int hoechstwert;

  if (diagonaleFrei) {
    hoechstwert=n-1;
    //Gesamtdiagonale rechts oben nach links unten
    {   
      ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
      for (int x=n, y=1; y<=n; x--, y++) {
        hamiltonianTerm.add(new Summand(+1, new PVector(x, y), new PVector(x, y)));
        hamiltonianTermIntern.add(new PVector(x, y));
      }    
      ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAufDiagonal(hamiltonianTermIntern);
      for (Summand s : hamiltonianTermInternAusmult) {
        hamiltonianTerm.add(s);
      }
    }
    //Gesamtdiagonale links oben nach rechts unten
    {   
      ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
      for (int x=1; x<=n; x++) {
        hamiltonianTermIntern.add(new PVector(x, x));
        hamiltonianTerm.add(new Summand(+1, new PVector(x, x), new PVector(x, x)));
      }
      ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAufDiagonal(hamiltonianTermIntern);
      for (Summand s : hamiltonianTermInternAusmult) {
        hamiltonianTerm.add(s);
      }
    }
  } else {
    hoechstwert=n;
  }

  //Diagonalen untere Hälfte (Ecke unten rechts; von rechts oben nach links unten) ohne Gesamtdiagonale
  for (int i = 1; i <= n-1; i++) {
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int x = i, y = n, j = 1; (x >= 1 || y >= 1) && j <= i; x--, y--, j++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAufDiagonal(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  } 


  //Diagonalen obere Hälfte (Ecke oben links; von rechts oben nach links unten)
  for (int i=hoechstwert; i>=1; i--) {
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int x=n, y=i, j=1; (x>=1||y>=1)&&j<=i; x--, y--, j++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAufDiagonal(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  }

  //diagonal obere hälfte links oben nach rechts unten ohne diagonale
  for (int i=1; i<=n-1; i++) {//i<n
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int x=1, y=i, j=1; (x<=n||y>=1)&&j<=i; x++, y--, j++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult = loeseKlammernAufDiagonal(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  }


  //diagonal untere hälfte links oben nach rechts unten
  for (int abbruch=hoechstwert, i=1; abbruch>=1||i<=n; abbruch--, i++) {
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int x=i, y=n, j=1; (x<=n||y>=1)&&j<=abbruch; x++, y--, j++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAufDiagonal(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  }

  //oben nach unten (y)
  for (int x=1; x<=n; x++) {
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int y=1; y<=n; y++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAuf(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  }

  //links nach rechts (x)
  for (int y=1; y<=n; y++) {
    ArrayList <PVector> hamiltonianTermIntern = new ArrayList<PVector>();
    for (int x=1; x<=n; x++) {
      hamiltonianTermIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> hamiltonianTermInternAusmult=loeseKlammernAuf(hamiltonianTermIntern);
    for (Summand s : hamiltonianTermInternAusmult) {
      hamiltonianTerm.add(s);
    }
  }
}



ArrayList <Summand> loeseKlammernAuf(ArrayList <PVector> hamiltonianTerm) {
  ArrayList <Summand> result = new ArrayList<Summand>();
  for (int i=0; i<hamiltonianTerm.size(); i++) {
    for (int j=i+1; j<hamiltonianTerm.size(); j++) {
      result.add(new Summand(+2, hamiltonianTerm.get(i), hamiltonianTerm.get(j)));//+="+ 2* s["+hamiltonianTerm.get(i).x+"]["+hamiltonianTerm.get(i).y+"]" + " * s["+hamiltonianTerm.get(j).x+"]["+hamiltonianTerm.get(j).y+"]";
    }
  }
  for (PVector p : hamiltonianTerm) {
    result.add(new Summand(-1, p, p));//+="-s["+p.x+"]["+p.y+"]";
  }
  return result;
}



ArrayList <Summand> loeseKlammernAufDiagonal(ArrayList <PVector> hamiltonianTerm) {
  ArrayList <Summand> result = new ArrayList<Summand>();
  for (int i=0; i<hamiltonianTerm.size(); i++) {
    for (int j=i+1; j<hamiltonianTerm.size(); j++) {
      result.add(new Summand(+2, hamiltonianTerm.get(i), hamiltonianTerm.get(j)));//+="+ 2* s["+hamiltonianTerm.get(i).x+"]["+hamiltonianTerm.get(i).y+"]" + " * s["+hamiltonianTerm.get(j).x+"]["+hamiltonianTerm.get(j).y+"]";
    }
  }

  return result;
}


void erstelleHamiltonianMatrix(ArrayList <Summand> hamiltonianTerm) {
  for (int i=0; i<hamiltonianTerm.size(); i++) {
    if  ( ((int(hamiltonianTerm.get(i).feld1.x)-1)+(int(hamiltonianTerm.get(i).feld1.y)-1)*n) < ((int(hamiltonianTerm.get(i).feld2.x)-1)+(int(hamiltonianTerm.get(i).feld2.y)-1)*n)) {
      hamiltonianMatrix[(int(hamiltonianTerm.get(i).feld1.x)-1)+(int(hamiltonianTerm.get(i).feld1.y)-1)*n][(int(hamiltonianTerm.get(i).feld2.x)-1)+(int(hamiltonianTerm.get(i).feld2.y)-1)*n]+=hamiltonianTerm.get(i).multiplikator;
    } else {
      hamiltonianMatrix[(int(hamiltonianTerm.get(i).feld2.x)-1)+(int(hamiltonianTerm.get(i).feld2.y)-1)*n][(int(hamiltonianTerm.get(i).feld1.x)-1)+(int(hamiltonianTerm.get(i).feld1.y)-1)*n] +=hamiltonianTerm.get(i).multiplikator;
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



void greedy() {
  println("greedy:");

  for (int durchlauf=0; durchlauf<100000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    zeichneGraph(durchlauf, alteKosten, color(0, 255, 0));
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten=kostenfunktion(schachfeld);
    if (kosten>alteKosten) {
      schachfeld[x][y]=!schachfeld[x][y];
    }    
    greedyGraph.add(durchlauf+" "+kostenfunktion(schachfeld));
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");      
      break;//exit();
    }
  }
  maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}



void thresholdAccepting() {
  println("threshold:");
  float threshold=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<10000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten=kostenfunktion(schachfeld);

    if ((kosten - alteKosten)>=threshold) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    thresholdGraph.add(durchlauf+" "+kostenfunktion(schachfeld));
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");
      println("threshold Schwelle: "+threshold);
      break;//exit();
    }
    threshold*=0.99; //0.95
  }
  maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}

void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<100000000; durchlauf++) {
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
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");
      println("simAnn Schwelle: "+simAnn);
      break;
    }
    simAnn*=0.9; //0.95
  }
  maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}


void greatDeluge() {
  println("greatDeluge");
  boolean[][] schachfeldWorstCase = new boolean[n][n];
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeldWorstCase[i][j]=true;
    }
  }
  float greatDeluge=kostenfunktion(schachfeldWorstCase);

  for (int durchlauf=0; durchlauf<100000000; durchlauf++) {
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten=kostenfunktion(schachfeld);

    if (kosten>greatDeluge) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    greatDelugeGraph.add(durchlauf+" "+kostenfunktion(schachfeld));
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");
      println("greatDeluge Schwelle: "+greatDeluge);
      break;//exit();
    }
    greatDeluge*=0.995;
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
  for (int x=0; x<n*n; x++) {
    export[x]="";
    for (int y=0; y<n*n; y++) {
      export[x]+=hamiltonianMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrix_" + n + "_" + (diagonaleFrei? ("diagonaletFrei") : ("diagonaleBesetzt")) + ".txt", export);
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
  saveStrings("Graph_"+n+"_"+(diagonaleFrei==true?("diagFrei"):("diagBesetzt"))+"_"+algo+".txt", graphWrite);
}
