
//Now the command list must be defined https://github.com/CreativeRobotics/Commander/blob/master/examples/BasicCommands/masterCommands.ino
const commandList_t commands[] = {
  {"setLightRGB", setLightRGB,   "Set color of the LED"},
  {"setLightGrowthON", setLightGrowthON,   "Set LED growth light ON"},
  {"setLightsON", setLightsON,   "Set all lights on"},
  {"setLightsOFF", setLightsOFF,   "Set all lights off"},
  {"setLightBloomON", setLightBloomON,   "Set LED bloomlight ON"},
  {"setLightGrowthOFF", setLightGrowthOFF,   "Set LED growth light ON"},
  {"setLightBloomOFF", setLightBloomOFF,   "Set LED bloomlight ON"},
  {"pumpRunFor",   pumpRunFor,   "Start pump and run for X minutes"},
  {"pumpStart",   pumpStart,   "Start pump"},
  {"pumpStop",    pumpStop,   "Stop pump"},
  {"setBrightness",         setBrightness,   "Set brightness"},
  {"removeOverrides",         removeOverrides,   "Remove all overrides"},
  {"LEDShow",         LEDShow,   "Start a ledshow of n seconds"},
  {"readTDS",         readTDS,   "Read TDS value"},
  {"sysInfo",         sysInfo,   "Prints some information on the system"},

};

// pumpStart
// pumpStop
// pumpRunFor 20
// setBrightness 15
// setLightRGB 23 10 115
// stopAll
// LEDShow 5 0.2
// sysInfo
// readTDS
// sendInfo

// setLightRGB
// setLightGrowthON
// setLightsON
// setLightsOFF
// setLightBloomON
// setLightGrowthOFF
// setLightBloomOFF
// pumpRunFor
// pumpStart
// pumpStop
// setBrightness
// removeOverrides
// LEDShow
// readTDS
// sysInfo


//Initialisation function
void initialiseCommander() {
  cmd.begin(&Serial, commands, sizeof(commands)); //start Commander on Serial
}


void LEDShow(Commander &Cmdr) {
  int val1 = 0;
  int val2 = 0;
  int val3 = 0;
  float freq = 0;
  float dur = 0;
  float values[3] = {0, 0};
  for (int n = 0; n < 2; n++) {
    //try and unpack an int, if it fails there are no more left so exit the loop
    if (Cmdr.getFloat(values[n])) {

    } else break;
  }
  dur = 1000 * values[0];
  freq = 1000 * values[1];

  sendInfo(String("Lightshow started. Duration " + String(dur/1000) + " freq " + String((freq/1000))));
  for (int i = 0; i < dur / freq; i++) {
    val1 = random();
    val2 = random();
    val3 = random();

    leds[0] = CRGB(val2, val3, val1);
    FastLED.show();
    delay(freq);
  }
  leds[0] = CRGB::Black;
  FastLED.show();
  sendInfo(String("Lightshow stopped"));

}

void sendInfo(String info)
{ // for help on dtostrf http://forum.arduino.cc/index.php?topic=85523.0
  //{"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  String line = "";
  line = String("{\"type\":") + String("\"I\",") + "\"message\":" + "\"" + info + "\"" + "}";
  Serial.println(line);
  delay(100);
  //return 0;
}

//this will be an emergency stop
void removeOverrides(Commander &Cmdr)
{

  removePumpOverride();
  removeLightOverride();
  sendInfo(String("Light and pump override manually removed"));

  return 0;
}


bool readTDS(Commander &Cmdr) {
 //temperature = readTemperature();  //add your temperature sensor and read it
  gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
  gravityTds.update();  //sample and calculate
  tdsValue = gravityTds.getTdsValue();  // then get the value
  return 0;
}


bool pumpStop(Commander &Cmdr) {
  if (!pumpOverride)
  { // Here code to swith the pump off
    pumpON = false;
    digitalWrite(PUMP_PIN,HIGH);

    sendInfo(String("Pump stopped"));
  }
  else
  {
    sendInfo(String("Punp cannot stop, pump stop override active"));
  }
  return 0;
}

