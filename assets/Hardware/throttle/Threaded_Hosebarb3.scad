$fn=150;

use <Threading.scad>
use <hollowCylinder.scad>
height = 15;
diamPipe=10;
diamThread=20;
funnelHeight = 5;
holeDiam = diamPipe -2;

    
    
translate([0,0,5])
    difference(){  
        union(){ 
            translate([0,0,0])cylinder(h = funnelHeight, d1 = diamThread, d2 = diamPipe);
            translate([0,0,funnelHeight])cylinder(h = 15, d = diamPipe);
                }
                 
       translate([0,0,-funnelHeight]) cylinder(h = 30, d2 = holeDiam,d1=0.5*diamThread);
                }
translate([0,0,0])hollowCylinder(diamThread, 5, 3);
translate([0,0,-8])Threading(D = diamThread, pitch = 1.25, d=0.8*diamThread, windings = 8, angle = 20); 
                
                