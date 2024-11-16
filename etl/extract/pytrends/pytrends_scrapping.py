# cuman contoh nama file
#pip install pytrends
#!pip install --upgrade pytrends 
import time
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Google Trends connection
pytrends = TrendReq(hl='id', tz=360, timeout=(10, 25), retries=3, backoff_factor=0.3)

# Set broader keyword and longer timeframe for testing
keyword = ['Skin Aqua Suncreen Skin Aqua Uv Moisture Gel Spf 30 Pa++ Gel 40g']  # Broader keyword for testing
geo_location = 'ID'  # 'ID' for Indonesia

# Configure payload with a longer timeframe
pytrends.build_payload(kw_list=keyword, timeframe='today 5-y', geo=geo_location, cat=0)

# Add delay to avoid Google Trends rate limits
time.sleep(5)

try:
    # Retrieve interest over time data
    interest_over_time = pytrends.interest_over_time()
    print("Interest Over Time Data:", interest_over_time)

    if interest_over_time.empty:
        print("No data returned from Google Trends.")
    else:
        # Save to CSV
        interest_over_time.to_csv('Skin Aqua Suncreen Skin Aqua Uv Moisture Gel Spf 30 Pa++ Gel 40g.csv')
        print("Data saved to 'sunscreen_trends_data.csv'")

        # Plot data
        interest_over_time.reset_index(inplace=True)
        plt.figure(figsize=(10, 6))
        plt.plot(interest_over_time['date'], interest_over_time[keyword[0]], label=keyword[0])
        plt.title('Google Trends Search Trend for Sunscreen in Indonesia')
        plt.xlabel('Date')
        plt.ylabel('Popularity')
        plt.legend()
        plt.grid(True)
        plt.show()
        
except Exception as e:
    print("Error:", e)

#maaf kalo salah bsk aku ubah lagi
