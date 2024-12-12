include <tornillos_union.scad>
include <mg995.scad>

ancho_soporte_servo_pie = 7;
alto_pie = 4;
ancho_soporte = 15;
alto_capa = 15;

borde_soporte = 2.5;

largo_base_piezas = 2*ancho_soporte_servo_pie+borde_soporte*2;
largo_base = largo_base_piezas+42;
ancho_base = 92;
ancho_base_servo = 38; 

	base();

	translate ([-ancho_soporte_servo_pie+largo_base/2-borde_soporte,-ancho_soporte+8,alto_pie+1.4])
	soporte_servo();

	translate ([-largo_base/2+borde_soporte,-ancho_soporte+8,alto_pie+1.4])
	soporte_servo();



module soporte_servo()
{
	rotate([90,0,0])
	difference() {
		cube([ancho_soporte_servo_pie, srv995_largo_alas, ancho_soporte]);
		tornillos_union2(srv995_ancho_alas, srv995_largo_alas, "v");
	}
}

module base()
{

difference () {
	union() {
		bcube([largo_base, ancho_base, alto_pie],cr=4, cres=4);
		translate ([0,8-ancho_base_servo/2,1.5+alto_pie/2])
			bcube([largo_base, ancho_base_servo, alto_pie],cr=4, cres=4);
	}


		bcube([largo_base-26, ancho_base-24, alto_pie+10],cr=4, cres=4);

}

}

//------------------------------------------------------------------------------
//-- Bevel Cube main function
//-- Parameters:
//--   * Size:  Cube size
//--   * cr : Corner radius (if cr==0, a standar cube is built)
//--   * cres:  Corner resolution (in points). cres=0 means flat corners
//------------------------------------------------------------------------------
module bcube(size,cr=0,cres=0)
{
  //-- Internal cube size
  bsize = size - 2*[cr,cr,0];

  //-- Get the (x,y) coorner coordinates in the 1st cuadrant
  x = bsize[0]/2;
  y = bsize[1]/2;

  //-- A corner radius of 0 means a standar cube!
  if (cr==0)
    cube(bsize,center=true);
  else {

      
      //-- The height of minkowski object is double. So
      //-- we sould scale by 0.5
      scale([1,1,0.5])

      //-- This translation is for centering the minkowski objet
      translate([-x, -y,0])

      //-- Built the  beveled cube with minkowski
      minkowski() {

        //-- Internal cube
        cube(bsize,center=true);

        //-- Cylinder in the corner (1st cuadrant)
        translate([x,y, 0])
          cylinder(r=cr, h=bsize[2],center=true, $fn=4*(cres+1));
      }
  }

}