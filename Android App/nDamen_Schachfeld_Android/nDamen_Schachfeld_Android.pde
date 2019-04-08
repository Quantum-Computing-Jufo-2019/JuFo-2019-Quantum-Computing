ArrayList <PVector> points = new ArrayList<PVector>();
int n=4;
boolean[][] schachfeldbool = new boolean[n][n];
int[][] hamiltonianMatrix = new int[n*n][n*n];
int kosten=100;
color background=color(255, 255, 255, 50);
PImage chess;
Picture plus;
Picture minus;
//Schachfeld array speichert jedes "physische" einzelne Feld des großen Schachfelds mit Position, breite(höhe), booolean: steht eine Dame drauf
Feld[][] schachfeld=new Feld[n][n];
int w=int(str(int(str(int(str(displayHeight-1))))));

void settings() {
  size((displayWidth>displayHeight?displayWidth:displayHeight), (displayWidth>displayHeight?displayWidth:displayHeight)*9/19);
}
void setup() {
  orientation(LANDSCAPE);
  //Bilder laden (Schachdame, minussymbol,plussymbol
  chess=loadImage("chess.png");
  minus=new Picture(loadImage("minus.png"), new PVector((width/2)+width/6, height/5), width/15);
  plus=new Picture(loadImage("plus.png"), new PVector((width/2)+width/6*2, height/5), width/15);
  erzeugeFelder();
  hamiltonianTermAufstellen();
}

void draw() {
  //hintergrund bei richtiger Lösung grün
  if (kosten==n*(-2)) {
    background(255);
    background=color(192, 207, 58, 200);
  } else {
    background=color(255, 255, 255, 150);
  }
  background(background);
  refresh();
  maleFelder();
  berechneKosten();
  maleKosten();
  maleChooser();
}


void mousePressed() {

  //ist die "Maus" in einem Schachfeld? Invertiere die "istBesetzt" bool Variable dieses Feldes
  //=> Damen können gesetzt und entfernt werden
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      if (schachfeld[i][j].mouseIsInside(new PVector(mouseX, mouseY))) {
        schachfeld[i][j].istBesetzt=!schachfeld[i][j].istBesetzt;
      }
    }
  }


  //wurde auf das minus-Symbol geklickt? n-- und dann Schachfelder und den Hamiltonian neu berechnen
  if (mouseIsInside(minus.pos.x-minus.groesse/2, minus.pos.y-minus.groesse/2, minus.groesse, minus.groesse, new PVector(mouseX, mouseY))) {
    n--;  
    n=n<4?4:n;
    schachfeldbool = new boolean[n][n];
    hamiltonianMatrix = new int[n*n][n*n];
    schachfeld=new Feld[n][n];
    erzeugeFelder();
    hamiltonianTermAufstellen();
    //das gleiche wie bei minus nur n++
  } else if (mouseIsInside(plus.pos.x-plus.groesse/2, plus.pos.y-plus.groesse/2, plus.groesse, plus.groesse, new PVector(mouseX, mouseY))) {
    n++;
    n=n>9?9:n;
    schachfeldbool = new boolean[n][n];
    hamiltonianMatrix = new int[n*n][n*n];
    schachfeld=new Feld[n][n];
    erzeugeFelder();
    hamiltonianTermAufstellen();
  }
}

//male das Wahlfenster mit  + und - Symbol und dem Wert von n
void maleChooser() {
  imageMode(CENTER);
  image(minus.pic, minus.pos.x, minus.pos.y, minus.groesse, minus.groesse);
  image(plus.pic, plus.pos.x, plus.pos.y, plus.groesse, plus.groesse);
  textAlign(CENTER, CENTER);
  fill(0);
  textSize(width/13>75*displayDensity?width/13:75*displayDensity);//75*displayDensity);
  text(n, (width/2)+(width/6)*1.5, height/5);
  fill(255);
  imageMode(CORNER);
}

