//  Sudoku Solver
//  Man Yiu Lam - 16458032
  int z = 300/9;
  int[][] array = new int[9][9]; //consists of NINE: 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 EACH row = 45, whole = 405  row squared = 205
  int[] array2 = new int[9]; // This holds numbers to test against.
  int[] x1 = new int[9]; int[] x2 = new int[9]; int[] x3 = new int[9]; int[] x4 = new int[9]; int[] x5 = new int[9]; int[] x6 = new int[9]; int[] x7 = new int[9]; int[] x8 = new int[9]; int[] x9 = new int[9];    // 1x9 Matrix = 45
  int[] y1 = new int[9]; int[] y2 = new int[9]; int[] y3 = new int[9]; int[] y4 = new int[9]; int[] y5 = new int[9]; int[] y6 = new int[9]; int[] y7 = new int[9]; int[] y8 = new int[9]; int[] y9 = new int[9];    // 9x1 Matrix = 45
  int[] z1 = new int[9]; int[] z2 = new int[9]; int[] z3 = new int[9]; int[] z4 = new int[9]; int[] z5 = new int[9]; int[] z6 = new int[9]; int[] z7 = new int[9]; int[] z8 = new int[9]; int[] z9 = new int[9];    // 3x3 Matrix = 45

//PFont Font1;
//PFont Font2;

