# PhishShield Extension

![Security](https://img.shields.io/badge/security-phishing%20detection-red)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost-blue)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![Platform](https://img.shields.io/badge/platform-Chrome%20Extension-yellow)

AI-powered phishing detection Chrome extension with FastAPI backend and XGBoost machine learning model.

---

# Project Overview

PhishShield is a browser security extension designed to protect users from phishing attacks.
The extension analyzes URLs in real time and uses a machine learning model to detect whether a website is legitimate or potentially malicious.

When a phishing website is detected, the extension immediately warns the user and prevents interaction with the malicious page.

---

# Key Features

* Real-time phishing website detection
* Machine learning-based URL classification
* Chrome extension integration
* FastAPI backend for phishing prediction API
* XGBoost model for phishing detection
* User alert popup for suspicious websites
* Safe website confirmation notification

---

# System Architecture

```
User Browser
     │
     ▼
Chrome Extension
(background.js / content.js)
     │
     ▼
URL Feature Extraction
     │
     ▼
FastAPI Backend
(app.py)
     │
     ▼
Machine Learning Model
(XGBoost)
     │
     ▼
Prediction Result
(Safe / Phishing)
     │
     ▼
Popup Warning Displayed
```

---

# Project Structure

```
phishshield-extension
│
├── frontend
│   ├── icons
│   │   ├── icon16.png
│   │   ├── icon48.png
│   │   └── icon128.png
│   │
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── styles.css
│
├── backend
│   ├── model
│   │   ├── scaler.pkl
│   │   └── xgb_model.json
│   │
│   ├── app.py
│   ├── url_feature_extractor.py
│   └── requirements.txt
│
├── screenshots
│   ├── phishing-detected.png
│   └── safe-detected.png
│
└── README.md
```

---

# Technologies Used

Frontend

* HTML
* CSS
* JavaScript
* Chrome Extension API

Backend

* Python
* FastAPI

Machine Learning

* XGBoost
* Scikit-learn
* Feature Engineering for URL analysis

---

# How to Run the Backend

1. Navigate to the backend folder

```
cd backend
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Start the FastAPI server

```
uvicorn app:app --reload
```

The API will start at:

```
http://127.0.0.1:8000
```

You can test the API documentation at:

```
http://127.0.0.1:8000/docs
```

---

# How to Load the Chrome Extension

1. Open Google Chrome
2. Navigate to

```
chrome://extensions/
```

3. Enable **Developer Mode**
4. Click **Load unpacked**
5. Select the **frontend folder**

The PhishShield extension will now be installed.

---

# How It Works

1. User visits a website
2. Extension extracts URL features
3. Features are sent to FastAPI backend
4. ML model predicts phishing probability
5. Extension shows **Safe or Phishing warning**

---

# Output Screenshots

## Phishing Website Detected

![Phishing Detection](screenshots/phishing-detected.png)

The extension detects suspicious phishing websites and alerts the user with a warning message.

---

## Safe Website Detection

![Safe Detection](screenshots/safe-detected.png)

The extension confirms when a website is safe to use.

---

# Security Impact

PhishShield helps protect users from:

* Credential theft attacks
* Fake banking login pages
* Phishing scams
* Malicious websites

By providing real-time detection and alerts, users are prevented from submitting sensitive information to phishing websites.

---

# Future Improvements

* Domain reputation analysis
* Integration with phishing blacklist APIs
* Browser dashboard for detected threats
* Email phishing detection module
* Real-time threat intelligence integration

---

# Author

**Gideon Kingsly**

Cybersecurity & Machine Learning Enthusiast

---
