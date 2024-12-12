include <tornillos_union.scad>
include <mg995.scad>

alto_capa = 3;
ancho_base = 8;
largo_base = 33;
alto_lado = 20;

difference() {
	cube([largo_base+2*alto_capa,ancho_base,alto_capa]);

	tornillos_union2(largo_base+2*alto_capa, ancho_base, "h");

}

rotate([0,90,0])
difference() {
	cube([alto_lado,ancho_base,alto_capa]);
	tornillos_union2(alto_lado, ancho_base, "h");
}

translate([33+alto_capa,0,0])
rotate([0,90,0])
difference() {
	cube([alto_lado,ancho_base,alto_capa]);
	tornillos_union2(alto_lado, ancho_base, "h");
}



