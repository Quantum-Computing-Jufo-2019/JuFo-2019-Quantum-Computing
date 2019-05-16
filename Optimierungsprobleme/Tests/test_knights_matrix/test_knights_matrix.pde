int n=3;
int matrix[][]=new int[n*n*n*n][n*n*n*n];

for(int i=0;i<n*n*n*n;i++){
 for(int j=0;j<n*n*n*n;j++){
   if((i<j&&(abs(((i-1)-((i-1)%n))-((j-1)-((j-1)%n)))!=1&&abs((i%n)-(j%n))==2))  ||  (i<j&&(abs(((i-1)-((i-1)%n))-((j-1)-((j-1)%n)))!=2&&abs((i%n)-(j%n))==1))){
     matrix[i][j]=-2;
   }
   if(i>j){
     matrix[i][j]=0;
   }
   if((i<j&&i%(n*n)==j%(n*n))  ||  (i<j&&(i-1)-((i-1)%(n*n))==(j-1)-((j-1)%(n*n)))  ||  (i<j&&(abs(((i-1)-((i-1)%n))-((j-1)-((j-1)%n)))==1&&abs((i%n)-(j%n))==2))  ||  (i<j&&(abs(((i-1)-((i-1)%n))-((j-1)-((j-1)%n)))==2&&abs((i%n)-(j%n))==1))){
     matrix[i][j]=2;
   } 
 }
}

  for (int i=0; i<n*n*n*n; i++) {
    for (int j=0; j<n*n*n*n; j++) {
      if (matrix[i][j] >= 0)
        print(" ");
      print(matrix[i][j]);
    }
    println();
  }
