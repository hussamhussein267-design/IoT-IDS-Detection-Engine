# IoT-IDS-Detection-Engine

## 📊 Project Overview

**IoT Intrusion Detection System** Detection Engine - A comprehensive solution for real-time detection of cyber attacks and anomalies in IoT networks using signature-based rules, machine learning ensembles, and hybrid detection methods.

This project implements a complete detection pipeline for identifying intrusions in IoT systems using advanced detection techniques, trained models from the **IoT-IDS-ML-Pipeline**, and the **CICIoT2023** dataset.

---

## 🎯 Project Objectives

- **Signature Detection**: Match traffic against predefined high-confidence rules for known attacks
- **Hybrid Detection**: Combine ML ensemble predictions with signature rules for balanced accuracy
- **Real-Time Simulation**: Stream IoT traffic and evaluate detection latency
- **Integration**: Seamlessly use trained models from ML-Pipeline
- **Output Analysis**: Generate detection logs, alerts, and performance metrics

---

## 📁 Project Structure

```
IoT-IDS-Detection-Engine/
├── 04_signature_based.py       # Signature-based detection rules
├── 05_hybrid_detection.py      # Hybrid IDS (ML + Signature)
├── 06_realtime_simulation.py   # Real-time traffic simulation
├── models/                     # Pre-trained models (from ML-Pipeline)
├── outputs/                    # Detection results & logs
└── README.md                   # Documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### 2. Installation

Clone the repository:
```bash
git clone https://github.com/hussamhussein267-design/IoT-IDS-Detection-Engine.git
cd IoT-IDS-Detection-Engine
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Import Models

Copy trained models from IoT-IDS-ML-Pipeline into this repository:
```bash
cp -r ../IoT-IDS-ML-Pipeline/models/* ./models/
```

Or manually download models from:
```
IoT-IDS-ML-Pipeline/models/
├── Logistic_Regression.pkl
├── Random_Forest.pkl
└── Gradient_Boosting.pkl
```

### 4. Run Detection

**Step 1: Signature-Based Detection**
```bash
python 04_signature_based.py
```
This will:
- Load predefined attack signatures
- Process network flows
- Generate detection alerts
- Save results in outputs/

**Step 2: Hybrid Detection**
```bash
python 05_hybrid_detection.py
```
This will:
- Load trained ML models
- Apply signature rules
- Combine predictions using weighted ensemble
- Generate hybrid detection reports

**Step 3: Real-Time Simulation**
```bash
python 06_realtime_simulation.py
```
This will:
- Simulate IoT network traffic streams
- Measure detection latency
- Generate performance statistics
- Output real-time alerts

---

## 📊 Dataset Information

**CICIoT2023 Dataset**
- Size: ~600 GB (full dataset)
- Records: ~7.8M flows (detection subset)
- Features: 46 features per flow
- Classes: 34 attack types + benign traffic
- Time Period: June 2023
- Source: University of New Brunswick (UNB)

👉 [Download CICIoT2023 Dataset](https://www.unb.ca/cic/datasets/iotdataset-2023.html)

---

## 🔄 Detection Workflow

```
Network Traffic Input
        ↓
Signature-Based Rules → Instant detection (~0.01ms)
        ↓
ML Ensemble Prediction → XGBoost 50%, RF 30%, DT 20%
        ↓
Hybrid Decision Engine → Combine both approaches
        ↓
Real-Time Alert Generation → Severity classification
        ↓
Detection Logs & Outputs
```

---

## 📈 Detection Performance

Expected detection performance on CICIoT2023 dataset:

| Detection Method | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Signature-Based | ~88% | ~90% | ~87% | ~88% |
| Hybrid (ML Only) | ~97% | ~97% | ~97% | ~97% |
| Hybrid (Combined) | ~98% | ~98% | ~98% | ~98% |

---

## 📊 Outputs

After running detection, you'll find:

- `outputs/detection_logs.csv` - Alert logs with timestamps and severity
- `outputs/performance_metrics.json` - Accuracy, precision, recall, F1-score
- `outputs/latency_measurements.csv` - Real-time detection latency metrics
- `outputs/attack_classification.png` - Attack type distribution chart
- `outputs/alerts_timeline.png` - Alert timeline visualization

---

## 🛠️ Technologies Used

- **Python 3.8+**: Programming language
- **Scikit-learn**: Machine learning algorithms
- **XGBoost**: Gradient boosting framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib & Seaborn**: Data visualization
- **Flask**: Web integration for dashboard

---

## 📝 File Descriptions

### 04_signature_based.py
Implements signature-based detection rules:
- Loads predefined attack signatures
- Matches network flows against signatures
- Generates immediate detection alerts
- Fast detection (~0.01ms per flow)
- Ideal for known attack patterns

### 05_hybrid_detection.py
Combines ML ensemble with signature detection:
- Loads trained models from models/ folder
- Applies weighted ensemble voting (XGBoost 50%, RF 30%, DT 20%)
- Integrates signature rule results
- Balances accuracy vs. computational efficiency
- Generates comprehensive detection reports

### 06_realtime_simulation.py
Simulates real-time IoT traffic streams:
- Generates or streams IoT network flows
- Applies detection methods in real-time
- Measures detection latency (~52ms average)
- Outputs alerts with severity levels
- Generates performance statistics

---

## 🔐 Security Considerations

This project is designed for:

✅ Research and educational purposes
✅ Cybersecurity analysis
✅ IoT network intrusion detection
✅ Real-time threat monitoring and alerting

**Security Best Practices:**
- Signature rules ensure instant detection of known attacks
- Hybrid detection balances accuracy vs. computational efficiency
- Detection logs secured and restricted to authorized administrators
- Models updated regularly with new threat intelligence
- Compliance with IoT security standards

---

## 📚 References

- [IoT-IDS-ML-Pipeline](https://github.com/hussamhussein267-design/IoT-IDS-ML-Pipeline) – Training models repository
- [CICIoT2023 Dataset](https://www.unb.ca/cic/datasets/iotdataset-2023.html)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

## 👨‍💻 Author

**Hussam Hussein**

GitHub: [@hussamhussein267-design](https://github.com/hussamhussein267-design)
Email: hussamhussein267@gmail.com

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Contact the author directly
- Check existing documentation

---

## 🎓 Learning Resources

- [Intrusion Detection Systems](https://en.wikipedia.org/wiki/Intrusion_detection_system)
- [IoT Security Best Practices](https://www.nist.gov/publications/framework-securing-internet-things)
- [Machine Learning for Cybersecurity](https://www.coursera.org/learn/machine-learning)
- [Network Traffic Analysis](https://www.wireshark.org/docs/)

---

**Last Updated:** May 2026 | **Status:** ✅ Active Development
