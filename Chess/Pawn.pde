PImage piece1;
class Pawn {
Pawn(){
piece1 = loadImage("Pawn.png");
image(piece1,z*0+25,z+8);
}

void pawn(int i) {
  image(piece1,z*i+25,z+8);
  pawn(1);
}
  
  
}