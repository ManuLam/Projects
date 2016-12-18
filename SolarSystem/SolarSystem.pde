PImage img , image1;
float OriginX=750 , OriginY=500;  
float angle=0;
float angle2=0;

void setup() {
  size(1500,1000);
  img = loadImage("Space.jpg");
  image1 = loadImage("Sun.png");
  background(img);
}

void draw() {
 background(img);

  angle+=(PI/180);    //Normal speed
  angle2+=(PI/180);   //x2 speed

fill(255,155,0);
ellipse(750,500,100,100);

double[][] Pvals = {{-10,10,10,-10} , {-10,-10,10,10}}; //Creating a square at start
Matrix P = new Matrix(Pvals);

draw_quad(P);  //drawing normal square

double [][] Rvals = {{cos(angle),-sin(angle)} , {sin(angle),cos(angle)}};    //rotate values
Matrix R = new Matrix(Rvals);

double [][] Ovals = {{cos(angle2),-sin(angle2)} , {sin(angle2),cos(angle2)}};
Matrix O = new Matrix(Ovals);

double ax =75 , ay=-50;
double [][] Avals = {{ax,ax,ax,ax} , {ay,ay,ay,ay}};      //moves the other square
Matrix A = new Matrix(Avals);

double bx =250 , by=-150;
double [][] Bvals = {{bx,bx,bx,bx} , {by,by,by,by}};      //moves the other square
Matrix B = new Matrix(Bvals);

double cx =300 , cy=-200;
double [][] Cvals = {{cx,cx,cx,cx} , {cy,cy,cy,cy}};      //moves the other square
Matrix C = new Matrix(Cvals);

double dx =350 , dy=-250;
double [][] Dvals = {{dx,dx,dx,dx} , {dy,dy,dy,dy}};      //moves the other square
Matrix D = new Matrix(Dvals);

Matrix P2=P;             //rotate by normal speed
P2=P2.plus(A);           //translate
P2=O.times(P2);          //ORBIT P + Normal Speed (R)
draw_quad(P2);           //draw square P2

//Matrix P1=P;             //rotate by x2 speed
//P1=P1.plus(A);           //translate
//P1=O.times(P2.plus(A));  //ORBIT P2 + X2 SPEED (O)
//draw_quad(P1);           //draw square P1

Matrix P3=P;             //rotate by 2x speed
P3=P3.plus(A);           //translate
P3=R.times(P.plus(B)); //ORBIT P
draw_quad(P3);           //draw square P3


Matrix P4=P;             //rotate by 2x speed
P4=P4.plus(A);           //translate
P4=R.times(P.plus(C)); //ORBIT P
draw_quad(P4);           //draw square P4


Matrix P5=P;             //rotate by 2x speed
P5=P5.plus(A);           //translate
P5=R.times(P.plus(D)); //ORBIT P
draw_quad(P5);           //draw square P4
}


void draw_quad(Matrix P) {
  fill(255);
  stroke(255);
  float X1=(float)P.get(0,0)+OriginX;
  float Y1=(float)P.get(1,0)+OriginY;
  float X2=(float)P.get(0,1)+OriginX;
  float Y2=(float)P.get(1,1)+OriginY;
  float X3=(float)P.get(0,2)+OriginX;
  float Y3=(float)P.get(1,2)+OriginY;
  float X4=(float)P.get(0,3)+OriginX;
  float Y4=(float)P.get(1,3)+OriginY;
  
  line(X1,Y1,X2,Y2);
  line(X2,Y2,X3,Y3);
  line(X3,Y3,X4,Y4);
  line(X1,Y1,X4,Y4);
}