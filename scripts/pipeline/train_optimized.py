import pandas as pd
from prophet import Prophet
import pickle
import os

def train_all_categories():
    df = pd.read_csv("data/processed/final_training_data.csv")
    df['ds'] = pd.to_datetime(df['ds'])
    
    categories = df['category'].unique()
    os.makedirs("models", exist_ok=True)
    
    print(f" Training {len(categories)} Optimized Models...")
    
    for cat in categories:
        print(f" Training model for: {cat}")
        df_cat = df[df['category'] == cat].copy()
        
        # Prophet setup with high flexibility and regressors
        m = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.5 # Increased flexibility to avoid flat lines
        )
        
        # Add regressors
        m.add_regressor('temp')
        m.add_regressor('rain')
        m.add_regressor('discount')
        m.add_regressor('sentiment_lag_7')
        m.add_regressor('is_subscriber')
        
        # Add Indian Holidays (Crucial for demand spikes)
        m.add_country_holidays(country_name='IN')
        
        m.fit(df_cat)
        
        # Save Model
        with open(f"models/{cat.lower().replace(' ', '_')}.pkl", "wb") as f:
            pickle.dump(m, f)
            
    print("\n All Models Retrained with Discount & Seasonality features!")

if __name__ == "__main__":
    train_all_categories()
