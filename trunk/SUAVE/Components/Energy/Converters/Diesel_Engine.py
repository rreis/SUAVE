# Diesel_Engine.py
#
# Created:  Aug, 2016: M. Vegh

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE
from SUAVE.Core import Data, Units

# package imports
import numpy as np
from SUAVE.Components.Energy.Energy_Component import Energy_Component

# ----------------------------------------------------------------------
#  Internal Combustion Engine Class
# ----------------------------------------------------------------------

class Diesel_Engine(Energy_Component):

    def __defaults__(self):

        self.sea_level_power                = 0.0
        self.flat_rate_altitude             = 6000. * Units.feet
        #self.speed                          = 0.0 #not used here
        self.BSFC                           = .36*Units['lb/hp/hr']  #reference SLS BSFC at 100% power
        
        #lapse coefficient; Y = lapse_coefficient*delta*theta^lapse_exponent
        #where delta is pressure ratio and theta is temperature ratio relative to SLS
        self.lapse_exponent                 = -1.575
        self.lapse_coefficient              = 1.1594
        
        #power available is linear with lapse factor, after the flat rate altitude
        self.power_available_linear_coefficent   = 1.0504
        self.power_available_constant_coefficent = .131
        
        #efficiency fuel_flow coefficients (model as a cubic polynomial based on ff/ff_ref = f(P/Pavailable))
        self.fuel_flow_constant_coefficient  = 0.
        self.fuel_flow_linear_coefficient    = 1.22
        self.fuel_flow_quadratic_coefficient = -.55
        self.fuel_flow_cubic_coefficient     = .33
        
        
    def power(self,conditions):
        """ The internal combustion engine output power and specific power consumption

        Inputs:
            Engine:
                sea-level power
                flat rate altitude
                speed (RPM)
                throttle setting
            Freestream conditions:
                altitude
                delta_isa
        Outputs:
            Brake power (or Shaft power)
            Power (brake) specific fuel consumption
            Fuel flow
            Torque

        """

        # Unpack
        altitude    = conditions.freestream.altitude
        delta_isa   = conditions.freestream.delta_ISA
        temperature = conditions.freestream.temperature
        
        throttle    = conditions.propulsion.combustion_engine_throttle
        PSLS        = self.sea_level_power
        h_flat      = self.flat_rate_altitude
        #speed       = self.speed
        BSFC        = self.BSFC

        
        #altitude_virtual = altitude - h_flat # shift in power lapse due to flat rate
        atmo = SUAVE.Analyses.Atmospheric.US_Standard_1976()
        atmo_values = atmo.compute_values(altitude)
        p   = atmo_values.pressure
        T   = atmo_values.temperature
        rho = atmo_values.density
        a   = atmo_values.speed_of_sound
        mu  = atmo_values.dynamic_viscosity

        # computing the sea-level ISA atmosphere conditions
        atmo_values = atmo.compute_values(0,0)
        p0   = atmo_values.pressure[0,0]
        T0   = atmo_values.temperature[0,0]
        rho0 = atmo_values.density[0,0]
        a0   = atmo_values.speed_of_sound[0,0]
        mu0  = atmo_values.dynamic_viscosity[0,0]

        # calculating the lapse factor:
        theta = T/T0
        delta = p/p0
        Y     = self.lapse_coefficient*delta*(theta**self.lapse_exponent)
        
        # calculating available power based on Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)
       
        '''
        Pavailable = PSLS * (sigma - 0.117) / 0.883        
        Pavailable[h_flat > altitude]  = PSLS
        '''
        
        # applying throttle setting
        Pavailable   = np.fmin(np.ones_like(Y),(self.power_available_linear_coefficent * Y +self.power_available_constant_coefficent))*PSLS
        output_power = Pavailable * throttle
        
        
        #print 'Pavailable[0] = ', Pavailable[0]
        #print 'output_power[0] = ', output_power[0]
        

        #fuel flow rate
        c0 = self.fuel_flow_constant_coefficient 
        c1 = self.fuel_flow_linear_coefficient   
        c2 = self.fuel_flow_quadratic_coefficient
        c3 = self.fuel_flow_cubic_coefficient    
        
        a = np.array([0.])
        ff = c0 + c1*throttle + c2*(throttle**2)+ c3*(throttle**3.) #fuel flow ratio
        
        fuel_flow_rate   = np.fmax(ff*BSFC*PSLS,np.array([0.]))

        #torque
        ## SHP = torque * 2*pi * RPM / 33000        (UK units)
        # store to outputs
        self.outputs.power                           = output_power
        self.outputs.power_specific_fuel_consumption = ff*BSFC
        self.outputs.fuel_flow_rate                  = fuel_flow_rate

       
        return self.outputs

if __name__ == '__main__':

    import numpy as np
    import pylab as plt
    import SUAVE
    from SUAVE.Core import Units, Data
    conditions = Data()
    atmo = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    ICE = SUAVE.Components.Energy.Converters.Internal_Combustion_Engine()
    ICE.sea_level_power = 250.0 * Units.horsepower
    ICE.flat_rate_altitude = 5000. * Units.ft
    ICE.speed = 2200. # rpm
    ICE.throttle = 1.0
    PSLS = 1.0
    delta_isa = 0.0
    i = 0
    altitude = list()
    rho = list()
    sigma = list()
    Pavailable = list()
    torque = list()
    for h in range(0,25000,500):
        altitude.append(h * 0.3048)
        atmo_values = atmo.compute_values(altitude[i],delta_isa)
        rho.append(atmo_values.density[0,0])
        sigma.append(rho[i] / 1.225)
##        Pavailable.append(PSLS * (sigma[i] - 0.117) / 0.883)
        conditions.altitude = altitude[i]
        conditions.delta_isa = delta_isa
        out = ICE.power(conditions)
        Pavailable.append(out.power)
        torque.append(out.torque)
        i += 1
    fig = plt.figure("Power and Torque vs altitude")
    axes = fig.add_subplot(2,1,1)
    axes.plot(np.multiply(altitude,1./Units.ft), np.multiply(Pavailable,1./Units.horsepower), 'bo-')
    axes.set_xlabel('Altitude [ft]')
    axes.set_ylabel('Output power [bhp]')
    axes.grid(True)

    axes = fig.add_subplot(2,1,2)
    axes.plot(np.multiply(altitude,1./Units.ft), np.multiply(torque,1./(Units.ft * Units.lbf)), 'rs-')
    axes.set_xlabel('Altitude [ft]')
    axes.set_ylabel('Torque [lbf*ft]')
    axes.grid(True)
    plt.show()