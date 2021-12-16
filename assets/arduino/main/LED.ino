// This is a placeholder for a LED module. I removed the LED relevant routines

// to keep the main serial_comm.ino file clean
// Now the command list must be defined
// https://github.com/CreativeRobotics/Commander/blob/master/examples/BasicCommands/masterCommands.ino
const commandList_t commands[] = {
  {
    "setLightRGB",
    setLightRGB,
    "Set color of the LED"
  },
  {
    "setLightGrowthON",
    setLightGrowthON,
    "Set LED growth light ON"
  },
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
    "setLightBloomON",
    setLightBloomON,
    "Set LED bloomlight ON"
  },
  {
    "setLightGrowthOFF",
    setLightGrowthOFF,
    "Set LED growth light ON"
  },
  {
    "setLightBloomOFF",
    setLightBloomOFF,
    "Set LED bloomlight ON"
  },
  {
    "pumpRunFor",
    pumpRunFor,
    "Start pump and run for X minutes"
  },
  {
    "pumpStart",
    pumpStart,
    "Start pump"
  },
  {
    "pumpStop",
    pumpStop,
    "Stop pump"
  },
  {
    "setBrightness",
    setBrightness,
    "Set brightness"
  },
  {
    "removeOverrides",
    removeOverrides,
    "Remove all overrides"
  },
  {
    "LEDShow",
    LEDShow,
    "Start a ledshow of n seconds"
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

void LEDShow(Commander& Cmdr) {
  int   val1      = 0;
  int   val2      = 0;
  int   val3      = 0;
  float freq      = 0;
  float dur       = 0;
  float values[3] = {
    0,
    0
  };

  for (int n = 0; n < 2; n++) {
    // try and unpack an int, if it fails there are no more left so exit the
    // loop
    if (Cmdr.getFloat(values[n])) {} else break;
  }
  dur  = 1000 * values[0];
  freq = 1000 * values[1];

  sendInfo(String("Lightshow started. Duration " + String(dur / 1000) + " freq " +
                  String((freq / 1000))));

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
