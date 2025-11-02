import json
import pandas as pd
import glob
import os
from typing import List, Dict

def extract_metrics_from_json(file_path: str) -> Dict:
    """استخراج معیارهای مهم از یک فایل JSON"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    metrics = {
        'filename': os.path.basename(file_path),
        'aggregate_score': data.get('aggregate_score', [None])[0],
        'ptm': data.get('ptm', [None])[0],
        'iptm': data.get('iptm', [None])[0],
        'complex_plddt': data.get('complex_plddt', [None]),
        'has_inter_chain_clashes': data.get('has_inter_chain_clashes', [None])[0],
    }
    
    per_chain_ptm = data.get('per_chain_ptm', [[None, None]])
    if per_chain_ptm and len(per_chain_ptm[0]) >= 2:
        metrics['ptm_chain_0'] = per_chain_ptm[0][0]
        metrics['ptm_chain_1'] = per_chain_ptm[0][1]
    else:
        metrics['ptm_chain_0'] = None
        metrics['ptm_chain_1'] = None
    
    per_chain_plddt = data.get('per_chain_plddt', [[None, None]])
    if per_chain_plddt and len(per_chain_plddt[0]) >= 2:
        metrics['plddt_chain_0'] = per_chain_plddt[0][0]
        metrics['plddt_chain_1'] = per_chain_plddt[0][1]
    else:
        metrics['plddt_chain_0'] = None
        metrics['plddt_chain_1'] = None
    
    chain_intra = data.get('chain_intra_clashes', [[0, 0]])
    if chain_intra and len(chain_intra[0]) >= 2:
        metrics['intra_clash_chain_0'] = chain_intra[0][0]
        metrics['intra_clash_chain_1'] = chain_intra[0][1]
    else:
        metrics['intra_clash_chain_0'] = None
        metrics['intra_clash_chain_1'] = None
    
    pae = data.get('pae', [[[None]]])
    if pae and len(pae[0]) > 0 and len(pae[0][0]) > 0:
        metrics['pae_0_0'] = pae[0][0][0]
        metrics['pae_0_1'] = pae[0][0][1] if len(pae[0][0]) > 1 else None
        metrics['pae_1_0'] = pae[0][1][0] if len(pae[0]) > 1 else None
        metrics['pae_1_1'] = pae[0][1][1] if len(pae[0]) > 1 and len(pae[0][1]) > 1 else None
    else:
        metrics['pae_0_0'] = metrics['pae_0_1'] = metrics['pae_1_0'] = metrics['pae_1_1'] = None
    
    return metrics

def json_to_csv(json_files: List[str], output_csv: str = "output_scores.csv"):
    results = []
    for file in json_files:
        try:
            row = extract_metrics_from_json(file)
            results.append(row)
            print(f"پردازش شد: {os.path.basename(file)}")
        except Exception as e:
            print(f"خطا در فایل {file}: {e}")
    
    df = pd.DataFrame(results)
    column_order = [
        'filename', 'aggregate_score', 'ptm', 'iptm', 'complex_plddt',
        'ptm_chain_0', 'ptm_chain_1',
        'plddt_chain_0', 'plddt_chain_1',
        'has_inter_chain_clashes',
        'intra_clash_chain_0', 'intra_clash_chain_1',
        'pae_0_0', 'pae_0_1', 'pae_1_0', 'pae_1_1'
    ]
    df = df[column_order]
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\nفایل CSV ذخیره شد: {output_csv}")
    return df

# ======================
# اجرا در Google Colab
# ======================

# ۱. آپلود فایل‌های JSON
from google.colab import files
uploaded = files.upload()  # اینجا همه فایل‌های JSON رو آپلود کن

# ۲. لیست فایل‌های آپلود شده
json_files = list(uploaded.keys())
print("فایل‌های آپلود شده:", json_files)

# ۳. تبدیل به CSV
df = json_to_csv(json_files, "all_scores_summary.csv")

# ۴. دانلود فایل CSV
files.download("all_scores_summary.csv")