📌 Project Overview
The IoT-IDS-Detection-Engine repository implements the real-time detection engine for IoT Intrusion Detection Systems.
It combines signature-based detection with machine learning ensemble models (trained in the ML-Pipeline repository) to provide a hybrid IDS capable of detecting both known and unknown attacks in IoT networks.

🎯 Project Objectives
Signature Detection → Match traffic patterns against predefined high-confidence rules.

Hybrid Detection → Combine ML ensemble predictions with signature rules for balanced accuracy.

Real-Time Simulation → Stream IoT traffic and evaluate detection latency.

Integration → Use trained models from ML-Pipeline repository.

Output Analysis → Generate detection logs, alerts, and performance metrics.

📂 Project Structure
Code
IoT-IDS-Detection-Engine/
├── 04_signature_based.py       # Signature-based detection rules
├── 05_hybrid_detection.py      # Hybrid IDS (ML + Signature)
├── 06_realtime_simulation.py   # Real-time traffic simulation
├── models/                     # Pre-trained models (from ML-Pipeline)
├── outputs/                    # Detection results & logs
└── README.md                   # Documentation
🚀 Quick Start
1. Prerequisites
Python 3.8+

pip (Python package manager)

Git

2. Installation
Clone the repository:

bash
git clone https://github.com/hussamhussein267-design/IoT-IDS-Detection-Engine.git
cd IoT-IDS-Detection-Engine
Install dependencies:

bash
pip install -r requirements.txt
3. Import Models
Copy trained models from IoT-IDS-ML-Pipeline/models/ into this repository’s models/ folder.

⚙️ Usage
Step 1: Signature-Based Detection
bash
python 04_signature_based.py
Detects known attacks using predefined rules.

Latency: ~0.01ms per packet.

Step 2: Hybrid Detection
bash
python 05_hybrid_detection.py
Combines ML ensemble (XGBoost 50%, Random Forest 30%, Decision Tree 20%) with signature rules.

Accuracy: ~86.63% on CICIoT2023 dataset.

Step 3: Real-Time Simulation
bash
python 06_realtime_simulation.py
Streams IoT traffic (e.g., 100 packets).

Measures detection latency (~52ms for ML ensemble).

Generates detection logs in outputs/.

📊 Outputs
Detection logs (alerts, timestamps, severity).

Performance metrics (accuracy, precision, recall, F1-score).

Real-time latency measurements.

🔐 Security Considerations
Signature rules ensure instant detection of high-confidence attacks.

Hybrid detection balances accuracy vs. computational efficiency.

Logs are secured and restricted to authorized administrators.

📚 References
IoT-IDS-ML-Pipeline – Training models repository.

CICIoT2023 Dataset: Download here.

Scikit-learn Documentation: https://scikit-learn.org/

XGBoost Documentation: https://xgboost.readthedocs.io/

👨‍💻 Author
Hussam Hussein
GitHub: @hussamhussein267-design
Email: hussamhussein267@gmail.com
