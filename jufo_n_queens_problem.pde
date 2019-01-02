/* //<>// //<>//
 TODO:
 -> Simulated annealing
 -> Graph mitteln
 */
import java.util.*;

int n=4;
boolean diagonaleFrei=true;
boolean[][] schachfeld = new boolean[n][n];
boolean[][] schachfeldUngeloest = new boolean[n][n];
int[][] matrix=new int[n*n][n*n];
//char[] alphabet={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'};
ArrayList <Summand> term = new ArrayList<Summand>();


void setup() {
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeldUngeloest[i][j]=int(random(0, 2))==1;
    }
  }
  size(60000, 450);
  noLoop();
}

void draw() {

  formelAufstellen();

  //formel ausgeben
  //for (int i=0; i<term.size(); i++) {
  //  Summand s=term.get(i);
  //  print("+"+s.multiplikator + "*" +alphabet[int((s.pvec1.x-1)*n+s.pvec1.y-1)]+"*"+alphabet[int((s.pvec2.x-1)*n+s.pvec2.y-1)]);
  //}
  println();
  println();
  //matrix ausgeben
  matrix(term);
  for (int i=0; i<n*n; i++) {
    for (int j=0; j<n*n; j++) {
      if (matrix[i][j]>=0)
        print(" ");
      print(matrix[i][j]);
    }
    println();
  }
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=schachfeldUngeloest[i][j];
    }
  }
  simulatedAnnealing();
  println();
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=schachfeldUngeloest[i][j];
    }
  }  
  greedy();
  println();
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=schachfeldUngeloest[i][j];
    }
  }
  thresholdAccepting();  
  println();
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeld[i][j]=schachfeldUngeloest[i][j];
    }
  }
  greatDeluge();

  //exit();
}

