$fn=150;

use <Threading.scad>
use <hollowCylinder.scad>
height = 15;
diamPipe=10;
diamThread=20.8;
funnelHeight = 5;
holeDiam = diamPipe -2;
thickness=3;
    
translate([0, 0, 5])
difference() {
    union() {
        difference() {
            translate([0, 0, 0]) cylinder(h = funnelHeight, d1 = diamThread + thickness, d2 = diamPipe);
            translate([0, 0, -1]) cylinder(h = funnelHeight, d1 = diamThread - thickness, d2 = diamPipe);
        }
       translate([0, 0, funnelHeight]) cylinder(h = 15, d = diamPipe);
    }

    translate([0, 0, -funnelHeight]) cylinder(h = 30, d2 = holeDiam, d1 = holeDiam);

    //Connection between thread and rest              
}
translate([0,0,0])hollowCylinder(diamThread+thickness, 5, 3);
translate([0, 0, -8]) Threading(D = diamThread + thickness, pitch = 1.25, d = 0.9 * diamThread + thickness, windings = 8, angle = 20);