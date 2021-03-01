use <Threading.scad>
use <hollowCylinder.scad>
difference () {
    union() {
        threading(pitch = 2, d = 27.77, windings = 8, helices = 1, angle = 60, steps=140, full = false);
        hollowCylinder(25.5, 20, 3, 150);
        hollowCylinder(20, 55, 3, 150);
        translate ([0,0,32])
        cylinder(h = 5, r1 = 10.5, r2 = 10,$fn=150, center = true);
        translate ([0,0,40])
        cylinder(h = 5, r1 = 10.5, r2 = 10,$fn=150, center = true);
        translate ([0,0,48])
        cylinder(h = 5, r1 = 10.5, r2 = 10,$fn=150, center = true);
        translate ([0,0,28]) 
        cylinder(h = 10, r1 = 16.0, r2 = 8, $fn = 150, center=true);
        translate ([0,0,13])
        hollowCylinder(32,10,8,150);
    }
    cylinder(h = 55, d = 14.5,$fn=150);
}