# ============================================================
# Script 03: Model Training
# Project: Real-Time IoT Intrusion Detection System
# Student: Hussam Eldien Hussein Hatem | ID: 22511094
# Models: Decision Tree + Random Forest + XGBoost
# ============================================================

import numpy as np
import pickle
import os
import time
import warnings
warnings.filterwarnings('ignore')

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score,
                             precision_score, recall_score)
from xgboost import XGBClassifier

# ============================================================
# 1. PATHS
# ============================================================
BASE_DIR   = r"C:\Users\cm\IoT-IDS-System"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ============================================================
# 2. تحميل البيانات المعالجة
# ============================================================
print("=" * 60)
print("📂 Loading processed data...")
print("=" * 60)

X_train = np.load(os.path.join(OUTPUT_DIR, "X_train.npy"))
X_test  = np.load(os.path.join(OUTPUT_DIR, "X_test.npy"))
X_val   = np.load(os.path.join(OUTPUT_DIR, "X_val.npy"))
y_train = np.load(os.path.join(OUTPUT_DIR, "y_train.npy"))
y_test  = np.load(os.path.join(OUTPUT_DIR, "y_test.npy"))
y_val   = np.load(os.path.join(OUTPUT_DIR, "y_val.npy"))

# تحميل الـ LabelEncoder
with open(os.path.join(MODELS_DIR, "label_encoder.pkl"), "rb") as f:
    le = pickle.load(f)

print(f"✅ X_train: {X_train.shape}")
print(f"✅ X_test:  {X_test.shape}")
print(f"✅ X_val:   {X_val.shape}")
print(f"✅ Classes: {len(le.classes_)}")

# ============================================================
# دالة لتقييم الموديل
# ============================================================
def evaluate_model(model_name, y_true, y_pred):
    acc  = accuracy_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    print(f"\n📊 {model_name} Results:")
    print(f"   Accuracy:  {acc*100:.4f}%")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   Precision: {prec:.4f}")
    print(f"   Recall:    {rec:.4f}")
    return acc, f1, prec, rec

results = {}

# ============================================================
# 3. Decision Tree
# ============================================================
print("\n" + "=" * 60)
print("🌳 Training Decision Tree...")
print("=" * 60)

dt_start = time.time()
dt_model = DecisionTreeClassifier(
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
dt_model.fit(X_train, y_train)
dt_time = time.time() - dt_start
print(f"✅ Training done in {dt_time:.1f} seconds")

# تقييم على Test
dt_pred_test = dt_model.predict(X_test)
acc, f1, prec, rec = evaluate_model("Decision Tree (Test)", y_test, dt_pred_test)
results['Decision Tree'] = {'accuracy': acc, 'f1': f1, 'precision': prec, 'recall': rec, 'time': dt_time}

# حفظ الموديل
dt_path = os.path.join(MODELS_DIR, "decision_tree.pkl")
with open(dt_path, "wb") as f:
    pickle.dump(dt_model, f)
print(f"✅ Model saved: {dt_path}")

# ============================================================
# 4. Random Forest
# ============================================================
print("\n" + "=" * 60)
print("🌲 Training Random Forest...")
print("⏳ This may take 15-25 minutes...")
print("=" * 60)

rf_start = time.time()
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    n_jobs=-1,          # يستخدم كل الـ CPU cores
    random_state=42
)
rf_model.fit(X_train, y_train)
rf_time = time.time() - rf_start
print(f"✅ Training done in {rf_time/60:.1f} minutes")

# تقييم على Test
rf_pred_test = rf_model.predict(X_test)
acc, f1, prec, rec = evaluate_model("Random Forest (Test)", y_test, rf_pred_test)
results['Random Forest'] = {'accuracy': acc, 'f1': f1, 'precision': prec, 'recall': rec, 'time': rf_time}

# حفظ الموديل
rf_path = os.path.join(MODELS_DIR, "random_forest.pkl")
with open(rf_path, "wb") as f:
    pickle.dump(rf_model, f)
print(f"✅ Model saved: {rf_path}")

# ============================================================
# 5. XGBoost
# ============================================================
print("\n" + "=" * 60)
print("⚡ Training XGBoost...")
print("⏳ This may take 10-20 minutes...")
print("=" * 60)

xgb_start = time.time()
xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='mlogloss',
    n_jobs=-1,
    random_state=42,
    tree_method='hist'   # أسرع على CPU
)
xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=50
)
xgb_time = time.time() - xgb_start
print(f"✅ Training done in {xgb_time/60:.1f} minutes")

# تقييم على Test
xgb_pred_test = xgb_model.predict(X_test)
acc, f1, prec, rec = evaluate_model("XGBoost (Test)", y_test, xgb_pred_test)
results['XGBoost'] = {'accuracy': acc, 'f1': f1, 'precision': prec, 'recall': rec, 'time': xgb_time}

# حفظ الموديل
xgb_path = os.path.join(MODELS_DIR, "xgboost.pkl")
with open(xgb_path, "wb") as f:
    pickle.dump(xgb_model, f)
print(f"✅ Model saved: {xgb_path}")

# ============================================================
# 6. مقارنة النتائج
# ============================================================
print("\n" + "=" * 60)
print("🏆 FINAL COMPARISON")
print("=" * 60)
print(f"\n{'Model':<20} {'Accuracy':>10} {'F1-Score':>10} {'Precision':>10} {'Recall':>10}")
print("-" * 65)
for model_name, metrics in results.items():
    print(f"{model_name:<20} {metrics['accuracy']*100:>9.4f}% {metrics['f1']:>10.4f} {metrics['precision']:>10.4f} {metrics['recall']:>10.4f}")

# أحسن موديل
best_model = max(results, key=lambda x: results[x]['accuracy'])
print(f"\n🥇 Best Model: {best_model} with {results[best_model]['accuracy']*100:.4f}% accuracy")

# ============================================================
# 7. Classification Report للأحسن موديل
# ============================================================
print("\n" + "=" * 60)
print(f"📋 Detailed Report - {best_model}")
print("=" * 60)

if best_model == 'XGBoost':
    best_pred = xgb_pred_test
elif best_model == 'Random Forest':
    best_pred = rf_pred_test
else:
    best_pred = dt_pred_test

print(classification_report(y_test, best_pred,
                             target_names=le.classes_,
                             zero_division=0))

# ============================================================
# 8. حفظ النتائج
# ============================================================
results_path = os.path.join(OUTPUT_DIR, "03_training_results.txt")
with open(results_path, "w", encoding="utf-8") as f:
    f.write("IoT-IDS Model Training Results\n")
    f.write("=" * 60 + "\n\n")
    for model_name, metrics in results.items():
        f.write(f"{model_name}:\n")
        f.write(f"  Accuracy:  {metrics['accuracy']*100:.4f}%\n")
        f.write(f"  F1-Score:  {metrics['f1']:.4f}\n")
        f.write(f"  Precision: {metrics['precision']:.4f}\n")
        f.write(f"  Recall:    {metrics['recall']:.4f}\n")
        f.write(f"  Time:      {metrics['time']/60:.1f} min\n\n")
    f.write(f"\nBest Model: {best_model}\n")
    f.write(f"Best Accuracy: {results[best_model]['accuracy']*100:.4f}%\n\n")
    f.write("Detailed Classification Report:\n")
    f.write(classification_report(y_test, best_pred,
                                  target_names=le.classes_,
                                  zero_division=0))

print(f"\n✅ Results saved: {results_path}")
print("\n" + "=" * 60)
print("🎉 Script 03 DONE! Ready for Script 04 (Report Generation)")
print("=" * 60)