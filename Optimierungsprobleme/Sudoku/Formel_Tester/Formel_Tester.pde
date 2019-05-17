void setup() {
  int n = 4;

  String paul[] = loadStrings("paul.txt");
  String jakov[] = loadStrings("jakov.txt");

  String[][] paulMatrix = new String[paul.length][paul.length];
  String[][] jakovMatrix = new String[jakov.length][jakov.length];

  for (int i=0; i< paul.length; i++) {
    paulMatrix[i] = paul[i].split(" ");
  }


  for (int i=0; i< jakov.length; i++) {
    jakovMatrix[i] = jakov[i].split(" ");
  }

  println(jakovMatrix[0]);
  println(paulMatrix[0]);


  int errors = 0;
  for (int ebene = 0; ebene< n; ebene++) {
    for (int x = 0; x < n; x++) {
      for (int y = 0; y< n; y++) {
        for (int x2 = 0; x < n; x2++) {
          for (int y2 = 0; y< n; y2++) {
            //println((ebene*x*y*x2*y2)+"/"+(n*n*n*n*n));
            println("ebene= "+ebene+";x="+x+", y="+y+"; x2="+x2+"; y2="+y2);
            int jakovStelleX = jakov_stelle(x, y, ebene, n);
            int jakovStelleY = jakov_stelle(x2, y2, ebene, n);

            int paulStelleX = paul_stelle(x, y, ebene, n);
            int paulStelleY = paul_stelle(x2, y2, ebene, n);

            if (paulMatrix[paulStelleY][paulStelleX].equals(jakovMatrix[jakovStelleY][jakovStelleX])) {
              //println("stimmt überein");
            } else {
              errors++;
              println("stimmt nicht überein");
            }
          }
        }
      }
    }
    println("errors= "+errors);
  }
}
int jakov_stelle(int feldX, int feldY, int ebene, int n) {
  //return (x+(y*n))*(ebene+1)*n;
  return (feldX+(feldY*n))*n+ebene;
}
int paul_stelle(int feldX, int feldY, int ebene, int n) {
  return feldX+(feldY*n)+(ebene*n*n);
}
void draw() {
}
