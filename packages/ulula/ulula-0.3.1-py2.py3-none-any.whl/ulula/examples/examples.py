###################################################################################################
#
# This file is part of the ULULA code.
#
# (c) Benedikt Diemer, University of Maryland
#
###################################################################################################

import ulula.simulation as ulula_sim
import ulula.run as ulula_run

import ulula.setups.advection as setup_advection
import ulula.setups.cloud_crushing as setup_cloud_crushing
import ulula.setups.freefall as setup_freefall
import ulula.setups.kelvin_helmholtz as setup_kelvin_helmholtz
import ulula.setups.rayleigh_taylor as setup_rayleigh_taylor
import ulula.setups.sedov as setup_sedov
import ulula.setups.shocktube as setup_shocktube
import ulula.setups.tidal_disruption as setup_tidal_disruption

###################################################################################################

# Default hydro scheme
def_hydro_scheme = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', 
                        riemann = 'hll', time_integration = 'hancock', cfl = 0.8)

###################################################################################################

def main():
    
    # ---------------------------------------------------------------------------------------------
    # Setups without gravity
    # ---------------------------------------------------------------------------------------------
    
    #advection()
    
    #cloudCrushing()
    
    #kelvinHelmholtz()
    #kelvinHelmholtzMovie()
    
    #sedovExplosion(plot1d = False)
    #sedovExplosion(plot1d = True)
    
    #shocktube()

    # ---------------------------------------------------------------------------------------------
    # Setups with gravity
    # ---------------------------------------------------------------------------------------------
    
    #freefall()

    #rayleighTaylor()
    
    #tidalDisruption()

    return

###################################################################################################

def advection():
    """
    Test of different solvers in 2D advection problem
    
    This function produces four runs of the same top-hat advection problem. An initial overdense
    disk is moving with the fluid towards the top right of the domain. The edges of the disk 
    diffuse into the surrounding fluid at a rate that depends on the hydro solver. When using the
    MC limiter with an Euler (first-order) time integration, the test fails entirely.
    
    The large ``plot_step`` and ``plot_ics = False`` ensure that only the final snapshots are 
    plotted.
    """

    setup = setup_advection.SetupAdvection()
    kwargs = dict(nx = 100, tmax = 2.5, plot_step = 1000, save_plots = True, plot_ics = False, q_plot = ['DN'])

    hs = ulula_sim.HydroScheme(reconstruction = 'const', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_const', **kwargs)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'minmod', time_integration = 'euler', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_minmod_euler', **kwargs)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'euler', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_mc_euler', **kwargs)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'hancock', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear_mc_hancock', **kwargs)

    return

###################################################################################################

def shocktube():
    """
    1D test of hydro solver with shock tube
    
    This function executes a shocktube test in pseudo-1D (by creating a domain that is much longer
    in x than in y, and by making it symmetric in y). The function creates outputs for piecewise-
    constant states and piecewise-linear reconstruction.
    """

    setup = setup_shocktube.SetupShocktubeX()
    kwargs = dict(tmax = 0.2, nx = 100, plot_step = 1000, save_plots = True, plot1d = True, 
                plot_ics = False, q_plot = ['DN', 'VX', 'PR'])
    
    hs = ulula_sim.HydroScheme(reconstruction = 'const', cfl = 0.5)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_const', **kwargs)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'vanleer', riemann = 'hll', 
                            time_integration = 'hancock', cfl = 0.5)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '_linear', **kwargs)
    
    return

###################################################################################################

def kelvinHelmholtz():
    """
    The Kelvin-Helmholtz instability
    
    This function creates an interactive plot of the Kelvin-Helmholtz instability. It should take
    less than a minute to run on a modern laptop.
    """

    kwargs = dict(tmax = 2.0, nx = 200, q_plot = ['DN', 'VX'], plot_step = 2000, save_plots = False, plot_ics = False)
    hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
    
    setup = setup_kelvin_helmholtz.SetupKelvinHelmholtz(n_waves = 1)
    ulula_run.run(setup, hydro_scheme = hs, **kwargs)

    return

