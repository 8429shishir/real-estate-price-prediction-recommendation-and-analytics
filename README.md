# 🏠 Real Estate Price Intelligence System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Model-1793d1.svg)](https://xgboost.readthedocs.io/)

An end-to-end machine learning and data analytics application for analyzing and predicting residential property prices in **Gurgaon, India**. Built from scratch, this project encompasses the entire data science pipeline—from raw data collection, rigorous cleaning, and extensive exploratory data analysis (EDA) to feature engineering, model optimization, and deployment as a full-stack interactive web application.

---

## 🌟 Key Highlights

- **13,000+** Properties Analyzed (Flats & Independent Houses)
- **12** Engineered Feature Variables
- **~90%** Model Accuracy (R² Score) achieved using an optimized pipeline
- **13** Jupyter Notebooks thoroughly documenting the ML workflow

## 🚀 Application Modules

The Streamlit web application is divided into two primary modules:

1. **💰 Price Predictor (`pages/1_Price Predictor.py`)**
   Enter property specifications (e.g., sector, built-up area, bedroom/bathroom count, luxury category, furnishing status) to receive an instant, AI-powered price estimate. Backed by a tuned XGBoost/Ensemble model wrapped in a Scikit-learn pipeline.
   
2. **📊 Analysis App (`pages/2_Analysis App.py`)**
   Dive deep into the Gurgaon real estate market through interactive visualizations. Explore sector heatmaps, feature correlations, and multi-variate insights powered by Plotly.

## 🛠️ Tech Stack

- **Language:** Python
- **Machine Learning:** Scikit-learn, XGBoost
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Plotly, Matplotlib
- **Web Framework:** Streamlit
- **Development & Analysis:** Jupyter Notebooks, Pandas Profiling
- **Serialization:** Pickle

## 📓 Data Science Workflow

The complete machine learning workflow is systematically organized in the `src/` directory across 13 step-by-step Jupyter notebooks:

1. `01_data_preprocessing_flat.ipynb` - Initial extraction & formatting for flats.
2. `02_data_preprocessing_house.ipynb` - Initial extraction & formatting for houses.
3. `03_merge_flat_house.ipynb` - Combining datasets into a unified structure.
4. `04_merge_flat_house_cleaning.ipynb` - Handling duplicates, inconsistencies, and formatting text.
5. `05_feature_engineering.ipynb` - Creating 12 key predictive features.
6. `06_eda_univariate_analysis.ipynb` - Single variable distributions.
7. `07_pandas_profiling.ipynb` - Automated, comprehensive data profiling.
8. `08_eda_multivariate.ipynb` - Multi-variable relationship analysis.
9. `09_outlier_removal.ipynb` - Detecting and managing statistical outliers.
10. `10_missing_value_immutation.ipynb` - Advanced imputation for missing data.
11. `11_feature_selection.ipynb` - Identifying the most impactful predictors.
12. `12_baseline_model.ipynb` - Initial benchmarking with standard models.
13. `13_model_selection.ipynb` - Evaluating Linear Regression, Ridge, Lasso, Decision Tree, Random Forest, Gradient Boosting, and XGBoost to finalize the best-performing pipeline.

## 💻 Installation & Setup

To run this project locally, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/8429shishir/Real-Estate-Price-Prediction-and-Recommendation-System.git
   cd Real-Estate-Price-Prediction-and-Recommendation-System
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**
   *(Ensure you have a `requirements.txt` file in your repository)*
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Application**
   ```bash
   streamlit run Home.py
   ```

## 👨‍💻 Author

**Shishir Singh**
- **Institution:** IIT Bhubaneswar (School of Electrical & Computer Sciences)
- **GitHub:** [@8429shishir](https://github.com/8429shishir)
- **LinkedIn:** [Shishir Singh](https://www.linkedin.com/in/shishir-singh)

---

*This project is a Data Science Capstone showcasing real-world application of machine learning in the real estate domain.*
