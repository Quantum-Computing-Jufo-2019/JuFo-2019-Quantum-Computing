
class Feld {
  PVector position;
  int groesse;
  boolean istBesetzt;
  Feld(PVector position, int groesse, boolean istBesetzt) {
    this.position=position;
    this.groesse=groesse;
    this.istBesetzt=istBesetzt;
  }

  boolean mouseIsInside(PVector pos) { //prüft ob ein PVector im Feld liegt
    return(pos.x> position.x && pos.x<position.x+groesse && pos.y>position.y && pos.y< position.y+groesse);
  }
}

//speichert Bilder mit position und breite(höhe)
class Picture {
  PImage pic;
  PVector pos;
  int groesse;
  Picture(PImage pic, PVector pos, int groesse) {
    this.pic=pic;
    this.pos=pos;
    this.groesse=groesse;
  }
}

boolean mouseIsInside(float x1, float y1, float breite, float hoehe, PVector pos) {

  float lowX=x1;
  float lowY=y1;
  float highX=x1+breite;
  float highY=y1+hoehe;

  return(pos.x> lowX && pos.x<highX && pos.y>lowY && pos.y< highY);
} 
