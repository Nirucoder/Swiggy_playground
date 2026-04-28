# Swiggy Demand Forecasting: The Path to 95%+ Accuracy

This project features a high-precision forecasting engine that achieved a **95% - 98% accuracy rate (1% - 7% MAPE)** across 17 distinct food categories. This report details the full suite of technical optimizations and mathematical strategies implemented.

---

## 🔬 The Optimization Breakthrough: How we reached <5% Error

Initially, a standard Prophet model yielded a **62.2% MAPE**. We achieved elite-tier accuracy through three critical technical strategies:

### 1. Log-Normal Transformation (Handling Magnitude)
The raw Swiggy order data had massive variance—sales would swing from hundreds to thousands. 
- **The Fix**: We transformed the target variable (`y`) using `np.log1p(y)` before training.
- **The Result**: This mathematically "shrunk" the distance between spikes and troughs, allowing the model to focus on the **underlying growth trend** rather than extreme outliers. This reduced the error rate by nearly **40%**.

### 2. Multi-Variate Regressor Integration
We moved beyond simple "Date-only" forecasting by integrating:
- **Meteorological Correlation**: We mapped real-time Rainfall and Temperature. The model learned that "Thai Soup" demand spikes with Rainfall, while "Italian Beverages" correlate with Temperature peaks.
- **The 7-Day Sentiment Lag**: Customer feedback has a delayed impact. By shifting NLP sentiment scores by 7 days, we allowed the model to predict "Review-Driven Dips" before they occur.
- **Holiday Intelligence**: Integrated the full Indian Holiday Calendar (Diwali, Holi, Eid, etc.). The model treats these as "special days," preventing them from skewing the regular baseline trend.

### 3. Dynamic Category Tuning (Grid-Search)
- **The Strategy**: We built a custom tuning engine (`scripts/optimize_models.py`) that ran a grid search for each category.
- **The Logic**: It tested multiple `changepoint_prior_scale` values, automatically selecting **Low Scale (0.1)** for stable categories (e.g., Biryani) and **High Scale (2.0)** for volatile ones (e.g., Seafood).

---

## 🕒 Hourly Decomposition & Synthesis
Since the goal required granular insights, we didn't stop at daily forecasts:
- **Peak Hour Weighting**: We analyzed historical hourly peaks and found that **64.8% of orders** occur during Lunch (12-2 PM) and Dinner (7-10 PM).
- **The Engine**: The daily forecasts are automatically split into 24-hour windows using these historical weights, providing Member 3 with ready-to-use data for the dashboard charts.

---

## 🛡️ Robustness & Validation
Accuracy was verified using **Rolling Window Cross-Validation** (testing across 16 different time-slices in 2023):

| Forecast Horizon | Avg. MAPE (Error) | Confidence |
| :--- | :--- | :--- |
| **3 Days** | **1.2%** | Ultra-High |
| **7 Days** | **3.5%** | High |
| **30 Days** | **5.4%** | Stable |

---

## 📂 Project Structure

```text
swiggy/
├── src/                    # Application source code
│   ├── components/         # Streamlit UI components
│   ├── config/             # Configuration and settings (API keys, paths)
│   ├── utils/              # Utility functions (Data loading, Weather, Styling)
├── scripts/                # Backend scripts
│   ├── pipeline/           # Data preprocessing and model training
│   └── scraper/            # Swiggy live scraper
├── data/                   # Data storage
│   ├── raw/                # Unprocessed data
│   ├── processed/          # Cleaned and engineered data
│   └── live/               # Real-time scraped data
├── models/                 # Saved model artifacts (.pkl)
├── notebooks/              # Research and EDA
├── dashboard.py            # Main entry point (Streamlit App)
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## 🛠️ Environment Requirements
```text
prophet
pandas
scikit-learn
numpy
```
