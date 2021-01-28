#include <Commander.h>
#include <arduino-timer.h>
#include <ArduinoJson.h>
#include <FastLED.h>


// How many leds in your strip?
#define NUM_LEDS 1

// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 2
#define CLOCK_PIN 3

#define MIN_BRIGHTNESS  0
#define MAX_BRIGHTNESS 255


// Define the array of leds
CRGB leds[NUM_LEDS];


//https://github.com/contrem/arduino-timer

auto timer = timer_create_default(); // create a timer with default settings

bool pumpON = false;
bool pumpOverride = false;
int RGBLED[3] = {0, 0, 0};
int Brightness = 0;
String info = "";

Commander cmd;

String SEPARATOR = ","; //Used as separator for telemetry
//Now the sketch setup, loop and any other functions
void setup() {
  randomSeed(analogRead(0));
  Serial.begin(115200);
  while (!Serial) {
    ; //Wait for the serial port to open (if using USB)
  }
  initialiseCommander();
  cmd.commandPrompt(OFF);                          //enable the command prompt
  cmd.echo(false);                                 //Echo incoming characters to theoutput port
  //Serial.println("Hello: Type 'help' to get help");
  //cmd.printCommandPrompt();
  initTimer();
  initLED();
}

void loop() {
  // put your main code here, to run repeatedly:
  cmd.update();
  timer.tick(); // tick the timer


}


void initLED() {
  int val1 = 0;
  int val2 = 0;
  int val3 = 0;
  FastLED.addLeds<P9813, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);  // BGR ordering is typical
  for (int i = 0; i < 10; i++) {
    val1 = random();
    val2 = random();
    val3 = random();

    leds[0] = CRGB(val2, val3, val1);
    FastLED.show();
    delay(200);
  }
  leds[0] = CRGB::Black;
  FastLED.show();
}
