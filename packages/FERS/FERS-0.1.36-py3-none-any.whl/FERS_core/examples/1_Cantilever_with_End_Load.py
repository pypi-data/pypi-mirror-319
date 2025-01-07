import os
from FERS_core import Node, Member, FERS, Material, Section, MemberSet, NodalSupport, NodalLoad
import fers_calculations

# =============================================================================
# Example and Validation: Cantilever Beam with End Load
# =============================================================================

# Step 1: Set up the model
# -------------------------
# Create the main FERS object that will manage the analysis
calculation_1 = FERS()

# Define the geometry of the beam
node1 = Node(0, 0, 0)  # Fixed end of the beam
node2 = Node(5, 0, 0)  # Free end of the beam, 5 meters away

# Define the material properties (Steel S235)
Steel_S235 = Material(name="Steel", e_mod=210e9, g_mod=80.769e9, density=7850, yield_stress=235e6)

# Define the beam cross-section (IPE 180)
section = Section(
    name="IPE 180 Beam Section", material=Steel_S235, i_y=0.819e-6, i_z=10.63e-6, j=0.027e-6, area=0.00196
)

# Create the beam element
beam = Member(start_node=node1, end_node=node2, section=section)

# Apply a fixed support at the fixed end (node1)
wall_support = NodalSupport()
node1.nodal_support = wall_support

# Add the beam to a member group
membergroup1 = MemberSet(members=[beam])

# Add the member group to the calculation model
calculation_1.add_member_set(membergroup1)

# Step 2: Apply the load
# ----------------------
# Create a load case for the analysis
end_load_case = calculation_1.create_load_case(name="End Load")

# Apply a 1 kN downward force (global y-axis) at the free end (node2)
nodal_load = NodalLoad(node=node2, load_case=end_load_case, magnitude=-1000, direction=(0, -1, 0))

# Save the model to a file for FERS calculations
file_path = os.path.join("examples", "json_input_solver", "1_cantilever_with_end_load.json")
calculation_1.save_to_json(file_path, indent=4)

# Step 3: Run FERS calculation
# ----------------------------
# Perform the analysis using the saved JSON model file
print("Running the analysis...")
result = fers_calculations.calculate_from_file(file_path)

# Extract results from the analysis
dy_fers = node2.displacement[1]  # Displacement at the free end in the y-direction
Mz_fers = node1.reaction_moment[2]  # Reaction moment at the fixed end

# Step 4: Validate Results Against Analytical Solution
# ----------------------------------------------------
# Analytical solution parameters
F = 1000  # Force in Newtons
L = 5  # Length of the beam in meters
E = 210e9  # Modulus of elasticity in Pascals
I = 0.819e-6  # Moment of inertia in m^4
x = L  # Distance to the free end for max deflection and slope

# Calculate analytical solutions for deflection and moment
delta_analytical = (-F * x**2 / (6 * E * I)) * (3 * L - x)  # Max deflection
M_max_analytical = -F * L  # Max moment at the fixed end

# Compare FERS results with analytical solutions
print("\nComparison of results:")
print(f"Deflection at free end (FERS): {dy_fers:.6f} m")
print(f"Deflection at free end (Analytical): {delta_analytical:.6f} m")
if abs(dy_fers - delta_analytical) < 1e-6:
    print("Deflection matches the analytical solution ✅")
else:
    print("Deflection does NOT match the analytical solution ❌")
    exit(1)  # Exit with an error if the test fails

print(f"Reaction moment at fixed end (FERS): {Mz_fers:.6f} Nm")
print(f"Reaction moment at fixed end (Analytical): {M_max_analytical:.6f} Nm")
if abs(Mz_fers - M_max_analytical) < 1e-3:
    print("Reaction moment matches the analytical solution ✅")
else:
    print("Reaction moment does NOT match the analytical solution ❌")
    exit(1)  # Exit with an error if the test fails

print("\nAll results validated successfully!")

# =============================================================================
# Notes for Users
# =============================================================================
# This script is both an example and a validation tool.
# 1. It demonstrates how to set up and analyze a cantilever beam with an end load.
# 2. It validates the FERS results against analytical solutions for deflection and moment.
# 3. Run this script as-is to learn, or integrate it into your CI/CD pipeline for validation.
