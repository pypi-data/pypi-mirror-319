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

class SetupCloudCrushing(setup.Setup):
    """
    Cloud-crushing setup

    In this setup, a denser cloud is embedded in a hot, fast-moving, less dense wind at equal
    pressure. The cloud is rapidly destroyed.

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
        self.rho1 = 100.0
        self.P0 = 1.0
        self.ux = 0.4
        self.r_c = 0.1
        self.gamma = 5.0 / 3.0
        
        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m

        return 

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'cloud_crushing'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialData(self, sim, nx):
        
        sim.setDomain(nx, nx // 3, xmin = 0.0, xmax = 3.0, ymin = 0.0, bc_type = 'outflow')
        sim.setFluidProperties(self.gamma)
        sim.setCodeUnits(unit_l = self.unit_l, unit_t = self.unit_t, unit_m = self.unit_m)

        sim.V[DN] = self.rho0
        sim.V[VX] = self.ux
        sim.V[VY] = 0.0
        sim.V[PR] = self.P0

        # Set tophat into the center of the domain
        x, y = sim.xyGrid()
        r = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
        mask = (r <= self.r_c)
        sim.V[DN][mask] = self.rho1
        sim.V[VX][mask] = 0.0
        
        return
        
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot):

        vmin = []
        vmax = []
        log = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho0)
                vmax.append(self.rho1 * 0.8)
                log.append(True)
            elif q in ['VX', 'VY']:
                vmin.append(-self.ux * 1.1)
                vmax.append(self.ux * 1.1)
                log.append(False)
            elif q == 'PR':
                vmin.append(self.P0 * 0.5)
                vmax.append(self.P0 * 1.3)
                log.append(True)
            else:
                vmin.append(None)
                vmax.append(None)
                log.append(False)
        
        return vmin, vmax, log

###################################################################################################
