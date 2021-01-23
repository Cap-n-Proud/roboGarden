
//Now the command list must be defined https://github.com/CreativeRobotics/Commander/blob/master/examples/BasicCommands/masterCommands.ino
const commandList_t commands[] = {
  {"setLightRGB", setLightRGB,   "Set color of the LED"},
  {"pumpRunFor",   pumpRunFor,   "Start pump and run for X minutes"},
  {"pumpStart",   pumpStart,   "Start pump"},
  {"pumpStop",    pumpStop,   "Stop pump"},
  {"setBrightness",         setBrightness,   "Set brightness"},
};

// pumpStart
// pumpStop
// setBrightness 15
// setLightRGB 23 10 115
// printSysInfo => TBD
// sendInfo

//Initialisation function
void initialiseCommander(){
  cmd.begin(&Serial, commands, sizeof(commands)); //start Commander on Serial
}

void sendInfo(String info)
{ // for help on dtostrf http://forum.arduino.cc/index.php?topic=85523.0
  //{"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  delay(100);
  String line = "";
  line = String("{\"type\":") + String("\"I\",") + "\"message\":" + "\"" + info + "\"" + "}";
  Serial.println(line);
  //return 0;
}


bool pumpStop(Commander &Cmdr){
  // Here code to swith the pump on
  pumpON = false;
  sendInfo(String("Pump stopped"));
  return 0;
}

bool pumpStart(Commander &Cmdr){
  // Here code to swith the pump on
  pumpON = true;
  sendInfo(String("Pump start"));
  return 0;
}

bool pumpRunFor(Commander &Cmdr){
  long myInt;
  if(Cmdr.getInt(myInt)){
    //Cmdr.print("Pump timer set to: ");
    //Cmdr.println(myInt);
  pumpON = true;
  timer.in(myInt * 1000 * 60, pumpStop);
  sendInfo(String("Pump started for: ") + myInt + String(" minutes"));
  }

  return 0;
}


bool setLightsONTime(Commander &Cmdr){
  String myString = "";
  int itms = Cmdr.countItems();


    if(Cmdr.getString(myString)){

        sendInfo(String("LED start set fron: ") + myString);

    }else Cmdr.println("Operation failed");

  //Cmdr.chain();
  //Cmdr.printDiagnostics();
  return 0;
}

bool setBrightness(Commander &Cmdr){
  // Here code to swith the pump on
   int myInt;
  if(Cmdr.getInt(myInt)){
    //Cmdr.print("Brightness set to: ");
   // Cmdr.println(myInt);
   Brightness = myInt;
  sendInfo(String("Brightness set to: ") + myInt + String("%"));
}

  return 0;
}


//setLightRGB 255 255 255
bool setLightRGB(Commander &Cmdr){
  //create an array to store any values we find
  int values[4] = {0,0,0};
  for(int n = 0; n < 3; n++){
    //try and unpack an int, if it fails there are no more left so exit the loop
    if(Cmdr.getInt(values[n])){

    }else break;
  }
  //print it out
  String pRGB ="";
  for(int n = 0; n < 3; n++){
    pRGB = pRGB + String(values[n]) + String(" ");
    RGB[n] = values[n];}
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
           String(RGB[0]) + " " + String(RGB[1]) + " " + String(RGB[2]) +  SEPARATOR +
           String(Brightness) +  SEPARATOR +
           String((float(random(1000,9999))/100)) +  SEPARATOR +

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
  line = String("{\"type\":") + String("\"T\",") + "\"pumpON\":" + pumpON + ",\"RGB\":" + "\"" + String(RGB[0]) + " "+ String(RGB[1]) + " " + String(RGB[2]) + "\"" + ",\"brightness\":" + Brightness + "}";
  Serial.println(line);
  //return 0;
}


//Initialisation function
void initTimer(){
  timer.every(0.5  * 1000, TelemetryTXJSON);

}
