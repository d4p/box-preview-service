$fa=1;
$fs=0.4;

box_dimension_X = 135;
box_dimension_Y = 225;
box_dimension_Z = 288;
wall_thickness = 2.8;
bottom_thickness = 3;
round_radius = 20;
hole_diameter =41; //diameter of the hole
hole_x= 0.5 * box_dimension_X; //allow hole to be only in the center
hole_y = 0;
//hole_Z = 0.5 *box_dimension_Z; //height of the center of the hole
hole_Z = 130;
rounded = false;
buffer = 0.02;

module rounded_box(x,y,z,radius){
    cube_x = box_dimension_X-(2*round_radius);
    cube_y = box_dimension_Y-(2*round_radius);
    minkowski(){
      translate([radius,radius,0]) //required to center objects correctly
        cube([cube_x,cube_y,z]);
      cylinder(r=radius);
    }
}

module rounded_box2(x,y,z,radius){
    cube_x = box_dimension_X-(2*round_radius);
    cube_y = box_dimension_Y-(2*round_radius);
    translate([radius,radius,0])
    union(){
    //mainbox
    translate([-buffer/2,-buffer/2,0])
        cube([cube_x+buffer,cube_y+buffer,z]);
    
    //round corners
    translate([cube_x,0,0]) 
        cylinder(z,r = radius);
    translate([0,cube_y,0]) 
        cylinder(z,r = radius);
    translate([cube_x,cube_y,0])
        cylinder(z,r = radius);
    translate([0,0,0]) 
        cylinder(z,r = radius);
    
    //gapfills
    translate([0,-radius,0])
        cube([cube_x,radius,z]);
    translate([0,cube_y,0])
        cube([cube_x,radius,z]);
        
    translate([cube_x,0,0])
        cube([radius,cube_y,z]);
    translate([-radius,0,0])
        cube([radius,cube_y,z]);
    }
}

//rounded_box2(box_dimension_X,box_dimension_Y,box_dimension_Z,round_radius);

difference(){
    rounded_box2(box_dimension_X,box_dimension_Y,box_dimension_Z,round_radius);
    
    scale_x = (box_dimension_X-(2*wall_thickness))/box_dimension_X;
    scale_y = (box_dimension_Y-(2*wall_thickness))/box_dimension_Y;
    
    translate([wall_thickness,wall_thickness,bottom_thickness])
            rounded_box2(box_dimension_X-wall_thickness,box_dimension_Y-wall_thickness,box_dimension_Z,round_radius-wall_thickness);
    
   translate([hole_x , hole_y + wall_thickness + buffer, hole_Z])
        rotate([90,0,0])
            cylinder(h=wall_thickness + 2*buffer, d= hole_diameter); 
}

