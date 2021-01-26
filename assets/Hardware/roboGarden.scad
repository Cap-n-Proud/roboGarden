$fn = 200;
towerDiam = 75;



towerThickness = 2;
towerID = towerDiam - 2* towerThickness;
towerHeight = 1000;
podHeight = 3;
podDiam = 38.5;
podThickness = 2;
podAngle = 90;
distanceBetweenLevels = 50;
minDistanceFromTowerBase = 30;
hollowPods =true
;

baseX = 800;
baseY = 550;
baseZ = 400;
baseThickness = 20;

borderBaseX = 80;
borderBaseY = 30;

lightBeamDiam = 30;



T = 1;


sprinkleRingThickness = 2;
sprinklerHolesAngle = 30;
sprinklePlateHeight = 3;
sprinlkerAngle=10;
sprinklerDiam=towerID;
sprinklerHoleDiam = 5;

anchor = false;


colFunnelHeight =10;
collectorCollarH = 40;
drainPipeHeight = 30;

collectorDiam =25;



numberofPods = towerHeight / (podDiam + distanceBetweenLevels);
dbpc = 2 * distanceBetweenLevels + 2 * podDiam;
echo("distace between pod centers: ", dbpc);
echo("number of pods per tower: ", 2 * floor(numberofPods));
echo("Angle between pods (alllevs): ", 3 / 2 * podAngle);
dBetweenTowers = (300 - towerDiam / 2 - borderBaseX);
echo("Distance between tower centers: ", dBetweenTowers);
echo("Sprinkler diam: ", sprinklerDiam);

module rotate_about_pt(z, y, pt) {
  translate(pt)
  rotate([0, y, z]) // CHANGE HERE
  translate( - pt)
  children();
}

module t() {
  difference() {
    cylinder(h = towerHeight, d1 = towerDiam, d2 = towerDiam);
    cylinder(h = towerHeight + 3 * towerThickness, d1 = towerDiam - towerThickness, d2 = towerDiam - towerThickness);
  }

}

module pod(hollowPods) {
if (hollowPods==true){
  difference(){
  translate([podHeight, 0, podDiam]) rotate([ - 0, 90, -90]) rotate_extrude(angle = 75, convexity = 10)
  translate([38.5, 0]) circle(d = podDiam);
  rotate([0, 90, 0]) cylinder(h = podHeight, d1 = podDiam, d2 = podDiam);


      translate([podHeight,0,podDiam])rotate([-0,90,-90])rotate_extrude(angle=75,convexity = 10)
  translate([38.5, 0])circle(d=podDiam-2);
  rotate([0, 90, 0]) cylinder(h = podHeight, d1 = podDiam - 2, d2 = podDiam - 2);
  }
}else{
      translate([podHeight, 0, podDiam]) rotate([ - 0, 90, -90]) rotate_extrude(angle = 75, convexity = 10)
  translate([38.5, 0]) circle(d = podDiam);
  rotate([0, 90, 0]) cylinder(h = podHeight, d1 = podDiam, d2 = podDiam);
    
    }
}

module level(angle) {
  rotate_about_pt(angle, 0, [0, 0, 0]) {
    rotate_about_pt(podAngle, 0, [0, 0, 0]) translate([towerDiam / 2 - podHeight / 2, 0, podDiam / 2 ]) pod(hollowPods);
    rotate_about_pt(0, 0, [0, 0, 0]) translate([towerDiam / 2 - podHeight / 2, 0, podDiam / 2 ]) pod(hollowPods);
  }
}

module base() {
  translate([0, 0, baseZ / 2]) difference() {
    cube([baseX, baseY, baseZ], center = true);
    cube([baseX - baseThickness, baseY + 3 * baseThickness, baseZ - baseThickness], center = true);

  }
}

module tower() {

  for (z = [0 : floor(numberofPods) - 1])
  translate([0, 0, (podDiam + distanceBetweenLevels) * z + +minDistanceFromTowerBase]) {
    level((z % 2) * podAngle / 2);
  minDistanceFromTowerBase = 0;
  }

  t();
}

module lightBeam() {
  cylinder(h = towerHeight, d1 = lightBeamDiam, d2 = lightBeamDiam);

}
//   pod();
module roboGarden() {
  base();
  translate([0, -baseY / 2 + towerDiam / 2 + borderBaseY, baseZ]) rotate([0, 0, 30]) tower();
  translate([ - dBetweenTowers, -baseY / 2 + towerDiam / 2 + borderBaseY, baseZ]) rotate([0, 0, 35]) tower();
  translate([dBetweenTowers, -baseY / 2 + towerDiam / 2 + borderBaseY, baseZ]) rotate([0, 0, 5]) tower();

