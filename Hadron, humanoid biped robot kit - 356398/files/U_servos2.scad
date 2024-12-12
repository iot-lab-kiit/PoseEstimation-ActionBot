include <tornillos_union.scad>
include <mg995.scad>

eje_cabeza = 8.8;
alto_capa = 3;

2manifol = 0.001;


// Rodamiento. Cambiar segun el rodamiento utilizado
radio_rodamiento = 2;


// servo
srv_separacion_eje = 10.4; //Separacion del eje de la esquina de la base

alto_capa = 3;
alto_base = 3;
ancho_lados = 3;

dist_tornillos_servo = 7.6;
largo_base = 54;
ancho_base = 23;
alto_lados = 27;
lados_cilindros = 60;
radio_tornillo = 1.5 ;
radio_hex = 6;
diametro_base_tornillo_eje = 8;

base();
lado_servo();
lado_eje();



module base()
{
	difference() {
		cube([ancho_base,largo_base+ancho_lados*2,alto_base]);
		tornillos_union4(ancho_base, largo_base+ancho_lados*2);
		tornillos_union4(ancho_base, (largo_base+ancho_lados*2)*1.5);
		tornillos_union4(ancho_base, (largo_base+ancho_lados*2)*1.34);
		tornillo (ancho_base/2, (largo_base+ancho_lados*2)/2);
		translate([ancho_base/2,srv_separacion_eje+alto_capa,-1])
			#cylinder(r=1+eje_cabeza/2,h=alto_capa,$fn=64);	

	}
}

module lado_servo()
{
 difference() {

 	union() {
	 translate([0,ancho_lados,alto_base-2manifol])
		 rotate([90,0,0]) 
			cube([ancho_base,alto_lados-alto_base,ancho_lados]);

	 translate([0,0,alto_lados])
		rotate([90,0,0]) 
		translate([ancho_base/2,0,-alto_base])
		cylinder(r=ancho_base/2, h=ancho_lados, $fn= lados_cilindros);
 	}


	for (i=[-1:1]) {
	   translate([0,0,alto_lados])
			rotate([90,0,0]) 
				translate([ancho_base/2+dist_tornillos_servo*i,0,-1-ancho_lados])
					cylinder(r=radio_tornillo, h=alto_base+2, $fn= lados_cilindros);
	} 

	//Restamos el cilindro para el hueco de la pieza del eje del servo
   translate([0,0,alto_lados])
		rotate([90,0,0]) 
		translate([ancho_base/2,0,-ancho_lados-1.8])
		#cylinder(r=diametro_base_tornillo_eje/2, h=alto_base, $fn= lados_cilindros);

 }
}

module lado_eje()
{
 difference() {

 union() {

 translate([0,largo_base+ancho_lados*2,alto_base-2manifol])
	rotate([90,0,0]) 
		cube([ancho_base,alto_lados-alto_base,ancho_lados]);

 translate([0,0,alto_lados])
	rotate([90,0,0]) 
	translate([ancho_base/2,0,-largo_base-ancho_lados-alto_base])
	cylinder(r=ancho_base/2, h=ancho_lados, $fn= lados_cilindros);
 }

 translate([0,0,alto_lados])
	rotate([90,0,0]) 
	translate([ancho_base/2,0,-largo_base-ancho_lados-1-ancho_lados])
	cylinder(r=radio_rodamiento, h=alto_base+2, $fn= lados_cilindros);
 }
}