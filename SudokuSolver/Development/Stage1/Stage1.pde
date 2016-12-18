//  Sudoku Solver
//  Man Yiu Lam - 16458032
int x = 100/3;
int y = 100/3;
int sum = 0;
int count = 0;

int[][] array = new int[9][9];

void setup() {
  size(300,300);
  background(255);
  


   for(int a=0; a<=8; a++) {
   for(int b=0; b<=8; b++) {
     array[a][b] = (int(random(1,9)));
   }
   }


    for(int j=22; j<=300;) {
    int a=0;
    for(int i=13; i<=300;) {  
    int b=0;
    
     fill(0); text(array[a][b],i,j);
   
  i += 300/9;
  b++;
  }
  j += 300/9;
  a++;
  }
  
   
  for(int i =0; i<=8; i++) {
  sum += array[0][i];
 }
  
  
  for(int j=0; j<=8; j++) {
 if(array[0][j] == 1 ) {
   count++;
 }
  }
   println(array[0][0]);
   println(count);
  
  strokeWeight(3);
  stroke(0);
  line(0,0,0,300);
  line(0,0,300,0);
  line(300,0,298,300);
  line(0,298,298,298);
  line(100,0,100,300);
  line(200,0,200,300);
  line(0,100,300,100);
  line(0,200,300,200);    // black lines (thick)
  
  stroke(0);
  strokeWeight(0);
  
  for(int i=0; i<300; i++) {
    for(int j=0; j<300; j++)  {
    stroke(0);
    strokeWeight(0);
    line(0,i*y,300,i*y);
    line(x*j,0,x*j,300);
    }
  }
}


void draw() {
  
}