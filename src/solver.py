import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.switch_backend('Agg')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    calc_pore_radius, calc_capillary_pressure, calc_permeability,
    calc_dryout_heat_flux, calc_safety_factor
)

def run_simulation(num_points=500):
    dpa = np.linspace(0, 20, num_points)
    
    r_p = calc_pore_radius(dpa)
    delta_P_cap = calc_capillary_pressure(r_p)
    K = calc_permeability(dpa)
    q_dryout = calc_dryout_heat_flux(dpa)
    SF = calc_safety_factor(q_dryout)
    
    # Base directory context
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(root_dir, 'data')
    fig_dir = os.path.join(root_dir, 'figures')
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    # Save Raw Data CSV
    df = pd.DataFrame({
        'dpa': dpa,
        'pore_radius_um': r_p,
        'capillary_pressure_kPa': delta_P_cap,
        'permeability_1e11_m2': K * 1e11,
        'dryout_heat_flux_MW_m2': q_dryout,
        'safety_factor': SF
    })
    df.to_csv(os.path.join(data_dir, 'raw_simulation_data.csv'), index=False)
    
    # Benchmark Summary JSON
    idx_0 = 0
    idx_9_8 = np.argmin(np.abs(dpa - 9.8))
    idx_13_0 = np.argmin(np.abs(dpa - 13.0))
    idx_20_0 = -1
    
    summary = {
        "pristine_0_dpa": {
            "dpa": 0.0,
            "pore_radius_um": round(float(r_p[idx_0]), 2),
            "capillary_pressure_kPa": round(float(delta_P_cap[idx_0]), 2),
            "permeability_1e11_m2": round(float(K[idx_0]*1e11), 2),
            "dryout_heat_flux_MW_m2": round(float(q_dryout[idx_0]), 2),
            "safety_factor": round(float(SF[idx_0]), 2)
        },
        "replacement_limit_9_8_dpa": {
            "dpa": 9.8,
            "pore_radius_um": round(float(r_p[idx_9_8]), 2),
            "capillary_pressure_kPa": round(float(delta_P_cap[idx_9_8]), 2),
            "permeability_1e11_m2": round(float(K[idx_9_8]*1e11), 2),
            "dryout_heat_flux_MW_m2": round(float(q_dryout[idx_9_8]), 2),
            "safety_factor": round(float(SF[idx_9_8]), 2)
        },
        "dryout_parity_limit_13_0_dpa": {
            "dpa": 13.0,
            "pore_radius_um": round(float(r_p[idx_13_0]), 2),
            "capillary_pressure_kPa": round(float(delta_P_cap[idx_13_0]), 2),
            "permeability_1e11_m2": round(float(K[idx_13_0]*1e11), 2),
            "dryout_heat_flux_MW_m2": round(float(q_dryout[idx_13_0]), 2),
            "safety_factor": round(float(SF[idx_13_0]), 2)
        },
        "extreme_damage_20_0_dpa": {
            "dpa": 20.0,
            "pore_radius_um": round(float(r_p[idx_20_0]), 2),
            "capillary_pressure_kPa": round(float(delta_P_cap[idx_20_0]), 2),
            "permeability_1e11_m2": round(float(K[idx_20_0]*1e11), 2),
            "dryout_heat_flux_MW_m2": round(float(q_dryout[idx_20_0]), 2),
            "safety_factor": round(float(SF[idx_20_0]), 2)
        }
    }
    
    with open(os.path.join(data_dir, 'benchmark_summary.json'), 'w') as f:
        json.dump(summary, f, indent=4)
    
    # Figure 1
    fig, ax1 = plt.subplots(figsize=(8, 4.5), dpi=300)
    color_navy = '#0f172a'
    color_red = '#dc2626'
    
    ax1.set_xlabel('Displacement Damage (dpa)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Pore Radius r_p (um)', color=color_navy, fontsize=11, fontweight='bold')
    ax1.plot(dpa, r_p, color=color_navy, linewidth=2.5, label='Pore Radius')
    ax1.tick_params(axis='y', labelcolor=color_navy)
    ax1.set_ylim(14, 26)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Capillary Retention Pressure (kPa)', color=color_red, fontsize=11, fontweight='bold')
    ax2.plot(dpa, delta_P_cap, color=color_red, linewidth=2.5, linestyle='--', label='Capillary Pressure')
    ax2.tick_params(axis='y', labelcolor=color_red)
    ax2.set_ylim(26, 46)
    
    plt.title('Porous Tungsten CPS Degradation vs Fast-Neutron Fluence', fontsize=12, fontweight='bold', pad=12)
    ax1.grid(True, linestyle=':', alpha=0.6)
    fig.tight_layout()
    
    plt.savefig(os.path.join(fig_dir, 'figure1_300dpi.png'), bbox_inches='tight')
    plt.savefig(os.path.join(fig_dir, 'figure1_vector.svg'), bbox_inches='tight')
    plt.close()
    
    # Figure 2
    fig, ax3 = plt.subplots(figsize=(8, 4.5), dpi=300)
    color_teal = '#0d9488'
    color_purple = '#7e22ce'
    
    ax3.set_xlabel('Displacement Damage (dpa)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Permeability K (10^-11 m^2)', color=color_teal, fontsize=11, fontweight='bold')
    ax3.plot(dpa, K*1e11, color=color_teal, linewidth=2.5, label='Carman-Kozeny Permeability')
    ax3.tick_params(axis='y', labelcolor=color_teal)
    ax3.set_ylim(0.2, 1.4)
    
    ax4 = ax3.twinx()
    ax4.set_ylabel('Critical Dryout Heat Flux q" (MW/m^2)', color=color_purple, fontsize=11, fontweight='bold')
    ax4.plot(dpa, q_dryout, color=color_purple, linewidth=2.5, linestyle='-.', label='Dryout Heat Flux')
    ax4.tick_params(axis='y', labelcolor=color_purple)
    ax4.set_ylim(5, 45)
    
    ax4.axhline(22.5, color='#d97706', linestyle='--', linewidth=1.5)
    ax4.axhline(15.0, color='#b91c1c', linestyle=':', linewidth=1.5)
    ax3.axvline(9.8, color='#d97706', linestyle='--', alpha=0.7)
    ax3.axvline(13.0, color='#b91c1c', linestyle=':', alpha=0.7)
    
    ax4.text(10.0, 23.5, '9.8 dpa (SF = 1.50 Limit)', color='#d97706', fontsize=9, fontweight='bold')
    ax4.text(13.2, 16.0, '13.0 dpa (SF = 1.00 Parity)', color='#b91c1c', fontsize=9, fontweight='bold')
    
    plt.title('Permeability Decay & Operational Dryout Safety Margins', fontsize=12, fontweight='bold', pad=12)
    ax3.grid(True, linestyle=':', alpha=0.6)
    fig.tight_layout()
    
    plt.savefig(os.path.join(fig_dir, 'figure2_300dpi.png'), bbox_inches='tight')
    plt.savefig(os.path.join(fig_dir, 'figure2_vector.svg'), bbox_inches='tight')
    plt.close()
    print("Simulation run completed.")

if __name__ == '__main__':
    run_simulation()
