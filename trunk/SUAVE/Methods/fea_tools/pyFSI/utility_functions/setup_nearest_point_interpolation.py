
from distutils.core import setup, Extension

code_module =Extension('_nearest_point_interpolation',

sources=['nearest_point_interpolation_wrap.cxx','nearest_point_interpolation.cpp'])

setup(name        ='nearest_point_interpolation',
      ext_modules  =[code_module])