bool pumpStart(Commander &Cmdr) {
  // Here code to swith the pump on
  digitalWrite(PUMP_PIN,LOW);
  pumpON = true;
  sendInfo(String("Pump start"));
  //setRGBLED(0,0,255);
  return 0;
}


//setLightsON 1 1000
bool setLightsON(Commander &Cmdr) {
  long v[2] = {0, 0};
  for (int n = 0; n < 2; n++) {
    //try and unpack an int, if it fails there are no more left so exit the loop
    if (Cmdr.getInt(v[n])) {
        Serial.println("*");

    } else break;
  }  

  if(!lightOverride){
    digitalWrite(LIGHT_GROWTH_PIN,LOW);
    digitalWrite(LIGHT_BLOOM_PIN,LOW);
    lightGrowthON = true;
    lightBloomON = true;
    sendInfo(String("All lights set to ON"));    
  }
  else {
    sendInfo(String("Tried to set lights ON but override is active"));    
  }

  if(v[0]==1){
    activateLightOverride(v[1]);
    timer.in(v[1] * 1000 - 1, removeLightOverride); 
  }
  // Here code to swith the LED on
  return 0;
}


bool setLightsOFF(Commander &Cmdr) {
    int removeOverride = 0;
    if (Cmdr.getInt(removeOverride)==1){

      removeLightOverride();
    }
    
    if(!lightOverride){
    // Here code to swith the LED on
      digitalWrite(LIGHT_GROWTH_PIN,HIGH);
      digitalWrite(LIGHT_BLOOM_PIN,HIGH);
      lightGrowthON = false;
      lightBloomON = false;
      sendInfo(String("All lights set to OFF"));

  }
  else {
    //sendInfo(String("Tried to set lights OFF but override is active"));    
  }

  return 0;
}

bool setLightGrowthON(Commander &Cmdr) {
  // Here code to swith the LED on
  digitalWrite(LIGHT_GROWTH_PIN,LOW);
  lightGrowthON = true;
  sendInfo(String("Light growth set to ON"));
  return 0;
}

bool setLightBloomON(Commander &Cmdr) {
  // Here code to swith the LED on
  digitalWrite(LIGHT_BLOOM_PIN,LOW);
  lightBloomON = true;
  sendInfo(String("Light bloom set to ON"));
  return 0;
}


bool setLightGrowthOFF(Commander &Cmdr) {
  // Here code to swith the LED on
  digitalWrite(LIGHT_GROWTH_PIN,HIGH);
  lightGrowthON = false;
  sendInfo(String("LED growth set to OFF"));
  return 0;
}

bool setLightBloomOFF(Commander &Cmdr) {
  // Here code to swith the LED on
  digitalWrite(LIGHT_BLOOM_PIN,HIGH);
  lightBloomON = false;
  sendInfo(String("LED bloom set to OFF"));
  return 0;
}

bool removePumpOverride() {
  pumpOverride = false;
  sendInfo(String("Pump override de-activated"));

}

bool removeLightOverride() {
  lightOverride = false;
  sendInfo(String("Light override de-activated"));

}


bool activateLightOverride(long t) {
  lightOverride = true;
  sendInfo(String("Light override activated for ") + String(t) + String(" seconds"));

}


bool pumpRunFor(Commander &Cmdr) {
  long myInt;
  pumpOverride = true;
  if (Cmdr.getInt(myInt)) {
    pumpON = true;
    digitalWrite(PUMP_PIN,LOW);
    timer.in(myInt * 1000 , pumpStop);
    timer.in(myInt * 1000 - 1, removePumpOverride);
    sendInfo(String("Pump started for ") + myInt + String(" seconds"));
    //setRGBLED(0,0,255);

  }
  else
  { sendInfo(String("Command pumpRunFor failed: no duration supplied"));
  }

  return 0;
}


