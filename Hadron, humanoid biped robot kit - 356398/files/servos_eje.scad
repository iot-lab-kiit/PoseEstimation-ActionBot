include <tornillos_union.scad>
include <mg995.scad>

// varios
alto_capa = 3; //Grosor de la capa de PLA

// servo
srv_separacion_eje = 10.4; //Separacion del eje de la esquina de la base

// tornillo
torn_ancho = 1.6;
torn_separa = 2.60;
torn_cabeza = 3.5;

//
eje_alto = 2.6;
eje_rosca = 4.1;
eje_cabeza = 8.1;

eje_nuevo_separa = 4.4;
eje_nuevo = 5.2;

difference() {
	union() {
		base();
		lado_servo();
		ala();
	}
	translate([srv995_largo_base+srv995_ancho_alas+1,0,0])
	rotate([0,90,0])
		translate([-1,srv_separacion_eje,1])
			cylinder(r=1.5+eje_cabeza/2,h=alto_capa+1,$fn=64);	
}

asiento_ancho = 3;
alto_asiento = 1.5;


//Base del eje
module base()
{
	difference () {
	  
	  union () {   
		cube([srv995_largo_base + srv995_ancho_alas  + 1 + alto_capa , srv995_ancho_base , alto_capa]);
	
		translate([srv995_ancho_base/2,srv_separacion_eje,2])
			cylinder(r=1+eje_cabeza/2,h=alto_capa,$fn=64);	
	  }  
	
	  tornillos_union4(srv995_largo_base+srv995_ancho_alas+5, srv995_ancho_base);
	  tornillos_asiento4(srv995_largo_base+srv995_ancho_alas+5, srv995_ancho_base);
	
	  translate([torn_separa,torn_separa,-1])
		cylinder(r=torn_ancho/2+0.1, h= alto_capa+ 2, $fn=32);
	  
	  translate([torn_separa,srv995_ancho_base-torn_separa,-1])
		cylinder(r=torn_ancho/2+0.1, h= alto_capa + 2, $fn=32); 
	  translate([srv995_largo_base-torn_separa,torn_separa,-1])
		cylinder(r=torn_ancho/2+0.1, h= alto_capa + 2, $fn=32); 
	  translate([srv995_largo_base-torn_separa,srv995_ancho_base-torn_separa,-1])	
		cylinder(r=torn_ancho/2+0.1, h= alto_capa + 2, $fn=32); 


	  translate([torn_separa,torn_separa,alto_capa-1])
		cylinder(r=torn_cabeza/2+0.1, h= 2, $fn=32);  
	  translate([torn_separa,srv995_ancho_base-torn_separa,alto_capa-1])
		cylinder(r=torn_cabeza/2+0.1, h= 2, $fn=32); 
	  translate([srv995_largo_base-torn_separa,torn_separa,alto_capa-1])
		cylinder(r=torn_cabeza/2+0.1, h=  2, $fn=32); 
	  translate([srv995_largo_base-torn_separa,srv995_ancho_base-torn_separa,alto_capa-1])
		cylinder(r=torn_cabeza/2+0.1, h=  2, $fn=32); 

	//hueco exagono y pase para el eje
	  translate([srv995_ancho_base/2,srv_separacion_eje,0])tornillo();
	
	//Hueco pase destornillador tornillos alas
	  translate([srv995_largo_base + eje_nuevo_separa ,eje_nuevo_separa,-1])
		cylinder(r=eje_nuevo/2, h= alto_capa + 2, $fn=32);  
	  translate([srv995_largo_base + eje_nuevo_separa ,srv995_ancho_base- eje_nuevo_separa,-1])
		cylinder(r=eje_nuevo/2, h= alto_capa + 2, $fn=32);  
	
	}
}

module ala()
{
	//ala
	translate([srv995_largo_base +1,0,-alto_capa-srv995_alto_base_fin_ala])
	difference() {
	cube([srv995_ancho_alas , srv995_ancho_base , alto_capa]);
	translate([srv995_ancho_alas/2,srv995_largo_alas/2+srv995_dist_tornillo_ala/2,0])
		cylinder(r=torn_ancho,h=alto_capa,$fn=64);
	translate([srv995_ancho_alas/2,srv995_largo_alas/2-srv995_dist_tornillo_ala/2,0])
		cylinder(r=torn_ancho,h=alto_capa,$fn=64);
	translate([0,srv995_largo_alas/2-0.75, alto_capa-1.3]) 
		cube([srv995_ancho_alas, srv995_ancho_muesca_ala, srv995_profundo_muesca_ala]);
	}
}

module lado_servo()
{
	//Lateral del servo
	translate([srv995_largo_base+srv995_ancho_alas+1,0,0])
	rotate([0,90,0])
	difference() {
		cube([srv995_alto_base_fin_ala+alto_capa , srv995_ancho_base , alto_capa]);
		tornillos_union4(srv995_alto_base_fin_ala, srv995_ancho_base);
	}
}




//cabeza tornillo
 module tornillo () {
  cylinder(r=eje_cabeza/2,h=eje_alto+0.2,$fn=6);
  cylinder(r=eje_rosca/2,h=eje_alto*4,$fn=32);
}

