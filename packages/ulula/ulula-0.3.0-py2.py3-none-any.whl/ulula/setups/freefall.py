###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import numpy as np

import ulula.simulation as ulula_sim
import ulula.setup_base as setup

###################################################################################################

# Shorthand for frequently used index constants
DN = ulula_sim.DN
VX = ulula_sim.VX
VY = ulula_sim.VY
PR = ulula_sim.PR

###################################################################################################

class SetupFreefall(setup.Setup):
    """
    Gravitational free-fall

    Parameters
    ----------
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup.Setup.__init__(self)
        
        self.rho0 = 0.1
        self.rho1 = 1.0
        self.P0 = 1.0
        self.gamma = 5.0 / 3.0
        self.g = 1.0

        self.blob_r = 0.2
        self.blob_y = 0.8
        
        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'freefall'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialData(self, sim, nx):
        
        n_x_fixed = 30
        
        sim.setGravityMode(gravity_mode = 'fixed_acc', g = self.g)
        sim.setDomain(n_x_fixed, nx, xmin = 0.0, xmax = float(n_x_fixed) / float(nx), ymin = 0.0, bc_type = 'outflow')
        sim.setCodeUnits(unit_l = self.unit_l, unit_t = self.unit_t, unit_m = self.unit_m)

        #sim.V[DN] = self.rho0
        sim.V[VX] = 0.0
        sim.V[VY] = 0.0
        sim.V[PR] = self.P0

        x, y = sim.xyGrid()
        r = np.sqrt((x - sim.xmax * 0.5)**2 + (y - self.blob_y)**2)
        sigma = self.blob_r * sim.xmax
        sim.V[DN] = self.rho0 + self.rho1 * np.exp(-0.5 * r**2 / sigma**2)
        
        sim.setGravityPotentials()
        
        return
        
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(0.0)
                #vmax.append(self.rho1 * 0.8)
                vmax.append(self.rho1 * 1.2)
            elif q in ['VX', 'VY']:
                vmin.append(-0.8)
                vmax.append(0.8)
            elif q == 'PR':
                vmin.append(self.P0 * 0.8)
                vmax.append(self.P0 * 1.4)
            elif q == 'ET':
                vmin.append(1.3)
                vmax.append(2.0)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None
  
    # ---------------------------------------------------------------------------------------------

    def trueSolution(self, sim, x, q_plot):
        
        t = sim.t
        y_blob = self.blob_y - 0.5 * self.g * t**2
        sigma = self.blob_r * sim.xmax
        
        sol = np.zeros((len(q_plot), len(x)))
        for i in range(len(q_plot)):
            q = q_plot[i]
            if q == 'DN':
                sol[i, :] = self.rho0 + self.rho1 * np.exp(-0.5 * (x - y_blob)**2 / sigma**2)
            else:
                pass
        
        return sol

###################################################################################################
