# ============================================================
# Script 02: Feature Selection & Preprocessing
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# Approach: FarihaAnis (Top 25 Features + RobustScaler)
# ============================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. PATHS
# ============================================================
BASE_DIR   = r"C:\Users\cm\IoT-IDS-System"
TRAIN_CSV  = os.path.join(BASE_DIR, "CICIOT23", "train",      "train.csv")
TEST_CSV   = os.path.join(BASE_DIR, "CICIOT23", "test",       "test.csv")
VAL_CSV    = os.path.join(BASE_DIR, "CICIOT23", "validation", "validation.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# ============================================================
# 2. تحميل البيانات
# ============================================================
print("=" * 60)
print("📂 Loading datasets...")
print("=" * 60)

print("⏳ Loading train.csv ...")
train_df = pd.read_csv(TRAIN_CSV)
print(f"✅ Train:      {train_df.shape[0]:,} rows")

print("⏳ Loading test.csv ...")
test_df = pd.read_csv(TEST_CSV)
print(f"✅ Test:       {test_df.shape[0]:,} rows")

print("⏳ Loading validation.csv ...")
val_df = pd.read_csv(VAL_CSV)
print(f"✅ Validation: {val_df.shape[0]:,} rows")

# ============================================================
# 3. فصل الـ Features عن الـ Labels
# ============================================================
print("\n" + "=" * 60)
print("✂️  Separating Features and Labels...")
print("=" * 60)

LABEL_COL = 'label'

X_train = train_df.drop(columns=[LABEL_COL])
y_train = train_df[LABEL_COL]

X_test  = test_df.drop(columns=[LABEL_COL])
y_test  = test_df[LABEL_COL]

X_val   = val_df.drop(columns=[LABEL_COL])
y_val   = val_df[LABEL_COL]

print(f"✅ X_train: {X_train.shape} | y_train: {y_train.shape}")
print(f"✅ X_test:  {X_test.shape}  | y_test:  {y_test.shape}")
print(f"✅ X_val:   {X_val.shape}   | y_val:   {y_val.shape}")

# ============================================================
# 4. Label Encoding (تحويل النصوص لأرقام)
# ============================================================
print("\n" + "=" * 60)
print("🏷️  Label Encoding (Text → Numbers)...")
print("=" * 60)

le = LabelEncoder()
le.fit(y_train)

y_train_enc = le.transform(y_train)
y_test_enc  = le.transform(y_test)
y_val_enc   = le.transform(y_val)

print(f"✅ Classes found: {len(le.classes_)}")
for i, cls in enumerate(le.classes_):
    print(f"   {i:2} → {cls}")

# حفظ الـ LabelEncoder
le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
with open(le_path, "wb") as f:
    pickle.dump(le, f)
print(f"\n✅ LabelEncoder saved: {le_path}")

# ============================================================
# 5. Feature Selection - Top 25 (FarihaAnis Approach)
# ============================================================
print("\n" + "=" * 60)
print("🔍 Feature Selection - Selecting Top 25 Features...")
print("=" * 60)

selector = SelectKBest(score_func=f_classif, k=25)
selector.fit(X_train, y_train_enc)

# أسماء الـ features المختارة
selected_mask     = selector.get_support()
selected_features = X_train.columns[selected_mask].tolist()

print(f"✅ Top 25 Selected Features:")
for i, feat in enumerate(selected_features, 1):
    print(f"   {i:2}. {feat}")

# تطبيق الاختيار
X_train_sel = X_train[selected_features]
X_test_sel  = X_test[selected_features]
X_val_sel   = X_val[selected_features]

# حفظ أسماء الـ features
feat_path = os.path.join(MODELS_DIR, "selected_features.pkl")
with open(feat_path, "wb") as f:
    pickle.dump(selected_features, f)
print(f"\n✅ Selected features saved: {feat_path}")

# ============================================================
# 6. Scaling - RobustScaler (مقاوم للـ outliers)
# ============================================================
print("\n" + "=" * 60)
print("⚖️  Scaling Features (RobustScaler)...")
print("=" * 60)

scaler = RobustScaler()
scaler.fit(X_train_sel)

X_train_scaled = scaler.transform(X_train_sel)
X_test_scaled  = scaler.transform(X_test_sel)
X_val_scaled   = scaler.transform(X_val_sel)

print(f"✅ Train scaled: {X_train_scaled.shape}")
print(f"✅ Test scaled:  {X_test_scaled.shape}")
print(f"✅ Val scaled:   {X_val_scaled.shape}")

# حفظ الـ Scaler
scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
with open(scaler_path, "wb") as f:
    pickle.dump(scaler, f)
print(f"\n✅ Scaler saved: {scaler_path}")

# ============================================================
# 7. حفظ الداتا المعالجة
# ============================================================
print("\n" + "=" * 60)
print("💾 Saving processed data...")
print("=" * 60)

# حفظ كـ numpy arrays (أسرع للتدريب)
np.save(os.path.join(OUTPUT_DIR, "X_train.npy"), X_train_scaled)
np.save(os.path.join(OUTPUT_DIR, "X_test.npy"),  X_test_scaled)
np.save(os.path.join(OUTPUT_DIR, "X_val.npy"),   X_val_scaled)
np.save(os.path.join(OUTPUT_DIR, "y_train.npy"), y_train_enc)
np.save(os.path.join(OUTPUT_DIR, "y_test.npy"),  y_test_enc)
np.save(os.path.join(OUTPUT_DIR, "y_val.npy"),   y_val_enc)

print("✅ Saved: X_train.npy, X_test.npy, X_val.npy")
print("✅ Saved: y_train.npy, y_test.npy, y_val.npy")

# ============================================================
# 8. ملخص نهائي
# ============================================================
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"  Original features:  46")
print(f"  Selected features:  25")
print(f"  Train samples:      {X_train_scaled.shape[0]:,}")
print(f"  Test samples:       {X_test_scaled.shape[0]:,}")
print(f"  Val samples:        {X_val_scaled.shape[0]:,}")
print(f"  Number of classes:  {len(le.classes_)}")
print(f"  Scaler:             RobustScaler")
print(f"  Feature Selection:  SelectKBest (f_classif) - Top 25")

print("\n" + "=" * 60)
print("🎉 Script 02 DONE! Ready for Script 03 (Model Training)")
print("=" * 60)