---
title: Backend Lungai Tabular
emoji: 🫁
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Backend Lungai Tabular

API backend berbasis Flask untuk memprediksi risiko Kanker Paru-Paru berdasarkan data tabular survei kesehatan menggunakan model XGBoost.

## API Endpoint

### POST `/predict`

**Request Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "GENDER": "M",
  "AGE": 69,
  "SMOKING": 1,
  "YELLOW_FINGERS": 2,
  "ANXIETY": 2,
  "PEER_PRESSURE": 1,
  "CHRONIC DISEASE": 1,
  "FATIGUE": 2,
  "ALLERGY": 1,
  "WHEEZING": 2,
  "ALCOHOL CONSUMING": 2,
  "COUGHING": 2,
  "SHORTNESS OF BREATH": 2,
  "SWALLOWING DIFFICULTY": 2,
  "CHEST PAIN": 2
}
```

**Response Body**:
```json
{
  "prediction": "Kanker Paru-Paru"
}
```
