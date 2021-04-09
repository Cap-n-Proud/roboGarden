$fn = 50;
outerDiam = 6;
screwDiam = 3;
pilarHeight = 8;

boardX = 180;
boardY = 180;
boardZ = 2.4;

boardHoleDiam = 25;
boardHoleSpace = 0.2 * boardHoleDiam;

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
LEDDriver = [ [ 0, 0 ], [ 37.6, 0 ], [ 0, 20 ], [ 37.6, 20 ] ];

relaisDim = [ [ 70.15, 50 ], [ 3, 3 ] ];
relais = [ [ 0, 0 ], [ 65.72, 0 ], [ 0, 45 ], [ 65.72, 45 ] ];

PHBoardDim = [ [ 40.5, 20 ], [ 1, 1 ] ];
PHBoard = [ [ 0, 0 ], [ 35.7, 0 ], [ 0, 15.7 ], [ 35.7, 15.7 ] ];

module pillar(base) {
  translate([ 0, 0, boardZ ]) difference() {
    cylinder(h = pilarHeight, d1 = outerDiam, d2 = outerDiam);
    translate([ 0, 0, -1 ])
        cylinder(h = pilarHeight + 2, d1 = screwDiam, d2 = screwDiam);
  }
  if(base){
  cylinder(h = boardZ, d = boardHoleDiam/2);}
}

module mount(component,basePillar) {

  color("Lime", 1.0) {
    for (i = [0:len(component)]) {
      translate([ component[i][0], component[i][1], 0 ]) pillar(basePillar);
    }
  }
}

// This prints the pillars and the board footprint
module fullmodule(boardDim, component, base,basePillar) {

  if (base) {
    cube([ boardDim[0][0], boardDim[0][1], 3 ]);
  }
  translate([ boardDim[1][0], boardDim[1][1], 0 ]) mount(component,basePillar);
}
// mount(mega);

