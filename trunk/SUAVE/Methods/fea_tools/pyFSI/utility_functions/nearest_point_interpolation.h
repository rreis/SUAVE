/*!
compute nearest point
 */

#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>



//void nearest_point_interpolation(double **fl, double **str, int no_of_fluid_points, int no_of_structure_points, int *pt_map);
    

int compare_arg_sort( const void * a, const void * b );

void nearest_n_point_interpolation(int no_of_fluid_points, int no_of_structure_points, int n);