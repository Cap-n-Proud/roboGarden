#include <Commander.h>
#include <arduino-timer.h>
#include <ArduinoJson.h>


//https://github.com/contrem/arduino-timer

auto timer = timer_create_default(); // create a timer with default settings

bool pumpON = false;
int RGB[3] = {0,0,0};
int Brightness = 0;
String info = "";

Commander cmd;

String SEPARATOR = ","; //Used as separator for telemetry
//Now the sketch setup, loop and any other functions
void setup() {
  
  randomSeed(analogRead(0));
  Serial.begin(115200);
  while(!Serial){;}                               //Wait for the serial port to open (if using USB)
  initialiseCommander();
  cmd.commandPrompt(OFF);                          //enable the command prompt
  cmd.echo(false);                                 //Echo incoming characters to theoutput port
  //Serial.println("Hello: Type 'help' to get help");
  //cmd.printCommandPrompt();
  initTimer();

}

void loop() {
  // put your main code here, to run repeatedly:
  cmd.update();
  timer.tick(); // tick the timer
  

}
