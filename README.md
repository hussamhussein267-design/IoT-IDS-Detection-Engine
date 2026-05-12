# 🚨 IoT-IDS-System

**Complete IoT Intrusion Detection System** - A comprehensive, end-to-end machine learning pipeline for detecting cyber attacks and anomalies in IoT networks. This system includes data exploration, feature engineering, model training, signature-based detection, hybrid detection, and real-time monitoring.

---

## 📌 Project Overview

The **IoT-IDS-System** is a unified solution for IoT network security that combines:
- 🔬 **ML Pipeline** - Training models using the CICIOT23 dataset
- 🛡️ **Detection Engine** - Real-time anomaly detection using ML + signature rules
- 📊 **Dashboard** - Web-based visualization and alert management

**Complete Workflow:**
CICIOT23 Dataset ↓ Data Exploration & Feature Engineering ↓ ML Model Training (3 models) ↓ Signature-Based + Hybrid Detection ↓ Real-Time Alert Simulation ↓ Web Dashboard Visualization

Code

---

## 🎯 Project Objectives

| Objective | Description |
|-----------|-------------|
| **Data Analysis** | Explore and understand IoT network traffic patterns |
| **Feature Engineering** | Extract and select the 20 most relevant features |
| **Model Training** | Build and compare multiple ML classification models |
| **Signature Detection** | Detect known attacks using predefined rules |
| **Hybrid Detection** | Combine ML predictions with signature-based rules |
| **Real-Time Detection** | Simulate and detect attacks in real-time streams |
| **Alert Management** | Notify and visualize detected anomalies |
| **Explainability** | Explain why attacks were detected |

---

## 📂 Project Structure

IoT-IDS-System/ │ ├── 📊 ML Pipeline (Training) │ ├── 01_data_exploration.py # Dataset analysis & visualization │ ├── 02_feature_selection.py # Feature engineering & selection │ └── 03_train_models.py # Model training & evaluation │ ├── 🛡️ Detection Engine │ ├── 04_signature_based.py # Signature-based detection rules │ ├── 05_hybrid_detection.py # Hybrid IDS (ML + Signature) │ └── 06_realtime_simulation.py # Real-time traffic simulation │ ├── 📈 Dashboard & Web Interface │ ├── 07_dashboard.py # Flask-based web dashboard │ ├── templates/ # HTML templates (Jinja2) │ │ ├── index.html │ │ ├── alerts.html │ │ ├── statistics.html │ │ └── explainability.html │ └── static/ # CSS, JS, Chart.js assets │ ├── css/ │ ├── js/ │ └── assets/ │ ├── 🤖 Models & Data │ ├── models/ # Pre-trained ML models (.pkl) │ │ ├── ensemble_model.pkl │ │ ├── random_forest.pkl │ │ ├── gradient_boosting.pkl │ │ ├── scaler.pkl │ │ └── label_encoder.pkl │ ├── data/ # Dataset location │ │ └── CICIOT23_Dataset_*.csv │ └── outputs/ # Results & visualizations │ ├── alerts_timeline.png │ ├── attack_statistics.png │ ├── severity_classification.json │ ├── detection_logs.csv │ └── performance_metrics.json │ ├── requirements.txt # Python dependencies ├── config.py # Configuration settings ├── .env.example # Environment variables template ├── utils.py # Helper functions └── README.md # This file

Code

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**
- **4GB+ RAM** (for model training)
- **Modern web browser** (for dashboard)

### 2. Installation

