$fn=150;
outerDiam = 6;
screwDiam = 2.5;
pilarHeight = 5;

//First is the board x, y second is the position of the first hole
megaDim = [[101.6,53.34],[14,2.5]];

mega = [[0,0], [79.4, 48.26], [0,48.26], [82.55,0], [50.8,0], [50.8,33] ];

unoDim = [[68.58, 53.34],[2.58, 7.62]];
uno =[[0,0],[0,27.94],[50.76, 43.18]];
//https://learn.adafruit.com/introducing-the-raspberry-pi-model-b-plus-plus-differences-vs-model-b/mounting-holes
//https://learn.adafruit.com/assets/17950
raspberryDim = [[85.6,54],[25.5,18]];
raspberryBPlus =[[],[],[],[],[]];
raspberryB =[[0,0],[55.1,23.5]];
raspberry3 =[[],[],[],[],[]];

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
    
  
for (i=[0:len(component)]){
    translate([component[i][0],component[i][1],0])pillar();
 
}  
    
}

module fullmodule(boardDim,component){
    
echo(boardDim[0][1]);
cube([boardDim[0][0],boardDim[0][1],3]);
translate([boardDim[1][0], boardDim[1][1], pilarHeight])
    mount(component);    
}
//mount(mega);

fullmodule(raspberryDim,raspberryB);
translate([raspberryDim[0][0] + 20,0,0])fullmodule(unoDim,uno);
