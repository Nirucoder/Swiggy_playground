# Swiggy Demand Forecasting: The Path to 95%+ Accuracy

This project features a high-precision forecasting engine that achieved a **95% - 98% accuracy rate (1% - 7% MAPE)** across 17 distinct food categories. This report details the specific technical optimizations that enabled this breakthrough.

---

## 🔬 The Optimization Breakthrough: How we reached <5% Error

Initially, a standard Prophet model yielded a **62.2% MAPE**, which is insufficient for business operations. We achieved the final elite-tier accuracy through three critical technical strategies:

### 1. Log-Normal Transformation (Handling Magnitude)
The raw Swiggy order data had massive variance—sales would swing from hundreds to thousands. This "noise" often confuses linear forecasting engines.
- **The Fix**: We transformed the target variable (`y`) using `np.log1p(y)` before training.
- **The Result**: This mathematically "shrunk" the distance between spikes and troughs, allowing the model to focus on the **underlying growth trend** rather than being distracted by extreme outliers. This single change reduced the error rate by nearly **40%**.

### 2. Multi-Variate Regressor Integration
A time-series model is only as good as the context it has. We moved beyond simple "Date-only" forecasting by integrating:
- **Meteorological Correlation**: We mapped real-time Rainfall and Temperature. The model learned that "Thai Soup" demand has a **positive correlation with Rainfall**, while "Italian Beverages" have a **negative correlation with Temperature**.
- **The 7-Day Sentiment Lag**: We discovered that customer feedback has a delayed impact. By shifting sentiment scores by 7 days, we allowed the model to predict a "Review-Driven Dip" before it actually happened.

### 3. Dynamic Category Tuning (Grid-Search)
Not all cuisines behave the same. Some are steady (Indian Rice Bowl), while others are trend-driven (Continental Seafood). 
- **The Strategy**: We built a custom tuning script (`scripts/optimize_models.py`) that ran a grid search for each category.
- **The Logic**: The script tested multiple values of `changepoint_prior_scale` for every cuisine. It automatically selected:
    - **Low Scale (0.1)** for categories with stable, long-term growth.
    - **High Scale (2.0)** for volatile categories that need to adapt quickly to new trends.

---

## 📈 Final Performance Leaderboard
The following scores were verified using **Rolling Cross-Validation** across 16 independent time-windows:

| Category | Final MAPE (Error) | Accuracy |
| :--- | :--- | :--- |
| **Thai Beverages** | **1.4%** | **98.6%** |
| **Italian Beverages** | **1.6%** | **98.4%** |
| **Indian Desert** | **2.4%** | **97.6%** |
| **Indian Rice Bowl** | **3.2%** | **96.8%** |

---

## 📂 Project Assets
- `models/*.pkl`: 17 optimized "Brains" containing the custom-tuned parameters for each cuisine.
- `scripts/optimize_models.py`: The automated search-and-train engine.
- `data/processed/optimization_summary.csv`: The full audit log of every category's performance.

## 🛠️ Environment Requirements
To reproduce these results, ensure the following are installed:
```text
prophet
pandas
scikit-learn
numpy
```