void formelAufstellen() {
  int hoechstwert;

  if (diagonaleFrei) {
    hoechstwert=n-1;
    //diagonale rechts oben nach links unten
    {   
      ArrayList <PVector> termIntern = new ArrayList<PVector>();
      for (int x=n, y=1; y<=n; x--, y++) {
        term.add(new Summand(+1, new PVector(x, y), new PVector(x, y)));
        termIntern.add(new PVector(x, y));
      }    
      ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
      for (Summand s : termInternAusmult) {
        term.add(s);
      }
    }
    //diagonale links oben nach rechts unten
    {   
      ArrayList <PVector> termIntern = new ArrayList<PVector>();
      for (int x=1; x<=n; x++) {
        termIntern.add(new PVector(x, x));
        term.add(new Summand(+1, new PVector(x, x), new PVector(x, x)));
      }
      ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
      for (Summand s : termInternAusmult) {
        term.add(s);
      }
    }
  } else {
    hoechstwert=n;
  }

  //diagonal untere hälfte rechts oben nach links unten ohne diagonale
  for (int i=1; i<=n-1; i++) {
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int x=i, y=n, j=1; (x>=1||y>=1)&&j<=i; x--, y--, j++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  } 


  //diagonal obere hälfte rechts oben nach links unten
  for (int i=hoechstwert; i>=1; i--) {
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int x=n, y=i, j=1; (x>=1||y>=1)&&j<=i; x--, y--, j++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  }

  //diagonal obere hälfte links oben nach rechts unten ohne diagonale
  for (int i=1; i<=n-1; i++) {//i<n
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int x=1, y=i, j=1; (x<=n||y>=1)&&j<=i; x++, y--, j++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  }



  //diagonal untere hälfte links oben nach rechts unten
  for (int abbruch=hoechstwert, i=2; abbruch>=1||i<=n; abbruch--, i++) {
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int x=i, y=n, j=1; (x<=n||y>=1)&&j<=abbruch; x++, y--, j++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAufDiagonal(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  }

  //oben nach unten
  for (int x=1; x<=n; x++) {
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int y=1; y<=n; y++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAuf(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  }

  //links nach rechts
  for (int y=1; y<=n; y++) {
    ArrayList <PVector> termIntern = new ArrayList<PVector>();
    for (int x=1; x<=n; x++) {
      termIntern.add(new PVector(x, y));
    }
    ArrayList <Summand> termInternAusmult=loeseKlammernAuf(termIntern);
    for (Summand s : termInternAusmult) {
      term.add(s);
    }
  }
}

ArrayList <Summand> loeseKlammernAuf(ArrayList <PVector> term) {
  ArrayList <Summand> result = new ArrayList<Summand>();
  for (int i=0; i<term.size(); i++) {
    for (int j=i+1; j<term.size(); j++) {
      result.add(new Summand(+2, term.get(i), term.get(j)));//+="+ 2* s["+term.get(i).x+"]["+term.get(i).y+"]" + " * s["+term.get(j).x+"]["+term.get(j).y+"]";
    }
  }
  for (PVector p : term) {
    result.add(new Summand(-1, p, p));//+="-s["+p.x+"]["+p.y+"]";
  }
  return result;
}

ArrayList <Summand> loeseKlammernAufDiagonal(ArrayList <PVector> term) {
  ArrayList <Summand> result = new ArrayList<Summand>();
  for (int i=0; i<term.size(); i++) {
    for (int j=i+1; j<term.size(); j++) {
      result.add(new Summand(+2, term.get(i), term.get(j)));//+="+ 2* s["+term.get(i).x+"]["+term.get(i).y+"]" + " * s["+term.get(j).x+"]["+term.get(j).y+"]";
    }
  }

  return result;
}

//ArrayList <Summand> loeseKlammernAufDiagonalN(ArrayList <PVector> term) {
//  ArrayList <Summand> result = new ArrayList<Summand>();
//  for (int i=0; i<term.size(); i++) {
//    for (int j=i+1; j<term.size(); j++) {
//      result.add(new Summand(+2, term.get(i), term.get(j)));//+="+ 2* s["+term.get(i).x+"]["+term.get(i).y+"]" + " * s["+term.get(j).x+"]["+term.get(j).y+"]";
//    }
//  }
//  for (PVector p : term) {
//    result.add(new Summand(+1, p, p));//+="-s["+p.x+"]["+p.y+"]";
//  }
//  return result;
//}

void matrix(ArrayList <Summand> term) {
  for (int i=0; i<term.size(); i++) {
    if  ( ((int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n) < ((int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n)) {
      matrix[(int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n][(int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n]+=term.get(i).multiplikator;
    } else {
      matrix[(int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n][(int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n] +=term.get(i).multiplikator;
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
      vektorerg[i]+=matrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n; i++) {
    ergebnis+=vektor[i]*vektorerg[i];
  }

  return ergebnis;
}



void greedy() {
  println("greedy:");

  for (int durchlauf=0; durchlauf<1000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    zeichneGraph(durchlauf, alteKosten, color(255, 0, 0));
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten=kostenfunktion(schachfeld);
    if (kosten>alteKosten) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");      
      break;//exit();
    }
  }
  //maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}



void thresholdAccepting() {
  println("threshold:");
  float threshold=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<10000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    zeichneGraph(durchlauf, alteKosten, color(0, 255, 0));
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten=kostenfunktion(schachfeld);

    if ((kosten - alteKosten)>=threshold) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");
      println("threshold Schwelle: "+threshold);
      break;//exit();
    }
    threshold*=0.99; //0.95
  }
  //maleSchachfeld(schachfeld);
  println("Kosten: "+kostenfunktion(schachfeld));
}

void simulatedAnnealing() {
  println("simAnn:");
  float simAnn=randomWalkTreshold();

  for (int durchlauf=0; durchlauf<100000000; durchlauf++) {
    int alteKosten = kostenfunktion(schachfeld);
    zeichneGraph(durchlauf, alteKosten, color(50, 50, 50));
    int x = int(random(n));
    int y = int(random(n));
    schachfeld[x][y]=!schachfeld[x][y];
    int kosten = kostenfunktion(schachfeld);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
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
    zeichneGraph(durchlauf, kosten, color(0, 0, 255));

    if (kosten>greatDeluge) {
      schachfeld[x][y]=!schachfeld[x][y];
    }
    if (kosten==n*(-2) ) {
      println(durchlauf+" Durchläufe");
      println("greatDeluge Schwelle: "+greatDeluge);
      break;//exit();
    }
    greatDeluge*=0.995;
  }
  //maleSchachfeld(schachfeld);
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