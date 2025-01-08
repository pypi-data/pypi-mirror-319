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

class SetupRayleighTaylor(setup.Setup):
    """
    Rayleigh-Taylor instability

    Parameters
    ----------
    n_waves: float
        The number of waves by which the boundary is perturbed.
    aspect_ratio: float
        The ratio of y to x extent of the domain.
    unit_l: float
        Code unit for length in units of centimeters.
    unit_t: float
        Code unit for time in units of seconds.
    unit_m: float
        Code unit for mass in units of gram.
    """
    
    def __init__(self, n_waves = 0.5, aspect_ratio = 3.0, unit_l = 1.0, unit_t = 1.0, unit_m = 1.0):

        setup.Setup.__init__(self)
        
        self.aspect_ratio = aspect_ratio
        self.rho_up = 2.0
        self.rho_dn = 1.0
        self.P0 = 2.5
        self.g = 1.0
        self.n_waves = n_waves
        self.delta_y =  0.05
        self.delta_vy =  0.1

        self.unit_l = unit_l
        self.unit_t = unit_t
        self.unit_m = unit_m

        return

    # ---------------------------------------------------------------------------------------------

    def shortName(self):
        
        return 'rt'

    # ---------------------------------------------------------------------------------------------
    
    def setInitialData(self, sim, nx):

        sim.setGravityMode(gravity_mode = 'fixed_acc', g = self.g)
        sim.setDomain(nx, int(nx * self.aspect_ratio), xmin = 0.0, xmax = 1.0 / self.aspect_ratio, 
                      ymin = 0.0, bc_type = 'wall')
        sim.setCodeUnits(unit_l = self.unit_l, unit_t = self.unit_t, unit_m = self.unit_m)
        
        # Sine wave in y-velocity
        x, y = sim.xyGrid()
        vy = self.delta_vy * np.sin(2.0 * np.pi * x * self.n_waves * self.aspect_ratio) \
                * np.exp(-0.5 * (y - 0.5)**2 / self.delta_y**2)

        # Set the pressure to increase towards the bottom to avoid some of the resulting shock waves
        sim.V[DN][y > 0.5] = self.rho_up
        sim.V[DN][y <= 0.5] = self.rho_dn
        sim.V[VX] = 0.0
        sim.V[VY] = vy
        sim.V[PR] = self.P0 + self.g * (1.0 - y) * self.rho_dn
    
        return
    
    # ---------------------------------------------------------------------------------------------

    def plotLimits(self, q_plot):
        
        vmin = []
        vmax = []

        for q in q_plot:
            if q == 'DN':
                vmin.append(self.rho_dn * 0.9)
                vmax.append(self.rho_up * 1.1)
            elif q in ['VX', 'VY']:
                vmin.append(-0.6)
                vmax.append(0.6)
            elif q == 'PR':
                vmin.append(self.P0 * 0.7)
                vmax.append(self.P0 * 1.3)
            else:
                vmin.append(None)
                vmax.append(None)
        
        return vmin, vmax, None

###################################################################################################
