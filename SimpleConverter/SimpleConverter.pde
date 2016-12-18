import controlP5.*;
ControlP5 cp5;
String textValue = "";
PImage img;
String sen1 = "Enter Binary";
String sen2 = "Enter Hexa";
String sen3 = "Enter Decimal";
void setup() {
  size(300,600);
  img = loadImage("image.png");
   background(img);
   cp5 = new ControlP5(this);
   
    cp5.addTextfield("1").setPosition(100, 70).setSize(100, 50).setFocus(true).setColor(color(255, 0, 0));
    cp5.addBang("DecToHex").setPosition(210, 70).setSize(80, 40);     
    cp5.addBang("DecToBinary").setPosition(210, 130).setSize(80, 40);   
    
    cp5.addTextfield("2").setPosition(100, 270).setSize(100, 50).setFocus(true).setColor(color(255, 0, 0));
    cp5.addBang("BinToDecimal").setPosition(210, 270).setSize(80, 40);     
    cp5.addBang("BinToHex").setPosition(210, 330).setSize(80, 40);  
    
    cp5.addTextfield("3").setPosition(100, 470).setSize(100, 50).setFocus(true).setColor(color(255, 0, 0));
    cp5.addBang("HexToDecimal").setPosition(210, 470).setSize(80, 40);     
    cp5.addBang("HexToBinary").setPosition(210, 530).setSize(80, 40);  
    

  
}

void draw() {
  background(img);
  fill(0,100,200,50);
  rect(100,10,100,50);
  
  fill(0,100,200,50);
  rect(100,210,100,50);
  
  fill(0,100,200,50);
  rect(100,410,100,50);
  
  fill(0);
  text(sen1,120,240);
  fill(0);
  text(sen2,120,440);
  fill(0);
  text(sen3,110,40);
}
  
  void mousePressed() {
  
if(mouseX>100 && mouseX<200 && mouseY>100 && mouseY<150) {
   fill(255,255,0);
  rect(100,300,100,50);
  }
}

void DecToHex() {
 String num =cp5.get(Textfield.class,"1").getText();
 int number = Integer.parseInt(num);
 println(hex(number));
}

void DecToBinary() {
 String num =cp5.get(Textfield.class,"1").getText();
 int number = Integer.parseInt(num);
 println(binary(number));
}



void BinToDecimal() {
 String num =cp5.get(Textfield.class,"2").getText();
 println(unbinary(num));
}

void BinToHex() {
 String num =cp5.get(Textfield.class,"2").getText();
 int number = unbinary(num);
 println(hex(number));
}



void HexToDecimal() {
 String num =cp5.get(Textfield.class,"3").getText();
 println(unhex(num));
}

void HexToBinary() {
 String num =cp5.get(Textfield.class,"3").getText();
 int number = unhex(num);
 println(binary(number));
}