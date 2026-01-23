# Install libraries if needed
!pip install biopython numpy pandas

from Bio.PDB import PDBParser
import numpy as np
import pandas as pd
from google.colab import files
import os

print("✔ Libraries loaded")

# ===============================
# UPLOAD PDB FILES (Colab)
# ===============================
uploaded = files.upload()
pdb_files = list(uploaded.keys())

print("✔ Uploaded PDB files:")
for f in pdb_files:
    print("   ", f)

# ===============================
# USER INPUT
# ===============================
ser_resid = int(input("Ser residue number: "))
his_resid = int(input("His residue number: "))
asp_resid = int(input("Asp residue number: "))
lig_name  = input("Ligand resname (e.g. MOL, PET): ").strip()

# ===============================
# FUNCTIONS
# ===============================
def dist(a, b):
    return np.linalg.norm(a - b)

def angle_deg(a, b, c):
    v1 = a - b
    v2 = c - b
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1, 1)
    return np.degrees(np.arccos(cos_theta))

def analyze_pose(pdb_file):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("complex", pdb_file)

    ser_og = None
    his_nd1 = None
    his_ne2 = None
    asp_od1 = None
    asp_od2 = None

    lig_carbons = []
    lig_oxygens = []
    lig_atoms = []

    for model in structure:
        for chain in model:
            for residue in chain:
                resname = residue.get_resname().strip()
                resid = residue.id[1]

                # SER
                if resname == "SER" and resid == ser_resid:
                    if "OG" in residue:
                        ser_og = residue["OG"].get_coord()

                # HIS
                if resname == "HIS" and resid == his_resid:
                    if "ND1" in residue:
                        his_nd1 = residue["ND1"].get_coord()
                    if "NE2" in residue:
                        his_ne2 = residue["NE2"].get_coord()

                # ASP
                if resname == "ASP" and resid == asp_resid:
                    if "OD1" in residue:
                        asp_od1 = residue["OD1"].get_coord()
                    if "OD2" in residue:
                        asp_od2 = residue["OD2"].get_coord()

                # LIGAND
                if resname == lig_name:
                    for atom in residue:
                        coord = atom.get_coord()
                        lig_atoms.append(coord)
                        if atom.element == "C":
                            lig_carbons.append(coord)
                        if atom.element == "O":
                            lig_oxygens.append(coord)

    # SAFETY CHECK
    if ser_og is None or not lig_carbons or not lig_oxygens:
        raise ValueError(f"❌ Missing atoms in {os.path.basename(pdb_file)}")

    # ---------------------------
    # H-BONDS
    # ---------------------------
    hbonds = []

    # Asp–His
    for asp_o in [asp_od1, asp_od2]:
        for his_n in [his_nd1, his_ne2]:
            if asp_o is None or his_n is None:
                continue
            d = dist(asp_o, his_n)
            if d <= 3.2:
                hbonds.append(["HIS", "ASP", round(d,3)])

    # His–Ser
    his_ser_distance = None
    his_ser_hbond = False

    for his_n in [his_nd1, his_ne2]:
        if his_n is None:
            continue
        d = dist(his_n, ser_og)
        his_ser_distance = d
        if d <= 3.2:
            hbonds.append(["SER", "HIS", round(d,3)])
            his_ser_hbond = True

    # ---------------------------
    # CLOSEST C=O (for attack angle only)
    # ---------------------------
    min_dist = 999
    best_c = None
    best_o = None

    for c in lig_carbons:
        for o in lig_oxygens:
            d = dist(ser_og, c)
            if d < min_dist:
                min_dist = d
                best_c = c
                best_o = o

    attack_angle = angle_deg(ser_og, best_c, best_o)

    # ---------------------------
    # ACTIVITY CRITERIA (snapshot)
    # ---------------------------
    ser_active = his_ser_hbond and attack_angle >= 100
    triad_active = any(h[0]=="HIS" and h[1]=="ASP" for h in hbonds) and his_ser_hbond

    return hbonds, {
        "PDB": os.path.basename(pdb_file),
        "His–Ser (Å)": round(his_ser_distance,3),
        "Attack angle (deg)": round(attack_angle,2),
        "Ser active (snapshot)": ser_active,
        "Catalytic triad formed": triad_active
    }

# ===============================
# RUN ENSEMBLE
# ===============================
all_hb = []
all_geom = []

for pdb in pdb_files:
    hb, geom = analyze_pose(pdb)
    all_hb.extend(hb)
    all_geom.append(geom)

df_hb = pd.DataFrame(all_hb, columns=["Donor", "Acceptor", "Distance (Å)"])
df_geom = pd.DataFrame(all_geom)

df_hb.to_csv("hbonds_ensemble.csv", index=False)
df_geom.to_csv("triad_geometry_ensemble.csv", index=False)

print("\n✅ H-bonds:")
print(df_hb)

print("\n✅ Geometry summary (snapshot, only attack angle + triad):")
print(df_geom)

print("\n📁 Files saved:")
print("   hbonds_ensemble.csv")
print("   triad_geometry_ensemble.csv")
