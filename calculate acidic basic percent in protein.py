def calculate_acidic_basic_percentage(sequence):
    # Define acidic and basic amino acids
    acidic_amino_acids = {'D', 'E'}
    basic_amino_acids = {'K', 'R', 'H'}
    
    # Count acidic and basic amino acids
    acidic_count = sum(1 for aa in sequence if aa in acidic_amino_acids)
    basic_count = sum(1 for aa in sequence if aa in basic_amino_acids)
    
    # Calculate the total number of amino acids
    total_amino_acids = len(sequence)
    
    # Calculate the percentage of acidic and basic amino acids
    acidic_percentage = (acidic_count / total_amino_acids) * 100
    basic_percentage = (basic_count / total_amino_acids) * 100
    
    return acidic_percentage, basic_percentage

# Example usage:
protein_sequence = "MDTNNYPTVENKTKLFLEKLQQSGGPPLYTLTPTEARNVLSGLQAGPIEKLPAEIENKTIPGGPNGEISIQIVRPQGSGNETLPVVMYTHGGGWVLGNFNTHERLLRELSTGAHAAIVFVNYTLSPEAKYPQSLEEAYAATKWISENGQSLNLDSSRLVVAGDSVGGNMATTLALLAKERGGPPITFQLLFYPVTDANFNTSSYNTYQEGYFLTRENMKWFWDNYVSKDTNRKEPTVSPLQASLEQLSGLPPTLIIVGENDVLRDEGEAYAHKLMQAGVPITATRYLGAIHDFMMLNPISDTPAARGAIDQASHTLKELFSK"
acidic_percent, basic_percent = calculate_acidic_basic_percentage(protein_sequence)
print("Acidic Amino Acids Percentage: {:.2f}%".format(acidic_percent))
print("Basic Amino Acids Percentage: {:.2f}%".format(basic_percent))
