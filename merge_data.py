import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# 1. Load environment variables untuk koneksi database
load_dotenv()

# Koneksi Database
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 2. Tentukan jalur file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data_scrapping")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_data")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# 3. Buat folder jika belum ada
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# 4. File log
MERGED_FILE = os.path.join(PROCESSED_FOLDER, "merged_data.csv")
LOG_FILE = os.path.join(LOG_FOLDER, "merge_upload_log.txt")

# 5. Konfigurasi logging
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s")

# 6. Koneksi ke database Supabase
try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    engine.connect()
    logging.info("Koneksi ke database Supabase berhasil.")
    print("Koneksi ke database Supabase berhasil.")
except Exception as e:
    logging.error(f"Error saat menghubungkan ke database: {e}")
    print(f"Error saat menghubungkan ke database: {e}")
    exit()

# 7. Gabungkan data Pytrends dan Female Daily
try:
    print("Membaca file data...")
    pytrends_files = [f for f in os.listdir(DATA_FOLDER) if f.startswith('pytrends_') and f.endswith('.csv')]
    female_daily_files = [f for f in os.listdir(DATA_FOLDER) if f.startswith('FemaleDaily_Review') and f.endswith('.csv')]
    
    merged_data_list = []
    for pytrend_file in pytrends_files:
        product_name = pytrend_file.replace('pytrends_', '').replace('.csv', '').replace('_', ' ').lower()
        matching_file = next((f for f in female_daily_files if product_name in f.lower()), None)
        if matching_file:
            print(f"Menggabungkan data untuk produk: {product_name}")
            logging.info(f"Menggabungkan data untuk produk: {product_name}")
            
            pytrend_data = pd.read_csv(os.path.join(DATA_FOLDER, pytrend_file))
            female_daily_data = pd.read_csv(os.path.join(DATA_FOLDER, matching_file))
            
            # Normalisasi kolom
            pytrend_data.rename(columns={"keyword": "product_name", "popularity": "popularity_score"}, inplace=True)
            
            # Gabungkan data
            merged = pd.merge(
                pytrend_data,
                female_daily_data,
                left_on="product_name",
                right_on="Nama_Produk",  # Sesuaikan dengan kolom Female Daily
                how="inner"
            )
            merged_data_list.append(merged)
        else:
            logging.warning(f"Tidak ada data Female Daily yang cocok untuk {product_name}. Melewati...")

    # Gabungkan semua data
    if merged_data_list:
        final_merged_data = pd.concat(merged_data_list, ignore_index=True)
        final_merged_data.to_csv(MERGED_FILE, index=False)
        print(f"Data gabungan disimpan di {MERGED_FILE}")
        logging.info(f"Data gabungan berhasil disimpan di {MERGED_FILE}")
    else:
        print("Tidak ada data yang berhasil digabungkan.")
        logging.info("Tidak ada data yang berhasil digabungkan.")
        exit()
except Exception as e:
    logging.error(f"Error saat menggabungkan data: {e}")
    print(f"Error saat menggabungkan data: {e}")
    exit()

# 8. Upload hasil ke database
try:
    print(f"Mengunggah data gabungan ke database Supabase...")
    table_name = "merged_data"
    final_merged_data.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"Data gabungan berhasil diunggah ke tabel '{table_name}' di database Supabase.")
    print(f"Data gabungan berhasil diunggah ke tabel '{table_name}' di database Supabase.")
except Exception as e:
    logging.error(f"Error saat mengunggah data ke database: {e}")
    print(f"Error saat mengunggah data ke database: {e}")
