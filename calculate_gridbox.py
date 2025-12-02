# نصب کتابخانه (در صورت نیاز)
!pip install biopython -q

import numpy as np
from Bio.PDB import PDBParser
from google.colab import files
import os

# آپلود فایل پروتئین
print("لطفاً فایل 'WB150-1-prep.pdb' را آپلود کنید:")
uploaded = files.upload()

# گرفتن نام دقیق فایل آپلود شده (Colab گاهی پسوند اضافه می‌کنه!)
protein_file = list(uploaded.keys())[0]
print(f"فایل آپلود شده: {protein_file}")

# خواندن ساختار
parser = PDBParser(QUIET=True)
structure = parser.get_structure('protein', protein_file)
model = structure[0]

# انتخاب زنجیره A (اگر نبود، اولین زنجیره موجود)
chain_id = 'A'
if chain_id not in model:
    chain_id = next(iter(model))
    print(f"زنجیره A پیدا نشد → از زنجیره '{chain_id}' استفاده می‌شود.")
chain = model[chain_id]

# دریافت شماره رزیدوهای کاتالیتیک از کاربر (اختیاری، ولی اینجا پیش‌فرض Ser36 و His110)
print("\nرزیدوهای کاتالیتیک در WB150-1:")
res1 = int(input("شماره رزیدو اول (معمولاً Ser) — پیش‌فرض 36: ") or "36")
res2 = int(input("شماره رزیدو دوم (معمولاً His) — پیش‌فرض 110: ") or "110")

# استخراج مختصات CA
try:
    ca1 = chain[res1]['CA'].get_coord()
    ca2 = chain[res2]['CA'].get_coord()
    print(f"رزیدو {res1} و {res2} با موفقیت پیدا شدند.")
except KeyError as e:
    raise KeyError(f"رزیدو {e} در زنجیره {chain_id} پیدا نشد! شماره را بررسی کن.")

# محاسبه مرکز و فاصله
center = np.mean([ca1, ca2], axis=0)
distance = np.linalg.norm(ca1 - ca2)

# تنظیم اندازه باکس (بهینه‌شده)
margin = 12.0
box_size = max(round(distance + margin, 1), 24.0)  # حداقل 24 آنگستروم برای پوشش تریاد + لیگاند

# ساخت فایل config.txt استاندارد برای Vina
config_content = f"""receptor = receptor.pdbqt
ligand = ligand.pdbqt

center_x = {center[0]:.3f}
center_y = {center[1]:.3f}
center_z = {center[2]:.3f}

size_x = {box_size}
size_y = {box_size}
size_z = {box_size}

exhaustiveness = 32
num_modes = 20
energy_range = 5

out = docked_output.pdbqt
log = docking_log.txt
"""

# ذخیره فایل
with open('config_vina.txt', 'w') as f:
    f.write(config_content.strip())

# نمایش اطلاعات
print("\n" + "="*60)
print(f"مرکز گرید باکس (میانگین CA رزیدو {res1} و {res2}):")
print(f"   center_x = {center[0]:.3f}")
print(f"   center_y = {center[1]:.3f}")
print(f"   center_z = {center[2]:.3f}")
print(f"فاصله بین دو رزیدو: {distance:.2f} Å")
print(f"اندازه گرید باکس: {box_size} × {box_size} × {box_size} Å")
print("فایل تنظیمات 'config_vina.txt' با موفقیت ساخته شد!")
print("="*60)

# دانلود خودکار
files.download('config_vina.txt')
