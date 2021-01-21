$fn=150;
outerDiam = 6;
screwDiam = 2;
pilarHeight = 5;


mega = [[0,0], [74.9,0], [50.8,-15.2], [50.8,-43.1], [86.3,-48.2], [0,-48.2] ];

uno =[[],[],[],[],[]];

echo(len(mega));

for (i=[0:len(mega)]){
    echo(mega[i][1] );
}

module pillar(){
    difference(){
        cylinder(h=pilarHeight, d1= outerDiam, d2= outerDiam);
        translate([0,0,-1])cylinder(h=pilarHeight+2, d1= screwDiam, d2= screwDiam);       
    }
    
}


module mount(component){
    
  
for (i=[0:len(mega)]){
    translate([mega[i][0],mega[i][1],0])pillar();
 
}  
    
}

mount(mega);