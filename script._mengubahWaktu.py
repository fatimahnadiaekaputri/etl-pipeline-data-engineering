import pandas as pd
import os
from datetime import datetime, timedelta

# 1. Tentukan tanggal hari ini
today_date = datetime(2024, 11, 16)

# 2. Tentukan folder file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data_scrapping")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_data")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# 3. Fungsi untuk mengubah format tanggal
def convert_date(date_str):
    try:
        # Jika formatnya "X days ago"
        if "days ago" in date_str:
            days = int(date_str.split()[0])
            return (today_date - timedelta(days=days)).strftime("%Y-%m-%d")
        # Jika formatnya "X months ago"
        elif "months ago" in date_str:
            months = int(date_str.split()[0])
            return (today_date - timedelta(days=30 * months)).strftime("%Y-%m-%d")
        # Jika formatnya "X years ago"
        elif "years ago" in date_str:
            years = int(date_str.split()[0])
            return (today_date - timedelta(days=365 * years)).strftime("%Y-%m-%d")
        # Jika format sudah berupa tanggal (misalnya "08 Nov 2024")
        else:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error memproses tanggal: {date_str} - {e}")
        return None

# 4. Proses semua file Female Daily
for file_name in os.listdir(DATA_FOLDER):
    if file_name.startswith("FemaleDaily") and file_name.endswith(".csv"):
        print(f"Memproses file: {file_name}")
        file_path = os.path.join(DATA_FOLDER, file_name)

        # Baca file
        df = pd.read_csv(file_path)

        # Pastikan kolom 'date' ada
        if 'date' in df.columns:
            # Konversi tanggal
            df['date'] = df['date'].apply(convert_date)
        else:
            print(f"Tidak ada kolom 'date' di file {file_name}")

        # Simpan file hasil
        output_path = os.path.join(PROCESSED_FOLDER, file_name)
        df.to_csv(output_path, index=False)
        print(f"Hasil diproses disimpan di: {output_path}")
