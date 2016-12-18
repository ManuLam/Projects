PImage img , image1 , image2;
float OriginX=750 , OriginY=500;  
float angle1=0;
float angle2=0;
float angle3=0;
float angle4=0;
float angle5=0;
float angle6=0;
float angle7=0;
float angle8=0;
float angle9=0;

void setup() {
  size(1500,1000);
  img = loadImage("Space.jpg");
  image1 = loadImage("Sun.png");
  image2 = loadImage("Earth1.png");
  background(img);
}

void draw() {
 background(img);
 
  angle1+=2*(PI/180);               //Mecury
  angle2+=.8*(PI/180);              //Venus
  angle3+=.5*(PI/180);              //Earth
  angle4+=0.233*(PI/180);           //Mars
  angle5+=0.04211862451*(PI/180);   //Jupiter
  angle6+=0.01696254299*(PI/180);   //Saturn
  angle7+=0.0059469499478*(PI/180); //Uranus
  angle8+=0.00300827481*(PI/180);   //Neptune
  

fill(255,155,0);
ellipse(750,500,100,100);

double[][] Pvals = {{-10,10,10,-10} , {-10,-10,10,10}}; //Creating a square at start
Matrix P = new Matrix(Pvals);

//draw_quad(P);  //drawing normal square

double [][] R1vals = {{cos(angle1),-sin(angle1)} , {sin(angle1),cos(angle1)}};    //rotate values
Matrix R1 = new Matrix(R1vals);

double [][] R2vals = {{cos(angle2),-sin(angle2)} , {sin(angle2),cos(angle2)}};
Matrix R2 = new Matrix(R2vals);

double [][] R3vals = {{cos(angle3),-sin(angle3)} , {sin(angle3),cos(angle3)}};
Matrix R3 = new Matrix(R3vals);

double [][] R4vals = {{cos(angle4),-sin(angle4)} , {sin(angle4),cos(angle4)}};
Matrix R4 = new Matrix(R4vals);

double [][] R5vals = {{cos(angle5),-sin(angle5)} , {sin(angle5),cos(angle5)}};
Matrix R5 = new Matrix(R5vals);

double [][] R6vals = {{cos(angle6),-sin(angle6)} , {sin(angle6),cos(angle6)}};
Matrix R6 = new Matrix(R6vals);

double [][] R7vals = {{cos(angle7),-sin(angle7)} , {sin(angle7),cos(angle7)}};
Matrix R7 = new Matrix(R7vals);

double ax =55 , ay=-55;
double [][] Avals = {{ax,ax,ax,ax} , {ay,ay,ay,ay}};      //moves the other square
Matrix A = new Matrix(Avals);

double bx =110 , by=-110;
double [][] Bvals = {{bx,bx,bx,bx} , {by,by,by,by}};      //moves the other square
Matrix B = new Matrix(Bvals);

double cx =165 , cy=-165;
double [][] Cvals = {{cx,cx,cx,cx} , {cy,cy,cy,cy}};      //moves the other square
Matrix C = new Matrix(Cvals);

double dx =220 , dy=-220;
double [][] Dvals = {{dx,dx,dx,dx} , {dy,dy,dy,dy}};      //moves the other square
Matrix D = new Matrix(Dvals);

double ex =275 , ey=-275;
double [][] Evals = {{ex,ex,ex,ex} , {ey,ey,ey,ey}};      //moves the other square
Matrix E = new Matrix(Evals);

double fx =330 , fy=-330;
double [][] Fvals = {{fx,fx,fx,fx} , {fy,fy,fy,fy}};      //moves the other square
Matrix F = new Matrix(Fvals);

double gx =385 , gy=-385;
double [][] Gvals = {{gx,gx,gx,gx} , {gy,gy,gy,gy}};      //moves the other square
Matrix G = new Matrix(Gvals);


Matrix P1=P;             //rotate by normal speed
P1=P1.plus(A);           //translate
P1=R1.times(P1);          //ORBIT P + Normal Speed (R)
draw_quad(P1);           //draw square P2

Matrix P2=P;             //rotate by normal speed
P2=P2.plus(B);           //translate
P2=R2.times(P2);          //ORBIT P + Normal Speed (R)
draw_quad(P2);           //draw square P2

//Matrix P2=P;             //rotate by x2 speed
//P2=P2.plus(A);           //translate
//P2=O.times(P1.plus(A));  //ORBIT P2 + X2 SPEED (O)
//draw_quad(P2);           //draw square P1

Matrix P3=P;             //rotate by 2x speed
P3=P3.plus(A);           //translate
P3=R3.times(P.plus(C)); //ORBIT P
draw_quad(P3);           //draw square P3


Matrix P4=P;             //rotate by 2x speed
P4=P4.plus(A);           //translate
P4=R4.times(P.plus(D)); //ORBIT P
draw_quad(P4);           //draw square P4


Matrix P5=P;             //rotate by 2x speed
P5=P5.plus(A);           //translate
P5=R5.times(P.plus(E)); //ORBIT P
draw_quad(P5);           //draw square P4

Matrix P6=P;             //rotate by 2x speed
P6=P6.plus(A);           //translate
P6=R6.times(P.plus(F)); //ORBIT P
draw_quad(P6);           //draw square P4

Matrix P7=P;             //rotate by 2x speed
P7=P7.plus(A);           //translate
P7=R7.times(P.plus(G)); //ORBIT P
draw_quad(P7);           //draw square P4
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
  //line(X1,Y1,X2,Y2);
  //line(X2,Y2,X3,Y3);
  //line(X3,Y3,X4,Y4);
  //line(X1,Y1,X4,Y4);
  image(image2,(X1+X2+X3+X4)/4,(Y1+Y2+Y3+Y4)/4);
  
}