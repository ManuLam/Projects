import processing.video.*;
Capture cam;
int h = 640;
int w = 550;

void setup() {
  frameRate(60);
   size(640, 550);
  String[]  cameras = Capture.list();
  
   if (cameras.length == 0) {
    println("There are no cameras available for capture.");
    exit();
   }
   else {
    cam = new Capture(this, 640, 480, cameras[1], 30);
    cam.start();
   }
      
}

void draw() {
  if (cam.available() == true) {
    cam.read();
  }
  
background(cam.pixels[((h+(w*cam.width))/2)]);
image(cam, 0 ,0);
ellipse(int(h/2), int(w/2), 7, 7);

}

void mouseClicked() {
  save(hour()+""+minute()+""+second()+"" +".jpg");
}