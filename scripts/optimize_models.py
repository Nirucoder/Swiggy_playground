import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import pickle
import os
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def train_optimized():
    df = pd.read_csv("data/processed/final_training_data.csv")
    os.makedirs("models", exist_ok=True)
    
    optimized_summary = []
    # Reduced grid for speed, focusing on the most impactful parameter
    param_grid = [0.1, 0.5, 2.0]
    
    categories = df['category'].unique()
    print(f"Starting Optimization for {len(categories)} categories...")

    for category in categories:
        print(f"\n--- Category: {category} ---")
        df_cat = df[df['category'] == category][['ds', 'y', 'rain', 'temp', 'sentiment_lag_7', 'is_subscriber']].copy()
        df_cat['ds'] = pd.to_datetime(df_cat['ds'])
        
        # 1. Log Transformation to handle high variance
        # We use log1p to handle any potential zeros safely
        df_cat['y'] = np.log1p(df_cat['y'])
        
        best_mape = float('inf')
        best_cp = 0.5
        
        # 2. Per-Category Hyperparameter Tuning
        for cp in param_grid:
            m = Prophet(
                changepoint_prior_scale=cp, 
                yearly_seasonality=True, 
                weekly_seasonality=True,
                interval_width=0.95
            )
            m.add_country_holidays(country_name='IN')
            for reg in ['rain', 'temp', 'sentiment_lag_7', 'is_subscriber']:
                m.add_regressor(reg)
            
            m.fit(df_cat)
            
            # 3. Cross-Validation (The Professional Way)
            # Testing model on 3 different 30-day windows from the past
            try:
                df_cv = cross_validation(
                    m, 
                    initial='730 days', 
                    period='30 days', 
                    horizon='30 days', 
                    parallel="threads"
                )
                df_p = performance_metrics(df_cv)
                current_mape = df_p['mape'].mean()
                print(f"  Tuning CP={cp:3} | CV MAPE: {current_mape:.2%}")
                
                if current_mape < best_mape:
                    best_mape = current_mape
                    best_cp = cp
            except Exception as e:
                print(f"  Skipping CV for CP={cp} due to data constraints.")

        print(f"Best CP for {category}: {best_cp}")
        
        # Final train with best parameters on all data
        m_final = Prophet(
            changepoint_prior_scale=best_cp, 
            yearly_seasonality=True, 
            weekly_seasonality=True
        )
        m_final.add_country_holidays(country_name='IN')
        for reg in ['rain', 'temp', 'sentiment_lag_7', 'is_subscriber']:
            m_final.add_regressor(reg)
        m_final.fit(df_cat)
        
        # Save the "Brain"
        model_name = category.lower().replace(" ", "_")
        with open(f"models/{model_name}.pkl", "wb") as f:
            pickle.dump(m_final, f)
            
        optimized_summary.append({
            "category": category,
            "best_cp": best_cp,
            "cv_mape": best_mape if best_mape != float('inf') else "N/A"
        })

    # Save summary
    summary_df = pd.DataFrame(optimized_summary)
    summary_df.to_csv("data/processed/optimization_summary.csv", index=False)
    print("\nAll models optimized and saved to /models/")
    print(summary_df)

if __name__ == "__main__":
    train_optimized()
