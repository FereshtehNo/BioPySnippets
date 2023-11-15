from Bio.PDB import PDBParser
import nglview as nv

# Path to the PDB file
pdb_file_path = r'D:\Research-All\Laccase\PersiLac1\6klg-prep-signal-deleted.pdb'

# Parse the PDB file using Bio.PDB
parser = PDBParser(QUIET=True)
structure = parser.get_structure("protein", pdb_file_path)

# Create an NGLViewer instance and visualize the structure
view = nv.show_biopython(structure)
view

# Display the viewer (you'll see the protein structure in your Jupyter Notebook)
