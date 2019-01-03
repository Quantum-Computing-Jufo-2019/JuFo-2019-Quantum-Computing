class Summand {
  int multiplikator;
  PVector pvec1;
  PVector pvec2;
  Summand(int multiplikator, PVector pvec1, PVector pvec2) {
    this.multiplikator=multiplikator;
    this.pvec2=pvec2;
    this.pvec1=pvec1;
  }   
  Summand(int multiplikator, PVector pvec1) {
    this.multiplikator=multiplikator;
    this.pvec1=pvec1;
  }
}
