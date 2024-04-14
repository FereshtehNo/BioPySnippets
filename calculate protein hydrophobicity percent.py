def calculate_hydrophobicity(sequence):
    # Define the set of hydrophobic amino acids
    hydrophobic_amino_acids = {'A', 'I', 'L', 'M', 'F', 'P', 'W', 'V'}
    
    # Count the number of hydrophobic amino acids in the sequence
    hydrophobic_count = sum(1 for aa in sequence if aa in hydrophobic_amino_acids)
    
    # Calculate the total number of amino acids in the sequence
    total_amino_acids = len(sequence)
    
    # Calculate the percentage of hydrophobic amino acids
    hydrophobic_percentage = (hydrophobic_count / total_amino_acids) * 100
    
    return hydrophobic_percentage

# Example usage:
protein_sequence = "MDTNNYPTVENKTKLFLEKLQQSGGPPLYTLTPTEARNVLSGLQAGPIEKLPAEIENKTIPGGPNGEISIQIVRPQGSGNETLPVVMYTHGGGWVLGNFNTHERLLRELSTGAHAAIVFVNYTLSPEAKYPQSLEEAYAATKWISENGQSLNLDSSRLVVAGDSVGGNMATTLALLAKERGGPPITFQLLFYPVTDANFNTSSYNTYQEGYFLTRENMKWFWDNYVSKDTNRKEPTVSPLQASLEQLSGLPPTLIIVGENDVLRDEGEAYAHKLMQAGVPITATRYLGAIHDFMMLNPISDTPAARGAIDQASHTLKELFSK"
print("Hydrophobicity Percentage: {:.2f}%".format(calculate_hydrophobicity(protein_sequence)))
