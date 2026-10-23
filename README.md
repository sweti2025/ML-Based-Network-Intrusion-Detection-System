 <div align="center">

<img src=Neon Cybersecurity README Dashboard.png" alt="ML-Based Network Intrusion Detection System Banner" width="100%">

# 🛡️ ML-Based Network Intrusion Detection System

### Intelligent Network Traffic Classification Using Machine Learning

**Random Forest · Python · Streamlit · Cybersecurity**

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/ML-Random%20Forest-00C7B7?style=for-the-badge" alt="Random Forest">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-163A5F?style=for-the-badge" alt="Cybersecurity">
</p>

**Analyze • Predict • Visualize • Export**

[View Repository](https://github.com/sweti2025/ML-Based-Network-Intrusion-Detection-System)

</div>

---

## 🔍 Project Overview

The **ML-Based Network Intrusion Detection System** is a machine-learning project designed to classify network traffic records as **Benign** or **Potential Attack**.

The system uses a trained **Random Forest classifier** and a modern Streamlit dashboard to analyze uploaded network-flow CSV files, summarize predictions, visualize traffic patterns, and export prediction results.

Developed as an academic cybersecurity project, it demonstrates how machine learning can support network traffic analysis and intrusion detection research.

## ✨ Key Features

- 📂 **CSV Upload:** Upload compatible network traffic datasets.
- 🧠 **Machine Learning:** Classify network-flow records using a trained Random Forest model.
- 📊 **Threat Overview:** Display total records, predicted attacks, and benign predictions.
- 📈 **Interactive Visualizations:** Explore traffic distribution and attack probability scores.
- 🔎 **Prediction Explorer:** Inspect and filter prediction results.
- 📥 **CSV Export:** Download the complete prediction report.
- 🌌 **Modern Dashboard:** Dark cybersecurity interface with neon accents and metric cards.
- ⚙️ **Saved Model Inference:** Load pre-trained model artifacts without retraining every time.

## 🖥️ Dashboard Preview

<!-- If your dashboard screenshot is in the repository root, change the filename below to its exact name. -->
<p align="center">
  <img src="dashboard.png" alt="Network Intrusion Detection Streamlit Dashboard" width="100%">
</p>

*The dashboard analyzes uploaded CSV records. Displayed attack counts are model predictions, not verified security incidents.*

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas & NumPy | Data processing |
| Scikit-learn | Machine-learning implementation |
| Random Forest | Classification algorithm |
| Joblib | Model artifact loading |
| Streamlit | Interactive web dashboard |
| Plotly | Data visualization |
| Google Colab / Jupyter | Model development |
| Git & GitHub | Version control and project hosting |

## 📚 Dataset

This project uses the **CIC-IDS2017** network intrusion detection dataset.

- **Dataset:** CIC-IDS2017
- **File used:** `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- **Records in the uploaded file:** 191,033
- **Columns reported during development:** 79
- **Observed original labels:** `BENIGN` and `Bot`

🔗 **Official dataset:** [Canadian Institute for Cybersecurity — CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)

### Binary Classification

The training experiment maps labels as follows:

| Encoded label | Meaning |
|---|---|
| `0` | BENIGN |
| `1` | Non-BENIGN / ATTACK |

The inspected dataset contained BENIGN and Bot labels. Therefore, the current experiment should not be interpreted as covering every possible type of network attack.

## 🏗️ System Architecture

```text
      Network Traffic CSV
               │
               ▼
       Feature Validation
               │
               ▼
      Numeric Preprocessing
       (NaN / Inf Handling)
               │
               ▼
     Trained Random Forest
               │
               ▼
      Binary Classification
       ┌───────┴────────┐
       ▼                ▼
     Benign           Attack
       └───────┬────────┘
               ▼
      Streamlit Dashboard
               │
       ┌───────┼─────────┐
       ▼       ▼         ▼
    Metrics  Charts   CSV Report
```

## 📊 Model Evaluation

The following metrics are from the recorded test-set evaluation output.

### Test Results

| Metric | ATTACK Class | Macro Average |
|---|---:|---:|
| Precision | 1.00 | 1.00 |
| Recall | 0.92 | 0.96 |
| F1-score | 0.96 | 0.98 |
| Support | 99 | 10,000 total records |

### Accuracy

**Test Accuracy: 99.92%**

The measured accuracy was `0.9992` on the recorded test split.

### Confusion Matrix

| Actual / Predicted | Predicted Benign | Predicted Attack |
|---|---:|---:|
| Actual Benign | 9,901 | 0 |
| Actual Attack | 8 | 91 |

| Result | Value |
|---|---:|
| True Negatives (TN) | 9,901 |
| False Positives (FP) | 0 |
| False Negatives (FN) | 8 |
| True Positives (TP) | 91 |

### Interpretation

The model correctly identified 91 out of 99 ATTACK-class test records and missed 8. Although the recorded accuracy is high, accuracy alone is not sufficient for evaluating an intrusion detection system. Class imbalance, recall, false negatives, and performance on new datasets must also be considered.

*Note: Precision, recall, and F1-score are rounded to two decimal places. These test-set metrics are separate from the predictions shown for a newly uploaded dashboard CSV.*

## 📁 Project Structure

```text
ML-Based-Network-Intrusion-Detection-System/
│
├── app.py
├── requirements.txt
├── intrusion_model.joblib
├── feature_names.joblib
├── ML-Based Network Intrusion Detection System.ipynb
├── Project-Report.pdf
├── README.md
├── github-banner.png
└── dashboard.png
```

*Update the notebook and PDF filenames above if yours are different. The image paths must match the actual filenames in your repository.*

## 🚀 Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/sweti2025/ML-Based-Network-Intrusion-Detection-System.git
cd ML-Based-Network-Intrusion-Detection-System
```

### 2. Create a virtual environment (recommended)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`, and upload a compatible network traffic CSV.

### Required Model Files

Ensure both model artifacts are in the same directory as `app.py`:

- `intrusion_model.joblib`
- `feature_names.joblib`

The uploaded CSV must contain all feature columns expected by the trained model.

## ⚙️ How It Works

1. The user uploads a network traffic CSV.
2. The application validates the required feature columns.
3. Feature values are converted to numeric format, and missing or infinite values are handled.
4. The trained Random Forest model predicts a class for each record.
5. The dashboard calculates prediction summaries and displays visualizations.
6. Users inspect individual results and download the complete CSV prediction report.

## ⚠️ Limitations

- This is an **academic and educational prototype**, not a production-grade security system.
- The application analyzes uploaded CSV files; it does not monitor live network packets.
- It does not block attacks or automatically respond to incidents.
- Predictions depend on the training data, feature compatibility, and class distribution.
- The observed dataset labels do not establish coverage of every possible attack category.
- Model probability scores are not necessarily calibrated real-world risk estimates.
- Test-set performance does not guarantee equivalent results on unseen or real-world traffic.

## 🔮 Future Improvements

- Evaluate the model on additional datasets and CIC-IDS2017 traffic captures.
- Extend classification to multiple attack categories.
- Improve evaluation for imbalanced classes.
- Add precision-recall curves and per-class performance reporting.
- Explore explainable AI methods such as feature importance and SHAP.
- Investigate safe live-traffic integration and monitoring as a separate future development.
- Add data-drift checks and more robust validation for large input files.

## 📄 Project Report

The final academic project report is available in this repository as `Project-Report.pdf`, provided that the report file has been uploaded.

## 👩‍💻 Author

**Sweti Yadav**

B.Tech — Computer Science & Engineering (Artificial Intelligence & Machine Learning)

GitHub: [@sweti2025](https://github.com/sweti2025)

## ⚖️ Disclaimer

This project is intended for academic and educational purposes only. It is not a substitute for professional security monitoring, incident response, or a validated production intrusion detection system.

---

<div align="center">

**Built with Python, Machine Learning, and Streamlit.**

⭐ If you find this project useful, consider giving the repository a star.

</div>
