//Man Yiu Lam , 28/09/17
//Updated Sudoku Solver full Recursive Backtracking System
import java.util.*;
 int[][] array = new int[9][9];

void setup() {
  //Extremely hard Sudoku puzzle given
  array[0][0] = 0; array[0][1] = 0; array[0][2] = 0;       array[0][3] = 0; array[0][4] = 0; array[0][5] = 7;       array[0][6] = 0; array[0][7] = 1; array[0][8] = 6;
  array[1][0] = 0; array[1][1] = 0; array[1][2] = 0;       array[1][3] = 0; array[1][4] = 6; array[1][5] = 0;       array[1][6] = 7; array[1][7] = 9; array[1][8] = 3;
  array[2][0] = 0; array[2][1] = 0; array[2][2] = 0;       array[2][3] = 0; array[2][4] = 0; array[2][5] = 0;       array[2][6] = 0; array[2][7] = 0; array[2][8] = 0;
  
  array[3][0] = 0; array[3][1] = 0; array[3][2] = 0;       array[3][3] = 0; array[3][4] = 0; array[3][5] = 0;       array[3][6] = 0; array[3][7] = 0; array[3][8] = 0;
  array[4][0] = 9; array[4][1] = 0; array[4][2] = 0;       array[4][3] = 6; array[4][4] = 0; array[4][5] = 1;       array[4][6] = 0; array[4][7] = 5; array[4][8] = 0;
  array[5][0] = 0; array[5][1] = 0; array[5][2] = 3;       array[5][3] = 0; array[5][4] = 0; array[5][5] = 0;       array[5][6] = 8; array[5][7] = 2; array[5][8] = 1;
  
  array[6][0] = 0; array[6][1] = 0; array[6][2] = 4;       array[6][3] = 0; array[6][4] = 8; array[6][5] = 6;       array[6][6] = 0; array[6][7] = 0; array[6][8] = 0;
  array[7][0] = 0; array[7][1] = 1; array[7][2] = 5;       array[7][3] = 9; array[7][4] = 2; array[7][5] = 0;       array[7][6] = 0; array[7][7] = 0; array[7][8] = 0;
  array[8][0] = 0; array[8][1] = 0; array[8][2] = 9;       array[8][3] = 0; array[8][4] = 4; array[8][5] = 0;       array[8][6] = 0; array[8][7] = 0; array[8][8] = 0;
  
  showArray(array);
   println();
  solver(array);    //solve the sudoku

}


boolean solver(int[][] a) {
 if(solve(a)==true) {
    solve(a);
    println();
    showArray(a);                  //solved solution
    
    return true;
   }
   
   showArray(a);        
   print("Cannot be solved");      //cannot be solved
  return false;
}


boolean solve(int[][] a) {
   int row = 0; int column = 0;      //setting row and column variables
   
   for(int i = 0; i < a.length; i++) {
   for(int j = 0; j < a.length; j++) {
     if(a[i][j] == 0 ) {        
       row = i; column = j;          //finding empty locations in the array
         }
       }
    }
   
  if(emptyLocation(a)) return true;    //if there are no empty slots, the sudoku is solved
    
  for(int n = 1; n <= 9; n++) {        //1-9 number set
      if(canPlace(a, row, column, n)) {//1-9 number set excluding row / column / matrix
        a[row][column] = n;            //set number to the location
     
        if(solve(a)) return true;      //recursion that repeats the process until the entire array is solved
    
        a[row][column] = 0;            //backtracks the element that couldn't continue the array to 0
            }
        }
      
  return false;                        //sudoku puzzle cannot be solved
}


boolean canPlace(int[][] a, int row, int column, int n) {            //Method for Exception cases, excluding row / column / matrix
 for(int i = 0; i < a.length; i++) {
   if(a[row][i] == n) return false;                     //if number is already used in row, return false
   if(a[i][column] == n) return false;                  //if number is already used in column, return false
 }
 for(int i = 0; i < 3; i++) {
   for(int j = 0; j < 3; j++) {
     if(a[i+(row-row%3)][j+(column-column%3)] == n) return false;    //Hard code to find the 3x3 matrix its in and exclude all number elements from it
   }
 }
  return true;      //if none are used, n may be used
}


void showArray(int[][] a) {            //Method for displaying the entire array
 for(int i = 0; i < a.length; i++) {
  for(int j = 0; j < a.length; j++) {
    print(a[i][j]+" ");
     }
     println();
   }
}
  
boolean emptyLocation(int[][]a) {      //Method for finding an empty space int the array
 for(int i = 0; i < a.length; i++) {  
   for(int j = 0; j < a.length; j++) {
     if(a[i][j] == 0 ) {
       return false;
           }
       } 
   }
   return true;
}