**Clone the repository:**
```bash
git clone https://github.com/hussamhussein267-design/IoT-IDS-System.git
cd IoT-IDS-System
Install dependencies:

bash
pip install -r requirements.txt
Setup environment variables:

bash
cp .env.example .env
nano .env  # Edit with your settings
3. Download Dataset
Download the CICIOT23 dataset from:

Code
https://www.unb.ca/cic/datasets/iotdataset-2023.html
Extract and place in data/ folder:

Code
data/
├── CICIOT23_Dataset_*.csv
└── ...
4. Run Complete Pipeline
Phase 1: Data Exploration & Model Training
bash
# Step 1: Explore data
python 01_data_exploration.py
# Output: Data statistics, class distribution, feature analysis

# Step 2: Feature selection
python 02_feature_selection.py
# Output: Top 20 features, processed dataset

# Step 3: Train models
python 03_train_models.py
# Output: 3 trained models saved to models/
Phase 2: Detection Engine
bash
# Step 4: Signature-based detection
python 04_signature_based.py
# Output: Attack detection using predefined rules

# Step 5: Hybrid detection
python 05_hybrid_detection.py
# Output: ML + Signature combined detection

# Step 6: Real-time simulation
python 06_realtime_simulation.py
# Output: Real-time detection latency & alerts
Phase 3: Web Dashboard
bash
# Step 7: Run dashboard
python 07_dashboard.py
# Access at: http://127.0.0.1:5000/
📊 Dataset Information
CICIOT23 Dataset

Size: ~600 GB (full dataset available)
Records: ~7.8M network flows (detection subset)
Features: 46 network traffic features
Attack Classes: 34 attack types + benign traffic
DDoS attacks
Scanning attacks
Spoofing attacks
Backdoor attacks
And more...
Time Period: June 2023
Source: University of New Brunswick (UNB)
📥 Download CICIOT23 Dataset

📈 Model Performance
ML Training Results
Model	Accuracy	Precision	Recall	F1-Score	Training Time
Logistic Regression	~92%	~91%	~92%	~91%	~5 min
Random Forest	~96%	~96%	~96%	~96%	~15 min
Gradient Boosting	~97%	~97%	~97%	~97%	~20 min
Detection Engine Results
Detection Method	Accuracy	Precision	Recall	F1-Score	Latency
Signature-Based	~88%	~90%	~87%	~88%	~0.01ms
Hybrid (Combined)	~98%	~98%	~98%	~98%	~52ms
🛠️ Technologies Used
Backend
Python 3.8+ - Core programming language
Flask - Web framework
scikit-learn - ML algorithms
XGBoost - Gradient boosting
Pandas - Data manipulation
NumPy - Numerical computing
Frontend
HTML5 - Markup
CSS3 - Styling
JavaScript (ES6+) - Interactivity
Chart.js - Visualizations
Bootstrap 5 - Responsive design
Data Visualization
Matplotlib - Static plots
Seaborn - Statistical graphics
Chart.js - Interactive dashboards
📝 Phase 1: ML Pipeline
01_data_exploration.py
Explores and analyzes the CICIOT23 dataset:

Load and inspect dataset structure
Generate descriptive statistics
Identify missing values and outliers
Create class distribution visualizations
Analyze feature distributions
Export statistical summaries
Output: outputs/class_distribution.png, statistical reports

02_feature_selection.py
Prepares and engineers features:

Handle missing values and outliers
Encode categorical variables
Scale numerical features (StandardScaler)
Select top 20 features using SelectKBest
Save processed dataset for modeling
Generate feature importance plots
Output: outputs/feature_importance.png, processed CSV

03_train_models.py
Trains and evaluates ML models:

Split data into train/test (80/20)
Train 3 classification models:
Logistic Regression
Random Forest (100 trees)
Gradient Boosting
Generate classification reports
Compare model performance
Save trained models as .pkl files
Output: models/*.pkl, outputs/performance_metrics.json

🛡️ Phase 2: Detection Engine
04_signature_based.py
Implements signature-based detection:

Load predefined attack signatures
Match network flows against signatures
Generate detection alerts with severity
Fast detection (~0.01ms per flow)
Ideal for known attack patterns
Output: outputs/signature_detections.csv

05_hybrid_detection.py
Combines ML ensemble with signature rules:

Load trained models from models/ folder
Apply ML predictions on test data
Weight ensemble voting:
Gradient Boosting: 50%
Random Forest: 30%
Logistic Regression: 20%
Integrate signature rule results
Combine predictions using weighted voting
Generate comprehensive detection reports
Output: outputs/hybrid_detection_results.csv, performance metrics

06_realtime_simulation.py
Simulates real-time IoT traffic streams:

Generate or stream IoT network flows
Apply detection methods in real-time
Measure detection latency
Classify severity levels (Low, Medium, High, Critical)
Generate real-time alerts
Output performance statistics
Output: outputs/realtime_alerts.csv, outputs/latency_measurements.csv

📊 Phase 3: Dashboard
[IoT-IDS-Dashboard](https://github.com/USERNAME/IoT-IDS-Dashboard)
07_dashboard.py
Flask-based web dashboard:

Real-time alert visualization
Live attack statistics
Severity classification displays
ML decision explainability
Interactive Chart.js visualizations
REST API endpoints for data
Features:

✅ Real-time traffic monitoring
✅ Attack type distribution
✅ Severity level indicators
✅ Alert notifications (sound + toast)
✅ Feature importance charts
✅ Event logging
Access: http://127.0.0.1:5000/

📈 Output Artifacts
After running the complete pipeline, you'll find:

Code
outputs/
├── class_distribution.png              # Attack type distribution
├── feature_importance.png              # Feature importance plot
├── attacks_timeline.png                # Alert timeline
├── severity_classification.png         # Severity distribution
├── performance_metrics.json            # Model performance metrics
├── detection_logs.csv                  # All detection events
├── alerts_timeline.csv                 # Alert timestamps & severity
├── latency_measurements.csv            # Detection latency data
└── attack_statistics.json              # Detailed attack statistics
🔐 Security Considerations
Access Control
✅ Dashboard access restricted to authorized users
✅ Role-based access control (Admin, Analyst, Viewer)
✅ Session timeout after 15 minutes inactivity
Data Protection
✅ HTTPS enforcement (in production)
✅ Secure log storage with restricted access
✅ Sensitive data masked in UI (API keys, credentials)
✅ SQL injection prevention via parameterized queries
API Security
✅ API key authentication for endpoints
✅ Rate limiting (100 requests/minute)
✅ CORS policy configuration
✅ Input validation on all endpoints
Compliance
✅ Audit logging of all activities
✅ GDPR-compliant data retention
✅ Compliance with IoT security standards (NIST, IEC 62443)
📚 API Reference
Dashboard Endpoints
Code
GET /
  → Main dashboard page

GET /api/alerts?limit=50&status=open
  → Fetch recent alerts (JSON)

GET /api/statistics?timerange=24h
  → Attack statistics

POST /api/predict
  → Real-time traffic prediction
  Input: {"features": [...]}
  Output: {"prediction": 1, "confidence": 0.92, "severity": "High"}

GET /api/models/info
  → Model metadata and performance
🐛 Troubleshooting
Port already in use
bash
python 07_dashboard.py --port 5001
CICIOT23 dataset not found
bash
# Check data folder
ls -la data/

# Download from:
# https://www.unb.ca/cic/datasets/iotdataset-2023.html
Models not loading
bash
# Check models folder
ls -la models/

# Ensure models exist from 03_train_models.py
python 03_train_models.py
Dashboard Chart not rendering
Code
Clear browser cache: Ctrl+Shift+Delete
Refresh page: F5 or Ctrl+R
Memory issues during training
bash
# Reduce batch size in 03_train_models.py
# Or process smaller dataset subset
👨‍💻 Author
Hussam Hussein

🌐 GitHub: @hussamhussein267-design
📧 Email: hussamhussein267@gmail.com
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Code
MIT License

Copyright (c) 2026 Hussam Hussein

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
🤝 Contributing
Contributions are welcome! Follow these steps:

Fork the repository

bash
git clone https://github.com/YOUR-USERNAME/IoT-IDS-System.git
Create a feature branch

bash
git checkout -b feature/your-feature-name
Commit your changes

bash
git commit -m "Add: Description of your changes"
Push to the branch

bash
git push origin feature/your-feature-name
Open a Pull Request

Code Standards
Follow PEP 8 for Python code
Use meaningful variable names
Add docstrings to functions
Include comments for complex logic
Write unit tests for new features
📞 Support & Help
Get Assistance
📝 Open an issue on GitHub Issues
💬 Start a discussion on GitHub Discussions
📧 Email: hussamhussein267@gmail.com
Related Resources
📊 CICIOT23 Dataset
🔬 scikit-learn Documentation
📚 Flask Documentation
📖 Chart.js Documentation
🎓 Learning Resources
Intrusion Detection Systems
IoT Security Best Practices - NIST
Machine Learning for Cybersecurity - Coursera
Network Traffic Analysis - Wireshark
Feature Engineering in ML
📊 Project Status
Component	Status	Version	Last Updated
🔬 ML Pipeline	✅ Complete	v1.0.0	2026-05-11
🛡️ Detection Engine	✅ Complete	v1.0.0	2026-05-11
📊 Dashboard	✅ Complete	v1.0.0	2026-05-11
📚 Documentation	✅ Complete	v1.0.0	2026-05-11
🧪 Testing	🔄 In Progress	-	-
🔐 Security Audit	🔄 In Progress	-	-
🙏 Acknowledgments
University of New Brunswick for the CICIOT23 dataset
scikit-learn community for ML libraries
Flask framework for web development
Chart.js for interactive visualizations
All contributors and users providing feedback
Made with ❤️ by Hussam Hussein

⭐ If this project helps you, please consider giving it a star on GitHub!

Code
🚀 Quick Commands:
python 01_data_exploration.py       # Explore data
python 02_feature_selection.py      # Select features
python 03_train_models.py           # Train models
python 04_signature_based.py        # Detect signatures
python 05_hybrid_detection.py       # Hybrid detection
python 06_realtime_simulation.py    # Real-time alerts
python 07_dashboard.py              # Launch dashboard → http://127.0.0.1:5000