###################################################################################################

def kelvinHelmholtzMovie():
    """
    Movie of the Kelvin-Helmholtz instability
    
    This function demonstrates how to make movies with Ulula. By passing the ``movie`` parameter,
    the function outputs frames at a user-defined rate and combines them into a movie at the end
    of the simulation.
    """

    kwargs = dict(tmax = 4.0, nx = 200, q_plot = ['DN', 'VX'], movie = True, movie_length = 20.0)
    hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
    
    setup = setup_kelvin_helmholtz.SetupKelvinHelmholtz(n_waves = 1)
    ulula_run.run(setup, hydro_scheme = hs, **kwargs)

    return

###################################################################################################

def sedovExplosion(nx = 200, plot1d = True):
    """
    Test of Sedov-Taylor explosion against analytic solution
    
    This function demonstrates another style of 1D plotting where the solution is averaged in 
    radial bins.
    """

    setup = setup_sedov.SetupSedov()
    kwargs = dict(tmax = 0.02, nx = nx, plot_step = 1000, save_plots = True, 
                plot_ics = False, plot_file_ext = 'pdf')    
    if plot1d:
        kwargs.update(dict(plot1d = True, q_plot = ['DN', 'PR', 'VT'], plot_type = 'radius'))
    else:
        kwargs.update(dict(q_plot = ['DN', 'PR']))

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.9)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '', **kwargs)

    return


###################################################################################################

def cloudCrushing():
    """
    Test of the cloud-crushing problem
    
    This function demonstrates a non-square domain with outflow boundary conditions.
    """

    setup = setup_cloud_crushing.SetupCloudCrushing()
    kwargs = dict(tmax = 20, nx = 300, q_plot = ['DN', 'VX'], plot_file_ext = 'pdf', plot_time = 1.0)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', time_integration = 'hancock', limiter = 'mc', cfl = 0.85)
    ulula_run.run(setup, hydro_scheme = hs, **kwargs)

    return

###################################################################################################

def freefall():
    """
    Test of the gravity solver
    
    In this setup, the entire domain (including a denser ball for visibility) falls under constant
    acceleration. A 1D plot shows that the result matches the expected position accurately.
    """

    setup = setup_freefall.SetupFreefall()
    kwargs = dict(nx = 300, tmax = 1.2, plot_step = None, plot_time = 0.1, print_step = 100, save_plots = True, plot_ics = True, 
                q_plot = ['DN'], plot_file_ext = 'pdf', plot1d = True)

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'hancock', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '', **kwargs)

    return

###################################################################################################

def rayleighTaylor():
    """
    Rayleigh-Taylor instability
    
    A denser fluid sits on top of a less dense fluid, but as the boundary is perturbed, a well-
    known mushroom-like structure forms.
    """

    setup = setup_rayleigh_taylor.SetupRayleighTaylor()
    kwargs = dict(nx = 80, tmax = 6.0, plot_time = 0.2, print_step = 100, save_plots = True, plot_ics = True, 
                q_plot = ['DN', 'VY'], plot_ghost_cells = False, plot_file_ext = 'pdf')

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'hancock', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, **kwargs)

    return

###################################################################################################

def tidalDisruption():
    """
    Tidal disruption of a gas blob
    
    A gas blob falls into a point-mass potential and is tidally disrupted. This test demonstrates
    how to set up a fixed gravitational potential.
    """

    setup = setup_tidal_disruption.SetupTidalDisruption()
    kwargs = dict(nx = 120, tmax = 3.0, plot_step = None, plot_time = 0.1, print_step = 100, save_plots = True, plot_ics = True, 
                q_plot = ['DN', 'GP'], plot_ghost_cells = False, plot_file_ext = 'pdf')

    hs = ulula_sim.HydroScheme(reconstruction = 'linear', limiter = 'mc', time_integration = 'hancock', cfl = 0.8)
    ulula_run.run(setup, hydro_scheme = hs, plot_suffix = '', **kwargs)

    return

###################################################################################################
# Trigger
###################################################################################################

if __name__ == "__main__":
    main()
