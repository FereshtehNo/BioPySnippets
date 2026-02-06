from google.colab import files

uploaded = files.upload()  # پنجره‌ای باز می‌شود تا فایل JSON خود را انتخاب کنی

import json
import math

# نام فایل آپلود شده
file_path = list(uploaded.keys())[0]

# دما بر حسب سلسیوس
temperature_C = 25
temperature_K = 273.15 + temperature_C
R = 8.3144626  # J/(mol·K)

# خواندن داده‌ها از فایل JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# پیدا کردن تمام کلیدهایی که شامل affinity_pred_value هستند
affinity_keys = [k for k in data.keys() if k.startswith('affinity_pred_value')]

# محاسبه و چاپ Kd و ΔG برای هر مقدار
for key in affinity_keys:
    pred_value = data[key]
    Kd = 10**pred_value / 1e6  # mol/L
    dG = R * temperature_K * math.log(Kd) / 1000  # kJ/mol
    print(f"{key}:")
    print(f"  Predicted Kd       : {Kd:.3e} mol/L  (= {Kd*1e6:.1f} µM)")
    print(f"  Predicted ΔG       : {dG:.3f} kJ/mol  (= {dG/4.184:.3f} kcal/mol)")
    print()
