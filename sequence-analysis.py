import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch
import matplotlib.patches as mpatches

# Sample data (replace with your actual protein sequence and secondary structure information)
sequence = "MSSASSNARDEVIAIHEEADWVDRTVYPESRCIGLSSGAVHYIDEGPDGGRETLLMHGNPTWSFLYRHLVRDLRDE"
secondary_structures = [
    ('alpha', 5, 15),  # Example: alpha helix from residue 5 to 15
    ('beta', 20, 25), # Example: beta strand from residue 20 to 25
    ('loop', 30, 35), # Example: loop from residue 30 to 35
    # Add more secondary structure elements here
]

def draw_alpha_helix(ax, start, end, y_level):
    """Draws an alpha helix on the plot."""
    width = end - start
    ax.add_patch(FancyBboxPatch((start, y_level), width, 0.4, boxstyle="round,pad=0.1", edgecolor="black", facecolor="cyan"))

def draw_beta_strand(ax, start, end, y_level):
    """Draws a beta strand on the plot."""
    width = end - start
    ax.add_patch(FancyArrow(start, y_level, width, 0, width=0.3, head_length=0.5, edgecolor="black", facecolor="orange"))

def draw_loop(ax, start, end, y_level):
    """Draws a loop on the plot."""
    ax.plot([start, end], [y_level, y_level], color="grey", linewidth=2)

def plot_protein(sequence, secondary_structures):
    fig, ax = plt.subplots(figsize=(14, 2))
    y_level = 0.5

    # Draw secondary structures
    for structure in secondary_structures:
        structure_type, start, end = structure
        if structure_type == 'alpha':
            draw_alpha_helix(ax, start, end, y_level)
        elif structure_type == 'beta':
            draw_beta_strand(ax, start, end, y_level)
        elif structure_type == 'loop':
            draw_loop(ax, start, end, y_level)
    
    # Annotate the sequence
    for i, residue in enumerate(sequence):
        ax.text(i + 0.5, y_level - 0.1, residue, ha='center', va='center', fontsize=8)

    # Set plot limits and labels
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks(range(0, len(sequence), 10))
    ax.set_xticklabels([str(i) for i in range(0, len(sequence), 10)])
    ax.set_xlabel("Residue number")
    
    # Create a legend
    legend_handles = [
        mpatches.Patch(color='cyan', label='Alpha Helix'),
        mpatches.FancyArrow(0, 0, 1, 0, width=0.3, head_length=0.5, edgecolor="black", facecolor="orange", label='Beta Strand'),
        mpatches.Patch(color='grey', label='Loop')
    ]
    ax.legend(handles=legend_handles, loc='upper right')

    plt.tight_layout()
    plt.show()

# Call the function with your data
plot_protein(sequence, secondary_structures)
