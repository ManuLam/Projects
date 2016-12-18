//chess
PImage img, piece2 , piece3 , piece4 ,  piece5 , piece6;
PImage piece1a , piece2a , piece3a , piece4a ,  piece5a , piece6a;
int[][] array = new int[8][8];
int z= 640/8;

void setup() {
 img = loadImage("Chess.png");
 piece1 = loadImage("Pawn.png");
 piece2 = loadImage("Bishop.png");
 piece3 = loadImage("Horse.png");
 piece4 = loadImage("Castle.png");
 piece5 = loadImage("Queen.png");
 piece6 = loadImage("King.png");
 
 piece1a = loadImage("PawnBlack.png");
 piece2a = loadImage("BishopBlack.png");
 piece3a = loadImage("HorseBlack.png");
 piece4a = loadImage("CastleBlack.png");
 piece5a = loadImage("QueenBlack.png");
 piece6a = loadImage("KingBlack.png");
 
 size(640,640);
 
 background(img);
 genGrids();
}

void draw() {
  image(piece1,z*0+25,z+8);
  image(piece1,z*1+25,z+8);
  image(piece1,z*2+25,z+8);
  image(piece1,z*3+25,z+8);
  image(piece1,z*4+25,z+8);
  image(piece1,z*5+25,z+8);
  image(piece1,z*6+25,z+8);
  image(piece1,z*7+25,z+8);
  image(piece4,z*0+25,z*0+8);
  image(piece4,z*7+25,z*0+8);
  image(piece3,z*1+25,z*0+6);
  image(piece3,z*5+25,z*0+6);
  image(piece2,z*2+25,z*0+2);
  image(piece2,z*6+25,z*0+2);
  image(piece5,z*3+25,z*0+11);
  image(piece6,z*4+25,z*0+2);
  
  image(piece1a,z*0+25,z*6+8);
  image(piece1a,z*1+25,z*6+8);
  image(piece1a,z*2+25,z*6+8);
  image(piece1a,z*3+25,z*6+8);
  image(piece1a,z*4+25,z*6+8);
  image(piece1a,z*5+25,z*6+8);
  image(piece1a,z*6+25,z*6+8);
  image(piece1a,z*7+25,z*6+8);
  image(piece1a,z*8+25,z*6+8);
  image(piece4a,z*0+25,z*7+8);
  image(piece4a,z*7+25,z*7+8);
  image(piece3a,z*1+25,z*7+6);
  image(piece3a,z*5+25,z*7+6);
  image(piece2a,z*2+25,z*7+2);
  image(piece2a,z*6+25,z*7+2);
  image(piece5a,z*3+25,z*7+11);
  image(piece6a,z*4+25,z*7+2);
  
}

void genGrids() {
  for(int i=0; i<=640; i++) {
    for(int j=0; j<=640; j++) {
      stroke(0);
      strokeWeight(0);
      line(0,i*z,640,i*z);
      line(z*j,0,z*j,640); 
    }
  }
  
}