int n=3;
int matrix[][]=new int[n*n*n*n][n*n*n*n];

for(int i=0;i<n*n*n*n;i++){
 for(int j=0;j<n*n*n*n;j++){
   if(((i<j&&((abs((((j-1)-((j-1)%(n*n)))/(n*n))-(((i-1)-((i-1)%(n*n)))/(n*n)))==1)&&(abs(((i%(n*n)-1)-((i%(n*n)-1)%n))-((j%(n*n)-1)-((j%(n*n)-1)%n)))==1&&abs((i%(n*n)%n)-(j%(n*n)%n))==2))))  ||  (i<j&&((abs((((j-1)-((j-1)%(n*n)))/(n*n))-(((i-1)-((i-1)%(n*n)))/(n*n)))==1)&&(abs(((i%(n*n)-1)-((i%(n*n)-1)%n))-((j%(n*n)-1)-((j%(n*n)-1)%n)))==2&&abs((i%(n*n)%n)-(j%(n*n)%n))==1)))){
     matrix[i][j]=-2;
   }
   if(i>j){
     matrix[i][j]=0;
   }
   //||  (i<j&&!(((((j-1)-((j-1)%(n*n)))/(n*n))-(((i-1)-((i-1)%(n*n)))/(n*n))==1)&&(abs(((i%(n*n)-1)-((i%(n*n)-1)%n))-((j%(n*n)-1)-((j%(n*n)-1)%n)))==1&&abs((i%(n*n)%n)-(j%(n*n)%n))==2)))  || (i<j&&!(((((j-1)-((j-1)%(n*n)))/(n*n))-(((i-1)-((i-1)%(n*n)))/(n*n))==1)&&(abs(((i%(n*n)-1)-((i%(n*n)-1)%n))-((j%(n*n)-1)-((j%(n*n)-1)%n)))==2&&abs((i%(n*n)%n)-(j%(n*n)%n))==1)))
   if((i<j&&i%(n*n)==j%(n*n))  ||  (i<j&&(i-1)-((i-1)%(n*n))==(j-1)-((j-1)%(n*n)))    ){
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