//Füllt die Werte ob ein Feld mit einer Dame besetzt ist von dem angezeigten Feld-Array in ein booleanarray um
void berechneKosten() {
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      schachfeldbool[i][j]=false;
    }
  }
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      if (schachfeld[i][j].istBesetzt) {
        schachfeldbool[i][j]=true;
      }
    }
  }
  kosten=kostenfunktion(schachfeldbool);
}


//Kosten werden angezeigt
void maleKosten() {
  textAlign(CENTER, CENTER);
  fill(0);
  //wenn Lösung richtig:
  if (kosten==n*(-2)) {
    textAlign(CENTER, TOP);
    textSize(43*displayDensity);
    text("Glueckwunsch!\nrichtige Loesung!", (width/4)*2.25, (height/5)*2, width/2-width/10, height-height/6);//width/2+width/20
    textSize(64*displayDensity);
    text("Kosten: "+ n*(-2), (width/4)*3, (height/5)*3.5);
    //wenn Lösung nicht richtig
  } else {
    noStroke();
    fill(255, 90, 90, 140);
    //rotes Rechteck
    rect((width/4)*2.25, (height/5)*2, width/2-width/10, height-height/2, 63);
    fill(0);
    textSize(83*displayDensity);
    text("Kosten:", (width/4)*3, (height/5)*2.6);
    textSize(95*displayDensity);
    text(kosten, (width/16)*11, (height/5)*3.8); 
    textAlign(CENTER, TOP);
    //optimale Kosten (nach rechts gerückt wenn Kosten 3 stellig)
    if (kosten<99) {
      textSize(27*displayDensity);
      text("optimal: "+n*(-2), (width/16)*13.5, (height/5)*3.9);
    } else {
      textSize(27*displayDensity);
      text("optimal: "+n*(-2), (width/16)*13.9, (height/5)*3.9);
    }
    stroke(0);
  }
  fill(255);
}


//befüllt das Felder Array mit den Positionen der Schachfelder
void erzeugeFelder() {
  int groesse=int((height-height/6)/n); //breite bzw höhe des Feldes
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      int xPos=width/10+groesse*i; //=> abstand zu Rand + breite jedes Feldes * Nummer des Feldes
      int yPos=height/12+groesse*j;
      schachfeld[i][j]=new Feld(new PVector(xPos, yPos), groesse, int(random(0, 4))==1?true:false);
    }
  }
}

//malt die Felder auf Basis der im Array gespeicherten Daten
void maleFelder() {
  strokeWeight(2*displayDensity);
  for (int i=0; i<n; i++) {
    for (int j=0; j<n; j++) {
      //jedes 2te Feld grau
      if (i%2==j%2) {
        fill(255);
      } else {
        fill(150);
      }
      rect(schachfeld[i][j].position.x, schachfeld[i][j].position.y, schachfeld[i][j].groesse, schachfeld[i][j].groesse);
      if (schachfeld[i][j].istBesetzt) { //wenn schachfeld besetzt -> Damenbild draufmalen
        image(chess, schachfeld[i][j].position.x+4, schachfeld[i][j].position.y+4, schachfeld[i][j].groesse-8, schachfeld[i][j].groesse-8);
      }
    }
  }
  strokeWeight(1);
}

//aktualisiert die punkte
void refresh() {
  points = new ArrayList<PVector>();
  for (int i=0; i<touches.length; i++) {
    points.add(new PVector(touches[i].x, touches[i].y));
  }
}

void hamiltonianTermAufstellen() {
  for (int x1 =0; x1<n; x1++) {
    for (int y1 =0; y1<n; y1++) {
      for (int x2 =0; x2<n; x2++) {
        for (int y2 =0; y2<n; y2++) {
          if (x1 == x2 && y1 == y2) {
            hamiltonianMatrix[n*x1+y1][n*x1+y1] = -2;
          } else if (x1 == x2 || y1 == y2 || abs(x1-x2) == abs(y1-y2)) {
            hamiltonianMatrix[min(n*x1+y1, n*x2+y2)][max(n*x1+y1, n*x2+y2)] += 2;
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
