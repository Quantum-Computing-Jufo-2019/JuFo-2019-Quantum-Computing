int n = 3;
int nVereinfacht = n-1;
boolean[][][] schachfeld = new boolean[n*n][nVereinfacht][nVereinfacht];
int[][] hamiltonMatrix = new int[n*n*nVereinfacht*nVereinfacht][n*n*nVereinfacht*nVereinfacht];
ArrayList<String> simAnnGraph = new ArrayList<String>();

void setup() {
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<nVereinfacht; i++) {
      for (int j=0; j<nVereinfacht; j++) {
        schachfeld[l][i][j] = int(random(0, 2)) == 1;
      }
    }
  }
  noLoop();
}



void draw() {
  hamiltonianTermAufstellen();

  //Hamiltonian-Matrix ausgeben
  for (int i=0; i<n*n*nVereinfacht*nVereinfacht; i++) {
    for (int j=0; j<n*n*nVereinfacht*nVereinfacht; j++) {
      if (hamiltonMatrix[i][j] >= 0)
        print(" ");
      print(hamiltonMatrix[i][j]);
    }
    println();
  }
  println("ausgangslösung:");
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<nVereinfacht; i++) {
      for (int j=0; j<nVereinfacht; j++) {
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
              int i=1000;
              int j=1000;
              //Berechnen der Position auf der Matrix. 
              //wenn richtige Farbe && wenn nicht mittleres Feld
              if (((l+y+x)%2==0 && (m+a+b)%2==0) && !((x==1&&y==1)||(a==1&&b==1))) {
                int nVerquad=nVereinfacht*nVereinfacht;
                if (l%2==0) {
                  i=(x==0&&y==2)?l*nVerquad : (x==2&&y==2)?l*nVerquad+1 : (x==0&&y==0)?l*nVerquad+2 : (x==2&&y==0)?l*nVerquad+3:null;
                } else {
                  i=(x==1&&y==2)?l*nVerquad : (x==2&&y==1)?l*nVerquad+1 : (x==0&&y==1)?l*nVerquad+2 : (x==1&&y==0)?l*nVerquad+3:null;
                }
                if (m%2==0) {
                  j=(a==0&&b==2)?m*nVerquad : (a==2&&b==2)?m*nVerquad+1 : (a==0&&b==0)?m*nVerquad+2 : (a==2&&b==0)?m*nVerquad+3:null;
                } else {
                  j=(a==1&&b==2)?m*nVerquad : (a==2&&b==1)?m*nVerquad+1 : (a==0&&b==1)?m*nVerquad+2 : (a==1&&b==0)?m*nVerquad+3:null;
                }

                //übereinander keine Springer
                if (x==a && y==b && m!=l) { 
                  hamiltonMatrix[(i<=j)?i:j][(i<=j)?j:i]+=2;
                }
                
                //auf der Zeitebene keine springer
                if (l==m && !(x==a && y==b)) {
                  hamiltonMatrix[(i<=j)?i:j][(i<=j)?j:i]+=1;
                }
                
                //Springerzug einhalten 
                if (abs(l-m)==1) {
                  if (abs(x-a)*abs(b-y)==2) {
                    hamiltonMatrix[(i<=j)?i:j][(i<=j)?j:i]-=1;
                  } else {
                    hamiltonMatrix[(i<=j)?i:j][(i<=j)?j:i]+=1;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}



int kostenfunktion(boolean[][][]schachfeldLocal) { //kostenfunktion debuggen
  int ergebnis=0;
  int[] vektor=new int[n*n*nVereinfacht*nVereinfacht];
  int[] vektorerg=new int[n*n*nVereinfacht*nVereinfacht];

  for (int l=0; l<n*n; l++) {
    for (int i=0; i<nVereinfacht; i++) {
      for (int j=0; j<nVereinfacht; j++) {
        vektor[l*nVereinfacht*nVereinfacht+i*nVereinfacht+j]=schachfeldLocal[l][i][j]==true? (1):(0);
      }
    }
  }

  for (int i=0; i<n*n*nVereinfacht*nVereinfacht; i++) {
    for (int j=0; j<n*n*nVereinfacht*nVereinfacht; j++) {
      vektorerg[i]+=hamiltonMatrix[i][j]*vektor[j];
    }
  }

  for (int i=0; i<n*n*nVereinfacht*nVereinfacht; i++) {
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
      if (pruefeErgebnis(schachfeld)) {
        println(durchlauf+" Durchläufe");
        println("simAnn Schwelle: "+simAnn);
        break;
      }
      print("#");
    }

    if (durchlauf%10000==0) {
      println();
      println(alteKosten);
      maleSchachfeld(schachfeld);
      println();
    }

    int x = int(random(nVereinfacht));
    int y = int(random(nVereinfacht));
    int l = int(random(n*n));
    schachfeld[l][x][y]=!schachfeld[l][x][y];
    int kosten = kostenfunktion(schachfeld);
    int kostenUnterschied=kosten-alteKosten;

    if ((kostenUnterschied>=0 && (random(1)>=exp(-kostenUnterschied/simAnn)))) {
      schachfeld[l][x][y]=!schachfeld[l][x][y];
    }
    simAnnGraph.add(durchlauf+" "+kostenfunktion(schachfeld));

    simAnn*=0.9997; //0.99999
  }

  maleSchachfeld(schachfeld);
  println("simAnn: "+simAnn);
  println("Kosten: "+kostenfunktion(schachfeld));
}


void maleSchachfeld(boolean[][][] schachfeldLocal) {
  for (int l=0; l<n*n; l++) {
    for (int i=0; i<nVereinfacht; i++) {
      for (int j=0; j<nVereinfacht; j++) {
        if (schachfeldLocal[l][i][j]==true) {
          int a=100, b=100;
          if (l%2==0) {
            switch(i+""+j) {
            case"00":
              a=0;
              b=0;
              break;
            case"01":
              a=0;
              b=2;
              break;
            case"10":
              a=2;
              b=0;
              break;
            case"11":
              a=2;
              b=2;
              break;
            }
          } else {
            switch(i+""+j) {
            case"00":
              a=0;
              b=1;
              break;
            case"01":
              a=1;
              b=2;
              break;
            case"10":
              a=1;
              b=0;
              break;
            case"11":
              a=2;
              b=1;
              break;
            }
          }
          println("<"+l+", "+a+", "+b+">");
        }
      }
    }
  }
}

void exportiereGraph(ArrayList <String> listToWrite, String algo) {
  String[]graphWrite= new String[listToWrite.size()];
  for (int i=0; i<listToWrite.size(); i++) {
    graphWrite[i]=listToWrite.get(i);
  }
  saveStrings("Graphroesslesprung_"+nVereinfacht+"_"+algo+".txt", graphWrite);
}

void exportiereHamiltonianMatrix() {
  String [] export=new String[n*n*nVereinfacht*nVereinfacht];
  for (int x=0; x<n*n*nVereinfacht*nVereinfacht; x++) {
    export[x]="";
    for (int y=0; y<n*n*nVereinfacht*nVereinfacht; y++) {
      export[x]+=hamiltonMatrix[x][y]+" ";
    }
  }
  saveStrings("qubomatrixroesslesprung_" + n +".txt", export);
}

boolean pruefeErgebnis(boolean schachfeld[][][]) { 
  //prüfen, ob in jeder ebene ein pferd steht => insgesamt 8 pferde sind
  ArrayList<Integer> pferdezahl=new ArrayList<Integer>();
  for (int l=0; l<n*n; l++) {
    for (int x=0; x<nVereinfacht; x++) {
      for (int y=0; y<nVereinfacht; y++) {
        for (int m=0; m<n*n; m++) {
          for (int a=0; a<nVereinfacht; a++) {
            for (int b=0; b<nVereinfacht; b++) {
              int x2=100, y2=100, a2=100, b2=100;
              if (l%2==0) {
                switch(x+""+y) {
                case"00":
                  x2=0;
                  y2=0;
                  break;
                case"01":
                  x2=0;
                  y2=2;
                  break;
                case"10":
                  x2=2;
                  y2=0;
                  break;
                case"11":
                  x2=2;
                  y2=2;
                  break;
                }
              } else {
                switch(x+""+y) {
                case"00":
                  x2=0;
                  y2=1;
                  break;
                case"01":
                  x2=1;
                  y2=2;
                  break;
                case"10":
                  x2=1;
                  y2=0;
                  break;
                case"11":
                  x2=2;
                  y2=1;
                  break;
                }
              }
              if (m%2==0) {
                switch(a+""+b) {
                case"00":
                  a2=0;
                  b2=0;
                  break;
                case"01":
                  a2=0;
                  b2=2;
                  break;
                case"10":
                  a2=2;
                  b2=0;
                  break;
                case"11":
                  a2=2;
                  b2=2;
                  break;
                }
              } else {
                switch(a+""+b) {
                case"00":
                  a2=0;
                  b2=1;
                  break;
                case"01":
                  a2=1;
                  b2=2;
                  break;
                case"10":
                  a2=1;
                  b2=0;
                  break;
                case"11":
                  a2=2;
                  b2=1;
                  break;
                }
              }

              //layer übereinander && |abstand| != 3 && beide Positionen = true
              if (abs(l-m)==1 && (abs(x2-a2)+abs(y2-b2))!=3 && schachfeld[l][x][y] && schachfeld[m][a][b]) {
                return false;
              }
            }
          }
        }
        if (schachfeld[l][x][y]) {
          pferdezahl.add(l);
        }
      }
    }
  }
  for (int p=0; p<pferdezahl.size(); p++ ) {
    for (int q=0; q<pferdezahl.size(); q++) {
      if (pferdezahl.get(p)==pferdezahl.get(q)&&p!=q) {
        return false;
      }
    }
  } //überprüfen ob alle layer der reihenfolge nach besetzt ist
  if (pferdezahl.size()!=8) {
    return false;
  }
  return true;
}
