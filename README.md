# Swiggy Demand Forecasting - Phase 1: Data & Feature Engineering

This branch contains the core data pipeline for the Swiggy Demand Forecasting project. The goal of Phase 1 was to "stitch" together disparate data sources into a unified, high-quality dataset ready for machine learning.

## 🚀 Project Overview
In a real-world scenario, food delivery platforms like Swiggy generate massive amounts of transactional data. To simulate this, we have integrated sales data, real historical weather, and customer sentiment to predict the **best-selling product/category for the upcoming month**.

## 📂 Repository Structure
```text
swiggy/
├── data/
│   └── processed/           # Final cleaned & merged datasets
│       ├── final_training_data.csv        # Daily totals (for ML models)
│       └── final_training_data_hourly.csv # Hourly peaks (for trend analysis)
├── scripts/
│   ├── fetch_weather.py     # Script to pull real Bangalore history via WeatherAPI
│   └── preprocess.py        # The engine for merging, NLP, and feature engineering
└── requirements.txt         # Project dependencies
```

## 🏗️ The 3 Pillars of Our Data
We unified three distinct "worlds" into one timeline:
1.  **Sales History**: Converted weekly "Food Demand" snapshots into daily continuous flows using linear interpolation.
2.  **Weather Intelligence**: Integrated **1,000+ days** of real Bangalore weather (Temperature & Rain) using the WeatherAPI.com Business Trial.
3.  **Customer Sentiment**: Processed **8,000 restaurant reviews** using the **TextBlob NLP engine** to calculate daily mood scores.

## 🧠 Intelligent Features
To boost model accuracy, we engineered behavioral features:
*   **Diverse Categories**: Mapped orders to **17 unique product types** (e.g., *Indian Biryani, Thai Starters, Italian Pasta*) based on `meal_id`.
*   **Hourly Synthesis**: Distributes daily orders across realistic peak hours (**Lunch 12-2 PM** and **Dinner 7-10 PM**) to support granular analysis.
*   **Sentiment Lag (7-Day)**: Captures the "delayed impact" of customer reviews on future ordering behavior.
*   **Subscriber Flag**: Simulates "Swiggy One" membership patterns.

## 🛠️ How to Reproduce
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  (Optional) Fetch fresh weather data:
    ```bash
    python scripts/fetch_weather.py
    ```
3.  Generate master datasets:
    ```bash
    python scripts/preprocess.py
    ```

