# ============================================================
# Script 06: Real-Time IoT Intrusion Detection Simulation
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# ============================================================

import pandas as pd
import numpy as np
import pickle
import os
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. PATHS
# ============================================================
BASE_DIR   = r"C:\Users\cm\IoT-IDS-System"
TEST_CSV   = os.path.join(BASE_DIR, "CICIOT23", "test", "test.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ============================================================
# 2. تحميل الموديلات
# ============================================================
print("=" * 60)
print("🚀 Real-Time IoT IDS - Loading System...")
print("=" * 60)

with open(os.path.join(MODELS_DIR, "xgboost.pkl"), "rb") as f:
    xgb_model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "random_forest.pkl"), "rb") as f:
    rf_model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "decision_tree.pkl"), "rb") as f:
    dt_model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "label_encoder.pkl"), "rb") as f:
    le = pickle.load(f)

with open(os.path.join(MODELS_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

with open(os.path.join(MODELS_DIR, "selected_features.pkl"), "rb") as f:
    selected_features = pickle.load(f)

print("✅ All models loaded successfully!")
print(f"✅ Monitoring {len(le.classes_)} attack types")

# ============================================================
# 3. Signature Rules (High-Confidence Only)
# ============================================================
def signature_check(record):
    """فحص سريع بالـ Signature rules"""
    if record.get('ICMP', 0) == 1 and record.get('Rate', 0) > 500:
        return 'DDoS-ICMP_Flood'
    if record.get('psh_flag_number', 0) > 500 and record.get('ack_flag_number', 0) > 500:
        return 'DDoS-PSHACK_Flood'
    if record.get('rst_flag_number', 0) > 500 and record.get('fin_flag_number', 0) > 500:
        return 'DDoS-RSTFINFlood'
    if record.get('syn_count', 0) > 500 and record.get('Rate', 0) > 500:
        return 'DDoS-SYN_Flood'
    if record.get('UDP', 0) == 1 and record.get('Std', 0) == 0 and record.get('Rate', 0) > 100:
        return 'Mirai-udpplain'
    if record.get('ARP', 0) == 1 and record.get('Variance', 0) > 10000:
        return 'MITM-ArpSpoofing'
    return None

# ============================================================
# 4. Hybrid Detection Function
# ============================================================
def hybrid_detect(record_dict):
    """
    Real-time hybrid detection لـ record واحد
    1. Signature check أولاً (سريع)
    2. لو مش متأكد → ML Ensemble
    """
    # Step 1: Signature check
    sig_result = signature_check(record_dict)
    if sig_result:
        return sig_result, 'Signature', 1.0

    # Step 2: ML Ensemble
    record_df  = pd.DataFrame([record_dict])[selected_features]
    record_scaled = scaler.transform(record_df)

    xgb_proba = xgb_model.predict_proba(record_scaled)
    rf_proba  = rf_model.predict_proba(record_scaled)
    dt_proba  = dt_model.predict_proba(record_scaled)

    ensemble_proba = (xgb_proba * 0.5) + (rf_proba * 0.3) + (dt_proba * 0.2)
    pred_idx    = np.argmax(ensemble_proba)
    confidence  = ensemble_proba[0][pred_idx]
    pred_label  = le.inverse_transform([pred_idx])[0]

    return pred_label, 'ML-Ensemble', confidence

# ============================================================
# 5. Real-Time Simulation
# ============================================================
print("\n" + "=" * 60)
print("📡 Starting Real-Time Detection Simulation...")
print("=" * 60)

# تحميل الـ test data للـ simulation
print("⏳ Loading test data for simulation...")
test_df = pd.read_csv(TEST_CSV)
y_true  = test_df['label'].values

# نأخذ sample عشوائي 100 record للـ simulation
np.random.seed(42)
sample_idx = np.random.choice(len(test_df), size=100, replace=False)
sample_df  = test_df.iloc[sample_idx].reset_index(drop=True)
sample_true = y_true[sample_idx]

print(f"✅ Simulating {len(sample_df)} network packets in real-time...\n")
print("=" * 60)

# إحصائيات الـ simulation
total_packets  = 0
alerts         = 0
correct        = 0
detection_times = []

# ألوان في الـ terminal
ALERT  = "🚨 ALERT"
NORMAL = "✅ NORMAL"
WRONG  = "⚠️  MISSED"

for i in range(len(sample_df)):
    record = sample_df.iloc[i].to_dict()
    true_label = sample_true[i]

    # قياس وقت الـ detection
    start_time = time.time()
    pred_label, method, confidence = hybrid_detect(record)
    detect_time = (time.time() - start_time) * 1000  # milliseconds

    detection_times.append(detect_time)
    total_packets += 1

    is_attack = pred_label != 'BenignTraffic'
    is_correct = pred_label == true_label

    if is_correct:
        correct += 1

    if is_attack:
        alerts += 1
        status = ALERT
    else:
        status = NORMAL

    # طباعة كل 10 packets
    if i % 10 == 0:
        print(f"Packet #{i+1:3} | {status} | {pred_label:<30} | "
              f"Method: {method:<12} | Conf: {confidence:.2f} | "
              f"Time: {detect_time:.2f}ms")

print("\n" + "=" * 60)

# ============================================================
# 6. نتائج الـ Simulation
# ============================================================
print("📊 REAL-TIME SIMULATION RESULTS")
print("=" * 60)

accuracy     = correct / total_packets * 100
alert_rate   = alerts / total_packets * 100
avg_time     = np.mean(detection_times)
max_time     = np.max(detection_times)
min_time     = np.min(detection_times)

print(f"\n  Total Packets Analyzed:  {total_packets}")
print(f"  Attacks Detected:        {alerts} ({alert_rate:.1f}%)")
print(f"  Detection Accuracy:      {accuracy:.2f}%")
print(f"\n  ⏱️  Avg Detection Time:   {avg_time:.2f} ms per packet")
print(f"  ⏱️  Min Detection Time:   {min_time:.2f} ms")
print(f"  ⏱️  Max Detection Time:   {max_time:.2f} ms")
print(f"\n  🚀 Throughput:           {1000/avg_time:.0f} packets/second")

# ============================================================
# 7. توزيع الـ Alerts
# ============================================================
print("\n" + "=" * 60)
print("🔍 Attack Distribution in Simulation")
print("=" * 60)

predictions = []
for i in range(len(sample_df)):
    record = sample_df.iloc[i].to_dict()
    pred, _, _ = hybrid_detect(record)
    predictions.append(pred)

pred_series = pd.Series(predictions)
print(f"\n{'Attack Type':<35} {'Count':>6}")
print("-" * 45)
for attack, count in pred_series.value_counts().items():
    icon = "✅" if attack == 'BenignTraffic' else "🚨"
    print(f"{icon} {attack:<33} {count:>6}")

# ============================================================
# 8. حفظ النتائج
# ============================================================
results_path = os.path.join(OUTPUT_DIR, "06_realtime_results.txt")
with open(results_path, "w", encoding="utf-8") as f:
    f.write("IoT-IDS Real-Time Simulation Results\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total Packets:       {total_packets}\n")
    f.write(f"Attacks Detected:    {alerts} ({alert_rate:.1f}%)\n")
    f.write(f"Detection Accuracy:  {accuracy:.2f}%\n")
    f.write(f"Avg Detection Time:  {avg_time:.2f} ms\n")
    f.write(f"Min Detection Time:  {min_time:.2f} ms\n")
    f.write(f"Max Detection Time:  {max_time:.2f} ms\n")
    f.write(f"Throughput:          {1000/avg_time:.0f} packets/second\n\n")
    f.write("Attack Distribution:\n")
    for attack, count in pred_series.value_counts().items():
        f.write(f"  {attack:<35} {count}\n")

print(f"\n✅ Results saved: {results_path}")
print("\n" + "=" * 60)
print("🎉 Script 06 DONE! Ready for Script 07 (Dashboard)")
print("=" * 60)