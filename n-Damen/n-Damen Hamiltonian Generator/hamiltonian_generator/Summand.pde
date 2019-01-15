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