void setup() {      //backtrack method. 
  size(298,298);
  background(255);
//  Font1 = createFont("Arial Bold",15);
//  Font2 = createFont("Arial",15);

  //given...
  array[0][0] = 5; array[0][1] = 3; array[0][4] = 7; 
  array[1][0] = 6; array[1][3] = 1; array[1][4] = 9; array[1][5] = 5;
  array[2][1] = 9; array[2][2] = 8; array[2][7] = 6;
  array[3][0] = 8; array[3][4] = 6; array[3][8] = 3;
  array[4][0] = 4; array[4][3] = 8; array[4][5] = 3; array[4][8] = 1;
  array[5][0] = 7; array[5][4] = 2; array[5][8] = 6;
  array[6][1] = 6; array[6][6] = 2; array[6][7] = 8;
  array[7][3] = 4; array[7][4] = 1; array[7][5] = 9; array[7][8] = 5;
  array[8][4] = 8; array[8][7] = 7; array[8][8] = 9;


  for(int i=0; i<=8; i++) {        // creating an array of [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ] and later removing dupes vs x1 , y1 , z1
    array2[i] = i+1;
  }
  
  
  for(int i=0; i<=8; i++) {        // Storing numbers in arrays and later Making restrictions for new numbers
   x1[i] = array[0][i]; 
  } for(int i=0; i<=8; i++) {
   x2[i] = array[1][i]; 
  } for(int i=0; i<=8; i++) {
   x3[i] = array[2][i]; 
  } for(int i=0; i<=8; i++) {
   x4[i] = array[3][i]; 
  } for(int i=0; i<=8; i++) {
   x5[i] = array[4][i]; 
  } for(int i=0; i<=8; i++) {
   x6[i] = array[5][i]; 
  } for(int i=0; i<=8; i++) {
   x7[i] = array[6][i]; 
  } for(int i=0; i<=8; i++) {
   x8[i] = array[7][i]; 
  } for(int i=0; i<=8; i++) {
   x9[i] = array[8][i]; 
  }
  
  
  //int x9sum = 0;                // Prep towards sum must = 45 for each row or 285 when all sum squared
 //for(int i=0; i<=8; i++) {     // Testing to see if it stored
  //  x9sum += x9[i];
  //  print(x9[i]+" ");
 //}
 //println("\n"+x9sum);
 
 int allSum = 0;
 for(int i=0; i<=8; i++) {
   for(int j=0; j<=8; j++) {
    allSum = array[i][j];
    print(allSum+ " ");
   }
   println();
 }
 
  for(int i=0; i<=8; i++) {        // Storing numbers in arrays and later Making restrictions for new numbers
   y1[i] = array[i][0]; 
  } for(int i=0; i<=8; i++) {
   y2[i] = array[i][1]; 
  } for(int i=0; i<=8; i++) {
   y3[i] = array[i][2]; 
  } for(int i=0; i<=8; i++) {
   y4[i] = array[i][3]; 
  } for(int i=0; i<=8; i++) {
   y5[i] = array[i][4]; 
  } for(int i=0; i<=8; i++) {
   y6[i] = array[i][5]; 
  } for(int i=0; i<=8; i++) {
   y7[i] = array[i][6]; 
  } for(int i=0; i<=8; i++) {
   y8[i] = array[i][7]; 
  } for(int i=0; i<=8; i++) {
   y9[i] = array[i][8]; 
  } 
  
 //int y9sum = 0;               // Prep towards sum must = 45 for each row
 //for(int i=0; i<=8; i++) {    // Testing to see if it stored
 //  y9sum += y9[i];
 //  println(y9[i]);
 //}
 //println("\n"+y9sum);
 
 int n=0;
 
  for(int i=0; i<=2; i++) {   // Z1
    for(int j=0; j<=2; j++) {
      z1[n] = array[i][j];
  //    print(z1[n]+" ");    To show the whole array of Z1 aka [ 5 3 0
  //                                                               6 0 0
  //                                                               0 9 8 ] in a 3x3 Matrix.
      n++; }
      println();
} n=0; for(int i=0; i<=2; i++) {   // Z2
    for(int j=3; j<=5; j++) {
      z2[n] = array[i][j];
  //    print(z2[n]+" ");   // To show the whole array of Z2 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=0; i<=2; i++) {   // Z3
     for(int j=6; j<=8; j++) {
      z3[n] = array[i][j];
  //    print(z3[n]+" ");    To show the whole array of Z3 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=3; i<=5; i++) {   // Z4
     for(int j=0; j<=2; j++) {
      z4[n] = array[i][j];
  //    print(z4[n]+" ");    To show the whole array of Z4 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=3; i<=5; i++) {   // Z5
     for(int j=3; j<=5; j++) {
      z5[n] = array[i][j];
  //    print(z5[n]+" ");    To show the whole array of Z5 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=3; i<=5; i++) {   // Z6
     for(int j=6; j<=8; j++) {
      z6[n] = array[i][j];
  //    print(z6[n]+" ");    To show the whole array of Z6 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=6; i<=8; i++) {   // Z7
     for(int j=0; j<=2; j++) {
      z7[n] = array[i][j];
  //    print(z7[n]+" ");    To show the whole array of Z7 in a 3x3 Matrix.
      n++; }
  //    println();
} n=0; for(int i=6; i<=8; i++) {   // Z8
     for(int j=3; j<=5; j++) {
      z8[n] = array[i][j];
  //    print(z8[n]+" ");    To show the whole array of Z8 in a 3x3 Matrix.
      n++; }
  //    println();
  } n=0; for(int i=6; i<=8; i++) {   // Z9
     for(int j=6; j<=8; j++) {
      z9[n] = array[i][j];
  //    print(z9[n]+" ");    To show the whole array of Z9 in a 3x3 Matrix.
      n++; }
  //    println();
  }   
  

  int a = 0;
  for(int i=22; i<300;) {        // Generates all the given numbers in the grids
  int b = 0;
    for(int j=13; j<300;) {
     
      if (array[a][b] == 0 ) {
      fill(255); text(array[a][b],j,i);
      }
      else {
      fill(0);
      text(array[a][b],j,i);      // Places the numbers onto screen
      }  
    b++;
    j += z;  
    }
    a++;
    i += z;
  }

  
  for(int i=0; i<300; i++) {      // Mapping out the grids for the 9x9 boxes
    for(int j=0; j<300; j++) {
      stroke(0);
      strokeWeight(0);
      line(0,i*z,300,i*z);
      line(z*j,0,z*j,300);
    }
  }
  
  strokeWeight(3);
  stroke(0);
  line(0,z*3,300,z*3);
  line(0,z*6,300,z*6);
  line(z*3,0,z*3,300);
  line(z*6,0,z*6,300);
  

    int sum = 0;
    
    for(int i=0; i<=8; i++) {
    if(array[0][i] == 0) {
    switch(i) {
    case 0: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y1, z1 ;
    case 1: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y2, z1 ;
    case 2: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y3, z1 ;
    case 3: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y4, z2 ;
    case 4: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y5, z2 ;
    case 5: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y6, z2 ;
    case 6: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y7, z3 ;
    case 7: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y8, z3 ;
    case 8: array[0][i] = (int)random(1,10); break;//gen rand exclude , x1, y9, z3 ;
    }
          fill(0,0,255);
      text(array[0][i],(i*z)+13,22);
   }
    sum += array[0][i]; 
  }
  
    for(int i=0; i<=8; i++) {
    if(array[1][i] == 0) {
    switch(i) {
    case 0: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y1, z1 ;
    case 1: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y2, z1 ;
    case 2: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y3, z1 ;
    case 3: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y4, z2 ;
    case 4: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y5, z2 ;
    case 5: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y6, z2 ;
    case 6: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y7, z3 ;
    case 7: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y8, z3 ;
    case 8: array[1][i] = (int)random(1,10); break;//gen rand exclude , x2, y9, z3 ;
    }
          fill(0,0,255);
      text(array[1][i],(i*z)+13,z+22); }
  }
  
    for(int i=0; i<=8; i++) {
    if(array[2][i] == 0) {
    switch(i) {
    case 0: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y1, z1 ;
    case 1: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y2, z1 ;
    case 2: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y3, z1 ;
    case 3: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y4, z2 ;
    case 4: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y5, z2 ;
    case 5: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y6, z2 ;
    case 6: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y7, z3 ;
    case 7: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y8, z3 ;
    case 8: array[2][i] = (int)random(1,10); break;//gen rand exclude , x3, y9, z3 ;
    }
          fill(0,0,255);
      text(array[2][i],(i*z)+13,(2*z)+22); }
  }
  
    for(int i=0; i<=8; i++) {
    if(array[3][i] == 0) {
    switch(i) {
    case 0: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y1, z4 ;
    case 1: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y2, z4 ;
    case 2: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y3, z4 ;
    case 3: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y4, z5 ;
    case 4: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y5, z5 ;
    case 5: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y6, z5 ;
    case 6: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y7, z6 ;
    case 7: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y8, z6 ;
    case 8: array[3][i] = (int)random(1,10); break;//gen rand exclude , x4, y9, z6 ;
    }
          fill(0,0,255);
      text(array[3][i],(i*z)+13,(3*z)+22); }
  } 
  
    for(int i=0; i<=8; i++) {
    if(array[4][i] == 0) {
    switch(i) {
    case 0: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y1, z4 ;
    case 1: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y2, z4 ;
    case 2: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y3, z4 ;
    case 3: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y4, z5 ;
    case 4: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y5, z5 ;
    case 5: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y6, z5 ;
    case 6: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y7, z6 ;
    case 7: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y8, z6 ;
    case 8: array[4][i] = (int)random(1,10); break;//gen rand exclude , x5, y9, z6 ;
    }
          fill(0,0,255);
      text(array[4][i],(i*z)+13,(4*z)+22); }
  }   
  
    for(int i=0; i<=8; i++) {
    if(array[5][i] == 0) {
    switch(i) {
    case 0: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y1, z4 ;
    case 1: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y2, z4 ;
    case 2: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y3, z4 ;
    case 3: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y4, z5;
    case 4: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y5, z5 ;
    case 5: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y6, z5 ;
    case 6: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y7, z6 ;
    case 7: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y8, z6 ;
    case 8: array[5][i] = (int)random(1,10); break;//gen rand exclude , x6, y9, z6 ;
    }
          fill(0,0,255);
      text(array[5][i],(i*z)+13,(5*z)+22); }
  } 
 
    for(int i=0; i<=8; i++) {
    if(array[6][i] == 0) {
    switch(i) {
    case 0: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y1, z7 ;
    case 1: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y2, z7 ;
    case 2: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y3, z7 ;
    case 3: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y4, z8 ;
    case 4: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y5, z8 ;
    case 5: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y6, z8 ;
    case 6: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y7, z9 ;
    case 7: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y8, z9 ;
    case 8: array[6][i] = (int)random(1,10); break;//gen rand exclude , x7, y9, z9 ;
    }
          fill(0,0,255);
      text(array[6][i],(i*z)+13,(6*z)+22); }
  }   
  
    for(int i=0; i<=8; i++) {
    if(array[7][i] == 0) {
    switch(i) {
    case 0: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y1, z7 ;
    case 1: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y2, z7 ;
    case 2: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y3, z7 ;
    case 3: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y4, z8 ;
    case 4: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y5, z8 ;
    case 5: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y6, z8 ;
    case 6: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y7, z9 ;
    case 7: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y8, z9 ;
    case 8: array[7][i] = (int)random(1,10); break;//gen rand exclude , x8, y9, z9 ;
    }
          fill(0,0,255);
      text(array[7][i],(i*z)+13,(7*z)+22); }
  }   

    for(int i=0; i<=8; i++) {
    if(array[8][i] == 0) {
    switch(i) {
    case 0: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y1, z7 ;
    case 1: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y2, z7 ;
    case 2: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y3, z7 ;
    case 3: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y4, z8 ;
    case 4: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y5, z8 ;
    case 5: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y6, z8 ;
    case 6: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y7, z9 ;
    case 7: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y8, z9 ;
    case 8: array[8][i] = (int)random(1,10); break;//gen rand exclude , x9, y9, z9 ;
    }
          fill(0,0,255);
      text(array[8][i],(i*z)+13,(8*z)+22); }
  } 
  
   int allSumAfter = 0;
   for(int i=0; i<=8; i++) {
    for(int j=0; j<=8; j++) {
    allSumAfter = array[i][j];
    print(allSumAfter+ " ");
   }
   println();
 }
  
   println();
  
  int total = 0;                  // TOTAL ARRAY MUST = 405
  for(int i=0; i<=8; i++) {
    for(int j=0; j<=8; j++) {
   total += Math.pow(array[i][j],2);   
    }
  }
  println("The sum of the whole array is = "+total+" must equal 2565");
  
  double rowTotalx = 0;            // EACH X ROW MUST = 45 or squared.. 285
  for(int i=0; i<=8; i++) {
    rowTotalx += Math.pow(array[0][i],2);
  }
  println("First row squared + sum = "+rowTotalx+" must equal 285 though");
  
  double rowTotaly = 0;            // EACH Y ROW MUST = 45 or squared.. 285
  for(int i=0; i<=8; i++) {
    rowTotaly += Math.pow(array[i][0],2);
  }
  println("First column squared + sum = "+rowTotaly+" must equal 285 though"); 
  
}