  translate([baseX / 2 - (lightBeamDiam / 2 + 20), baseY / 2 - (lightBeamDiam / 2 + 20), baseZ]) lightBeam();
  translate([ - baseX / 2 + (lightBeamDiam / 2 + 20), baseY / 2 - (lightBeamDiam / 2 + 20), baseZ]) lightBeam();

}

module dome(d = 5, h = 2, hollow = false, wallWidth = 0.5) {
  sphereRadius = (pow(h, 2) + pow((d / 2), 2)) / (2 * h);

  translate([0, 0, (sphereRadius - h) * -1]) {
    difference() {
      sphere(sphereRadius);
      translate([0, 0, -h]) {
        cube([2 * sphereRadius, 2 * sphereRadius, 2 * sphereRadius], center = true);
      }

      if (hollow) sphere(sphereRadius - wallWidth);

    }
  }
}


module towerDome() {
  difference(){
   union(){   dome(d = towerDiam, h = 9, hollow = true);
  difference() {
    translate([0, 0, -10]) cylinder(h = 10, d1 = (sprinklerDiam), d2 = (sprinklerDiam));
    translate([0, 0, -15]) cylinder(h = 15, d1 = (sprinklerDiam-sprinkleRingThickness), d2 = (sprinklerDiam-sprinkleRingThickness));
    
  } }
    translate([0, 0, -10]) cylinder(h = 100, d1 = 0.1*sprinklerDiam, d2 = 0.1*sprinklerDiam);

}
}

/* 
 * Excerpt from... 
 * 
 * Parametric Encoder Wheel 
 *
 * by Alex Franke (codecreations), March 2012
 * http://www.theFrankes.com
 * 
 * Licenced under Creative Commons Attribution - Non-Commercial - Share Alike 3.0 
*/

module arc(height, depth, radius, degrees) {
  // This dies a horible death if it's not rendered here 
  // -- sucks up all memory and spins out of control 
  render() {
    difference() {
      // Outer ring
      rotate_extrude($fn = 100)
      translate([radius - height, 0, 0])
      square([height, depth]);

      // Cut half off
      translate([0, -(radius + 1), -.5])
      cube([radius + 1, (radius + 1) * 2, depth + 1]);

      // Cover the other half as necessary
      rotate([0, 0, 180 - degrees])
      translate([0, -(radius + 1), -.5])
      cube([radius + 1, (radius + 1) * 2, depth + 1]);

    }
  }
}

module SUB_sprinklerInflow(anchor) {
  sprinklerTubeThick = 3;
    //Inflow attachment
  translate([0,0,-15])difference() {
    union() {
      cylinder(h = 20, d1 = (pipeDiamIN+1), d2 = (pipeDiamIN+1));
   // translate([0,0,2])SUB_sprinklerRing();
     if (anchor == true){ anchor_diameter = 1;
      for (i = [0 : 3]) {
        translate([0, 0, 4 * i]) rotate_extrude(angle = 360) {
          translate([(pipeDiamIN + 1 * T) / 2 - anchor_diameter / 2, 0])
          circle(d = anchor_diameter);
        }
      }
    }}
    translate([0, 0, -10]) rotate([0, 0, 0]) cylinder(h = 40, d1 = (pipeDiamIN - sprinklerTubeThick), d2 = (pipeDiamIN - sprinklerTubeThick));
    
     }
}
    
     
module SUB_cutSprinklerTop(){
    
     //Remove excess material on the inflow.
cutHeight = 100;
   rotate([0, -sprinlkerAngle, 0])translate([0, 0, cutHeight/2+sprinklePlateHeight]) cube([2*towerDiam, 2*towerDiam, cutHeight], center = true);

}
  
module SUB_cutSprinklerSide() {

  //Cut the externaledges due to the inclination of the plate
 translate([0,0,-30])difference() {
    cylinder(h = 60, d1 = (2*towerDiam), d2 = (2*towerDiam));

    cylinder(h = 60, d1 = (sprinklerDiam), d2 = (sprinklerDiam));
  }

  }


    
