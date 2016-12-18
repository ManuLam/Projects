//  Sudoku Solver
//  Man Yiu Lam - 16458032
import javax.swing.*;
import java.awt.*;
import java.lang.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;
JTextField[][] boxes = new JTextField[9][9];
JFrame frame = new JFrame();

  int z = 300/9;
  int[][] array = new int[9][9]; //consists of NINE: 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9   Whole array = 2565 , Row squared = 285
  int[] array2 = new int[9]; // This holds numbers to test against.
  int[] x1 = new int[9]; int[] x2 = new int[9]; int[] x3 = new int[9]; int[] x4 = new int[9]; int[] x5 = new int[9]; int[] x6 = new int[9]; int[] x7 = new int[9]; int[] x8 = new int[9]; int[] x9 = new int[9];    // 1x9 Matrix = 45
  int[] y1 = new int[9]; int[] y2 = new int[9]; int[] y3 = new int[9]; int[] y4 = new int[9]; int[] y5 = new int[9]; int[] y6 = new int[9]; int[] y7 = new int[9]; int[] y8 = new int[9]; int[] y9 = new int[9];    // 9x1 Matrix = 45
  int[] z1 = new int[9]; int[] z2 = new int[9]; int[] z3 = new int[9]; int[] z4 = new int[9]; int[] z5 = new int[9]; int[] z6 = new int[9]; int[] z7 = new int[9]; int[] z8 = new int[9]; int[] z9 = new int[9];    // 3x3 Matrix = 45
  boolean T = true;
  boolean K = true;
  int valve1 = 0;
  int valve2 = 0;
  int valve3 = 0;
  
//PFont Font1;
  
