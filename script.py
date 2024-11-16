import pandas as pd
import os

# Periksa apakah file ada
pytrends_path = r'data_scrapping/pytrends_Calm My Acne Sunscreen Moisturiser SPF 35 PA+++.csv'
female_daily_path = r'data_scrapping/FemaleDaily_Review Azarine Calm My Acne Sunscreen Moisturizer.csv'

if not os.path.exists(pytrends_path):
    print(f"File tidak ditemukan: {pytrends_path}")
    exit()
if not os.path.exists(female_daily_path):
    print(f"File tidak ditemukan: {female_daily_path}")
    exit()

# Load Data
pytrends_data = pd.read_csv(pytrends_path)
female_daily_data = pd.read_csv(female_daily_path)

# Standarisasi Nama Produk
product_mapping = {
    "Azarine Calm My Acne Sunscreen Moisturizer": "Azarine Calm My Acne Sunscreen Moisturizer SPF 35 PA+++"
}

# Tambahkan kolom untuk mencocokkan nama produk di Female Daily
female_daily_data['Nama_Produk'] = "Azarine Calm My Acne Sunscreen Moisturizer SPF 35 PA+++"

# Filter data Pytrends berdasarkan kata kunci produk
pytrends_filtered = pytrends_data[pytrends_data['keyword'] == product_mapping["Azarine Calm My Acne Sunscreen Moisturizer"]]

# Gabungkan data Pytrends dan Female Daily berdasarkan kata kunci (produk)
combined_data = pd.merge(
    pytrends_filtered,               # Data Pytrends
    female_daily_data,               # Data Female Daily
    left_on='keyword',               # Kata kunci di Pytrends
    right_on='Nama_Produk',          # Nama produk di Female Daily
    how='inner'                      # Gabungkan hanya data yang cocok
)

# Simpan hasil gabungan
combined_data.to_csv('data_scrapping/fixData_azarine.csv', index=False)

# Tampilkan hasil
print("Data berhasil digabungkan!")
print(combined_data.head())
