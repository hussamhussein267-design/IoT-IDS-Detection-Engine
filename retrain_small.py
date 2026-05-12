# ============================================================
# Script: retrain_small.py
# Retrain all 3 models on 200K records for GitHub upload
# ============================================================

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import accuracy_score, f1_score
from xgboost import XGBClassifier
import pickle, os, time, warnings
warnings.filterwarnings('ignore')

TRAIN_CSV  = r"C:\Users\cm\IoT-IDS-System\CICIOT23\train\train.csv"
TEST_CSV   = r"C:\Users\cm\IoT-IDS-System\CICIOT23\test\test.csv"
MODELS_DIR = r"C:\Users\cm\IoT-IDS-GitHub\models"
os.makedirs(MODELS_DIR, exist_ok=True)

SAMPLE_SIZE = 200000

print("="*55)
print("Loading and sampling data...")
print("="*55)

train_df = pd.read_csv(TRAIN_CSV).sample(n=SAMPLE_SIZE, random_state=42)
test_df  = pd.read_csv(TEST_CSV).sample(n=50000,  random_state=42)

print(f"Train: {len(train_df):,} | Test: {len(test_df):,}")

X_train = train_df.drop(columns=['label'])
y_train = train_df['label']
X_test  = test_df.drop(columns=['label'])
y_test  = test_df['label']

# Label Encoding
le = LabelEncoder()
le.fit(y_train)
y_train_enc = le.transform(y_train)
y_test_enc  = le.transform(y_test)

# Feature Selection
selector = SelectKBest(score_func=f_classif, k=25)
selector.fit(X_train, y_train_enc)
feats = X_train.columns[selector.get_support()].tolist()
X_train_sel = X_train[feats]
X_test_sel  = X_test[feats]

# Scaling
scaler = RobustScaler()
X_train_sc = scaler.fit_transform(X_train_sel)
X_test_sc  = scaler.transform(X_test_sel)

# Save encoders
pickle.dump(le,     open(os.path.join(MODELS_DIR,"label_encoder.pkl"),"wb"))
pickle.dump(scaler, open(os.path.join(MODELS_DIR,"scaler.pkl"),"wb"))
pickle.dump(feats,  open(os.path.join(MODELS_DIR,"selected_features.pkl"),"wb"))

results = {}

# Decision Tree
print("\nTraining Decision Tree...")
t = time.time()
dt = DecisionTreeClassifier(max_depth=20, random_state=42)
dt.fit(X_train_sc, y_train_enc)
acc = accuracy_score(y_test_enc, dt.predict(X_test_sc))
print(f"✅ DT Accuracy: {acc*100:.2f}% | {time.time()-t:.1f}s")
pickle.dump(dt, open(os.path.join(MODELS_DIR,"decision_tree.pkl"),"wb"))
results['Decision Tree'] = acc

# Random Forest
print("\nTraining Random Forest...")
t = time.time()
rf = RandomForestClassifier(n_estimators=50, max_depth=15, n_jobs=-1, random_state=42)
rf.fit(X_train_sc, y_train_enc)
acc = accuracy_score(y_test_enc, rf.predict(X_test_sc))
print(f"✅ RF Accuracy: {acc*100:.2f}% | {time.time()-t:.1f}s")
pickle.dump(rf, open(os.path.join(MODELS_DIR,"random_forest.pkl"),"wb"))
results['Random Forest'] = acc

# XGBoost
print("\nTraining XGBoost...")
t = time.time()
xgb = XGBClassifier(n_estimators=100, max_depth=6, n_jobs=-1,
                    eval_metric='mlogloss', tree_method='hist', random_state=42)
xgb.fit(X_train_sc, y_train_enc)
acc = accuracy_score(y_test_enc, xgb.predict(X_test_sc))
print(f"✅ XGBoost Accuracy: {acc*100:.2f}% | {time.time()-t:.1f}s")
pickle.dump(xgb, open(os.path.join(MODELS_DIR,"xgboost.pkl"),"wb"))
results['XGBoost'] = acc

print("\n" + "="*55)
print("RESULTS")
print("="*55)
for m, a in results.items():
    print(f"{m}: {a*100:.2f}%")

print("\nChecking model file sizes...")
for f in os.listdir(MODELS_DIR):
    size = os.path.getsize(os.path.join(MODELS_DIR,f))
    mb = size/1024/1024
    status = "✅" if mb < 100 else "❌ TOO BIG"
    print(f"{status} {f}: {mb:.1f} MB")

print("\n✅ Done! Models saved to models_small/")