void setup() {      //Solution method for Sudoku. 
  size(298,298);
  background(255);
//  Font1 = createFont("Arial Bold",15);

  for(int i=0; i<=8; i++) {        // creating an array of [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 ] and later removing dupes vs x1 , y1 , z1
    array2[i] = i+1;
  //  print(array2[i]+" ");
  }
  
    framework();
    grids();
         
  
 // given...
  array[0][0] = 9; array[0][1] = 0; array[0][2] = 0;       array[0][3] = 0; array[0][4] = 6; array[0][5] = 1;       array[0][6] = 2; array[0][7] = 8; array[0][8] = 0;
  array[1][0] = 2; array[1][1] = 6; array[1][2] = 8;       array[1][3] = 0; array[1][4] = 0; array[1][5] = 4;       array[1][6] = 7; array[1][7] = 0; array[1][8] = 0;
  array[2][0] = 4; array[2][1] = 0; array[2][2] = 0;       array[2][3] = 5; array[2][4] = 0; array[2][5] = 8;       array[2][6] = 0; array[2][7] = 3; array[2][8] = 9;
  array[3][0] = 0; array[3][1] = 8; array[3][2] = 0;       array[3][3] = 2; array[3][4] = 5; array[3][5] = 0;       array[3][6] = 1; array[3][7] = 4; array[3][8] = 0;
  array[4][0] = 0; array[4][1] = 0; array[4][2] = 4;       array[4][3] = 8; array[4][4] = 1; array[4][5] = 0;       array[4][6] = 0; array[4][7] = 9; array[4][8] = 3;
  array[5][0] = 1; array[5][1] = 5; array[5][2] = 9;       array[5][3] = 0; array[5][4] = 0; array[5][5] = 3;       array[5][6] = 0; array[5][7] = 0; array[5][8] = 6;
  array[6][0] = 5; array[6][1] = 0; array[6][2] = 2;       array[6][3] = 0; array[6][4] = 0; array[6][5] = 7;       array[6][6] = 4; array[6][7] = 0; array[6][8] = 8;
  array[7][0] = 0; array[7][1] = 1; array[7][2] = 0;       array[7][3] = 9; array[7][4] = 4; array[7][5] = 0;       array[7][6] = 0; array[7][7] = 7; array[7][8] = 5;
  array[8][0] = 0; array[8][1] = 4; array[8][2] = 7;       array[8][3] = 1; array[8][4] = 8; array[8][5] = 0;       array[8][6] = 9; array[8][7] = 0; array[8][8] = 0;
  
  
   while(valve1!=1){        // valves or levers allowing my circuit to run even futher by clicking buttons
    print();
  }
  
  for(int i=0; i<=8; i++) {                 // Automatic System ( No need to enter numbers )
  for(int j=0; j<=8; j++) {                             
  boxes[i][j].setText(String.valueOf(array[i][j]));      // This collects all the information from my ARRAY Above and stores it
    }
  }  

  //for(int i=0; i<=8; i++) {               //Manually System ( Enter the Sudoku to be solved )                       
  //for(int j=0; j<=8; j++) {
  //JTextField f1 = boxes[i][j]; String text = f1.getText();    // This collects all the information from my Fieldtext and is stored
  //array[i][j] = Integer.parseInt(text);  
  //  }
  //}         
  
  fullArray();
    
  storeAll();                 // Stores EVERY LINE and Box that is necessary for the solution

  generateNumbersGiven();    // Generates the numbers already given in the Sudoku
  generateGrids();           // Generates all the grids and lines for the 9x9 Sudoku
  
  p=0;  count=0;  drop=0; m=1; n=1;  
  CheckAll();                // Checks all the outcomes and returns information
  println("Number of Open boxes is "+count);      // returns information about Open slots and filled slots
  println("Number of filled boxes is "+drop);     // returns information about Open slots and filled slots
  
  while(valve2!=1){        // valves or levers allowing my circuit to run even futher by clicking buttons
    print();
    }

  while( T == true ) {                            // An infinite loop that only stops when there could be more than 1 possible solution Etc. R2 C2 [2,3] , R5 C6[5,4,2]
  Checking();    // inserts the numbers that has only 1 possible solution Etc. location R4 C5 [5] ,  location R1 R1 [1]
  }

  p=0;  count=0;  drop=0; m=1; n=1;              // reseting the counter

  CheckAll();                                   // Checks all the outcomes and returns information
  println();
  println("Number of Open boxes is "+count);    // returns information about Open slots and filled slots
  println("Number of filled boxes is "+drop);   // returns information about Open slots and filled slots


  println();
  fullArray();    // Showing the full Sudoku In prompt
  
 // showRow(x5);
 // showRow(y5);
 // showRow(z5);
  
  mathsOfArray();      // This shows the entire sum of the whole Sudoku (1^2 + 2^2 + 3^2 .... + 9^2 = 2565
                       // Also show the entire sum of the first row and column and must equal = 285              
}

int c;
ArrayList<Integer> distinctTerms = new ArrayList<Integer>();
ArrayList<Integer> nums = new ArrayList<Integer>();

int n=1 , m=1, p=0 , count=0 , drop=0;
int Check(int a, int b, int x[], int y[], int z[]) {    // Used for information gathering
  distinctTerms.removeAll(distinctTerms);
  nums.removeAll(nums);
  for(int i=0; i<=8; i++) {
    int temp = array2[i];
    distinctTerms.add(temp);
    }
    
   for(int i=0; i<=8; i++) {                // Finding which numbers are needed with array lists.
   int temp1 = x[i];
   int temp2 = y[i];
   int temp3 = z[i];
   nums.add(temp1);
   nums.add(temp2);
   nums.add(temp3);
   distinctTerms.removeAll(nums);
 }
 if(array[a][b] != 0) {
   drop++;
 }
 if(array[a][b] == 0) {
  count++;
  p++;    // used to ONLY COUNT and present the areas where it is empty in (if statement)
 println(p+" ",m+"R",n+"C",distinctTerms); // used to ONLY COUNT and present the areas where it is empty in (if statement)
 }
 n++;
 if(n==10) {
  m++;
  n=1;
 }
 return c;
}