bool setLightsONTime(Commander &Cmdr) {
  String myString = "";
  int itms = Cmdr.countItems();


  if (Cmdr.getString(myString)) {

    sendInfo(String("LED start set fron: ") + myString);

  } else Cmdr.println("Operation failed");

  //Cmdr.chain();
  //Cmdr.printDiagnostics();
  return 0;
}

bool setBrightness(Commander &Cmdr) {
  // Here code to swith the pump on
  long myInt;
  //The server has brigtness range 0-255, the hardware is library dependent. We do not scale but keep the same ranger in the GUI Sx:100=Hx:MAX_BRIGHTNESS
  if (Cmdr.getInt(myInt)) {
    Brightness = myInt;
    FastLED.setBrightness(Brightness);
    FastLED.show();
    sendInfo(String("Brightness set to: ") + myInt + String(" (") + 100*myInt/255 + String("%)"));
  }
  return 0;
}

bool sysInfo(Commander &Cmdr){
  String line = "";
  String commands ="pumpStart, pumpStop, pumpRunFor 2, setBrightness 15, setLightRGB 23 10 115, stopAll, LEDShow 5 0.2, readTDS, sysInfo";
  line = String("{\"type\":") + String("\"S\",") +
                "\"version\":" + VERSION + 
                ",\"baud rate\":" + 
                "\"" + BAUDRATE + 
                "\"" ",\"commands\":" + 
                "\"" + commands + 
                "\"}";

  Serial.println(line);
  delay(100);


}

//setLightRGB 255 255 255
bool setLightRGB(Commander &Cmdr) {
  //create an array to store any values we find
  int values[4] = {0, 0, 0};
  for (int n = 0; n < 3; n++) {
    //try and unpack an int, if it fails there are no more left so exit the loop
    if (Cmdr.getInt(values[n])) {

    } else break;
  }
  //print it out
  String pRGB = "";
  for (int n = 0; n < 3; n++) {
    pRGB = pRGB + String(values[n]) + String(" ");
    RGBLED[n] = values[n];
  }

  leds[0] = CRGB(RGBLED[0], RGBLED[1], RGBLED[2]);
  FastLED.show();
  sendInfo(String("LED set to RGB: ") + pRGB);

  return 0;
}



void TelemetryTX()
{ // for help on dtostrf http://forum.arduino.cc/index.php?topic=85523.0

  String line = "";
  String telemMarker = "T";
  //Need to calculate parameters here because the main loop has a different frequency
  //TxLoopTime = millis() - TxLoopTime;


  line = telemMarker + SEPARATOR +
         String(pumpON) +  SEPARATOR +
         String(RGBLED[0]) + " " + String(RGBLED[1]) + " " + String(RGBLED[2]) +  SEPARATOR +
         String(Brightness) +  SEPARATOR +
         String((float(random(1000, 9999)) / 100)) +  SEPARATOR +

         String(info) +  SEPARATOR;
  Serial.println(line);


  /*line = "T" + SEPARATOR
         + yaw + SEPARATOR
         + pitch + SEPARATOR
         + roll + SEPARATOR
         + heading + SEPARATOR
         + Info
    //+ SEPARATOR
    //+ LastEvent;*/
  //Serial.println(line);

}
 
void TelemetryTXJSON() //statusReport
{ // for help on dtostrf http://forum.arduino.cc/index.php?topic=85523.0
  //{"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  delay(100);
  String line = "";
  line = String("{\"type\":") + String("\"T\",") + "\"pumpON\":" + pumpON + 
                  ",\"lightGrowthON\":" + lightGrowthON + 
                  ",\"lightBloomON\":" + lightBloomON + 
                  ",\"RGB\":" + "\"" + String(RGBLED[0]) + " " + String(RGBLED[1]) + " " + String(RGBLED[2]) +
                  "\"" + ",\"brightness\":" + Brightness +
                  ",\"tds\":" + tdsValue +
                  ",\"pumpOverride\":" + pumpOverride +
                  ",\"lightOverride\":" + lightOverride +

                  "}";
  Serial.println(line);
  //return 0;
}


//Initialisation function
void initTimer() {
  timer.every(1  * 1000, TelemetryTXJSON);

}