module holes() {
  for (y = [0:boardHoleDiam +
           boardHoleSpace:boardY - 2 * (boardHoleDiam + boardHoleSpace)]) {

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


module baseSupport(){
    cube([boardX/2-0.2*boardX,10,20]);
    
    
}


module electronicsBase(){
board();
baseShow = false;
basePillar = true;
basePPH = false;
// translate([0,0,0])rotate([0,0,0])mount(uno);
translate([ raspberryDim[0][0] + 10, raspberryDim[0][1] + 10, 0 ])
    rotate([ 0, 0, 180 ])
        fullmodule(raspberryDim, raspberryB, baseShow,basePillar); // mount(raspberryB);
translate([ 70, 120, 0 ]) rotate([ 0, 0, 180 ])
    fullmodule(unoDim, uno, baseShow, basePillar);

translate([ 170, 10, 0 ]) rotate([ 0, 0, 90 ])
    fullmodule(relaisDim, relais, baseShow, basePillar);
translate([ 129, 95, 0 ]) rotate([ 0, 0, 0 ])
    fullmodule(LEDDiverDim, LEDDriver, baseShow, basePillar);
//translate([ 129, 135, 0 ]) rotate([ 0, 0, 0 ])
//    fullmodule(LEDDiverDim, LEDDriver, baseShow, basePillar);

translate([ 140, 155, 0 ]) rotate([ 0, 0, 0 ])
    fullmodule(PHBoardDim, PHBoard, baseShow, basePPH);

// fullmodule(raspberryDim,raspberryB);
// translate([raspberryDim[0][0] + 20,0,0])fullmodule(unoDim,uno);
}


//baseSupport();
//pillar();

boxX = 80;
boxY = 100;
boxZ = 30;
boxThickness = 3;


//OpenScad D-Sub Library by stevetheprinter
//Published on February 2, 2018
//www.thingiverse.com/thing:2779088

// sc = scale, set larger if your part doesn't fit. default is the exact dimensions of the connector housing. recomended 1.1 for most mounting holes,
// sz = size, set to the correct size for your dsub. Common values are 17.04 for db9 or high density db15, 25.37 for standard db15, 39.09 for db25. 
//dp= depth, set to a size that can penetrate the panel you are using it with
module dsub(sc,sz,dp){
    $fn=64;
    
    cs=(sz/2)-2.6;
    cs2=(sz/2)-4.095;
    ns=(sz/2)+4.04;
     translate([1.66,-ns,0]){
    cylinder(r=1.6,h=10);
    }
    translate([1.66,ns,0]){
    cylinder(r=1.6,h=10);
    }
    
    scale([sc,sc,sc]){
    
    hull(){
    translate([0,-cs,0]){
    cylinder(r=2.6,h=10);
    }
    translate([0,cs,0]){
    cylinder(r=2.6,h=10);
    }
    translate([3.28,-cs2,0]){
    cylinder(r=2.6,h=10);
    }
    translate([3.28,cs2,0]){
    cylinder(r=2.6,h=10);
    }
}
}
}

electWireDiam = 5.8;
module cableClampUP(){
    difference(){
    cube([20,5,5], center=true);
    translate([-8,0,-4])cylinder(d=2.5,h=10);
    mirror(){translate([-8,0,-4])cylinder(d=2.5,h=10);}
   translate([0,-10,2.5])rotate([0,90,90])cylinder(d=electWireDiam, h=30);    }

}

module SUB_cableClamp(){
    difference(){
    cube([20,5,5], center=true);
    translate([-8,0,-4])cylinder(d=1.5,h=10);
    mirror(){translate([-8,0,-4])cylinder(d=1.5,h=10);}}
}

module electricalBoxLid(){
    lidZ = 15;
    tolerance = 0.4;
   difference(){
    union(){translate([0,0,lidZ/2])cube([boxX-boxThickness-tolerance, boxY-boxThickness-tolerance, lidZ], center=true);
        translate([0,0,lidZ])cube([boxX, boxY, boxThickness], center=true);

    }
    translate([0,0,lidZ/2-2])cube([boxX-3*boxThickness, boxY-3*boxThickness,lidZ+2], center=true);
    //Holes for socket
    translate([0,10,-10])rotate([0,0,90])SUB_socketHoles();
     
   //Serial port 
    //translate([0,-boxY/3-2,5])rotate([0,0,90])dsub(1.1,17.04,10);
    //USB Port TODO: cleanup the code below
       translate([0,-boxY/2+10,5])cube([14.7,7.3,30], center=true);    }
 
difference(){       
           translate([0,-boxY/2+10,10])cube([18,15,10], center=true);  translate([0,-boxY/2+10,5])cube([14.7,7.3,30], center=true);     
}

}

       
    


module electricalBox(){
    difference(){
        
        union(){difference(){
        cube([boxX, boxY, boxZ], center=true);
        translate([0,0,boxThickness])cube([boxX-boxThickness, boxY-boxThickness, boxZ], center=true);
    }
    //cable clamp
    translate([-boxX/3,boxY/2-4,-boxZ/2+5])SUB_cableClamp();
    
 //cable clamp
    translate([boxX/3,boxY/2-4,-boxZ/2+5])SUB_cableClamp();

    }
        //Hole for electricity        
    translate([-boxX/3,boxY/2-10,-boxZ/3+boxThickness])rotate([0,90,90])cylinder(d=electWireDiam, h=30);    
   //Hole for electricity        
    translate([boxX/3,boxY/2-10,-boxZ/3+boxThickness])rotate([0,90,90])cylinder(d=electWireDiam, h=30);    
   
    

}

}
  
module SUB_socketHoles(){
 dHole=3;    
 
for ( i = [0 : 3] ){
    rotate( i * 120, [0, 0, 1])
    translate([25, 0, 0])
    cylinder(d=3,h=30);
}
 cylinder(d=25,h=30);
}


attachX = 10;
attachY = 10;
attachZ = 5;

module SUB_support(){    
    difference(){cube([attachX,attachY,attachZ]);
    translate([attachX/2,attachY/2+2,-attachZ/2])cylinder(h=30,d1=3,d2=3);}
}


//electricalBox();
//cableClampUP();
electricalBoxLid();
//translate([0, 0, 15])electricalBoxLid();

//electricalBox();
//translate([-boxX/2,boxY/3,-boxZ/2])rotate([0,0,90])SUB_support();
//translate([-boxX/2,-boxY/3,-boxZ/2])rotate([0,0,90])SUB_support();
//translate([+boxX/2,boxY/3,-boxZ/2])rotate([0,0,-90])SUB_support();
//translate([+boxX/2,-boxY/3,-boxZ/2])rotate([0,0,-90])SUB_support();