int drop1=0;
int Check2(int a, int b, int x[], int y[], int z[], int f) {    // Used to solve logic 
  
  distinctTerms.removeAll(distinctTerms);
  nums.removeAll(nums);
  for(int i=0; i<=8; i++) {
    int temp = array2[i];
    distinctTerms.add(temp);
    }

   for(int i=0; i<=8; i++) {              // Finding which numbers are needed with array lists.
   int temp1 = x[i];
   int temp2 = y[i];
   int temp3 = z[i];
   nums.add(temp1);
   nums.add(temp2);
   nums.add(temp3);
   distinctTerms.removeAll(nums);
 }
 if(distinctTerms.size()==1 && array[a][b] == 0) {
  creating(a,b,f);
  drop1=0;
  
  storeX(x1 , 0);                    
  storeX(x2 , 1);
  storeX(x3 , 2);
  storeX(x4 , 3);
  storeX(x5 , 4);
  storeX(x6 , 5);
  storeX(x7 , 6);
  storeX(x8 , 7);
  storeX(x9 , 8);
  storeY(y1 , 0);                    
  storeY(y2 , 1);
  storeY(y3 , 2);
  storeY(y4 , 3);
  storeY(y5 , 4);
  storeY(y6 , 5);
  storeY(y7 , 6);
  storeY(y8 , 7);
  storeY(y9 , 8);
  storeZ(z1, 0, 2, 0, 2);                  
  storeZ(z2, 0, 2, 3, 5);
  storeZ(z3, 0, 2, 6, 8);
  storeZ(z4, 3, 5, 0, 2);
  storeZ(z5, 3, 5, 3, 5);
  storeZ(z6, 3, 5, 6, 8);
  storeZ(z7, 6, 8, 0, 2);
  storeZ(z8, 6, 8, 3, 5);
  storeZ(z9, 6, 8, 6, 8);
 }
 
 if(drop1==1000) {
   T = false;
 }
 
 if(array[a][b] != 0) {
   drop1++;
 }
 return c;
}

void CheckAll() {              // checks all outcomes and shows information
Check(0, 0, x1, y1, z1); Check(0, 1, x1, y2, z1); Check(0, 2, x1, y3, z1); 
Check(0, 3, x1, y4, z2); Check(0, 4, x1, y5, z2); Check(0, 5, x1, y6, z2);  
Check(0, 6, x1, y7, z3); Check(0, 7, x1, y8, z3); Check(0, 8, x1, y9, z3);
Check(1, 0, x2, y1, z1); Check(1, 1, x2, y2, z1); Check(1, 2, x2, y3, z1);    
Check(1, 3, x2, y4, z2); Check(1, 4, x2, y5, z2); Check(1, 5, x2, y6, z2);  
Check(1, 6, x2, y7, z3); Check(1, 7, x2, y8, z3); Check(1, 8, x2, y9, z3); 
Check(2, 0, x3, y1, z1); Check(2, 1, x3, y2, z1); Check(2, 2, x3, y3, z1); 
Check(2, 3, x3, y4, z2); Check(2, 4, x3, y5, z2); Check(2, 5, x3, y6, z2);   
Check(2, 6, x3, y7, z3); Check(2, 7, x3, y8, z3); Check(2, 8, x3, y9, z3);
Check(3, 0, x4, y1, z4); Check(3, 1, x4, y2, z4); Check(3, 2, x4, y3, z4);     
Check(3, 3, x4, y4, z5); Check(3, 4, x4, y5, z5); Check(3, 5, x4, y6, z5);     // This mistake messed my code, had to find it without program
Check(3, 6, x4, y7, z6); Check(3, 7, x4, y8, z6); Check(3, 8, x4, y9, z6);
Check(4, 0, x5, y1, z4); Check(4, 1, x5, y2, z4); Check(4, 2, x5, y3, z4);     
Check(4, 3, x5, y4, z5); Check(4, 4, x5, y5, z5); Check(4, 5, x5, y6, z5);     
Check(4, 6, x5, y7, z6); Check(4, 7, x5, y8, z6); Check(4, 8, x5, y9, z6);
Check(5, 0, x6, y1, z4); Check(5, 1, x6, y2, z4); Check(5, 2, x6, y3, z4);     
Check(5, 3, x6, y4, z5); Check(5, 4, x6, y5, z5); Check(5, 5, x6, y6, z5);     
Check(5, 6, x6, y7, z6); Check(5, 7, x6, y8, z6); Check(5, 8, x6, y9, z6);
Check(6, 0, x7, y1, z7); Check(6, 1, x7, y2, z7); Check(6, 2, x7, y3, z7);     
Check(6, 3, x7, y4, z8); Check(6, 4, x7, y5, z8); Check(6, 5, x7, y6, z8);     
Check(6, 6, x7, y7, z9); Check(6, 7, x7, y8, z9); Check(6, 8, x7, y9, z9);
Check(7, 0, x8, y1, z7); Check(7, 1, x8, y2, z7); Check(7, 2, x8, y3, z7);     
Check(7, 3, x8, y4, z8); Check(7, 4, x8, y5, z8); Check(7, 5, x8, y6, z8);     
Check(7, 6, x8, y7, z9); Check(7, 7, x8, y8, z9); Check(7, 8, x8, y9, z9);
Check(8, 0, x9, y1, z7); Check(8, 1, x9, y2, z7); Check(8, 2, x9, y3, z7);     
Check(8, 3, x9, y4, z8); Check(8, 4, x9, y5, z8); Check(8, 5, x9, y6, z8);     
Check(8, 6, x9, y7, z9); Check(8, 7, x9, y8, z9); Check(8, 8, x9, y9, z9);
}

