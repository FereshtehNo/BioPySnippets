# Install BioPython and pandas (if needed)
!pip install biopython pandas

# Import libraries
try:
    from Bio.PDB import *
    import pandas as pd
    print("Libraries loaded successfully.")
except ImportError as e:
    print(f"Error loading libraries: {e}")
    raise

# Path to PDB file
pdb_file = r"D:\PhD-Thesis\Thesis-Files\Step1\petase\DDMut\6qgc-ChainA.pdb"

# Check if PDB file exists
import os
if not os.path.exists(pdb_file):
    print(f"Error: File {pdb_file} not found. Please check the file path.")
    raise FileNotFoundError(f"File {pdb_file} does not exist.")

# Load PDB file
try:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_file)
    print(f"File {pdb_file} loaded successfully.")
except Exception as e:
    print(f"Error loading PDB file: {e}")
    raise

# Check chains and residues
print("Chains available in the structure:")
available_residues = {}
for chain in structure[0]:
    residues = [(res.id[1], res.resname) for res in chain.get_residues()]
    available_residues[chain.id] = residues
    print(f"Chain {chain.id}: {len(residues)} residues")
    print(f"Residues in chain {chain.id}: {[f'{r[0]} ({r[1]})' for r in residues]}")

# Reference residues
reference_residues = [
    {"chain": "A", "id": 160, "name": "SER"},
    {"chain": "A", "id": 206, "name": "ASP"},
    {"chain": "A", "id": 237, "name": "HIS"}
]

# Check existence of reference residues
for ref in reference_residues:
    chain_id = ref["chain"]
    residue_id = ref["id"]
    residue_name = ref["name"]
    if chain_id not in available_residues:
        print(f"Error: Chain {chain_id} not found in PDB file.")
        raise KeyError(f"Chain {chain_id} not found.")
    if residue_id not in [r[0] for r in available_residues[chain_id]]:
        print(f"Error: Residue {residue_id} not found in chain {chain_id}.")
        raise KeyError(f"Residue {residue_id} not found.")
    if not any(r[0] == residue_id and r[1] == residue_name for r in available_residues[chain_id]):
        print(f"Warning: Residue {residue_id} in chain {chain_id} is not named {residue_name}.")

# List to store nearby amino acids
nearby_residues = []

# Calculate distances for each reference residue
for ref in reference_residues:
    chain_id = ref["chain"]
    residue_id = ref["id"]
    residue_name = ref["name"]
    try:
        chain = structure[0][chain_id]
        ref_residue = chain[residue_id]
        print(f"\nChecking reference residue {residue_id} ({residue_name}) in chain {chain_id}")
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue == ref_residue:
                        continue
                    # Calculate shortest distance between all atoms of reference and other residues
                    min_distance = float("inf")
                    for ref_atom in ref_residue:
                        for res_atom in residue:
                            try:
                                distance = ref_atom - res_atom
                                if distance < min_distance:
                                    min_distance = distance
                            except KeyError:
                                continue
                    if min_distance <= 5.0:  # Distance less than or equal to 5 Å
                        nearby_residues.append([
                            chain.id,
                            residue.id[1],
                            residue.resname,
                            round(min_distance, 2),
                            f"{residue_id} ({residue_name})"
                        ])
                        print(f"Residue {residue.id[1]} ({residue.resname}) in chain {chain.id} found at {min_distance:.2f} Å from {residue_id} ({residue_name}).")
    except KeyError as e:
        print(f"Error: Residue {residue_id} or chain {chain_id} not found in PDB file.")
        raise

# Check results
if not nearby_residues:
    print("Warning: No residues found within 5 Å of the reference residues. Please increase the distance or check the PDB file.")
else:
    print(f"Found {len(nearby_residues)} residues within 5 Å of the reference residues.")

# Convert to DataFrame
df = pd.DataFrame(nearby_residues, columns=["Chain", "Residue_ID", "Residue_Name", "Distance", "Reference_Residue"])

# Try saving to CSV file
output_csv = r"D:\PhD-Thesis\Thesis-Files\Step1\petase\DDMut\nearby_residues.csv"
try:
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved as '{output_csv}'.")
except PermissionError as e:
    print(f"PermissionError: Unable to save to '{output_csv}'. Trying to save in current directory.")
    fallback_csv = "nearby_residues.csv"
    try:
        df.to_csv(fallback_csv, index=False)
        print(f"CSV file saved as '{fallback_csv}' in the current working directory: {os.getcwd()}.")
    except Exception as e:
        print(f"Error saving CSV: {e}")
        print("DataFrame contents will be displayed below.")

# Display DataFrame contents
print("\nResults:")
print(df)