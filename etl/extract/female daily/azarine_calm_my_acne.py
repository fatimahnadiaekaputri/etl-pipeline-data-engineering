from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

driver = webdriver.Chrome()

def extract_all_products(url):
    driver.get(url)
    time.sleep(5)  # Initial wait to allow page to load

    products = []

    for page in range(1, 30):  # Limit to pages 1 through 3
        # Scroll down the page to load more products
        scroll_pause_time = 3
        screen_height = driver.execute_script("return window.screen.height;")
        scroll_height = 0

        # Scroll to the end of the current page
        while True:
            driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(scroll_pause_time)
            scroll_height += screen_height
            if scroll_height >= driver.execute_script("return document.body.scrollHeight;"):
                break

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sections = soup.find_all('div', class_='review-card')

        if not sections:
            print(f"No reviews found on page {page}.")
            break

        for section in sections:
            # Extract information based on provided class names
            username_tag = section.find('p', class_='profile-username')
            age_tag = section.find('p', class_='profile-age')
            profile_description_tag = section.find('p', class_='profile-description')
            date_tag = section.find('p', class_='review-date')
            review_content_tag = section.find('p', class_='text-content')
            usage_period_tag = section.find('div', class_='information-wrapper').find('b') if section.find('div', class_='information-wrapper') else None
            purchase_point_tag = section.find('div', class_='information-wrapper').find_all('b')[1] if section.find('div', class_='information-wrapper') and len(section.find('div', class_='information-wrapper').find_all('b')) > 1 else None
            recommend_tag = section.find('p', class_='recommend').find('b') if section.find('p', class_='recommend') else None

            products.append({
                "username": username_tag.text.strip() if username_tag else None,
                "age": age_tag.text.strip() if age_tag else None,
                "profile_description": profile_description_tag.text.strip() if profile_description_tag else None,
                "date": date_tag.text.strip() if date_tag else None,
                "review_content": review_content_tag.text.strip() if review_content_tag else None,
                "usage_period": usage_period_tag.text.strip() if usage_period_tag else None,
                "purchase_point": purchase_point_tag.text.strip() if purchase_point_tag else None,
                "recommend": recommend_tag.text.strip() if recommend_tag else None
            })

        # Try to click the "Next" button to move to the next page
        try:
            next_button = driver.find_element(By.ID, 'id_next_page')
            next_button.click()
            time.sleep(5)  # Wait for page to load
        except:
            print("Next button not found or unable to click.")
            break

    # Create a DataFrame
    df = pd.DataFrame(products)
    return df

url = 'https://reviews.femaledaily.com/products/moisturizer/sun-protection-1/azarine-cosmetic/azarine-calm-my-acne-sunscreen-moisturizer-1'
data_df = extract_all_products(url)
print(data_df)

# Path untuk menyimpan hasil scraping
output_folder = '../result scrapping data'
output_path = os.path.join(output_folder, 'Data Skincare Azarine Calm My Acne Sunscreen Moisturizer.csv')

# Membuat folder jika belum ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save to CSV
data_df.to_csv(output_path, encoding='utf-8', index=True)

driver.quit()
