# weight_estimation.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Data, Data_Exception, Data_Warning
from SUAVE.Analyses import Analysis, Results
from Weights import Weights

#path to external framework
import sys

import numpy as np

#import SUAVE.Methods.fea_tools.pyFSI
#import weight_estimation
#
#
#from SUAVE.Methods.fea_tools.pyFSI.functions.geometry_generation import geometry_generation
#from weight_estimation import FEA_Weight
#from weight_estimation import Filenames
#from SUAVE.Plugins.VyPy.regression import gpr

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

class UADF(Weights):
    """ SUAVE.Analyses.Weights.Weights()
    """
    def __defaults__(self):
        self.tag = 'weights'
        self.vehicle  = Data()
        self.external = None
        self.settings = Data()
        self.settings.empty_weight_method = \
            SUAVE.Methods.Weights.FEA_based.empty
        
        self.surrogate = 0
        self.scaling_FD  = None
        self.surrogate_model_FD = None   
        
        
        
    def evaluate(self,conditions=None):
        
        
        #call weight estimation driver from weigfht estimation framework
        
        # unpack
        vehicle = self.vehicle
        empty   = self.settings.empty_weight_method
        
        if(self.surrogate == 0):
        
            # evaluate
            recompute_dvs = 1
            split_mesh = 0
            self.external.setup_design_problem(recompute_dvs,split_mesh)
            
            fea_code = 1 #tacs
            self.external.evaluate_weight(fea_code)
            weight_model = 2.0*self.external.primary_structure_weight
            
        
        elif(self.surrogate == 1):
            
            inputs = np.zeros(4)
            inputs[0] = vehicle.mass_properties.max_takeoff
            inputs[1] = vehicle.wings[0].taper
            #inputs[2] = vehicle.wings[0].tip_origin[0]
            #inputs[3] = vehicle.wings[0].tip_origin[2]
                      

            inputs[0] = (inputs[0]-30000.)/(100000.0 - 30000.)
            inputs[1] = (inputs[1]-0.25)/(0.5 - 0.25)
            #inputs[2] = (inputs[2]-10.0)/(30.0 - 10.0)
            #inputs[3] = (inputs[3]-19.0)/(40.0 - 19.0)
            
            
            #inputs[0] = vehicle.wings[0].tip_origin[2]
            #inputs[1] = vehicle.wings[0].tip_origin[0]            
            #inputs[2] = vehicle.wings[0].taper
            
            #inputs[0] = (inputs[0]-30.0)/(44.0-30.0)
            #inputs[1] = (inputs[1]-12.0)/(24.0-12.0)
            #inputs[2] = (inputs[2]-0.28)/(0.42-0.28)
            
            
            
            
            #setup inputs
            
            #evaluate the response surface
            surrogate_based_weight = self.evaluate_surrogate(inputs)
            
            
            weight_model = surrogate_based_weight*10000.
            
            

        results = empty(vehicle,weight_model)

        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results 

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty
        
        # done!
        return results
    
    
    
    def finalize(self):
        
        self.mass_properties = self.vehicle.mass_properties
        
        return
        
        
    def build_surrogate(self,filename = None,no_of_samples = None):
        
        filename = None
    
        if filename:
            
            #read the file name
            XS = np.zeros((no_of_samples,2))
            FS = np.zeros((no_of_samples,1))
            
            fid  = open(filename,'r')
            
            for iLine in range(0,no_of_samples):
                for line in fid:
                    line_split = line.split(',')
                    print line_split
                    
                    XS[iLine,0] = float(line_split[1])
                    XS[iLine,1] = float(line_split[2])
                    XS[iLine,2] = float(line_split[3])     
                    
                    FS[iLine,0] = float(line_split[0])
                    break
            
            
            fid.close()
        
            #build the surrogate using the GPR code
            
            [model_FD, scaling_FD] = self.setup_surrogate_spec(XS, FS)
            self.scaling_FD  = scaling_FD
            self.surrogate_model_FD = model_FD        
             
            
            self.surrogate = 1
        
        else:
            
            [XS,FS] = self.surrogate_data()
            
            #build the surrogate using the GPR code
            
            [model_FD, scaling_FD] = self.setup_surrogate_spec(XS, FS)
            self.scaling_FD  = scaling_FD
            self.surrogate_model_FD = model_FD        
             
            
            self.surrogate = 1            
            
            print "Surrogate filename not specified"
        
        
        
        
        
        
    def evaluate_surrogate(self,inputs):
        
        weight = self.evaluate_surrogate_spec(inputs,self.surrogate_model_FD,self.scaling_FD)        
        
        return weight

        
        
        
        
    def setup_surrogate_spec(self,XS,FS):
    
    
        # ---------------------------------------------------------
        #  Machine Learning
        # ---------------------------------------------------------
        # Build a gpr modeling object and train it with data
        # hypercube bounds
        # hypercube bounds
        ND = 2 # dimensions
        XB = np.array( [[0.,1.],[0.,1.]] )
        
        
        # start a training data object
        Train = gpr.training.Training(XB,XS,FS)
        #Train = gpr.training.Training(XB,XS,FS,DFS)
        
        # find scaling factors for normalizing data
        Scaling = gpr.scaling.Linear(Train)
        
        # scale the training data
        Train_Scl = Scaling.set_scaling(Train)
        
        # choose a kernel
        Kernel = gpr.kernel.Gaussian(Train_Scl)
        
        # choose an inference model (only one for now)
        Infer  = gpr.inference.Gaussian(Kernel)
        
        # choose a learning model (only one for now)
        Learn  = gpr.learning.Likelihood(Infer)
        
        # start a gpr modling object
        Model  = gpr.modeling.Regression(Learn)
        
        # learn on the training data
        Model.learn()
        
        #print Scaling
        
        return Model, Scaling    
    
    
    
    def evaluate_surrogate_spec(self,inputs,Model,Scaling):
    
        
        XI_scl = inputs/Scaling.XI
        
        # evaluate the model with the scaled features
        The_Data_Scl = Model.predict(XI_scl)
        
        The_Data = Scaling.unset_scaling(The_Data_Scl)
        
        # pull the estimated target function values
        FI = The_Data.YI
        
        return FI    
    
    
    def surrogate_data(self):
        
        
        XS  = np.array([[ 0.582291567143 ,  0.4 ],
                        [ 0.75929006 ,  0.31035315],
                        [ 0.21082239 ,  0.17967033],
                        [ 0.93418626 ,  0.78134223],
                        [ 0.48463971 ,  0.48867265],
                        [ 0.38812425 ,  0.61494747],
                        [ 0.65559148 ,  0.63847139],
                        [ 0.71795913 ,  0.11008306],
                        [ 0.1431664 ,  0.82422613],
                        [ 0.18022067 ,  0.9143566],
                        [ 0.57753258 ,  0.00662432],
                        [ 0.95174314 ,  0.23714105],
                        [ 0.58612539 ,  0.19839257],
                        [ 0.2894172 ,  0.84422439],
                        [ 0.850724 ,  0.87388061],
                        [ 0.4472769 ,  0.71309827],
                        [ 0.61375826 ,  0.88377927],
                        [ 0.80382709 ,  0.67095206],
                        [ 0.64071041 ,  0.86179073],
                        [ 0.09197384 ,  0.89737758],
                        [ 0.70361179 ,  0.02926583 ],
                        [ 0.76035503 ,  0.16602773 ],
                        [ 0.77568593 ,  0.4705908 ],
                        [ 0.79840453 ,  0.32643144 ],
                        [ 0.67539722 ,  0.34677039 ],
                        [ 0.30155682 ,  0.36597886 ],
                        [ 0.02630196 ,  0.05129641],
                        [ 0.8636613 ,  0.27158514 ],
                        [ 0.73716829 ,  0.64258022 ],
                        [ 0.25028125 ,  0.41398424 ],
                        [ 0.78046016 ,  0.56443844 ],
                        [ 0.1981673 ,  0.29257811 ],
                        [ 0.59047736 ,  0.15012879 ],
                        [ 0.88008109 ,  0.6815342 ],
                        [ 0.23729579 ,  0.9440055]])
            
            
        FS = np.array([1.48257620365 ,
                       3.28030476753 ,
                       1.33537304091 ,
                       3.30726209606 ,
                       1.91692867883 ,
                       3.73852022067 ,
                       4.36224305103 ,
                       4.60106195468 ,
                       1.39317357265 ,
                       1.8992892895 ,
                       4.03249625515 ,
                       8.05987436036 ,
                       2.96259571195 ,
                       3.04707554943 ,
                       9.45250631775 , 
                       3.87930786258 , 
                       10.9446805591 , 
                       8.04285298316 , 
                       3.05767086149 , 
                       1.71817409347 , 
                       2.09972663651 , 
                       2.85424381122 , 
                       5.10416845798 , 
                       2.98313918629 , 
                       2.29071472766 , 
                       2.14102749417 , 
                       1.29141698267 , 
                       3.02850643632 , 
                       3.76948528992 , 
                       2.48614348666 , 
                       3.9379471008 , 
                       2.68160253946 , 
                       9.85270548848 , 
                       10.0630411346 , 
                       1.92264462701 ])


        
        return XS,FS