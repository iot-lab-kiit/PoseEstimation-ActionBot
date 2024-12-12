include <tornillos_union.scad>
include <mg995.scad>

alto_capa = 3;
alto_base = 1;
largo_mano = srv995_ancho_base+4*alto_capa+10;

mano();

module mano()
{
	//Lateral del servo
	difference() {
		cube([srv995_alto_base_fin_ala+2*alto_capa , srv995_ancho_base+2*alto_capa , alto_capa+alto_base]);
		translate([alto_capa,alto_capa,alto_capa])
			cube([srv995_alto_base_fin_ala , srv995_ancho_base+alto_capa , alto_base]);
		tornillos_union4(srv995_alto_base_fin_ala+2*alto_capa, srv995_ancho_base+2*alto_capa+5);
	}

	//Lado mano
	translate([0,alto_capa,alto_base+alto_capa-0.1])
	rotate([90,0,0])
		cube([srv995_ancho_base+5*alto_capa, srv995_alto_base_fin_ala+alto_capa+10 , alto_capa]);

	//Dedos
	translate([0,alto_capa,alto_base+alto_capa+largo_mano-1])
	rotate([70,0,0])
		cube([srv995_ancho_base+5*alto_capa, srv995_alto_base_fin_ala+alto_capa , alto_capa]);

}