void Checking() {                        // checks for all outcomes + prints onto grids
Check2(0, 0, x1, y1, z1, 0); Check2(0, 1, x1, y2, z1, 0); Check2(0, 2, x1, y3, z1, 0); 
Check2(0, 3, x1, y4, z2, 0); Check2(0, 4, x1, y5, z2, 0); Check2(0, 5, x1, y6, z2, 0);  
Check2(0, 6, x1, y7, z3, 0); Check2(0, 7, x1, y8, z3, 0); Check2(0, 8, x1, y9, z3, 0);
Check2(1, 0, x2, y1, z1, 1); Check2(1, 1, x2, y2, z1, 1); Check2(1, 2, x2, y3, z1, 1);    
Check2(1, 3, x2, y4, z2, 1); Check2(1, 4, x2, y5, z2, 1); Check2(1, 5, x2, y6, z2, 1);  
Check2(1, 6, x2, y7, z3, 1); Check2(1, 7, x2, y8, z3, 1); Check2(1, 8, x2, y9, z3, 1); 
Check2(2, 0, x3, y1, z1, 2); Check2(2, 1, x3, y2, z1, 2); Check2(2, 2, x3, y3, z1, 2); 
Check2(2, 3, x3, y4, z2, 2); Check2(2, 4, x3, y5, z2, 2); Check2(2, 5, x3, y6, z2, 2);   
Check2(2, 6, x3, y7, z3, 2); Check2(2, 7, x3, y8, z3, 2); Check2(2, 8, x3, y9, z3, 2);
Check2(3, 0, x4, y1, z4, 3); Check2(3, 1, x4, y2, z4, 3); Check2(3, 2, x4, y3, z4, 3);     
Check2(3, 3, x4, y4, z5, 3); Check2(3, 4, x4, y5, z5, 3); Check2(3, 5, x4, y6, z5, 3);     
Check2(3, 6, x4, y7, z6, 3); Check2(3, 7, x4, y8, z6, 3); Check2(3, 8, x4, y9, z6, 3);
Check2(4, 0, x5, y1, z4, 4); Check2(4, 1, x5, y2, z4, 4); Check2(4, 2, x5, y3, z4, 4);     
Check2(4, 3, x5, y4, z5, 4); Check2(4, 4, x5, y5, z5, 4); Check2(4, 5, x5, y6, z5, 4);     
Check2(4, 6, x5, y7, z6, 4); Check2(4, 7, x5, y8, z6, 4); Check2(4, 8, x5, y9, z6, 4);
Check2(5, 0, x6, y1, z4, 5); Check2(5, 1, x6, y2, z4, 5); Check2(5, 2, x6, y3, z4, 5);     
Check2(5, 3, x6, y4, z5, 5); Check2(5, 4, x6, y5, z5, 5); Check2(5, 5, x6, y6, z5, 5);     
Check2(5, 6, x6, y7, z6, 5); Check2(5, 7, x6, y8, z6, 5); Check2(5, 8, x6, y9, z6, 5);
Check2(6, 0, x7, y1, z7, 6); Check2(6, 1, x7, y2, z7, 6); Check2(6, 2, x7, y3, z7, 6);     
Check2(6, 3, x7, y4, z8, 6); Check2(6, 4, x7, y5, z8, 6); Check2(6, 5, x7, y6, z8, 6);     
Check2(6, 6, x7, y7, z9, 6); Check2(6, 7, x7, y8, z9, 6); Check2(6, 8, x7, y9, z9, 6);
Check2(7, 0, x8, y1, z7, 7); Check2(7, 1, x8, y2, z7, 7); Check2(7, 2, x8, y3, z7, 7);     
Check2(7, 3, x8, y4, z8, 7); Check2(7, 4, x8, y5, z8, 7); Check2(7, 5, x8, y6, z8, 7);     
Check2(7, 6, x8, y7, z9, 7); Check2(7, 7, x8, y8, z9, 7); Check2(7, 8, x8, y9, z9, 7);
Check2(8, 0, x9, y1, z7, 8); Check2(8, 1, x9, y2, z7, 8); Check2(8, 2, x9, y3, z7, 8);     
Check2(8, 3, x9, y4, z8, 8); Check2(8, 4, x9, y5, z8, 8); Check2(8, 5, x9, y6, z8, 8);     
Check2(8, 6, x9, y7, z9, 8); Check2(8, 7, x9, y8, z9, 8); Check2(8, 8, x9, y9, z9, 8);
}

