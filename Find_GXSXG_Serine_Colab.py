# @title ### Find Catalytic Serine in MOTIF GXSXG
# @markdown ### Upload a FASTA file or paste the sequence directly

# Install required packages (runs once)
!pip install biopython matplotlib ipywidgets -q

import re
import matplotlib.pyplot as plt
from Bio import SeqIO
from io import StringIO
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# --- Settings ---
motif_pattern = r"G[A-Z]S[A-Z]G"  # Updated to GXSXG
motif_name = "GXSXG"

# --- Widgets ---
upload = widgets.FileUpload(
    accept='.fasta,.fa,.txt', 
    multiple=False,
    description='Upload FASTA'
)
textarea = widgets.Textarea(
    value='',
    placeholder='>Example_PETase\nMNFPRASRLMQAAVLGGLMASTSAQAGKPTSVSYPGQRFADWINSDVHALFRQAFWH...\n',
    description='Or paste here:',
    layout=widgets.Layout(width='100%', height='160px')
)
run_button = widgets.Button(description="Find Serine!", button_style='success', layout=widgets.Layout(width='200px'))
output = widgets.Output()

# --- Main function ---
def find_catalytic_serine(fasta_content):
    try:
        sequences = list(SeqIO.parse(StringIO(fasta_content), "fasta"))
        if not sequences:
            return None, "Invalid or empty FASTA file."
        
        results = []
        for seq_record in sequences:
            sequence = str(seq_record.seq).upper()
            name = seq_record.id if seq_record.id else "Unknown"
            matches = list(re.finditer(motif_pattern, sequence))

            for match in matches:
                serine_pos = match.start() + 2  # 1-based position of S
                motif_seq = match.group()
                start_context = max(0, serine_pos - 15)
                end_context = min(len(sequence), serine_pos + 14)
                context = sequence[start_context:end_context]
                highlighted = context.replace(sequence[serine_pos-1], f"**{sequence[serine_pos-1]}**")
                results.append({
                    'ID': name,
                    'Position': serine_pos,
                    'Motif': motif_seq,
                    'Context': f"...{highlighted}..."
                })

        if not results:
            return None, f"**MOTIF `{motif_name}` not found in sequence!** No catalytic serine."
        
        return results, sequences[0]
    
    except Exception as e:
        return None, f"Processing error: {str(e)}"

# --- Run search ---
def on_run_clicked(b):
    with output:
        clear_output()
        fasta_input = ""

        if upload.value:
            uploaded = list(upload.value.values())[0]
            fasta_input = uploaded['content'].decode('utf-8')
        elif textarea.value.strip():
            fasta_input = textarea.value.strip()

        if not fasta_input.strip():
            display(HTML("<p style='color:red;'>Please upload a file or paste a sequence!</p>"))
            return

        results, info = find_catalytic_serine(fasta_input)

        if results is None:
            display(HTML(f"<p style='color:orange; font-size:18px;'>{info}</p>"))
            return

        seq_record = info
        print(f"Catalytic serine found in MOTIF `{motif_name}`!\n")
        for r in results:
            print(f"**{r['ID']}** → Position **{r['Position']}** → `{r['Motif']}`")
            print(f"   Context: {r['Context']}\n")

        # Plot
        seq_len = len(str(seq_record.seq))
        fig, ax = plt.subplots(1, 1, figsize=(min(16, seq_len//30), 3))
        ax.set_xlim(0, seq_len)
        ax.set_ylim(0, 1)
        ax.axis('off')

        for i, r in enumerate(results):
            ax.plot(r['Position']-1, 0.5, 'ro', markersize=12, label='Serine' if i == 0 else "")
            ax.text(r['Position']-1, 0.65, f"S{r['Position']}", ha='center', fontsize=11, fontweight='bold', color='red')

        ax.set_title(f"Serine Position in {results[0]['ID']}", fontsize=14, pad=20)
        ax.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

run_button.on_click(on_run_clicked)

# --- Display interface ---
display(HTML("<h3>Upload FASTA file or paste sequence:</h3>"))
display(upload)
display(textarea)
display(run_button)
display(output)