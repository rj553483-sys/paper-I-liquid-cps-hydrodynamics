import numpy as np

R_P0 = 25.0        # Pristine pore radius (um)
R_P_20 = 15.2      # Pore radius at 20 dpa compaction (um)
GAMMA_LV = 0.350   # Liquid lithium surface tension at 573 K (N/m)
THETA_DEG = 15.0   # Wetting contact angle (degrees)
THETA_RAD = np.radians(THETA_DEG)

K0 = 1.25e-11      # Pristine Carman-Kozeny permeability (m^2)
Q_DRYOUT_0 = 41.50 # Pristine dryout heat flux (MW/m^2)
Q_BASELINE = 15.00 # Divertor operational baseline heat flux (MW/m^2)
K_Q = 0.0626       # Calibrated exponential dryout decay constant (dpa^-1)

def calc_pore_radius(dpa, beta_r=0.12):
    return R_P0 - (R_P0 - R_P_20) * (1.0 - np.exp(-beta_r * dpa)) / (1.0 - np.exp(-beta_r * 20.0))

def calc_capillary_pressure(r_p_um):
    return (2.0 * GAMMA_LV * np.cos(THETA_RAD)) / (r_p_um * 1e-6) / 1000.0

def calc_permeability(dpa, beta_k=0.115, decay_frac=0.696):
    return K0 * (1.0 - decay_frac * (1.0 - np.exp(-beta_k * dpa)) / (1.0 - np.exp(-beta_k * 20.0)))

def calc_dryout_heat_flux(dpa):
    return Q_DRYOUT_0 * np.exp(-K_Q * dpa)

def calc_safety_factor(q_dryout):
    return q_dryout / Q_BASELINE
