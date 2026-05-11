🎯 Project Objectives
Signature Detection → Match traffic against predefined high-confidence rules.

Hybrid Detection → Combine ML ensemble predictions with signature rules for balanced accuracy.

Real-Time Simulation → Stream IoT traffic and evaluate detection latency.

Integration → Use trained models from ML-Pipeline.

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

pip

Git

2. Installation
bash
git clone https://github.com/hussamhussein267-design/IoT-IDS-Detection-Engine.git
cd IoT-IDS-Detection-Engine
pip install -r requirements.txt
3. Import Models
Copy trained models from IoT-IDS-ML-Pipeline/models/ into this repository’s models/ folder.

4. Run Detection
Signature-Based Detection

bash
python 04_signature_based.py
Hybrid Detection

bash
python 05_hybrid_detection.py
Real-Time Simulation

bash
python 06_realtime_simulation.py
📊 Dataset Information
Dataset: CICIoT2023

Records: 7.8M flows

Features: 46 per flow

Attacks: 34 types + benign traffic
👉 Download: CICIoT2023 Dataset

🔄 Detection Workflow
Signature-Based Rules → Instant detection (~0.01ms).

Hybrid IDS → Weighted Ensemble (XGBoost 50%, RF 30%, DT 20%).

Real-Time Simulation → Stream traffic, measure latency (~52ms).

📈 Outputs
Detection logs (alerts, timestamps, severity).

Performance metrics (accuracy, precision, recall, F1-score).

Real-time latency measurements.

🔐 Security Considerations
Signature rules ensure instant detection of known attacks.

Hybrid detection balances accuracy vs. computational efficiency.

Logs secured and restricted to authorized administrators.

🛠️ Technologies Used
Python 3.8+

Scikit-learn, XGBoost

Pandas, NumPy

Matplotlib

Flask (for integration with dashboard)

📝 File Descriptions
04_signature_based.py → Implements signature rules for known attacks.

05_hybrid_detection.py → Combines ML ensemble with signature detection.

06_realtime_simulation.py → Simulates IoT traffic and measures detection latency.

📚 References
IoT-IDS-ML-Pipeline – Training models repository.

CICIoT2023 Dataset: Download here

Scikit-learn Documentation: https://scikit-learn.org/

XGBoost Documentation: https://xgboost.readthedocs.io/

👨‍💻 Author
Hussam Hussein
GitHub: @hussamhussein267-design
Email: hussamhussein267@gmail.com

📄 License
MIT License – see LICENSE file for details.

🤝 Contributing
Fork the repository

Create a feature branch

Commit changes

Push to branch

Open a Pull Request

📞 Support
Open an issue on GitHub

Contact author: hussamhussein267@gmail.com
