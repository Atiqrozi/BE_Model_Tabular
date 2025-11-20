import re
import joblib
import numpy as np
import pandas as pd


# Normalisasi nama kolom
def _norm_name(s: str) -> str:
    return re.sub(r"\s+", "", str(s)).lower()


# Load artefak saat start
saved = joblib.load("app/model/xgb_model.pkl")
model = saved.get("model", saved)
scaler = saved.get("scaler")
encoders = saved.get("encoders")
feature_order = saved.get("feature_order")
num_cols = saved.get("num_cols")

# Cari fitur saat training
if feature_order is not None:
    train_features = list(feature_order)
elif hasattr(model, "feature_names_in_"):
    train_features = list(model.feature_names_in_)
else:
    train_features = None


def preprocess_and_predict(data_json):
    """
    Terima dict (JSON) dari request, ubah ke DataFrame,
    preprocessing, lalu prediksi.
    """
    # Data baru ke DataFrame
    data_baru = pd.DataFrame([data_json])

    # Mapping otomatis nama kolom (hapus spasi, kapitalisasi)
    norm_to_train = {_norm_name(c): c for c in train_features}
    mapping = {}
    for col in list(data_baru.columns):
        n = _norm_name(col)
        if n in norm_to_train and norm_to_train[n] != col:
            mapping[col] = norm_to_train[n]
    if mapping:
        data_baru = data_baru.rename(columns=mapping)

    # Tambahkan kolom yang hilang
    for col in train_features:
        if col not in data_baru.columns:
            data_baru[col] = 0

    # Urutkan sesuai train_features
    data_baru = data_baru[train_features]

    # Encode kategorikal
    if isinstance(encoders, dict):
        for c, le in encoders.items():
            if c in data_baru.columns:
                vals = data_baru[c].astype(str)
                unseen = sorted(set(vals.unique()) - set(le.classes_))
                if unseen:
                    le.classes_ = np.concatenate(
                        [le.classes_, np.array(unseen, dtype=object)]
                    )
                data_baru[c] = le.transform(vals)

    # Scale numerik
    if scaler is not None:
        if hasattr(scaler, "feature_names_in_"):
            scaler_cols = list(scaler.feature_names_in_)
        elif num_cols:
            scaler_cols = num_cols
        else:
            scaler_cols = [
                c
                for c in data_baru.select_dtypes(include=[np.number]).columns
                if c in train_features
            ]

        for c in scaler_cols:
            if c not in data_baru.columns:
                data_baru[c] = 0
        data_baru[scaler_cols] = scaler.transform(data_baru[scaler_cols])

    # Prediksi
    pred = model.predict(data_baru)

    if pred[0] == 0:
        return "normal"
    else:
        return "Kanker Paru-Paru"
