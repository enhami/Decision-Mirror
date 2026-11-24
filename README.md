# 🔍Decision-Mirror
**Understand how reliable your machine learning decisions really are.**

DecisionMirror is an interactive AI/ML model reliability and sensitivity analysis tool built with Python, Streamlit, and Scikit-learn. Instead of stopping at a single accuracy score, it lets users stress-test individual predictions, detect exact decision boundaries, and measure which input features make a model flip its decisions.

## 🚀 Key Features
- **Dataset Upload & Inspection:** Upload any tabular CSV dataset to inspect rows, columns, data types, and missing values automatically. *(Includes `train.csv` from the classic Kaggle Titanic dataset for instant testing).*
- **Automated Model Training:** Builds a complete Scikit-learn preprocessing pipeline (median/mode imputation + One-Hot Encoding) and trains a Random Forest classifier with accuracy metrics and a confusion matrix.
- **Automated Decision Flip Lab:** Sweeps a chosen numeric feature across 21+ values to detect whether and where the model's prediction flips, pinpointing approximate **decision boundaries**.
- **Feature Sensitivity Comparison:** Compares flip rates across all numerical features simultaneously to reveal which inputs influence decision stability the most.

## 🛠️ Tech Stack
- **Frontend & UI:** Streamlit, Custom CSS
- **Machine Learning:** Scikit-learn (`RandomForestClassifier`, `ColumnTransformer`, `Pipeline`)
- **Data Processing:** Pandas, NumPy

## 💻 Run Locally
```bash
git clone https://github.com
cd Decision-Mirror
pip install -r requirements.txt
streamlit run app.py
```

## ⚠️ Scope & Limitations
DecisionMirror currently evaluates **input sensitivity and local decision stability**. A low flip rate shows stability against single-feature perturbations, but does not by itself guarantee real-world fairness or absence of dataset bias.
