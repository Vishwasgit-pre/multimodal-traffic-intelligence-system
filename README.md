# 🚦 Multimodal Traffic Intelligence System

> **Note on Repository Name**  
> This repository is named **helmet-violation-system** for legacy reasons.  
> The project has since evolved into a broader system and is now called  
> **Multimodal Traffic Intelligence System**, covering image- and video-based
> traffic safety analysis with temporal intelligence.

---

## 📌 Project Overview

The **Multimodal Traffic Intelligence System** is a lightweight, deployable AI-based
traffic safety analysis platform that processes **both images and videos** to detect
helmet compliance and derive **temporal traffic warnings**.

The system is designed to be:
- Honest (no false precision)
- Explainable
- Resource-efficient
- Suitable for edge or low-resource environments

---

## 🧠 Key Capabilities

### 🪖 Image Helmet Detection
- Detects helmet compliance from a single image
- Uses a trained deep learning classifier
- Outputs:
  - Compliance / Violation
  - Confidence score
  - Applicable traffic rule (Section 129 – Helmet Mandatory)

---

### 🎥 Video Traffic Analysis
- Processes videos frame-by-frame
- Aggregates helmet and no-helmet frames
- Outputs:
  - Helmet frame count
  - No-helmet frame count
  - Severity level (Low / Medium / High)
  - Confidence estimation

---

### ⏱️ Temporal Frame-Based Warnings
- Derived from **temporal inconsistencies** across video frames
- Does NOT rely on calibrated sensors or speed data
- Includes:
  - Erratic riding behavior (Detected / Not Detected)
  - Indicative speed pattern analysis

> ⚠️ **Disclaimer**  
> Temporal warnings are **indicative** and based on frame-level analysis,
> not real-world calibrated measurements.

---

### 🔮 Future Traffic Intelligence (Planned)
- 🚦 Signal jump detection (object tracking + signal state)
- ⚡ FPS-calibrated speed estimation
- 📸 License plate recognition (ANPR)
- 🧠 Multi-violation policy engine

---

## 🏗️ System Architecture

User Upload (Image / Video)  
→ React Frontend (Dashboard UI)  
→ Flask Backend (API Layer)  
→ CNN-based Helmet Classifier  
→ Temporal Frame Aggregation  
→ Rule Mapping & Risk Interpretation  

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Custom CSS (dashboard-style UI)

### Backend
- Python
- Flask
- Flask-CORS

### Machine Learning
- TensorFlow / Keras
- CNN-based image classifier
- Frame-based temporal analysis for videos

---

## 🎯 Design Philosophy

- **Multimodal**: Works with both images and videos
- **Lightweight**: No heavy object detection required
- **Explainable**: Clear outputs, no black-box claims
- **Scalable**: Can be extended with YOLO, ANPR, speed calibration, etc.

---

## 🚀 How to Run the Project

### Backend
```
cd traffic_violation_project
python app.py
```
Runs on: http://localhost:5000

### Frontend
```
cd helmet-violation-frontend
npm start
```
Runs on: http://localhost:3000

---

## 📊 Demo Flow (Suggested)
1. Upload an image → View helmet compliance + confidence
2. Upload a video → View aggregated helmet analysis
3. Observe temporal warnings (erratic behavior, speed pattern)
4. Discuss future scope and scalability

---

## 📌 Final Notes
- The project intentionally avoids false precision.
- All warnings are clearly labeled as indicative.
- The system prioritizes **engineering honesty** and **real-world feasibility**.

---

**Author:**  
Vishwas
