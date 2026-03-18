# ✅ Import required libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from url_feature_extractor import URLFeatureExtractor  # Custom class to extract features from a raw URL

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS (Cross-Origin Resource Sharing) to allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load the scaler and XGBoost model
scaler = joblib.load("scaler.pkl")
booster = xgb.Booster()
booster.load_model("xgb_model.json")

# ✅ Define the expected feature columns in correct order
FEATURE_COLUMNS = [
    "URLLength", "DomainLength", "TLDLength", "NoOfImage", "NoOfJS", "NoOfCSS", 
    "NoOfSelfRef", "NoOfExternalRef", "IsHTTPS", "HasObfuscation", "HasTitle", 
    "HasDescription", "HasSubmitButton", "HasSocialNet", "HasFavicon", 
    "HasCopyrightInfo", "popUpWindow", "Iframe", "Abnormal_URL", 
    "LetterToDigitRatio", "Redirect_0", "Redirect_1"
]

# ✅ Define input model schema for direct feature input
class URLFeatures(BaseModel):
    URLLength: int
    DomainLength: int
    TLDLength: int
    NoOfImage: int
    NoOfJS: int
    NoOfCSS: int
    NoOfSelfRef: int
    NoOfExternalRef: int
    IsHTTPS: int
    HasObfuscation: int
    HasTitle: int
    HasDescription: int
    HasSubmitButton: int
    HasSocialNet: int
    HasFavicon: int
    HasCopyrightInfo: int
    popUpWindow: int
    Iframe: int
    Abnormal_URL: int
    LetterToDigitRatio: float
    Redirect_0: int
    Redirect_1: int

# ✅ Define input model for raw URL input
class URLInput(BaseModel):
    url: str

# ✅ Predict directly from structured features
@app.post("/predict")
def predict(features: URLFeatures):
    try:
        # Convert to DataFrame with feature names
        input_df = pd.DataFrame([features.dict()], columns=FEATURE_COLUMNS)

        # Scale using the original scaler
        scaled_input = scaler.transform(input_df)

        # Create DMatrix with feature names
        dmatrix = xgb.DMatrix(scaled_input, feature_names=FEATURE_COLUMNS)

        # Predict
        pred = booster.predict(dmatrix)
        label = int(round(pred[0]))

        return {
            "prediction": label,
            "result": "Legitimate" if label == 1 else "Phishing"
        }
    except Exception as e:
        return {"error": str(e)}

# ✅ Predict from raw URL using feature extractor
@app.post("/predict_url")
def predict_from_url(input_data: URLInput):
    try:
        # Extract features using custom extractor
        extractor = URLFeatureExtractor(input_data.url)
        features = extractor.extract_model_features()

        if "error" in features:
            return {"error": features["error"]}

        # Convert to DataFrame
        input_df = pd.DataFrame([features], columns=FEATURE_COLUMNS)

        # Scale
        scaled_input = scaler.transform(input_df)

        # Predict with DMatrix
        dmatrix = xgb.DMatrix(scaled_input, feature_names=FEATURE_COLUMNS)
        pred_prob = booster.predict(dmatrix)[0]   # probability
        label = int(round(pred_prob))

        # ------------------------------
        # 🔍 Explainable AI (Reasons)
        # ------------------------------
        reasons = []

        if features["URLLength"] > 75:
            reasons.append("URL is very long")

        if features["IsHTTPS"] == 0:
            reasons.append("Website is not using HTTPS")

        if features["Abnormal_URL"] == 1:
            reasons.append("URL structure is abnormal")

        if features["HasSubmitButton"] == 1:
            reasons.append("Contains login or submit form")

        if features["HasObfuscation"] == 1:
            reasons.append("URL contains obfuscated characters")

        if features["Iframe"] == 1:
            reasons.append("Page uses iframe (common in phishing)")

        if features["popUpWindow"] == 1:
            reasons.append("Uses popup windows")

        # Confidence %
        confidence = round(float(pred_prob) * 100, 2)

        return {
            "url": input_data.url,
            "prediction": label,
            "result": "Legitimate" if label == 1 else "Phishing",
            "confidence": confidence,
            "reasons": reasons,
            "features": features
        }

    except Exception as e:
        return {"error": str(e)}

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "PhishShield API is running 🚀"}