#include <math.h>

#ifndef _COORDINATE_SYSTEM_FUNCS_LIB_
#define _COORDINATE_SYSTEM_FUNCS_LIB_
#define pi 3.141592653589793

double mod_double(double value1, double value2){
	int help1 = (int)(value1 / value2);
	value1 -= value2 * help1;
	if (value1 < 0) value1 += value2;
	return value1;
}

void rotation2D(double x, double y, double _phi, double centerX, double centerY, double* resultX, double* resultY){
	double phi = mod_double(_phi, 2 * pi);
	double new_x = cos(phi) * (x - centerX) - sin(phi) * (y - centerY) + centerX;
	double new_y = sin(phi) * (x - centerX) + cos(phi) * (y - centerY) + centerY;
	*resultX = new_x;
	*resultY = new_y;
}
#endif