int storeX (int[] x, int y) {        // Refreshes the array storing and stores to X 1x9 Matrix
    for(int i=0; i<=8; i++) {        // Storing numbers in arrays and later Making restrictions for new numbers
   x[i] = array[y][i]; 
    }
 //   int sum = 0;
   for(int i=0; i<=8; i++) {     // Testing to see if it stored
 //  sum += x[i];
 //   print(x[i]+" ");
 }
 //  println("\n"+sum);
 //  println();
   return c;
  }
  
int storeY (int[] x, int y) {        // Refreshes the array storing and stores to Y 1x9 Matrix
    for(int i=0; i<=8; i++) {        // Storing numbers in arrays and later Making restrictions for new numbers
   x[i] = array[i][y]; 
    }
 //   int sum = 0;
   for(int i=0; i<=8; i++) {     // Testing to see if it stored
 //  sum += x[i];
 //   print(x[i]+" ");
 }
 //  println("\n"+sum);
 //  println();
   return c;
  }  
  
int storeZ (int[] x, int y1, int y2, int z1, int z2) {            // Refreshes the array storing and stores to Z 3x3 matrix
    int n=0;
    for(int i=y1; i<=y2; i++) {  // Z(1-9) created
    for(int j=z1; j<=z2; j++) {
       x[n] = array[i][j];
  //  print(x[n]+" ");   // To show the whole array of Z1 etc. [ 5 3 0
  //                                                             6 0 0
  //                                                             0 9 8 ] in a 3x3 Matrix.
      n++; }
  //     println();
    }
    return c;
  }
  
