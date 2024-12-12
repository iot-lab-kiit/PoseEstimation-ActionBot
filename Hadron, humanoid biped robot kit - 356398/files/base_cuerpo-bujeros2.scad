include <tornillos_union.scad>
include <mg995.scad>
use <Writescad/write.scad>




anclaje = 60;
dx = 60; //distancia al centro
dy = 60;
dy1 = 35;
dz = 0;
dz1 = 8;
alto_capa = 3;
dist_torn_eje_brazo = 50; //distancia entre huecos
dist_torn_eje_cabeza = 30;
dist_torn_eje_pierna1 = 46;
dist_torn_eje_pierna2 = 26;



difference() {
	cuerpo(2, 0);

	//Brazo derecho e izquierdo
	tornillos_servos_cuerpo(-dx, dy+37, dist_torn_eje_brazo);
	mirror([0,1,0])
	tornillos_servos_cuerpo(-dx, dy+37, dist_torn_eje_brazo);


	//miembro inferior
	rotate([0,0,-23])
		tornillos_servos_cuerpo(dx-35, dy+30, dist_torn_eje_brazo);
	mirror([0,1,0])
	rotate([0,0,-23])
		tornillos_servos_cuerpo(dx-35, dy+30, dist_torn_eje_brazo);

	//tornillos de soporte para piernas bípedas
	rotate([0,0,90])
		tornillos_servos_cuerpo(dx-60, -dy+15, dist_torn_eje_pierna1);
	rotate([0,0,90])
		tornillos_servos_cuerpo(dx-60, -dy+15, dist_torn_eje_pierna2);

	//Soporte para servo de la cabeza del bipedo
	rotate([0,0,90])
		tornillos_servos_cuerpo(dx-60, dy+50, dist_torn_eje_cabeza);
	
	/*Superior derecha e izquierda
	rotate([0,0,80])
		tornillos_servos_cuerpo(dx-15, dy+55, dist_torn_eje_brazo);
	mirror([0,1,0])
	rotate([0,0,80])
		tornillos_servos_cuerpo(dx-15, dy+55, dist_torn_eje_brazo);*/

	//Cilindro central
	cylinder(r=srv995_ancho_saliente_cilindro_eje/2+1,h=alto_capa,$fn=64);


// Bujeros - eugenio
//translate([-26,10,0])rotate([0,0,90])write("H      ",t=20.5,h=26,center=true);

// H
translate([-39,-53,-1])cube([26,3,10]);
translate([-39,-39.5,-1])cube([26,3,10]);
translate([-28,-53,-1])cube([3,16,10]);

// N
translate([-39,50,-1])cube([26,3,10]);
translate([-39,37,-1])cube([26,3,10]);
translate([-37.4,37,-1])rotate([0,0,28])cube([27.4,3,10]);

// R
translate([-39,1,-1])cube([26,3,10]);
translate([-39,1,-1])cube([15,8,10]);
translate([-31.5,8.5,-1])cylinder(r=7.5,h=6, $fn=64);

difference (){
translate([-37.4,2,-1])rotate([0,0,28])cube([29,3,10]);
translate([-14,-58,-1])rotate([0,0,0])cube([5,115,10]);

}

// D
difference (){
translate([-26,-13.5,-1])scale([1.1,1.0,3.0])cylinder(r=12,h=6, $fn=64);
translate([-42,-27.5,-1])cube([31.1,11.0,3.0]);

}
// O 
translate([-26,27,-1])scale([1.8,1.1,3.0]) sphere(r=7.5); 

// A

difference (){

union (){
translate([-39.8,-28,-1])rotate([0,0,15])cube([29,3,10]);
translate([-40.4,-28,-1])rotate([0,0,-15])cube([29,3,10]);
}
translate([-44,-58,-1])rotate([0,0,0])cube([5,115,10]);
translate([-14,-58,-1])rotate([0,0,0])cube([5,115,10]);
}
translate([-25.4,-31,-1])rotate([0,0,0])cube([3,9,10]);
translate([-26.4,-26,-1])rotate([0,0,180])scale([1,0.6,3.0])cylinder(r=12,h=6, $fn=3);



//
translate([-54,-30,0])cylinder(r=8,h=6, $fn=64);
translate([-54,30,0])cylinder(r=8,h=6, $fn=64);

translate([0,-22,0])cylinder(r=10,h=6, $fn=64);
translate([0,22,0])cylinder(r=10,h=6, $fn=64);

translate([24,-36,0])cylinder(r=6,h=6, $fn=64);
translate([24,36,0])cylinder(r=6,h=6, $fn=64);

translate([40,-26,0])cylinder(r=6,h=6, $fn=64);
translate([40,26,0])cylinder(r=6,h=6, $fn=64);

translate([-33,-26.5,0])rotate([0,0,180])cylinder(r=3.8,h=6, $fn=3);
translate([-28,-26.5,0])rotate([0,0,180])cylinder(r=5.6,h=6, $fn=3);
translate([-26,-26.5,0])rotate([0,0,180])cylinder(r=5.6,h=6, $fn=3);

translate([45,0,-1])rotate([0,0,180])cylinder(r=18,h=6, $fn=3);
translate([-55,0,-1])rotate([0,0,180])cylinder(r=10,h=6, $fn=64);




}
module cuerpo(dz, dz1)
{
	polyhedron(
	  points=[ [0,dy,dz], 
              [-dx,dy,dz],[-dx-10,0,dz],[-dx,-dy,dz],
              [0,-dy,dz],
				  [dx, -dy1, dz],[dx, dy1, dz], 

				  [0,dy,dz1], 
              [-dx,dy,dz1],[-dx-10,0,dz1],[-dx,-dy,dz1],
              [0,-dy,dz1],
				  [dx, -dy1, dz1],[dx, dy1, dz1] 				],  
                              
	  triangles=[  [0,4,2], [2,4,3], [0,2,1], 
						[0,5,4], [0,6,5], 
                  [0,1,7], [1,8,7],
						[1,2,8], [2,9,8], 
						[2,3,9], [3,10,9],
						[3,4,10], [4,11,10],
						[4,5,11], [5,12,11],
						[5,6,12], [6,13,12],
						[6,0,13], [0,7,13],
						[7,9,11], 
						[9,10,11],[7,8,9], [7,11,12], [12,13, 7] 
]
	 );

}

module tornillos_servos_cuerpo(dx, dy, d)
{
	tornillos_union2(dx-d, dy, "v");
	tornillos_union2(dx+d, dy, "v");
}

