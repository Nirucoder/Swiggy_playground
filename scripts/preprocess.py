import pandas as pd
import numpy as np
from textblob import TextBlob
from datetime import datetime, timedelta
import os

def process_sales():
    print("Processing Sales Data by Category...")
    train_df = pd.read_csv(os.path.join("data", "raw", "train.csv"))
    meal_info_df = pd.read_csv(os.path.join("data", "raw", "meal_info.csv"))
    
    # 1. Merge Meal Info (Assignment basis: meal_id)
    train_df = train_df.merge(meal_info_df, on='meal_id')
    
    # Diversify: Combine Cuisine + Category (e.g., Thai Beverages, Indian Biryani)
    train_df['category'] = train_df['cuisine'] + " " + train_df['category']
    
    # 2. Map weeks to dates (Starting Jan 3, 2021)
    start_date = datetime(2021, 1, 3)
    train_df['ds'] = train_df['week'].apply(lambda w: start_date + timedelta(weeks=w-1))
    
    # 3. Aggregate by date and category
    sales_cat = train_df.groupby(['ds', 'category'])['num_orders'].sum().reset_index()
    sales_cat.columns = ['ds', 'category', 'y']
    
    # 4. Upsample each category to daily frequency
    print("Upsampling categories to daily frequency...")
    categories = sales_cat['category'].unique()
    daily_sales_list = []
    
    for cat in categories:
        cat_df = sales_cat[sales_cat['category'] == cat].set_index('ds')
        cat_df = cat_df.resample('D').interpolate(method='linear')
        cat_df['category'] = cat
        daily_sales_list.append(cat_df.reset_index())
    
    return pd.concat(daily_sales_list)

def process_sentiment(num_days):
    print("Processing Sentiment Data...")
    reviews_df = pd.read_csv(os.path.join("data", "raw", "sentiment analyis.csv"))
    
    # NLP Pipeline: Score sentiment
    print("Calculating sentiment scores (TextBlob)...")
    reviews_df['sentiment_score'] = reviews_df['Review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
    # Assign dates (spread reviews across the timeframe)
    start_date = datetime(2021, 1, 3)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    reviews_df['ds'] = np.random.choice(dates, size=len(reviews_df))
    
    daily_sentiment = reviews_df.groupby('ds')['sentiment_score'].mean().reset_index()
    return daily_sentiment

def get_weather():
    print("Loading Weather Data...")
    weather_path = os.path.join("data", "processed", "weather_data.csv")
    if os.path.exists(weather_path):
        weather_df = pd.read_csv(weather_path)
        weather_df['ds'] = pd.to_datetime(weather_df['ds'])
        return weather_df
    else:
        # This shouldn't happen now since we fetched real data
        print("Warning: Real weather data not found. This script requires weather_data.csv")
        return None

def main():
    # 1. Process Sales (with Categories)
    sales_df = process_sales()
    num_days = (sales_df['ds'].max() - sales_df['ds'].min()).days + 1
    
    # 2. Process Sentiment
    sentiment_df = process_sentiment(num_days)
    sentiment_df['ds'] = pd.to_datetime(sentiment_df['ds'])
    
    # 3. Get Weather
    weather_df = get_weather()
    
    # 4. Merge All
    print("Merging datasets...")
    master_df = sales_df.merge(weather_df, on='ds', how='left')
    master_df = master_df.merge(sentiment_df, on='ds', how='left')
    
    # Fill missing
    master_df['sentiment_score'] = master_df['sentiment_score'].fillna(master_df['sentiment_score'].mean())
    master_df['rain'] = master_df['rain'].fillna(0)
    master_df['temp'] = master_df['temp'].fillna(master_df['temp'].mean())
    
    # 5. Feature Engineering
    print("Engineering Trend and Behavioral Features...")
    # Time features
    master_df['ds'] = pd.to_datetime(master_df['ds'])
    master_df['day_of_week'] = master_df['ds'].dt.day_name()
    master_df['month'] = master_df['ds'].dt.month_name()
    master_df['is_weekend'] = master_df['ds'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Lag and Subscriber
    master_df['sentiment_lag_7'] = master_df.groupby('category')['sentiment_score'].shift(7).fillna(master_df['sentiment_score'].mean())
    master_df['is_subscriber'] = np.random.randint(0, 2, size=len(master_df))
    
    # 6. Hourly Synthesis (For Hourly Analysis)
    print("Synthesizing Hourly Data...")
    hourly_dist = {
        0: 0.005, 1: 0.002, 2: 0.001, 3: 0.001, 4: 0.001, 5: 0.005, 6: 0.01,
        7: 0.02, 8: 0.03, 9: 0.03, 10: 0.04, 11: 0.08, 12: 0.12, 13: 0.15, 14: 0.10,
        15: 0.05, 16: 0.04, 17: 0.04, 18: 0.05, 19: 0.10, 20: 0.12, 21: 0.15, 22: 0.10, 23: 0.05
    }
    
    hourly_rows = []
    # Take a sample for hourly to keep file size reasonable (last 6 months)
    recent_date = master_df['ds'].max() - timedelta(days=180)
    recent_df = master_df[master_df['ds'] >= recent_date]
    
    for _, row in recent_df.iterrows():
        for hr, weight in hourly_dist.items():
            h_row = row.copy()
            h_row['ds'] = row['ds'].replace(hour=hr)
            h_row['y'] = row['y'] * weight
            h_row['hour'] = hr
            hourly_rows.append(h_row)
    
    hourly_df = pd.DataFrame(hourly_rows)
    
    # 7. Final Export
    daily_output = os.path.join("data", "processed", "final_training_data.csv")
    hourly_output = os.path.join("data", "processed", "final_training_data_hourly.csv")
    
    master_df.to_csv(daily_output, index=False)
    hourly_df.to_csv(hourly_output, index=False)
    
    print(f"DONE! Daily dataset: {daily_output}")
    print(f"DONE! Hourly dataset (Last 6 months): {hourly_output}")
    print(f"Total Daily rows: {len(master_df)}")
    print(f"Total Hourly rows: {len(hourly_df)}")

if __name__ == "__main__":
    main()
