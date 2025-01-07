import os
from FERS_core import Node, Member, FERS, Material, Section, MemberSet, NodalSupport, NodalLoad
import fers_calculations
import time

# =============================================================================
# Creating a cantilever with an end_load
# =============================================================================

# Create analysis object
calculation_1 = FERS()


# Create nodes
node1 = Node(0, 0, 0)  # Fixed end
node2 = Node(5, 0, 0)  # Free end

# Create material
Steel_S235 = Material(name="Steel", e_mod=210e9, g_mod=80.769e9, density=7850, yield_stress=235e6)

# Create a section
# For example IPE 180 - A:

section = Section(
    name="IPE 180 Beam Section", material=Steel_S235, i_y=0.819e-6, i_z=10.63e-6, j=0.027e-6, area=0.00196
)


# Create member
beam = Member(start_node=node1, end_node=node2, section=section)

# Creating a boundary conditions (by default all 6 d.o.f. are constraint)
wall_support = NodalSupport()

# Assigning the nodal_support to the correct node.
node1.nodal_support = wall_support

# =============================================================================
# Now that the geometrical part is created. Lets create the model and the loadcases
# =============================================================================
# Create a memberset holding the beam
membergroup1 = MemberSet(members=[beam])


# Adding the memberset to the model
calculation_1.add_member_set(membergroup1)

# Create a loadcase for the end load
end_load_case = calculation_1.create_load_case(name="End Load")

# Apply end load at node2 1 kN downward force (global y-axis) to the loadcase
nodal_load = NodalLoad(node=node2, load_case=end_load_case, magnitude=-1000, direction=(0, -1, 0))


file_path = os.path.join("examples", "json_input_solver", "1_cantilever_with_end_load.json")
calculation_1.save_to_json(file_path, indent=4)
start_time = time.time()  # record the starting time

for i in range(1000):
    jer = fers_calculations.calculate_from_file(file_path)

end_time = time.time()  # record the ending time

elapsed_time = end_time - start_time
print(f"Total time for 1000 calculations: {elapsed_time:.2f} seconds")
print(f"Average time per calculation: {elapsed_time / 1000:.4f} seconds")
# Run analysis
# result = FERS_calculation(calculation_1)

# # Print results
# print("Displacement at free end (node2):")
# print(f"dy = {node2.displacement[1]:.6f} m")

# print("\nReaction forces at fixed end (node1):")
# print(f"Fy = {node1.reaction_force[1]:.2f} kN")
# print(f"Mz = {node1.reaction_moment[2]:.2f} kN·m")

# # With the use of beam equations https://mechanicalc.com/reference/beam-analysis


# # Calculate and print maximum bending stress
# i_z = beam.moment_of_inertia_z
# y_max = beam.height / 2
# M_max = abs(node1.reaction_moment[2])
# sigma_max = M_max * y_max / i_z

# print(f"\nMaximum bending stre