module SUB_sprinklerRing() {
  //Builds the external ring
  translate([0,0,-15])difference() {
    cylinder(h = 40, d1 = (sprinklerDiam), d2 = (sprinklerDiam));
    translate([0,0,-5])cylinder(h = 40, d1 = (sprinklerDiam-sprinkleRingThickness), d2 = (sprinklerDiam-sprinkleRingThickness));

  }}
  
  module SprinklerShelve() {
  //Builds the external ring
  translate([0,0,-25])difference() {
    cylinder(h = 15, d1 = (sprinklerDiam+1), d2 = (sprinklerDiam+1));
    translate([0,0,0])cylinder(h = 15, d1 = (sprinklerDiam-2*sprinkleRingThickness), d2 = (sprinklerDiam-2*sprinkleRingThickness));

  }
  


}

module SUB_sprinklerPlate() {
  translate([0,0,0])difference() {
    rotate([0, -sprinlkerAngle, 0]) cylinder(h = sprinklePlateHeight , d1 = (sprinklerDiam+2*cos(sprinlkerAngle)), d2 = (sprinklerDiam+2*cos(sprinlkerAngle)));
   translate([0,0,-10])cylinder(h = 60, d1 = (pipeDiamIN - T), d2 = (pipeDiamIN - T));
    SUB_sprinklerHoles();
    rotate([0, 0, 160])arc(10, 20, 30, 130);

  }
 // translate([0, 0, -5]) SUB_inflow();
}

module SUB_sprinklerHoles() {

  n = 20; // number of holes
  step = 360 / n;

  rotate([sprinklerHolesAngle, 0, 160-45])translate([0,-5,-30]) {
    for (j = [3 : 2]) {

      for (i = [0 : step: 160]) {
        //translate([r*cos(i),r*sin(i),0])
        //rotate([0,15,0])cylinder(h= 30, d1= sprinklerHoleDiam, d2=sprinklerHoleDiam); 
        r = j / 10 * (sprinklerDiam) + 8;
        angle = i;
        dx = r * cos(angle);
        dy = r * sin(angle);
        translate([dx, dy, 0]) rotate([0, 0, 0]) cylinder(h = 50, d1 = sprinklerHoleDiam, d2 = sprinklerHoleDiam);

      }
    }
  }
}

module sprinkler() {
    difference(){
    union(){
    SUB_sprinklerPlate();
    SUB_sprinklerRing();
    SUB_sprinklerInflow();
    }
    SUB_cutSprinklerTop();
    SUB_cutSprinklerSide();
    
}}


module collectorShell(){
union(){
 translate([0,0,collectorCollarH])cylinder(h=collectorCollarH, d2=collectorDiam,d1=collectorDiam);
translate([0,0,0])cylinder(h=collectorCollarH, d2=towerDiam + 2*towerThickness ,d1=towerDiam + 2*towerThickness);
}

}



module collectorHole(){
union(){
    //Funnel
 translate([0,0,collectorCollarH-colFunnelHeight])cylinder(h=colFunnelHeight , d2=collectorDiam-2*towerThickness,d1=towerDiam);
    //Top
translate([0,0,-2*collectorCollarH])cylinder(h=6*collectorCollarH, d=collectorDiam-2*towerThickness);    //Bottom
translate([0,0,-colFunnelHeight])cylinder(h=collectorCollarH, d2=towerDiam ,d1=towerDiam );
}}

module collector(){
difference(){
collectorShell();
translate([0,0,-2])collectorHole();
    
    
}

translate([0,0,collectorCollarH-attachZ])attachment(towerDiam);
}


attachX = 10;
attachY = 15;
attachZ = 5;

module SUB_support(){    
    difference(){cube([attachX,attachY,attachZ]);
    translate([attachX/2,attachY/2+2,-attachZ/2])cylinder(h=10,d1=3,d2=3);}
}

module attach(diam){    
translate([diam/2,0,0])rotate([0,0,-90])translate([-attachX/2,0,0])SUB_support();
                
        
    
mirror(){    
 translate([diam/2,0,0])rotate([0,0,-90])translate([-attachX/2,0,0])SUB_support();
}
}

module attachment(diam){
attach(diam);
rotate([0,0,90])attach(diam);
}



module lightPoleSupport(){
 difference(){
    union(){ cylinder (h=20, d=lightBeamDiam + 1 + 2*towerThickness);
    translate([0,0,20-attachZ])attachment(lightBeamDiam);        
        
    }
     translate([0,0,-towerThickness])cylinder (h=20, d=lightBeamDiam+1);
    
 }
    
}

//lightPoleSupport();
//collector();
//roboGarden();

//SprinklerShelve();
//sprinkler();

//towerDome();

//tower();
//level(1);
towerDome();
