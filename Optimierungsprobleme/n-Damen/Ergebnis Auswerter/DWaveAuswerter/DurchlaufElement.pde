class DurchlaufElement {
  int energie;
  int durchlaeufe;
  boolean[][] matrix;
  DurchlaufElement(int energie, int durchlaeufe, boolean[][] matrix) {
    this.matrix=matrix;
    this.energie=energie;
    this.durchlaeufe=durchlaeufe;
  }
}
