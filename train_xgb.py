import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import joblib
import xgboost as xgb

# 1. Load dataset
df = pd.read_csv("survey lung cancer.csv")

# 2. Drop duplicate
df.drop_duplicates(inplace=True)

# 3. Identifikasi fitur
numeric_features = df.select_dtypes(include=["int64", "float64"]).columns
categorical_features = df.select_dtypes(include=["object"]).columns

# 4. Scaling AGE
scaler = MinMaxScaler()
df["AGE"] = scaler.fit_transform(df[["AGE"]])

# 5. Label encoding categorical features
encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# 6. Split data
x = df.drop("LUNG_CANCER", axis=1)
y = df["LUNG_CANCER"]
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# 7. SMOTE
smote = SMOTE(random_state=42)
xtrain, ytrain = smote.fit_resample(xtrain, ytrain)

# 8. Train XGBoost model
model = xgb.XGBClassifier(
    n_estimators=100, random_state=42, use_label_encoder=False, eval_metric="logloss"
)
model.fit(xtrain, ytrain)

# 9. Simpan artefak model dan preprocessing
artefak = {
    "model": model,
    "scaler": scaler,
    "encoders": encoders,
    "obj_cols": list(categorical_features),
    "num_cols": list(numeric_features),
    "feature_order": xtrain.columns.tolist(),
}

joblib.dump(artefak, "app/model/xgb_model.pkl")
print(
    "Model XGBoost dan artefak preprocessing berhasil disimpan di app/model/xgb_model.pkl"
)
