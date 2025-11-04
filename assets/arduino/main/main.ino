#include <Commander.h>
#include <arduino-timer.h>
#include <ArduinoJson.h>
#include "GravityTDS.h"

// How many leds in your strip?
#define NUM_LEDS 1

// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 2
#define CLOCK_PIN 3
#define PUMP_PIN 53
#define LIGHT_GROWTH_PIN 52
#define LIGHT_BLOOM_PIN 51
#define TDS_SENSOR_PIN A1
#define MIN_BRIGHTNESS 0
#define MAX_BRIGHTNESS 255

#define VERSION "1.1.2"
#define BAUDRATE 115200
#define TELEMTRY_PERIOD 1

auto timer = timer_create_default(); // create a timer with default settings

bool pumpON = false;
bool pumpOverride = false;
bool lightOverride = false;
bool lightGrowthON = false;
bool lightBloomON = false;
float temperature = 25, tdsValue = 0;
float PUMP_MAX_RUN = 90; // Max time the pump can run

String info = "";

Commander cmd;
GravityTDS gravityTds;

String SEPARATOR = ","; // Used as separator for telemetry
// Now the sketch setup, loop and any other functions
void setup()
{
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LIGHT_GROWTH_PIN, OUTPUT);
  pinMode(LIGHT_BLOOM_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  digitalWrite(LIGHT_GROWTH_PIN, HIGH);
  digitalWrite(LIGHT_BLOOM_PIN, HIGH);

  randomSeed(analogRead(0));
  Serial.begin(BAUDRATE);

  while (!Serial)
  {
    // Wait for the serial port to open (if using USB)
  }
  initialiseCommander();
  cmd.commandPrompt(OFF); // enable the command prompt
  cmd.echo(false);        // Echo incoming characters to the output port
  // Serial.println("Hello: Type 'help' to get help");
  // cmd.printCommandPrompt();
  initTimer();
  initTDS();
}

void loop()
{
  // put your main code here, to run repeatedly:
  cmd.update();
  timer.tick(); // tick the timer
}

void initTDS()
{
  gravityTds.setPin(TDS_SENSOR_PIN);
  gravityTds.setAref(5.0);      // reference voltage on ADC, default 5.0V on
                                // Arduino UNO
  gravityTds.setAdcRange(1024); // 1024 for 10bit ADC;4096 for 12bit ADC
  gravityTds.begin();           // initialization
}
