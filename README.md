# Fast-Neutron CPS Degradation Simulation Package

**Target Journal:** *Fusion Engineering and Design* (Elsevier | ISSN: 0920-3796)  
**Author:** Jacob James Rasmussen  
**Affiliation:** Independent Researcher & Incoming CVTC STEM Scholar  

---

## Overview
This repository contains the computational physics code, verification dataset, and compiled manuscript documents for **"Predicting Fast-Neutron Permeability Decay and Thermal Dryout Thresholds in Liquid Lithium Capillary Porous Systems"**.

The framework models the degradation of tungsten capillary porous systems (CPS) in tokamak divertors under 14.1 MeV fast-neutron irradiation (0 to 20 dpa).

---

## Repository Structure


---

## Governing Equations

1. Young-Laplace Capillary Pressure Retention: Delta P_cap = (2 * gamma_LV * cos(theta)) / r_p
2. Carman-Kozeny Hydraulic Permeability: K = phi^3 / [ C_CK * (1 - phi)^2 * S_0^2 ]
3. Critical Dryout Heat Flux Degradation: q''_dryout(dpa) = q''_0 * exp(-k_q * dpa) (k_q = 0.0626 dpa^-1)

---

## Verification Benchmarks

- Pristine State (0.0 dpa): r_p = 25.00 um, Delta P_cap = 27.05 kPa, K = 1.25x10^-11 m^2, q''_dryout = 41.50 MW/m^2, SF = 2.77
- Replacement Limit (9.8 dpa): r_p = 17.54 um, Delta P_cap = 38.55 kPa, K = 0.60x10^-11 m^2, q''_dryout = 22.50 MW/m^2, SF = 1.50
- Thermal Dryout Parity Limit (13.0 dpa): r_p = 16.49 um, Delta P_cap = 41.00 kPa, K = 0.50x10^-11 m^2, q''_dryout = 15.00 MW/m^2, SF = 1.00
- Extreme Damage (20.0 dpa): r_p = 15.20 um, Delta P_cap = 44.48 kPa, K = 0.38x10^-11 m^2, q''_dryout = 11.89 MW/m^2, SF = 0.79

---

## Quickstart

To run the simulation and generate all dataset and figure files:

    pip install -r requirements.txt
    python src/solver.py
