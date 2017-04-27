import numpy as np
import copy
import SUAVE
import pyOpt
import sklearn
from sklearn import gaussian_process
from SUAVE.Core import Units, Data
from SUAVE.Optimization import helper_functions as help_fun
from SUAVE.Methods.Utilities.latin_hypercube_sampling import latin_hypercube_sampling

def Additive_Solve(problem,num_fidelity_levels=2,num_samples=10):
    
    if num_fidelity_levels != 2:
        raise NotImplementedError
    
    inp = problem.optimization_problem.inputs
    obj = problem.optimization_problem.objective
    con = problem.optimization_problem.constraints 
    tr = problem.trust_region
    # Set inputs
    nam = inp[:,0] # Names
    ini = inp[:,1] # Initials
    bnd = inp[:,2] # Bounds
    scl = inp[:,3] # Scale
    typ = inp[:,4] # Type

    # Pull out the constraints and scale them
    bnd_constraints = help_fun.scale_const_bnds(con)
    scaled_constraints = help_fun.scale_const_values(con,bnd_constraints)

    x   = ini/scl        
    # need to make this into a vector of some sort that can be added later
    lbd  = []#np.zeros(np.shape(bnd[:][1]))
    ubd  = []#np.zeros(np.shape(bnd[:][1]))
    edge = []#np.zeros(np.shape(bnd[:][1]))
    name = []#[None]*len(bnd[:][1])
    up_edge  = []
    low_edge = []
    
    
    #bnd[1000]
    for ii in xrange(0,len(inp)):
        lbd.append(bnd[ii][0]/scl[ii])
        ubd.append(bnd[ii][1]/scl[ii])

    for ii in xrange(0,len(con)):
        name.append(con[ii][0])
        edge.append(scaled_constraints[ii])
        if con[ii][1]=='<':
            up_edge.append(edge[ii])
            low_edge.append(-np.inf)
        elif con[ii][1]=='>':
            up_edge.append(np.inf)
            low_edge.append(edge[ii])
            
        elif con[ii][1]=='=':
            up_edge.append(edge[ii])
            low_edge.append(edge[ii])
        
    lbd = np.array(lbd)
    ubd = np.array(ubd)
    edge = np.array(edge)
    up_edge  = np.array(up_edge)         
    low_edge = np.array(low_edge)     
    
    x_samples = latin_hypercube_sampling(len(x),num_samples,bounds=(lbd,ubd))
    
    f = np.zeros(num_fidelity_levels,num_samples)
    g = np.zeros(num_fidelity_levels,num_samples)
    
    for level in range(num_fidelity_levels):
        problem.fidelity_level = level
        for ii,x in enumerate(x_samples):
            res = self.evaluate_model(problem,x,scaled_constraints)
            f[level-1,ii]  = res[0]    # objective value
            g[level-1,ii]  = res[1]    # constraints vector
        
    # Build objective surrogate
    f_diff = f[1,:] - f[0,:]
    f_additive_surrogate_base = gaussian_process.GaussianProcess()
    f_additive_surrogate = f_additive_surrogate_base.fit(f[0,:], f_diff)     
    
    # Build constraint surrogate
    g_diff = g[1,:] - g[2,:]
    g_additive_surrogate_base = gaussian_process.GaussianProcess()
    g_additive_surrogate = g_additive_surrogate_base.fit(g[0,:], g_diff)     
    
    # Optimize corrected model
    
    opt_prob = pyOpt.Optimization('SUAVE',evaluate_corrected_model, \
                                  obj_surrogate=f_additive_surrogate,cons_surrogate=g_additive_surrogate)
    
    for ii in xrange(len(obj)):
        opt_prob.addObj('f',f[-1]) 
    for ii in xrange(0,len(inp)):
        vartype = 'c'
        opt_prob.addVar(nam[ii],vartype,lower=tr.lower_bound[ii],upper=tr.upper_bound[ii],value=x[ii])    
    for ii in xrange(0,len(con)):
        if con[ii][1]=='<':
            opt_prob.addCon(name[ii], type='i', upper=edge[ii])
        elif con[ii][1]=='>':
            opt_prob.addCon(name[ii], type='i', lower=edge[ii],upper=np.inf)
        elif con[ii][1]=='=':
            opt_prob.addCon(name[ii], type='e', equal=edge[ii])      
            
       
    opt = pyOpt.pySNOPT.SNOPT()      
    #opt.setOption('Major iterations limit'     , self.optimizer_max_iterations)
    #opt.setOption('Major optimality tolerance' , self.optimizer_convergence_tolerance)
    #opt.setOption('Major feasibility tolerance', self.optimizer_constraint_tolerance)
    #opt.setOption('Function precision'         , self.optimizer_function_precision)
    #opt.setOption('Verify level'               , self.optimizer_verify_level) 
    
    problem.fidelity_level = 1
    outputs = opt(opt_prob, sens_type='FD',problem=problem, \
                  obj_surrogate=f_additive_surrogate,cons_surrogate=g_additive_surrogate)#, sens_step = sense_step)  
    fOpt_lo = outputs[0]
    xOpt_lo = outputs[1]
    gOpt_lo = np.zeros([1,len(con)])[0]    
    
    return (fOpt,xOpt)
    
    
def evaluate_model(problem,x,cons,der_flag=True):
    f  = np.array(0.)
    g  = np.zeros(np.shape(cons))
    
    f  = problem.objective(x)
    g  = problem.all_constraints(x)
    
    return f,g
    
def evaluate_corrected_model(x,problem=None,obj_surrogate=None,cons_surrogate=None):
    obj   = problem.objective(x)
    const = problem.all_constraints(x).tolist()
    fail  = np.array(np.isnan(obj.tolist()) or np.isnan(np.array(const).any())).astype(int)
    
    obj_addition  = obj_surrogate(x)
    cons_addition = cons_surrogate(x)
    
    obj   = obj + obj_addition
    const = const + cons_addition
    const = const.tolist()

    print 'Inputs'
    print x
    print 'Obj'
    print obj
    print 'Con'
    print const
        
    return obj,const,fail