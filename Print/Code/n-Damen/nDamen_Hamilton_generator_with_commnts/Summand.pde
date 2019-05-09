/*
Dieses Programm ist Teil des Jugend-forscht Projekts "Lösung des n-Damenproblems auf einem adiabatischen Quantencomputer"
 FILE 2
 */

//Hilfsklasse zum Speichern des Terms; siehe Doku S.3 / S.6
class Summand {
  int multiplikator;
  PVector feld1;
  PVector feld2;

  Summand(int multiplikator, PVector feld1, PVector feld2) {
    this.multiplikator = multiplikator;
    this.feld2 = feld2;
    this.feld1 = feld1;
  }   

  Summand(int multiplikator, PVector feld1) {
    this.multiplikator = multiplikator;
    this.feld1 = feld1;
  }
}
