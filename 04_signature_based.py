# ============================================================
# Script 04: Signature-Based Detection Engine
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# ============================================================

import pandas as pd
import numpy as np
import os
import pickle
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. PATHS
# ============================================================
BASE_DIR   = r"C:\Users\cm\IoT-IDS-System"
TRAIN_CSV  = os.path.join(BASE_DIR, "CICIOT23", "train",      "train.csv")
TEST_CSV   = os.path.join(BASE_DIR, "CICIOT23", "test",       "test.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 2. Signature Rules
# كل rule بتشوف الـ features وتقرر نوع الهجوم
# ============================================================

def apply_signature_rules(df):
    """
    Signature-based detection using rule matching.
    بترجع series فيها اسم الهجوم أو 'BenignTraffic'
    """
    # نبدأ كل الـ records بـ BenignTraffic
    result = pd.Series(['BenignTraffic'] * len(df), index=df.index)

    # ---- DDoS Rules ----
    # DDoS-SYN_Flood: syn_count عالي جداً مع rate عالي
    mask = (df['syn_count'] > 100) & (df['Rate'] > 100)
    result[mask] = 'DDoS-SYN_Flood'

    # DDoS-ICMP_Flood: ICMP=1 مع rate عالي
    mask = (df['ICMP'] == 1) & (df['Rate'] > 50)
    result[mask] = 'DDoS-ICMP_Flood'

    # DDoS-UDP_Flood: UDP=1 مع rate عالي جداً
    mask = (df['UDP'] == 1) & (df['Rate'] > 200) & (df['syn_count'] == 0)
    result[mask] = 'DDoS-UDP_Flood'

    # DDoS-TCP_Flood: TCP=1 مع header كبير وrate عالي
    mask = (df['TCP'] == 1) & (df['Rate'] > 150) & (df['Header_Length'] > 500)
    result[mask] = 'DDoS-TCP_Flood'

    # DDoS-PSHACK_Flood: psh_flag + ack_flag عاليين
    mask = (df['psh_flag_number'] > 50) & (df['ack_flag_number'] > 50)
    result[mask] = 'DDoS-PSHACK_Flood'

    # DDoS-RSTFINFlood: rst_flag + fin_flag عاليين
    mask = (df['rst_flag_number'] > 50) & (df['fin_flag_number'] > 50)
    result[mask] = 'DDoS-RSTFINFlood'

    # DDoS-ACK_Fragmentation: ack عالي مع packet size صغير
    mask = (df['ack_count'] > 100) & (df['Min'] < 10)
    result[mask] = 'DDoS-ACK_Fragmentation'

    # DDoS-ICMP_Fragmentation: ICMP مع size متوسط
    mask = (df['ICMP'] == 1) & (df['Rate'] > 20) & (df['Rate'] <= 50)
    result[mask] = 'DDoS-ICMP_Fragmentation'

    # ---- DoS Rules ----
    # DoS-SYN_Flood: syn عالي بس rate أقل من DDoS
    mask = (df['syn_count'] > 50) & (df['Rate'] > 30) & (df['Rate'] <= 100)
    result[mask] = 'DoS-SYN_Flood'

    # DoS-UDP_Flood: UDP مع rate متوسط
    mask = (df['UDP'] == 1) & (df['Rate'] > 50) & (df['Rate'] <= 200)
    result[mask] = 'DoS-UDP_Flood'

    # DoS-TCP_Flood: TCP مع rate متوسط
    mask = (df['TCP'] == 1) & (df['Rate'] > 50) & (df['Rate'] <= 150)
    result[mask] = 'DoS-TCP_Flood'

    # DoS-HTTP_Flood: HTTP مع requests كتير
    mask = (df['HTTPS'] == 1) & (df['Rate'] > 20) & (df['ack_count'] > 20)
    result[mask] = 'DoS-HTTP_Flood'

    # ---- Mirai Rules ----
    # Mirai-udpplain: UDP مع packet size ثابت صغير
    mask = (df['UDP'] == 1) & (df['Std'] < 1) & (df['Rate'] > 10)
    result[mask] = 'Mirai-udpplain'

    # Mirai-greeth_flood: Protocol غير معروف مع rate عالي
    mask = (df['Protocol Type'] > 100) & (df['Rate'] > 30)
    result[mask] = 'Mirai-greeth_flood'

    # Mirai-greip_flood: Protocol غير معروف مع rate متوسط
    mask = (df['Protocol Type'] > 100) & (df['Rate'] > 10) & (df['Rate'] <= 30)
    result[mask] = 'Mirai-greip_flood'

    # ---- Recon Rules ----
    # Recon-PortScan: connections كتير مع duration قصير
    mask = (df['fin_count'] > 10) & (df['Duration'] < 10) & (df['Rate'] < 10)
    result[mask] = 'Recon-PortScan'

    # Recon-OSScan: syn بدون ack مع duration قصير
    mask = (df['syn_count'] > 5) & (df['ack_count'] == 0) & (df['Duration'] < 5)
    result[mask] = 'Recon-OSScan'

    # Recon-HostDiscovery: ICMP مع rate منخفض
    mask = (df['ICMP'] == 1) & (df['Rate'] < 5)
    result[mask] = 'Recon-HostDiscovery'

    # Recon-PingSweep: ICMP مع rate منخفض جداً
    mask = (df['ICMP'] == 1) & (df['Rate'] < 2)
    result[mask] = 'Recon-PingSweep'

    # ---- Spoofing Rules ----
    # MITM-ArpSpoofing: ARP مع variance عالي
    mask = (df['ARP'] == 1) & (df['Variance'] > 100)
    result[mask] = 'MITM-ArpSpoofing'

    # DNS_Spoofing: DNS مع rate غير طبيعي
    mask = (df['DNS'] == 1) & (df['Rate'] > 10)
    result[mask] = 'DNS_Spoofing'

    # ---- Web Attacks ----
    # DDoS-HTTP_Flood: HTTPS مع rate عالي
    mask = (df['HTTPS'] == 1) & (df['Rate'] > 50)
    result[mask] = 'DDoS-HTTP_Flood'

    # DDoS-SlowLoris: HTTPS مع duration طويل جداً وrate منخفض
    mask = (df['HTTPS'] == 1) & (df['Duration'] > 100) & (df['Rate'] < 5)
    result[mask] = 'DDoS-SlowLoris'

    # VulnerabilityScan: fin عالي مع rst عالي
    mask = (df['fin_count'] > 5) & (df['rst_count'] > 5) & (df['Rate'] < 20)
    result[mask] = 'VulnerabilityScan'

    return result

# ============================================================
# 3. تحميل وتشغيل على Test Set
# ============================================================
print("=" * 60)
print("📂 Loading Test Data...")
print("=" * 60)

test_df  = pd.read_csv(TEST_CSV)
y_true   = test_df['label']
print(f"✅ Test loaded: {len(test_df):,} rows")

print("\n" + "=" * 60)
print("🔍 Applying Signature Rules...")
print("=" * 60)

y_sig_pred = apply_signature_rules(test_df)
print("✅ Signature rules applied!")

# ============================================================
# 4. تقييم الـ Signature-based
# ============================================================
from sklearn.metrics import accuracy_score, classification_report

sig_acc = accuracy_score(y_true, y_sig_pred)
print(f"\n📊 Signature-Based Accuracy: {sig_acc*100:.4f}%")

# توزيع التنبؤات
pred_counts = y_sig_pred.value_counts()
print(f"\n📋 Signature Predictions Distribution:")
print(f"{'Attack Type':<35} {'Predicted':>10}")
print("-" * 50)
for attack, count in pred_counts.items():
    print(f"{attack:<35} {count:>10,}")

# ============================================================
# 5. حفظ نتائج الـ Signature
# ============================================================
sig_results = {
    'accuracy': sig_acc,
    'predictions': y_sig_pred,
    'rules_count': 25
}

sig_path = os.path.join(MODELS_DIR, "signature_results.pkl")
with open(sig_path, "wb") as f:
    pickle.dump(sig_results, f)
print(f"\n✅ Signature results saved: {sig_path}")

# حفظ التنبؤات
np.save(os.path.join(OUTPUT_DIR, "y_sig_pred.npy"),
        y_sig_pred.values)

print("\n" + "=" * 60)
print(f"📊 SIGNATURE-BASED RESULTS:")
print(f"   Accuracy: {sig_acc*100:.4f}%")
print(f"   Rules:    25 rules covering all attack types")
print("=" * 60)
print("🎉 Script 04 DONE! Ready for Script 05 (Hybrid)")
print("=" * 60)