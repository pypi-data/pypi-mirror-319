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

class SetupAdvection(setup.Setup):
    """
    Tophat advection test
    
    In this test, an initially overdense tophat is placed at the center of the domain. The entire
    fluid moves towards the northeast direction. This test is the 2D equivalent of tophat 
    advection in 1D and mostly tests how diffusive a hydro solver is.
    
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
        
        self.rho0 = 1.0
        self.rho1 = 2.0
        self.P0 = 1.0
        self.ux = 0.5
        self.uy = 0.3
        self.r_th = 0.1
        self.gamma = 5.0 / 3.0

        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m
        
        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'advection'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialData(self, sim, nx):
        
        sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')
        sim.setFluidProperties(self.gamma)
        sim.setCodeUnits(unit_l = self.unit_l, unit_t = self.unit_t, unit_m = self.unit_m)

        sim.V[DN] = self.rho0
        sim.V[VX] = self.ux
        sim.V[VY] = self.uy
        sim.V[PR] = self.P0

        # Set tophat into the center of the domain
        x, y = sim.xyGrid()
        r = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
        mask = (r <= self.r_th)
        sim.V[DN][mask] = self.rho1
        
        return
        
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot):

        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho0 * 0.9)
                vmax.append(self.rho1 * 1.05)
            elif q in ['VX', 'VY']:
                vmin.append(0.0)
                vmax.append(1.0)
            elif q == 'PR':
                vmin.append(self.P0 * 0.8)
                vmax.append(self.P0 * 1.2)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
