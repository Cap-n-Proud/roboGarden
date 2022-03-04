// Now the command list must be defined

// https://github.com/CreativeRobotics/Commander/blob/master/examples/BasicCommands/masterCommands.ino
const commandList_t commands[] = {
  {
    "setLightsON",
    setLightsON,
    "Set all lights on"
  },
  {
    "setLightsOFF",
    setLightsOFF,
    "Set all lights off"
  },


  {
    "pumpRunFor",
    pumpRunFor,
    "Start pump and run for X minutes"
  },
  {
    "pumpStop",
    pumpStop,
    "Stop pump"
  },
  {
    "removeOverrides",
    removeOverrides,
    "Remove all overrides"
  },
  {
    "readTDS",
    readTDS,
    "Read TDS value"
  },
  {
    "sysInfo",
    sysInfo,
    "Prints some information on the system"
  },
};


// setLightsON
// setLightsOFF
// pumpRunFor
// pumpStop
// removeOverrides
// sysInfo

// --------------------------------------------------------------------
// Initialisation function
void initialiseCommander() {
  cmd.begin(&Serial, commands, sizeof(commands)); // start Commander on Serial
}

// --------------------------------------------------------------------
void sendInfo(String info) { // for help on dtostrf
                             // http://forum.arduino.cc/index.php?topic=85523.0
  // {"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  String line = "";

  line = String("{\"type\":") + String("\"I\",") + "\"message\":" + "\"" + info +
         "\"" + "}";
  Serial.println(line);
  delay(100);

  // return 0;
}

// --------------------------------------------------------------------
void sendDebug(String info) { // for help on dtostrf
                              // http://forum.arduino.cc/index.php?topic=85523.0
  // {"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  String line = "";

  line = String("{\"type\":") + String("\"D\",") + "\"message\":" + "\"" + info +
         "\"" + "}";
  Serial.println(line);
  delay(100);

  // return 0;
}

// --------------------------------------------------------------------
// this will be an emergency stop
void removeOverrides(Commander& Cmdr) {
  removePumpOverride();
  removeLightOverride();
  sendInfo(String("Light and pump override manually removed"));

  return 0;
}

// --------------------------------------------------------------------
bool readTDS(Commander& Cmdr) {
  // temperature = readTemperature();  //add your temperature sensor and read it
  gravityTds.setTemperature(temperature); // set the temperature and execute
                                          // temperature compensation
  gravityTds.update();                    // sample and calculate
  tdsValue = gravityTds.getTdsValue();    // then get the value
  return 0;
}

// --------------------------------------------------------------------
bool pumpStop(Commander& Cmdr) {
  if (!pumpOverride) { // Here code to swith the pump off
    pumpON = false;
    digitalWrite(PUMP_PIN, HIGH);

    sendInfo(String("Pump stopped"));
  } else {
    sendInfo(String("Pump cannot stop, pump stop override active"));
  }
  return 0;
}

// --------------------------------------------------------------------
// setLightsON 1000
// Set the lights on
bool setLightsON(Commander& Cmdr) {
  int sLOverride = 0;

  if (Cmdr.getInt(sLOverride) > 0) {
    removeLightOverride();
  }

  if (!lightOverride) {
    digitalWrite(LIGHT_GROWTH_PIN, LOW);
    digitalWrite(LIGHT_BLOOM_PIN,  LOW);
    lightGrowthON = true;
    lightBloomON  = true;
    sendInfo(String("All lights set to ON"));
  } else {
    sendDebug(String("Tried to set lights ON but override is active"));
  }

  if (sLOverride > 0) {
    setLightOverride(sLOverride);
  }

  // Here code to swith the LED on
  return 0;
}

// --------------------------------------------------------------------
bool setLightsOFF(Commander& Cmdr) {
  int sLOverride = 0;

  if (Cmdr.getInt(sLOverride) > 0) {
    removeLightOverride();
  }

  if (!lightOverride) {
    // Here code to swith the LED on
    digitalWrite(LIGHT_GROWTH_PIN, HIGH);
    digitalWrite(LIGHT_BLOOM_PIN,  HIGH);
    lightGrowthON = false;
    lightBloomON  = false;
    sendInfo(String("All lights set to OFF"));
  } else {
    sendDebug(String("Tried to set lights OFF but override is active"));
  }

  // Serial.println(sLOverride);
  if (sLOverride > 0) {
    setLightOverride(sLOverride);
  }
  return 0;
}

// --------------------------------------------------------------------
bool removePumpOverride() {
  pumpOverride = false;
  sendInfo(String("Pump override de-activated"));
}

// --------------------------------------------------------------------
bool removeLightOverride() {
  lightOverride = false;
  sendInfo(String("Light override de-activated"));
}

// --------------------------------------------------------------------
// Used to tell the scheduler that lights needs to be on outside schedule hours
bool setLightOverride(long t) {
  lightOverride = true;
  timer.in(t * 1000 - 1, removeLightOverride);

  sendInfo(String("Light override activated for ") + String(t) + String(
             " seconds"));
}

// --------------------------------------------------------------------
bool pumpRunFor(Commander& Cmdr) {
  long myInt;

  pumpOverride = true;

  if (Cmdr.getInt(myInt)) {
    pumpON = true;
    digitalWrite(PUMP_PIN, LOW);
    timer.in(myInt * 1000,     pumpStop);
    timer.in(myInt * 1000 - 1, removePumpOverride);
    sendInfo(String("Pump started for ") + myInt + String(" seconds"));

    // setRGBLED(0,0,255);
  } else {
    sendInfo(String("Command pumpRunFor failed: no duration supplied"));
  }

  return 0;
}

// --------------------------------------------------------------------
bool sysInfo(Commander& Cmdr) {
  String line     = "";
  String commands =
    "pumpStart, pumpStop, pumpRunFor 2, setBrightness 15, setLightRGB 23 10 115, stopAll, LEDShow 5 0.2, readTDS, sysInfo";

  line = String("{\"type\":") + String("\"S\",") +
         "\"version\":" + VERSION +
         ",\"baud rate\":" +
         "\"" + BAUDRATE +
         "\""
         ",\"commands\":" +
         "\"" + commands +
         "\"}";

  Serial.println(line);
  delay(100);
}

// --------------------------------------------------------------------
void TelemetryTXJSON() // statusReport
{                      // for help on dtostrf
                       // http://forum.arduino.cc/index.php?topic=85523.0
  // {"type": "I", "pumpON":1,"RGB": "20 255 30","brightness":80}
  delay(100);
  String line = "";
  line = String("{\"type\":") + String("\"T\",") + "\"pumpON\":" + pumpON +
         ",\"lightGrowthON\":" + lightGrowthON +
         ",\"lightBloomON\":" + lightBloomON +
         ",\"tds\":" + tdsValue +
         ",\"pumpOverride\":" + pumpOverride +
         ",\"lightOverride\":" + lightOverride +
         ",\"timestamp\":" + millis()
         "}";
  Serial.println(line);

  // return 0;
}

// --------------------------------------------------------------------
// Initialisation function
void initTimer() {
  timer.every(TELEMTRY_PERIOD * 1000, TelemetryTXJSON);
}
