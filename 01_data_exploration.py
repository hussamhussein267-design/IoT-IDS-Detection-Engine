# ============================================================
# Script 01: Data Loading & Exploration
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# ============================================================

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. PATHS - عدّل لو الـ path مختلف عندك
# ============================================================
BASE_DIR    = r"C:\Users\cm\IoT-IDS-System"
TRAIN_CSV   = os.path.join(BASE_DIR, "CICIOT23", "train",      "train.csv")
TEST_CSV    = os.path.join(BASE_DIR, "CICIOT23", "test",       "test.csv")
VAL_CSV     = os.path.join(BASE_DIR, "CICIOT23", "validation", "validation.csv")
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 2. تحميل البيانات
# ============================================================
print("=" * 60)
print("📂 Loading datasets...")
print("=" * 60)

print("⏳ Loading train.csv ...")
train_df = pd.read_csv(TRAIN_CSV)
print(f"✅ Train loaded:      {train_df.shape[0]:,} rows × {train_df.shape[1]} columns")

print("⏳ Loading test.csv ...")
test_df = pd.read_csv(TEST_CSV)
print(f"✅ Test loaded:       {test_df.shape[0]:,} rows × {test_df.shape[1]} columns")

print("⏳ Loading validation.csv ...")
val_df = pd.read_csv(VAL_CSV)
print(f"✅ Validation loaded: {val_df.shape[0]:,} rows × {val_df.shape[1]} columns")

total_rows = train_df.shape[0] + test_df.shape[0] + val_df.shape[0]
print(f"\n📊 Total records: {total_rows:,}")

# ============================================================
# 3. استكشاف البيانات الأساسي
# ============================================================
print("\n" + "=" * 60)
print("🔍 Basic Exploration (Train set)")
print("=" * 60)

print("\n📋 Column names:")
for i, col in enumerate(train_df.columns.tolist(), 1):
    print(f"   {i:2}. {col}")

print(f"\n📌 Data types:\n{train_df.dtypes.value_counts()}")

print(f"\n❓ Missing values in train: {train_df.isnull().sum().sum()}")
print(f"❓ Missing values in test:  {test_df.isnull().sum().sum()}")
print(f"❓ Missing values in val:   {val_df.isnull().sum().sum()}")

# ============================================================
# 4. توزيع الـ Labels (أنواع الهجمات)
# ============================================================
print("\n" + "=" * 60)
print("🏷️  Label Distribution (Train)")
print("=" * 60)

# نحاول نلاقي عمود الـ label تلقائياً
label_candidates = ['label', 'Label', 'attack_type', 'Attack', 'class', 'Class', 'target', 'Target']
label_col = None
for col in label_candidates:
    if col in train_df.columns:
        label_col = col
        break

if label_col is None:
    # آخر عمود غالباً هو الـ label
    label_col = train_df.columns[-1]
    print(f"⚠️  Label column not found by name, using last column: '{label_col}'")
else:
    print(f"✅ Label column found: '{label_col}'")

label_counts = train_df[label_col].value_counts()
label_pct    = train_df[label_col].value_counts(normalize=True) * 100

print(f"\n{'Attack Type':<35} {'Count':>10} {'%':>8}")
print("-" * 55)
for attack, count in label_counts.items():
    pct = label_pct[attack]
    print(f"{str(attack):<35} {count:>10,} {pct:>7.2f}%")

print(f"\n🔢 Total unique classes: {train_df[label_col].nunique()}")

# ============================================================
# 5. إحصائيات عامة
# ============================================================
print("\n" + "=" * 60)
print("📈 Basic Statistics (numeric columns - Train)")
print("=" * 60)

numeric_cols = train_df.select_dtypes(include=[np.number]).columns.tolist()
print(f"Number of numeric features: {len(numeric_cols)}")
print("\nFirst 5 rows preview:")
print(train_df.head())

# ============================================================
# 6. حفظ ملخص في ملف
# ============================================================
summary_path = os.path.join(OUTPUT_DIR, "01_exploration_summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("IoT-IDS Dataset Exploration Summary\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Train rows:      {train_df.shape[0]:,}\n")
    f.write(f"Test rows:       {test_df.shape[0]:,}\n")
    f.write(f"Validation rows: {val_df.shape[0]:,}\n")
    f.write(f"Total rows:      {total_rows:,}\n")
    f.write(f"Columns:         {train_df.shape[1]}\n")
    f.write(f"Label column:    {label_col}\n\n")
    f.write("Label Distribution (Train):\n")
    f.write("-" * 40 + "\n")
    for attack, count in label_counts.items():
        f.write(f"{str(attack):<35} {count:,}\n")
    f.write("\nColumn Names:\n")
    for col in train_df.columns:
        f.write(f"  - {col}\n")

print(f"\n✅ Summary saved to: {summary_path}")

print("\n" + "=" * 60)
print("🎉 Script 01 DONE! Ready for Script 02 (Feature Selection)")
print("=" * 60)
