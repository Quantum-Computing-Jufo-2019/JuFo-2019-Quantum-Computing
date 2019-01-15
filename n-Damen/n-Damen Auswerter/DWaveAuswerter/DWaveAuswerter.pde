int n=4;
boolean diagonaleFrei=false;
int[][] matrix=new int[n*n][n*n];
ArrayList <Summand> term = new ArrayList<Summand>();
ArrayList <DurchlaufElement> resultList = new ArrayList<DurchlaufElement>();
String[] result;
void setup() {
  noLoop();
  result=loadStrings("results.txt");
  formelAufstellen();
  matrix(term);
}

void draw() {
  for (int i=1; i<result.length; i++) {
    println(result[i]);
    String[]split1=split(result[i], "000000");
    String[]split2=split(split1[1], "[");

    boolean[][] matrixLocal=new boolean[n][n];
    String[] split3=split(split2[1], "]");
    String[] matrixString=split(split3[0], " ");
    for (int j=0; j<matrixString.length; j++) {
      matrixLocal[int(j/n)][j-int(j/n)*4]=matrixString[j].equals("1");
    }
    resultList.add(new DurchlaufElement(kostenfunktion(matrixLocal), int(trim(split2[0])), matrixLocal));
    println(kostenfunktion(matrixLocal));
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
  println(ergebnis);
  return ergebnis;
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

void matrix(ArrayList <Summand> term) {
  for (int i=0; i<term.size(); i++) {
    if  ( ((int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n) < ((int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n)) {
      matrix[(int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n][(int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n]+=term.get(i).multiplikator;
    } else {
      matrix[(int(term.get(i).pvec2.x)-1)+(int(term.get(i).pvec2.y)-1)*n][(int(term.get(i).pvec1.x)-1)+(int(term.get(i).pvec1.y)-1)*n] +=term.get(i).multiplikator;
    }
  }
}
