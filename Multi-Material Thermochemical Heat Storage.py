# Multi-Material Thermochemical Heat Storage Simulation
# Requirements: pip install numpy matplotlib

import numpy as np
import matplotlib.pyplot as plt

# ---------------- Define thermochemical materials ----------------
# Material properties: (delta_H [kJ/mol], delta_S [J/mol·K], T_range [°C])
materials = {
    "Material 1": {"delta_H": 150, "delta_S": 120, "T_range": (200, 400)},
    "Material 2": {"delta_H": 220, "delta_S": 160, "T_range": (300, 500)},
}

# ---------------- Functions ----------------
def equilibrium_pressure(delta_H, delta_S, T):
    """
    Van 't Hoff relation: ln(P) = -ΔH/(R*T) + ΔS/R
    P in bar, T in K
    """
    R = 8.314  # J/mol·K
    T_K = T + 273.15
    lnP = (-delta_H * 1000) / (R * T_K) + delta_S / R
    return np.exp(lnP)

def equilibrium_temperature(delta_H, delta_S, P):
    """
    Solve Van 't Hoff for T given P (bar)
    """
    R = 8.314
    return (-delta_H * 1000 / (R * np.log(P)) + delta_S / R) - 273.15

def energy_density(delta_H, n_mol=1):
    """Energy per mole in kJ"""
    return delta_H * n_mol

# ---------------- Simulation ----------------
T = np.linspace(200, 500, 300)  # Temperature range in °C
pressures = {}

for mat, props in materials.items():
    delta_H, delta_S = props["delta_H"], props["delta_S"]
    pressures[mat] = equilibrium_pressure(delta_H, delta_S, T)

# Combine materials (series storage: discharge sequentially)
combined_energy = np.zeros_like(T)
for mat, props in materials.items():
    delta_H = props["delta_H"]
    combined_energy += delta_H  # Simplified sum

# ---------------- Visualization ----------------
plt.figure(figsize=(10,6))

# Pressure vs Temperature
for mat in materials:
    plt.semilogy(T, pressures[mat], label=f'{mat} P_eq (bar)')

plt.xlabel('Temperature [°C]')
plt.ylabel('Equilibrium Pressure [bar]')
plt.title('Equilibrium Pressure vs Temperature for Multiple Materials')
plt.legend()
plt.grid(True)
plt.show()

# Energy Density Bar Chart
plt.figure(figsize=(8,5))
energy_vals = [energy_density(m["delta_H"]) for m in materials.values()]
plt.bar(materials.keys(), energy_vals, color=['orange','green'])
plt.ylabel('Energy Density [kJ/mol]')
plt.title('Energy Density of Each Material')
plt.show()

# Combined energy visualization
plt.figure(figsize=(8,5))
plt.plot(T, [combined_energy[0]]*len(T), 'r--', label='Combined Energy (approx.)')
plt.xlabel('Temperature [°C]')
plt.ylabel('Energy [kJ/mol]')
plt.title('Approximate Combined Energy of Multi-Material Storage')
plt.legend()
plt.grid(True)
plt.show()
