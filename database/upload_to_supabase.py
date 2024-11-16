import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# 1. Load environment variables dari file .env
load_dotenv()

# 2. Ambil parameter koneksi dari environment
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 3. Jalur folder untuk file CSV, log, dan catatan file yang sudah diunggah
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data_scrapping")
LOG_FOLDER = os.path.join(BASE_DIR, "..", "logs")
PROCESSED_LOG = os.path.join(LOG_FOLDER, "processed_files.txt")  # File untuk mencatat file yang sudah diunggah

# 4. Buat folder log jika belum ada
os.makedirs(LOG_FOLDER, exist_ok=True)

# 5. Konfigurasi logging
LOG_FILE = os.path.join(LOG_FOLDER, "upload_log.txt")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s")

# 6. Coba koneksi ke database
try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    engine.connect()
    logging.info("Koneksi ke database Supabase berhasil.")
    print("Koneksi ke database Supabase berhasil.")
except Exception as e:
    logging.error(f"Error saat menghubungkan ke database: {e}")
    print(f"Error saat menghubungkan ke database: {e}")
    exit()

# 7. Cek folder data_scrapping untuk file CSV
try:
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
    if not files:
        print("Tidak ada file CSV di folder data_scrapping!")
        logging.warning("Tidak ada file CSV di folder data_scrapping!")
        exit()
except FileNotFoundError:
    print(f"Folder data_scrapping tidak ditemukan di {DATA_FOLDER}. Periksa jalurnya!")
    logging.error(f"Folder data_scrapping tidak ditemukan di {DATA_FOLDER}.")
    exit()

# 8. Load file yang sudah diproses
processed_files = set()
if os.path.exists(PROCESSED_LOG):
    with open(PROCESSED_LOG, 'r') as f:
        processed_files = set(f.read().splitlines())

# 9. Upload setiap file CSV yang belum diproses ke database
for file_name in files:
    if file_name in processed_files:
        print(f"File {file_name} sudah pernah diunggah. Melewati...")
        logging.info(f"File {file_name} sudah pernah diunggah. Melewati...")
        continue

    # Buat nama tabel dari nama file, potong jika terlalu panjang
    table_name = file_name.replace('.csv', '').replace(' ', '_').lower()
    if len(table_name) > 63:
        logging.warning(f"Nama tabel '{table_name}' terlalu panjang. Dipersingkat.")
        table_name = table_name[:63]

    file_path = os.path.join(DATA_FOLDER, file_name)

    try:
        print(f"Memuat data dari {file_name}...")
        logging.info(f"Memuat data dari {file_name}...")

        # Baca data CSV
        data = pd.read_csv(file_path)
        logging.info(f"Data {table_name} berhasil dimuat. Jumlah baris: {len(data)}")

        # Upload data ke tabel
        print(f"Mengunggah data ke tabel '{table_name}'...")
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data berhasil diunggah ke tabel '{table_name}'.")
        print(f"Data berhasil diunggah ke tabel '{table_name}'.")

        # Tambahkan file ke daftar file yang sudah diproses
        with open(PROCESSED_LOG, 'a') as f:
            f.write(f"{file_name}\n")
    except Exception as e:
        logging.error(f"Error saat mengunggah data dari {file_name} ke tabel '{table_name}': {e}")
        print(f"Error saat mengunggah data dari {file_name} ke tabel '{table_name}': {e}")

print("Proses upload selesai. Periksa log untuk detail lebih lanjut.")
logging.info("Proses upload selesai.")
