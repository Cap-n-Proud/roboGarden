$fn=150;

use <Threading.scad>
use <hollowCylinder.scad>
height = 15;
diamPipe=10;
diamThread=20;

difference () {
    union() {
   Threading(D = diamThread, pitch = 2, d=0.8*diamThread, windings = 10, angle = 20); 
    translate([0,0,30])hollowCylinder(diamThread, 0.8*diamThread, 3, height);
       
    }
    //cylinder(h = 55, d = 14.5,$fn=150);
}