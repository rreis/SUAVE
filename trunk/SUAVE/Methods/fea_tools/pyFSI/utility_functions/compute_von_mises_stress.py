#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
import numpy as np

def compute_von_mises_stress(elemlist):

    for i in range(0,len(elemlist)):
        elemlist[i].von_mises_computed = np.sqrt(0.5*(elemlist[i].in_stress_x-elemlist[i].in_stress_y)**2 + 3*elemlist[i].in_stress_xy**2)















    







