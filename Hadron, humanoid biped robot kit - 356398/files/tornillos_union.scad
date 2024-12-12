dist_tornillos = 5; //Distancia entre los tornillos de enlace de piezas
torn_ancho = 1.6;
alto_capa = 3;


module tornillos_union4(centrox, centroy) {
		translate([centrox/2+dist_tornillos,centroy/2+dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
		translate([centrox/2-dist_tornillos,centroy/2+dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
		translate([centrox/2-dist_tornillos,centroy/2-dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
		translate([centrox/2+dist_tornillos,centroy/2-dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
}

module tornillo(x, y) {
		translate([x, y, 0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
}

module tornillos_asiento4(centrox, centroy) {
		translate([centrox/2+dist_tornillos,centroy/2+dist_tornillos,0])
			cylinder(r2=torn_ancho, r1=asiento_ancho,h=alto_asiento,$fn=64);
		translate([centrox/2-dist_tornillos,centroy/2+dist_tornillos,0])
			cylinder(r2=torn_ancho, r1=asiento_ancho,h=alto_asiento,$fn=64);
		translate([centrox/2-dist_tornillos,centroy/2-dist_tornillos,0])
			cylinder(r2=torn_ancho, r1=asiento_ancho,h=alto_asiento,$fn=64);
		translate([centrox/2+dist_tornillos,centroy/2-dist_tornillos,0])
			cylinder(r2=torn_ancho, r1=asiento_ancho,h=alto_asiento,$fn=64);
}

module tornillos_union2(centrox, centroy, orientacion) {
	if (orientacion == "h")
	{
		translate([centrox/2+dist_tornillos,centroy/2,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
		translate([centrox/2-dist_tornillos,centroy/2,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
	}
	else
	{
		translate([centrox/2,centroy/2-dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
		translate([centrox/2,centroy/2+dist_tornillos,0])
			cylinder(r=torn_ancho,h=alto_capa,$fn=64);
	}
}