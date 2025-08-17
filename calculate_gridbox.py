# Install required library
!pip install biopython

import numpy as np
from Bio.PDB import PDBParser
import os
from google.colab import files

# Request upload of the protein file
print("Please upload the 'petase_wild_prep.pdb' file.")
uploaded = files.upload()

# Check for the existence of the file
protein_file = "petase_wild_prep.pdb"
if protein_file not in uploaded:
    raise FileNotFoundError("Please upload the 'petase_wild_prep.pdb' file.")

# Read the protein PDB file
parser = PDBParser(QUIET=True)
structure = parser.get_structure('protein', protein_file)
model = structure[0]
chain = model['A']

# Extract coordinates of CA atoms for Ser160 and His237
try:
    ser160_ca = chain[160]['CA'].get_coord()
    his237_ca = chain[237]['CA'].get_coord()
except KeyError:
    raise KeyError("Residues Ser160 or His237 not found in the PDB file. Please check the PDB file.")

# Calculate the center of the grid box (mean of coordinates)
center = np.mean([ser160_ca, his237_ca], axis=0)

# Calculate the distance between Ser160 and His237 to estimate dimensions
distance = np.linalg.norm(ser160_ca - his237_ca)

# Set grid box dimensions
size_margin = 10.0  # Margin to cover surrounding space
size_x = size_y = size_z = round(distance + size_margin, 2)

# Ensure minimum dimensions (20 Ångstroms)
min_size = 20.0
size_x = max(size_x, min_size)
size_y = max(size_y, min_size)
size_z = max(size_z, min_size)

# Create AutoDock Vina configuration file (without performing docking)
config_content = f"""receptor = protein.pdbqt
ligand = ligand.pdbqt
center_x = {center[0]:.2f}
center_y = {center[1]:.2f}
center_z = {center[2]:.2f}
size_x = {size_x}
size_y = {size_y}
size_z = {size_z}
out = output.pdbqt
log = vina.log
exhaustiveness = 8
"""

# Save the configuration file
with open('config.txt', 'w') as f:
    f.write(config_content)

# Print grid box information
print(f"Grid box center coordinates: x={center[0]:.2f}, y={center[1]:.2f}, z={center[2]:.2f}")
print(f"Grid box dimensions: {size_x}x{size_y}x{size_z} Ångstroms")
print("Configuration file 'config.txt' has been created.")

# Download the configuration file
print("Download the configuration file:")
files.download('config.txt')