import os
import pandas as pd
import logging

# 1. Tentukan jalur file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data_scrapping")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_data")
FINAL_FOLDER = os.path.join(BASE_DIR, "merge_data")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# 2. Buat folder jika belum ada
os.makedirs(FINAL_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# 3. File log
LOG_FILE = os.path.join(LOG_FOLDER, "merge_log.txt")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s")

# 4. Daftar pasangan file yang akan digabungkan
file_combinations = [
    {
        "female_daily_file": "FemaleDaily_Azarine Calm My Acne Sunscreen Moisturizer.csv",
        "pytrends_file": "pytrends_Calm My Acne Sunscreen Moisturiser SPF 35 PA+++.csv",
        "output_name": "Merged_Azarine_Calm_My_Acne.csv"
    },
    {
        "female_daily_file": "FemaleDaily_Review Azarine Hydramax C Sunscreen Serum.csv",
        "pytrends_file": "pytrends_Azarine Azarine Hm-c Sunsc Srm Spf50 Pa++++ 40ml.csv",
        "output_name": "Merged_Azarine_Hydramax_C.csv"
    },
    {
        "female_daily_file": "FemaleDaily_Review Azarine Hydrashoote Sunscreen Gel.csv",
        "pytrends_file": "pytrends_Hydrashoothe Sunscreen Gel Spf45+++.csv",
        "output_name": "Merged_Azarine_Hydrashoote.csv"
    },
    {
        "female_daily_file": "FemaleDaily_Review Skinaqua UV Moisture Milk.csv",
        "pytrends_file": "pytrends_Skin Aqua Super Moisture Milk Sunscreen PA++++ 40mL.csv",
        "output_name": "Merged_Skinaqua_Moisture_Milk.csv"
    },
    {
        "female_daily_file": "FemaleDaily_Review Skinaqua UV Whitening Milk.csv",
        "pytrends_file": "pytrends_Skin Aqua Skin Aqua Uv Whitening Milk Spf 50 40ml.csv",
        "output_name": "Merged_Skinaqua_Whitening_Milk.csv"
    }
]

# 5. Proses penggabungan
try:
    for combination in file_combinations:
        female_file_path = os.path.join(PROCESSED_FOLDER, combination["female_daily_file"])
        pytrends_file_path = os.path.join(DATA_FOLDER, combination["pytrends_file"])
        output_file_path = os.path.join(FINAL_FOLDER, combination["output_name"])
        
        print(f"Menggabungkan: {combination['female_daily_file']} + {combination['pytrends_file']}")
        logging.info(f"Menggabungkan: {combination['female_daily_file']} + {combination['pytrends_file']}")

        # Pastikan kedua file ada
        if os.path.exists(female_file_path) and os.path.exists(pytrends_file_path):
            # Baca kedua file
            female_df = pd.read_csv(female_file_path)
            pytrends_df = pd.read_csv(pytrends_file_path)

            # Lakukan merge berdasarkan kolom 'date'
            merged_df = pd.merge(female_df, pytrends_df, on="date", how="inner")  # Gunakan 'outer' agar semua data muncul

            # Simpan hasil gabungan
            merged_df.to_csv(output_file_path, index=False)
            print(f"Hasil gabungan disimpan di: {output_file_path}")
            logging.info(f"Hasil gabungan disimpan di: {output_file_path}")
        else:
            if not os.path.exists(female_file_path):
                print(f"File Female Daily tidak ditemukan: {female_file_path}")
                logging.warning(f"File Female Daily tidak ditemukan: {female_file_path}")
            if not os.path.exists(pytrends_file_path):
                print(f"File Pytrends tidak ditemukan: {pytrends_file_path}")
                logging.warning(f"File Pytrends tidak ditemukan: {pytrends_file_path}")
except Exception as e:
    logging.error(f"Error saat memproses data: {e}")
    print(f"Error saat memproses data: {e}")
