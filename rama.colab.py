# =============================================
#   Ramachandran Plot - Colab
# =============================================


!pip install ramachandraw -q


from google.colab import files

print("📤 لطفاً فایل PDB خودتان را انتخاب کنید:")
uploaded = files.upload()


pdb_file = list(uploaded.keys())[0]
print(f"✅ فایل آپلود شد: {pdb_file}")

# رسم Ramachandran Plot
from ramachandraw.utils import plot

print("🔄 در حال رسم پلات...")

fig = plot(
    pdb_file,
    cmap="viridis",      # می‌توانید تغییر دهید: plasma, inferno, coolwarm, jet
    alpha=0.85,
    dpi=200,
    save=True,
    show=True,
    filename=f"Ramachandran_{pdb_file}.png"
)

print("🎉 پلات با موفقیت ساخته شد!")
print(f"فایل تصویر ذخیره شد: Ramachandran_{pdb_file}.png")
