# cuman contoh nama file
#pip install pytrends
#!pip install --upgrade pytrends 
import time
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Inisialisasi koneksi ke Google Trends
pytrends = TrendReq(hl='id', tz=360, timeout=(10, 25), retries=3, backoff_factor=0.3)

# Set kata kunci dan lokasi geografis
keyword = ['Azarine Hydrashoothe Sunscreen Gel Spf45+++']  # Ubah kata kunci di sini jika diperlukan
geo_location = 'ID'  # 'ID' untuk Indonesia

# Mengonfigurasi payload dengan jangka waktu 365 hari terakhir (12 bulan)
pytrends.build_payload(kw_list=keyword, timeframe='today 12-m', geo=geo_location, cat=0)

# Tambahkan jeda waktu untuk menghindari batasan Google Trends
time.sleep(5)

try:
    # 1. Interest Over Time (Minat dari Waktu ke Waktu)
    interest_over_time = pytrends.interest_over_time()
    print("Interest Over Time Data:", interest_over_time)

    if interest_over_time.empty:
        print("No data returned from Google Trends for Interest Over Time.")
    else:
        # Simpan ke CSV
        interest_over_time.to_csv('Hydrashoothe_Sunscreen_Gel_Spf45+++.csv')
        print("Interest Over Time data saved to 'sunscreen_trends_data.csv'")

        # Plot data
        interest_over_time.reset_index(inplace=True)
        plt.figure(figsize=(10, 6))
        plt.plot(interest_over_time['date'], interest_over_time[keyword[0]], label=keyword[0])
        plt.title('Google Trends Search Trend for Sunscreen in Indonesia (Last 365 Days)')
        plt.xlabel('Date')
        plt.ylabel('Popularity')
        plt.legend()
        plt.grid(True)
        plt.show()

    # 2. Interest by Region (Minat Berdasarkan Wilayah)
    interest_by_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    print("Interest by Region Data:", interest_by_region)

    # Simpan ke CSV
    interest_by_region.to_csv('sunscreen_interest_by_region.csv')
    print("Interest by Region data saved to 'sunscreen_interest_by_region.csv'")

    # 3. Related Queries (Kueri Terkait)
    related_queries = pytrends.related_queries()
    top_related_queries = related_queries[keyword[0]]['top']
    rising_related_queries = related_queries[keyword[0]]['rising']
    
    print("Top Related Queries:", top_related_queries)
    print("Rising Related Queries:", rising_related_queries)

    # Simpan ke CSV
    if top_related_queries is not None:
        top_related_queries.to_csv('sunscreen_top_related_queries.csv')
        print("Top Related Queries saved to 'sunscreen_top_related_queries.csv'")
    if rising_related_queries is not None:
        rising_related_queries.to_csv('sunscreen_rising_related_queries.csv')
        print("Rising Related Queries saved to 'sunscreen_rising_related_queries.csv'")

    # 4. Related Topics (Topik Terkait)
    related_topics = pytrends.related_topics()
    print("Related Topics:", related_topics)

    if keyword[0] in related_topics:
        top_topics = related_topics[keyword[0]]['top']
        rising_topics = related_topics[keyword[0]]['rising']

        if top_topics is not None:
            top_topics.to_csv('sunscreen_related_topics_top.csv')
            print("Top Related Topics saved to 'sunscreen_related_topics_top.csv'")
        
        if rising_topics is not None:
            rising_topics.to_csv('sunscreen_related_topics_rising.csv')
            print("Rising Related Topics saved to 'sunscreen_related_topics_rising.csv'")

except Exception as e:
    print("Error:", e)
#maaf kalo salah bsk aku ubah lagi
