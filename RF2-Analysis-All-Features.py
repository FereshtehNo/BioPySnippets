# Cell 1: Install libraries (اگر قبلاً نصب شده، می‌توانید رد کنید)
!pip install pandas matplotlib seaborn openpyxl

# Cell 2: Import و آپلود فایل
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files
from IPython.display import display

# آپلود فایل
uploaded = files.upload()
file_name = list(uploaded.keys())[0]
print(f"فایل آپلود شده: {file_name}")

# خواندن فایل
if file_name.endswith('.csv'):
    encodings = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(file_name, encoding=enc)
            print(f"CSV با انکودینگ {enc} خوانده شد.")
            break
        except:
            pass
    if df is None:
        raise ValueError("فایل CSV قابل خواندن نیست.")
else:
    excel_file = pd.ExcelFile(file_name, engine='openpyxl')
    print("شیت‌های موجود:", excel_file.sheet_names)
    sheet_name = input("نام شیت را وارد کنید (یا Enter برای شیت اول): ") or excel_file.sheet_names[0]
    df = pd.read_excel(file_name, sheet_name=sheet_name, engine='openpyxl')
    print(f"شیت '{sheet_name}' خوانده شد.")

print("\nستون‌ها:", df.columns.tolist())
print("\nچند ردیف اول:")
display(df.head(10))

# شناسایی ستون ID و ویژگی‌های عددی
if 'ID' in df.columns:
    id_col = 'ID'
else:
    id_col = df.columns[0]  # فرض اولین ستون ID است

numeric_cols = [col for col in df.select_dtypes(include='number').columns if col != id_col]

if not numeric_cols:
    raise ValueError("هیچ ستون عددی پیدا نشد!")

print(f"\nویژگی‌های عددی موجود: {numeric_cols}")

# دیکشنری برای ذخیره Wild-type و جهت هر ویژگی
wild_types = {}
directions = {}  # True اگر بالاتر بهتر، False اگر پایین‌تر بهتر

print("\nلطفاً برای هر ویژگی اطلاعات Wild-type را وارد کنید:")
for col in numeric_cols:
    while True:
        try:
            wild_val = float(input(f"Wild-type مقدار {col}: "))
            break
        except:
            print("لطفاً یک عدد معتبر وارد کنید.")
    
    while True:
        dir_input = input(f"برای {col} بالاتر بهتر است (h) یا پایین‌تر بهتر است (l)? ").lower().strip()
        if dir_input in ['h', 'l']:
            break
        print("لطفاً فقط h یا l وارد کنید.")
    
    wild_types[col] = wild_val
    directions[col] = (dir_input == 'h')

# محاسبه تعداد ویژگی‌های بهتر برای هر variant
better_counts = pd.Series(0, index=df.index)

for col in numeric_cols:
    wild_val = wild_types[col]
    higher_better = directions[col]
    
    data = df[col].dropna()
    valid_indices = data.index
    
    if higher_better:
        better_mask = df.loc[valid_indices, col] > wild_val
    else:
        better_mask = df.loc[valid_indices, col] < wild_val
    
    better_counts.loc[valid_indices] += better_mask.astype(int)

# اضافه کردن ستون تعداد ویژگی‌های بهتر به دیتافریم
df['Better_than_WT_count'] = better_counts

# استخراج variantهایی که حداقل در ۲ ویژگی بهتر هستند
min_better = 2
better_variants_df = df[df['Better_than_WT_count'] >= min_better].copy()

# مرتب‌سازی بر اساس تعداد ویژگی‌های بهتر (نزولی)
better_variants_df = better_variants_df.sort_values('Better_than_WT_count', ascending=False)

print(f"\nتعداد variantهایی که حداقل در {min_better} ویژگی بهتر از Wild-type هستند: {len(better_variants_df)}")
print("\nلیست این variantها (به همراه تعداد ویژگی‌های بهتر):")
display(better_variants_df[[id_col, 'Better_than_WT_count'] + numeric_cols])

# ذخیره در CSV و دانلود
output_file = 'better_variants_min2.csv'
better_variants_df.to_csv(output_file, index=False)
print(f"\nفایل {output_file} ساخته شد.")

# دانلود خودکار
files.download(output_file)