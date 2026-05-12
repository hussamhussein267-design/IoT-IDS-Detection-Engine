# ============================================================
# Script 05: Hybrid Detection Engine
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# Hybrid = Anomaly (DT + RF + XGBoost) + Signature Rules
# ============================================================

import pandas as pd
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import (accuracy_score, f1_score,
                             precision_score, recall_score,
                             classification_report)

# ============================================================
# 1. PATHS
# ============================================================
BASE_DIR   = r"C:\Users\cm\IoT-IDS-System"
TEST_CSV   = os.path.join(BASE_DIR, "CICIOT23", "test", "test.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ============================================================
# 2. تحميل الموديلات والبيانات
# ============================================================
print("=" * 60)
print("📂 Loading models and data...")
print("=" * 60)

with open(os.path.join(MODELS_DIR, "decision_tree.pkl"), "rb") as f:
    dt_model = pickle.load(f)
print("✅ Decision Tree loaded")

with open(os.path.join(MODELS_DIR, "random_forest.pkl"), "rb") as f:
    rf_model = pickle.load(f)
print("✅ Random Forest loaded")

with open(os.path.join(MODELS_DIR, "xgboost.pkl"), "rb") as f:
    xgb_model = pickle.load(f)
print("✅ XGBoost loaded")

with open(os.path.join(MODELS_DIR, "label_encoder.pkl"), "rb") as f:
    le = pickle.load(f)

with open(os.path.join(MODELS_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

with open(os.path.join(MODELS_DIR, "selected_features.pkl"), "rb") as f:
    selected_features = pickle.load(f)

print("✅ LabelEncoder, Scaler, Features loaded")

print("\n⏳ Loading test data...")
test_df = pd.read_csv(TEST_CSV)
y_true  = test_df['label']
print(f"✅ Test loaded: {len(test_df):,} rows")

# ============================================================
# 3. تجهيز البيانات للـ ML
# ============================================================
X_test        = test_df[selected_features]
X_test_scaled = scaler.transform(X_test)

# ============================================================
# 4. Anomaly-based Predictions (الـ 3 موديلات)
# ============================================================
print("\n" + "=" * 60)
print("🤖 Anomaly-Based Detection (3 Models)...")
print("=" * 60)

print("⏳ Decision Tree predicting...")
dt_proba         = dt_model.predict_proba(X_test_scaled)
dt_pred          = dt_model.predict(X_test_scaled)
dt_pred_labels   = le.inverse_transform(dt_pred)
dt_acc           = accuracy_score(y_true, dt_pred_labels)
print(f"✅ Decision Tree Accuracy: {dt_acc*100:.4f}%")

print("⏳ Random Forest predicting...")
rf_proba         = rf_model.predict_proba(X_test_scaled)
rf_pred          = rf_model.predict(X_test_scaled)
rf_pred_labels   = le.inverse_transform(rf_pred)
rf_acc           = accuracy_score(y_true, rf_pred_labels)
print(f"✅ Random Forest Accuracy: {rf_acc*100:.4f}%")

print("⏳ XGBoost predicting...")
xgb_proba        = xgb_model.predict_proba(X_test_scaled)
xgb_pred         = xgb_model.predict(X_test_scaled)
xgb_pred_labels  = le.inverse_transform(xgb_pred)
xgb_acc          = accuracy_score(y_true, xgb_pred_labels)
print(f"✅ XGBoost Accuracy:       {xgb_acc*100:.4f}%")

# ============================================================
# 5. Weighted Ensemble Voting (DT + RF + XGBoost)
# XGBoost وزنه أعلى لأنه أحسن موديل
# ============================================================
print("\n" + "=" * 60)
print("🗳️  Ensemble Voting (DT 20% + RF 30% + XGBoost 50%)...")
print("=" * 60)

ensemble_proba      = (xgb_proba * 0.5) + (rf_proba * 0.3) + (dt_proba * 0.2)
ensemble_pred       = np.argmax(ensemble_proba, axis=1)
ensemble_confidence = ensemble_proba.max(axis=1)
ensemble_pred_labels = le.inverse_transform(ensemble_pred)

ensemble_acc = accuracy_score(y_true, ensemble_pred_labels)
print(f"✅ Ensemble Accuracy: {ensemble_acc*100:.4f}%")
print(f"   Avg confidence:   {ensemble_confidence.mean()*100:.2f}%")

# ============================================================
# 6. Signature-based Rules
# ============================================================
print("\n" + "=" * 60)
print("📋 Signature-Based Detection...")
print("=" * 60)

def apply_signature_rules(df):
    result = pd.Series(['BenignTraffic'] * len(df), index=df.index)

    # Rule 1: DDoS-ICMP_Flood
    result[(df['ICMP'] == 1) & (df['Rate'] > 500)] = 'DDoS-ICMP_Flood'

    # Rule 2: DDoS-PSHACK_Flood
    result[(df['psh_flag_number'] > 500) & (df['ack_flag_number'] > 500)] = 'DDoS-PSHACK_Flood'

    # Rule 3: DDoS-RSTFINFlood
    result[(df['rst_flag_number'] > 500) & (df['fin_flag_number'] > 500)] = 'DDoS-RSTFINFlood'

    # Rule 4: DDoS-SYN_Flood
    result[(df['syn_count'] > 500) & (df['Rate'] > 500)] = 'DDoS-SYN_Flood'

    # Rule 5: Mirai-udpplain
    result[(df['UDP'] == 1) & (df['Std'] == 0) & (df['Rate'] > 100)] = 'Mirai-udpplain'

    # Rule 6: MITM-ArpSpoofing
    result[(df['ARP'] == 1) & (df['Variance'] > 10000)] = 'MITM-ArpSpoofing'

    return result

sig_pred = apply_signature_rules(test_df)
sig_acc  = accuracy_score(y_true, sig_pred)
print(f"✅ Signature Rules Accuracy: {sig_acc*100:.4f}%")

# ============================================================
# 7. Hybrid Logic
# لو الـ Ensemble واثق بـ 70%+ → نستخدمه
# لو مش واثق → نستخدم Signature
# ============================================================
print("\n" + "=" * 60)
print("🔀 Hybrid Detection (Ensemble + Signature)...")
print("=" * 60)

CONFIDENCE_THRESHOLD = 0.95

# المنطق الجديد:
# لو Ensemble قال هجوم → نثق فيه مباشرة
# لو Ensemble قال BenignTraffic → نتأكد بالـ Signature
#    لو Signature اكتشفت هجوم → نستخدم الـ Signature
#    لو Signature قالت Benign برضو → نثق في الـ Ensemble

hybrid_pred = []
used_ml_attack  = 0
used_ml_benign  = 0
used_sig_override = 0

for i in range(len(test_df)):
    ml_label  = ensemble_pred_labels[i]
    sig_label = sig_pred.iloc[i]

    if ml_label != 'BenignTraffic':
        # ML اكتشف هجوم → نثق فيه
        hybrid_pred.append(ml_label)
        used_ml_attack += 1
    else:
        # ML قال Benign → نتأكد بالـ Signature
        if sig_label != 'BenignTraffic':
            # Signature اكتشفت هجوم → نستخدمها
            hybrid_pred.append(sig_label)
            used_sig_override += 1
        else:
            # الاتنين قالوا Benign → Benign
            hybrid_pred.append('BenignTraffic')
            used_ml_benign += 1

hybrid_pred = np.array(hybrid_pred)
used_ml = used_ml_attack + used_ml_benign
used_sig = used_sig_override

print(f"✅ ML attack decisions:     {used_ml_attack:,}")
print(f"✅ ML benign decisions:     {used_ml_benign:,}")
print(f"✅ Signature overrides:     {used_sig_override:,}")

print(f"✅ ML decisions:        {used_ml_attack + used_ml_benign:,}")
print(f"✅ Signature overrides: {used_sig_override:,}")

# ============================================================
# 8. المقارنة النهائية
# ============================================================
print("\n" + "=" * 60)
print("🏆 FINAL COMPARISON - ALL METHODS")
print("=" * 60)

hybrid_acc  = accuracy_score(y_true, hybrid_pred)
hybrid_f1   = f1_score(y_true, hybrid_pred, average='weighted', zero_division=0)
hybrid_prec = precision_score(y_true, hybrid_pred, average='weighted', zero_division=0)
hybrid_rec  = recall_score(y_true, hybrid_pred, average='weighted', zero_division=0)

dt_f1  = f1_score(y_true, dt_pred_labels,  average='weighted', zero_division=0)
rf_f1  = f1_score(y_true, rf_pred_labels,  average='weighted', zero_division=0)
xgb_f1 = f1_score(y_true, xgb_pred_labels, average='weighted', zero_division=0)
ens_f1 = f1_score(y_true, ensemble_pred_labels, average='weighted', zero_division=0)

print(f"\n{'Method':<30} {'Accuracy':>10} {'F1-Score':>10}")
print("-" * 55)
print(f"{'Signature-Based':<30} {sig_acc*100:>9.4f}%       N/A")
print(f"{'Anomaly - Decision Tree':<30} {dt_acc*100:>9.4f}%    {dt_f1:.4f}")
print(f"{'Anomaly - Random Forest':<30} {rf_acc*100:>9.4f}%    {rf_f1:.4f}")
print(f"{'Anomaly - XGBoost':<30} {xgb_acc*100:>9.4f}%    {xgb_f1:.4f}")
print(f"{'Ensemble (DT+RF+XGB)':<30} {ensemble_acc*100:>9.4f}%    {ens_f1:.4f}")
print(f"{'🥇 Hybrid (Ensemble+Sig)':<30} {hybrid_acc*100:>9.4f}%    {hybrid_f1:.4f}")

improvement = hybrid_acc - xgb_acc
print(f"\n📈 Hybrid vs XGBoost alone: {improvement*100:+.4f}%")

# ============================================================
# 9. حفظ النتائج
# ============================================================
np.save(os.path.join(OUTPUT_DIR, "y_hybrid_pred.npy"), hybrid_pred)

results_path = os.path.join(OUTPUT_DIR, "05_hybrid_results.txt")
with open(results_path, "w", encoding="utf-8") as f:
    f.write("IoT-IDS Hybrid Detection Results\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}\n\n")
    f.write(f"Signature-Based Accuracy:  {sig_acc*100:.4f}%\n")
    f.write(f"Decision Tree Accuracy:    {dt_acc*100:.4f}%\n")
    f.write(f"Random Forest Accuracy:    {rf_acc*100:.4f}%\n")
    f.write(f"XGBoost Accuracy:          {xgb_acc*100:.4f}%\n")
    f.write(f"Ensemble Accuracy:         {ensemble_acc*100:.4f}%\n")
    f.write(f"Hybrid Accuracy:           {hybrid_acc*100:.4f}%\n")
    f.write(f"Hybrid F1-Score:           {hybrid_f1:.4f}\n")
    f.write(f"Hybrid Precision:          {hybrid_prec:.4f}\n")
    f.write(f"Hybrid Recall:             {hybrid_rec:.4f}\n")
    f.write(f"\nML decisions:        {used_ml_attack + used_ml_benign:,}\n")
    f.write(f"Signature overrides: {used_sig_override:,}\n")
    f.write(f"\nImprovement over XGBoost: {improvement*100:+.4f}%\n\n")
    f.write("Classification Report (Hybrid):\n")
    f.write(classification_report(y_true, hybrid_pred, zero_division=0))

print(f"\n✅ Results saved: {results_path}")
print("\n" + "=" * 60)
print("🎉 Script 05 DONE! Ready for Script 06 (Real-Time Simulation)")
print("=" * 60)
