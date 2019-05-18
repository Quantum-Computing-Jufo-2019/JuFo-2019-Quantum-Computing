int n=4;
int matrix[][]=new int[n*n*n][n*n*n];

for(int i=0;i<n*n*n;i++){
 for(int j=0;j<n*n*n;j++){
   int xi=(((i-1)%(n*n)+1)-1)-(((i-1)%(n*n)+1)-1)%n;
   int xj=(((j-1)%(n*n)+1)-1)-(((j-1)%(n*n)+1)-1)%n;
   int yi=(((i-1)%(n*n))%n+1);
   int yj=(((j-1)%(n*n))%n+1);
   if(i==j){
     matrix[i][j]=-2;
   }
   if(i>j){
    matrix[i][j]=0; 
   }
   //
   //
   if(i<j &&  (((i%(n*n))==(j%(n*n))  || (((i-1)%(n*n)+1)%n==((j-1)%(n*n)+1)%n)  || ((((i-1)%(n*n)+1)-1)-(((i-1)%(n*n)+1)-1)%n==(((j-1)%(n*n)+1)-1)-(((j-1)%(n*n)+1)-1)%n)||  ((xi-1)-((xi-1)%2)==(xj-1)-((xj-1)%2) && (yi-1)-((yi-1)%2)==(yj-1)-((yj-1)%2))  ))){
     matrix[i][j]=2;
   }
 }
}

  for (int i=0; i<n*n*n; i++) {
    for (int j=0; j<n*n*n; j++) {
      if (matrix[i][j] >= 0)
        print(" ");
      print(matrix[i][j]);
    }
    println();
  }
