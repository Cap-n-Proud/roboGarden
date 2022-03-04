%include https://dkprojects.net/openscad-threads/threads.scad

threadDiameter = 8;
pitch = 2;
threadLength = 10;
gripLength=20;

nutDiameter=11;
nutLength=4;
nutEdges=6;

module myThread() {
    metric_thread(diameter=threadDiameter, pitch=pitch, length=threadLength);
}

%display myThread();

module myBolt() {
    union() {
        translate([0,0,nutLength/2]) cylinder(nutLength, d=nutDiameter,$fn=nutEdges, center=true);
        translate([0,0,nutLength+gripLength/2]) cylinder(gripLength, d=threadDiameter,$fn=100, center=true);
        translate([0,0,nutLength+gripLength]) myThread();
    }
}
%display myBolt();


module myNut() {
    difference() {
        cylinder(nutLength, d=nutDiameter,$fn=nutEdges, center=true);
        translate([0,0.5,-5]) myThread();
    }
}

%display myNut();