void storeAll() {        // Storing all the arrays
  storeX(x1 , 0);                    
  storeX(x2 , 1);
  storeX(x3 , 2);
  storeX(x4 , 3);
  storeX(x5 , 4);
  storeX(x6 , 5);
  storeX(x7 , 6);
  storeX(x8 , 7);
  storeX(x9 , 8);
  storeY(y1 , 0);                    
  storeY(y2 , 1);
  storeY(y3 , 2);
  storeY(y4 , 3);
  storeY(y5 , 4);
  storeY(y6 , 5);
  storeY(y7 , 6);
  storeY(y8 , 7);
  storeY(y9 , 8);
  storeZ(z1, 0, 2, 0, 2);                  
  storeZ(z2, 0, 2, 3, 5);
  storeZ(z3, 0, 2, 6, 8);
  storeZ(z4, 3, 5, 0, 2);
  storeZ(z5, 3, 5, 3, 5);
  storeZ(z6, 3, 5, 6, 8);
  storeZ(z7, 6, 8, 0, 2);
  storeZ(z8, 6, 8, 3, 5);
  storeZ(z9, 6, 8, 6, 8);
  
}
  
void generateNumbersGiven(){
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
}

void generateGrids(){
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
}
  
  
void showRow(int x[]) {                      // Shows any row you'd like to view
  for(int i=0; i<=8; i++) {  
  print(x[i]+" "); 
  }
    println();
}

  
void creating (int x, int y, int l) {        // Creates all the numbers on the screen

  array[x][y] = distinctTerms.get(0);
  
      fill(0,0,255);
      text(array[x][y],(y*z)+13,(l*z)+22); 

}

void fullArray() {        // Shows the Entire array
   int allSumAfter = 0;
   for(int i=0; i<=8; i++) {
    for(int j=0; j<=8; j++) {
    allSumAfter = array[i][j];
    print(allSumAfter+ " ");
   }
   println();
 }
   println();
}
void mathsOfArray(){
  int total = 0;                  // TOTAL ARRAY MUST = 2565
  for(int i=0; i<=8; i++) {
    for(int j=0; j<=8; j++) {
   total += Math.pow(array[i][j],2);   
    }
  }
  println("The sum of the whole array is = "+total+" must equal 2565");
  
  double rowTotalx = 0;            // EACH X ROW MUST = 285
  for(int i=0; i<=8; i++) {
    rowTotalx += (int)Math.pow(array[0][i],2);
  }
  println("First row squared + sum = "+(int)rowTotalx+" must equal 285 though");
  
  double rowTotaly = 0;            // EACH Y ROW MUST = 285
  for(int i=0; i<=8; i++) {
    rowTotaly += (int)Math.pow(array[i][0],2);
  }
  println("First column squared + sum = "+(int)rowTotaly+" must equal 285 though"); 
}  

void grids() {          // Making a grid to allow input
frame.setSize(325, 325);
frame.setLayout(new GridLayout(9,9,1,1));
frame.setLocation(500,500);


    for (int i = 0 ; i < 9 ; i++){
        for (int j = 0 ; j < 9 ; j++){
            boxes[i][j] = new JTextField("0");
            JTextField f1 = boxes[i][j]; String text = f1.getText(); 
            array[i][j] = Integer.parseInt(text);
            frame.add(boxes[i][j]).setBounds(0,0,220,30);

        }
    }
    frame.setVisible(true);
}

void framework() {
    JFrame frame = new JFrame("Solution");
    JPanel panel = new JPanel();
    frame.add(panel);
    frame.setSize(50,125);
    JButton button1 = new JButton("Set");
    JButton button2 = new JButton("Solve");
    panel.add(button1);
    panel.add(button2);
    button1.addActionListener(new Action1());      // allowing the button1 to have an action
    button2.addActionListener(new Action2());      // allowing the button2 to have an action
    frame.setVisible(true);
    panel.setVisible(true);
    button1.setVisible(true);
    button2.setVisible(true);
    frame.setLocation(378,500);
}

      class Action1 implements ActionListener{                // Creating a class that recognises the function of the button
      public void actionPerformed(ActionEvent e){
      println("Soduko is Set to");
      valve1=1;
      }
    }
    
     class Action2 implements ActionListener{                // Creating a class that recognises the function of the button
      public void actionPerformed(ActionEvent e){
      println();
      println("Solving for the solution");
      println(".");
      println("..");
      println("...");
      valve2 =1;
      }
    }