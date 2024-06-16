/*////
 * Auther:  Elijah Lovsey
 * Date:    9/10/2019
 * Email:   Elovsey@gmail.com
 * Version: 1.0.2
/*/////

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif
// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 14
// Which pin on the Arduino is connected to the NeoPixels?
#define LED_PIN    2

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

//DO NOT CHANGE BELOW.

const int trigerdistance = 32; // distance until timer starts in inches.
const int timeLength = 0.5; // time for LED change in seconds.
const int trigPin  = 3; //UltraSonic Triger Pin
const int echoPin  = 4; //UltraSonic Echo Pin
float     distance = 0;//reference do not delete
float     TimerA   = 0;//reference do not delete
float     flip = 0;//var for loop flip

void setup()
{
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(255); // Set BRIGHTNESS to about 1/5 (max = 255)Serial.begin (9600); 
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  //  pinMode(BlueLED, OUTPUT);
  //  pinMode(RedLED, OUTPUT);
}

void sendtorasberypi(String message) {
  Serial.println(message);
}

void loop() {
  distance = getDistance();  
  sendtorasberypi("\n"); 
  // Serial.print(distance);     
  // Serial.println(" in"); 
  // Serial.print("TimerA ");
  // Serial.println(TimerA);
  delay(50);
  if (flip == 1) {
    blue();
  }
  else {
    red();
  }
}

void blue() {
   if (distance <= 8) {
    // Fill along the length of the strip in various colors...
    colorWipe(strip.Color(255,   0,   0), 50); // Red
    flip = 0; 
    sendtorasberypi("RED\n");
    delay(3000);
  } 
}
void red() {
   if (distance <= 8) {
    // Fill along the length of the strip in various colors...
    colorWipe(strip.Color(  0,   0, 255), 50); // Blue
    flip = 1; 
    sendtorasberypi("BLUE\n");
    delay(3000);
  } 

}
  
// Ok I give up Do what you want.

float getDistance()
{
  float echoTime;
  float calculatedDistance;
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  echoTime = pulseIn(echoPin, HIGH);
  calculatedDistance = echoTime / 148.0;
  return calculatedDistance;
}
void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}
