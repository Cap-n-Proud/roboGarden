include <BOSL2/std.scad>
include <BOSL2/screws.scad>


$fn=20;

module cross(){
    
    translate([0,0,5])cube([30,30,20], true);
cube([2,30,10], true);
rotate([0,0,90])cube([2,30,10], true);
}


module drain(){
difference(){
    
union(){
    translate([0,0,0])screw("M10", head="socket", length=20);
    translate([0,0,20])cylinder(r=10, h=2);

}
translate([0,0,27])cross();
translate([0,0,0])cylinder(r=3.5, h=30);
    }
}


module nut_drain(){
    
    translate([0,0,3])
difference(){
 cylinder(r=10, h=2);
translate([0,0,-5])cylinder(r=5, h=30);
   
}
nut("M10", 16, 5);
}

//cross();
drain();
//nut_drain();