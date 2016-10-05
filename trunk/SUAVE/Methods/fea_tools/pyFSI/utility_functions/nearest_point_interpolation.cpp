/*!
compute nearest point
 */

//void nearest_point_interpolation(double **fl, double **str, int no_of_fluid_points, int no_of_structure_points, int *point_map){

//for each fluid point, find the array of the distance between the fluid and structure nodes
//array of the input node numbers
//arg_sort_list = fl_str_distances;
//qsort(structure_node_numbers, num_str_nodes, sizeof(int), compare_arg_sort);
//arg_sort_list = NULL;


//static const int * arg_sort_list = NULL;
//
//static int compare_arg_sort( const void * a, const void * b ){
//    // return (*(int*)a - *(int*)b)
//    return arg_sort_list[*(int*)a] - arg_sort_list[*(int*)b];
//}



#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;


double * arg_sort_list = NULL;

int compare_arg_sort( const void * a, const void * b ){

    int return_value=0;
    
    if ( arg_sort_list[*(int*)a] - arg_sort_list[*(int*)b] <0 ) return -1;
    if ( arg_sort_list[*(int*)a] - arg_sort_list[*(int*)b] == 0 ) return 0;
    if ( arg_sort_list[*(int*)a] - arg_sort_list[*(int*)b] > 0 ) return 1;
    
}

void nearest_n_point_interpolation(int no_of_fluid_points, int no_of_structure_points, int n){
    
    
    
    ifstream mesh_file;
    ofstream output_file;
    char meshfile[200];
    int closest_point;
    double distance;
    double minimum_distance;
    unsigned long point_map[no_of_fluid_points];
    
    double * fl_str_distances;
    int * str_order;
    
    int * closest_n_elements;
    
    
    //int *point_map;
    //double fl[no_of_fluid_points][3];
    double ** fl;
    fl =  new double *[no_of_fluid_points];
    for (int i=0;i<no_of_fluid_points;i++){
        
        fl[i]  = new double[3];
        
    }
    
    
    
    //double str[no_of_structure_points][3];
    double ** str;
    str =  new double *[no_of_structure_points];
    for (int i=0;i<no_of_structure_points;i++){
        
        str[i]  = new double[3];
        
    }
    
    
    string text_line;
    
    //read the fluid and structure points from the specified filename
    
    mesh_file.open("loads.txt", ios::in);
    for (int iPoint = 0; iPoint < no_of_fluid_points; iPoint ++) {
        getline(mesh_file, text_line);
        istringstream point_line(text_line);
        point_line >> fl[iPoint][0]; point_line >> fl[iPoint][1];point_line >> fl[iPoint][2];
    }
    
    for (int iPoint = 0; iPoint < no_of_structure_points; iPoint ++) {
        getline(mesh_file, text_line);
        istringstream point_line(text_line);
        point_line >> str[iPoint][0]; point_line >> str[iPoint][1];point_line >> str[iPoint][2];
    }
    
    
     mesh_file.close();
    
    
    
    //now find the nearest 10 points by first sorting and then storing the top 10 elements=a
    fl_str_distances = new double[no_of_structure_points];
    str_order = new int[no_of_structure_points];
    closest_n_elements =  new int[n*no_of_fluid_points];
    

    // interpolate the mesh
    for(int i=0;i<no_of_fluid_points;i++){
        
        
        for (int j=0;j<no_of_structure_points;j++){
            
            str_order[j] = j;
            
            fl_str_distances[j] = (fl[i][0] -str[j][0])*(fl[i][0] -str[j][0]) + (fl[i][1] -str[j][1])*(fl[i][1] -str[j][1]) + (fl[i][2] -str[j][2])*(fl[i][2] -str[j][2]);
            
            
        }
        

        
        
        arg_sort_list = fl_str_distances;
        
        qsort(str_order, no_of_structure_points, sizeof(int), compare_arg_sort);

        
        
        for (int ij=0;ij<n;ij++){
            
            closest_n_elements[i*n + ij] = str_order[ij];
            
        }
        
        
        arg_sort_list = NULL;
        
    }
    


    
    output_file.open("interpolation.txt", ios::out);
    for (int iPoint = 0; iPoint < no_of_fluid_points; iPoint ++) {
        for (int ij=0;ij<n;ij++){
            
            output_file << closest_n_elements[iPoint*n + ij] << ",";
            
        }
        
        output_file << "\n";
        
    }
    
    
    output_file.close();

    
    for (int i=0;i<no_of_fluid_points;i++){
        
         delete[] fl[i];
        
    }
    delete[] fl;
    
    

    for (int i=0;i<no_of_structure_points;i++){
        
         delete[] str[i];
        
    }

    delete[] str;
    
    delete[] fl_str_distances;
    delete[] str_order;
    delete[] closest_n_elements;
    
    

    
    
}


