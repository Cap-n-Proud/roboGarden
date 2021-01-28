$fn = 100;
outerDiam = 4;
screwDiam = 2.5;
pilarHeight = 5;

boardX = 200;
boardY = 220;
boardZ = 2;

boardHoleDiam = 10;
boardHoleSpace = 15;

// First is the board x, y second is the position of the first hole
megaDim = [ [ 101.6, 53.34 ], [ 14, 2.5 ] ];

mega = [
  [ 0, 0 ], [ 79.4, 48.26 ], [ 0, 48.26 ], [ 82.55, 0 ], [ 50.8, 0 ],
  [ 50.8, 33 ]
];

unoDim = [ [ 68.58, 53.34 ], [ 2.58, 7.62 ] ];
uno = [ [ 0, 0 ], [ 0, 27.94 ], [ 50.76, 43.18 ] ];
// https://learn.adafruit.com/introducing-the-raspberry-pi-model-b-plus-plus-differences-vs-model-b/mounting-holes
// https://learn.adafruit.com/assets/17950
raspberryDim = [ [ 85.6, 54 ], [ 25.5, 18 ] ];
raspberryBPlus = [ [], [], [], [], [] ];
raspberryB = [ [ 0, 0 ], [ 55.1, 23.5 ] ];
raspberry3 = [ [], [], [], [], [] ];

LEDDiverDim = [ [ 42.5, 24 ], [ 2, 2 ] ];
LEDDriver = [ [ 0, 0 ], [ 36.6, 0 ], [ 0, 20 ], [ 36.6, 20 ] ];

relaisDim = [ [ 70.15, 50 ], [ 3, 3 ] ];
relais = [ [ 0, 0 ], [ 65.72, 0 ], [ 0, 45 ], [ 65.72, 45 ] ];

PHBoardDim = [ [ 40.5, 20 ], [ 1, 1 ] ];
PHBoard = [ [ 0, 0 ], [ 35.7, 0 ], [ 0, 15.7 ], [ 35.7, 15.7 ] ];

module pillar() {
  translate([ 0, 0, boardZ ]) difference() {
    cylinder(h = pilarHeight, d1 = outerDiam, d2 = outerDiam);
    translate([ 0, 0, -1 ])
        cylinder(h = pilarHeight + 2, d1 = screwDiam, d2 = screwDiam);
  }
  cylinder(h = boardZ, d = boardHoleDiam);
}

module mount(component) {

  color("Lime", 1.0) {
    for (i = [0:len(component)]) {
      translate([ component[i][0], component[i][1], 0 ]) pillar();
    }
  }
}

// This prints the pillars and the board footprint
module fullmodule(boardDim, component, base) {

  if (base) {
    cube([ boardDim[0][0], boardDim[0][1], 3 ]);
  }
  translate([ boardDim[1][0], boardDim[1][1], 0 ]) mount(component);
}
// mount(mega);

module holes() {
  for (y = [0:boardHoleDiam +
           boardHoleSpace:boardY - 1 * (boardHoleDiam + boardHoleSpace)]) {

    for (x = [0:boardHoleDiam +
             boardHoleSpace:boardX - 2 * (boardHoleDiam + boardHoleSpace)]) {
      translate([ x, y, 0 ]) cylinder(h = 10, d = boardHoleDiam);
    }
  }
}

module board() {

  color("Gray", 1.0) {
    difference() {
      cube([ boardX, boardY, boardZ ]);
      translate([
        (boardHoleDiam + boardHoleSpace), (boardHoleDiam + boardHoleSpace), -5
      ]) holes();
    }
  }
}

board();
baseShow = false;
// translate([0,0,0])rotate([0,0,0])mount(uno);
translate([ raspberryDim[0][0] + 10, raspberryDim[0][1] + 10, 0 ])
    rotate([ 0, 0, 180 ])
        fullmodule(raspberryDim, raspberryB, baseShow); // mount(raspberryB);
translate([ 70, 120, 0 ]) rotate([ 0, 0, 180 ])
    fullmodule(unoDim, uno, baseShow);

translate([ 180, 10, 0 ]) rotate([ 0, 0, 90 ])
    fullmodule(relaisDim, relais, baseShow);
translate([ 139, 95, 0 ]) rotate([ 0, 0, 0 ])
    fullmodule(LEDDiverDim, LEDDriver, baseShow);
translate([ 139, 135, 0 ]) rotate([ 0, 0, 0 ])
    fullmodule(LEDDiverDim, LEDDriver, baseShow);

translate([ 160, 180, 0 ]) rotate([ 0, 0, 0 ])
    fullmodule(PHBoardDim, PHBoard, baseShow);

// fullmodule(raspberryDim,raspberryB);
// translate([raspberryDim[0][0] + 20,0,0])fullmodule(unoDim,uno);
