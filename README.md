# 🚦 Multimodal Traffic Intelligence System

> **Repository Note**  
> This repository was originally created as **helmet-violation-system** and later
> evolved into a broader system. The current implementation and scope are aligned
> with the name **Multimodal Traffic Intelligence System**.

---

## 📌 Problem Statement

Road safety violations such as **riding without a helmet**, **erratic riding behavior**,
and **unsafe traffic patterns** are major contributors to accidents. While large-scale
traffic monitoring systems exist, they are often:

- Expensive
- Hardware-dependent
- Resource-heavy
- Difficult to deploy at smaller checkpoints

There is a need for a **lightweight, software-based, AI-driven traffic intelligence system**
that can operate using **images and videos** and provide **interpretable results**.

---

## 🎯 Solution Overview

This project presents a **multimodal AI system** capable of:

- Detecting helmet compliance from images
- Analyzing helmet usage patterns in videos
- Generating **temporal traffic warnings**
- Mapping violations to traffic rules
- Providing an intuitive frontend for live demonstration

The system is intentionally designed to be:
- Honest (no false claims of precision)
- Explainable
- Scalable for future extensions

---

## 🧠 Machine Learning Implementation (Backend)

### 🔹 Model Type
- **Convolutional Neural Network (CNN)**
- Transfer learning using **MobileNetV2**
- Binary classification:
  - Helmet
  - No Helmet

### 🔹 Training Details
- Dataset: Custom curated helmet / no-helmet image dataset
- Input size: 224 × 224
- Loss function: Binary Crossentropy
- Optimizer: Adam
- Framework: TensorFlow + Keras

The model was trained locally on a CPU-based environment,
keeping the architecture lightweight for real-world deployability.

### 🔹 Why CNN + Transfer Learning?
- Efficient for image-based tasks
- Works well with limited datasets
- Faster convergence
- Suitable for edge or low-resource devices

---

## 🎥 Video Analysis Logic (Multimodal Aspect)

Instead of training a separate heavy video model, the system uses:

### 🔹 Frame-Based Temporal Analysis
- Videos are split into frames
- Each frame is passed through the **same trained CNN**
- Results are aggregated across frames

### 🔹 Outputs Generated
- Helmet vs No-Helmet frame count
- Violation severity (Low / Medium / High)
- Confidence estimation
- Temporal inconsistency warnings

> ℹ️ **Important Disclaimer**  
> Video warnings are **indicative** and based on temporal frame patterns,
> not calibrated real-world measurements.

This design avoids:
- Heavy object detection models
- Excessive GPU requirements
- Large-scale video datasets

---

## ⚠️ Traffic Warnings & Policy Layer

The system includes a **rule interpretation layer** that maps AI outputs to
human-understandable warnings:

- Helmet violation (Motor Vehicles Act, Section 129)
- Indicative erratic riding detection
- Indicative speed pattern warning

These warnings are:
- Clearly labeled
- Not presented as legal enforcement
- Designed for decision support, not automation

---

## 🏗️ System Architecture

User (Image / Video Upload)  
→ React Frontend (Dashboard UI)  
→ Flask Backend (API Layer)  
→ CNN Helmet Classifier  
→ Frame-Level Aggregation  
→ Rule Mapping & Severity Analysis  
→ Interpretable Output

---

## 🛠️ Tech Stack & Libraries

### Frontend
- React.js
- HTML / CSS
- Fetch API

### Backend
- Python 3.10
- Flask
- Flask-CORS
- OpenCV (cv2)
- NumPy

### Machine Learning
- TensorFlow 2.x
- Keras
- MobileNetV2 (pretrained weights)

---

## 🚀 How to Run

### Backend
```
cd traffic_violation_project
python app.py
```
Runs at: http://localhost:5000

### Frontend
```
cd helmet-violation-frontend
npm start
```
Runs at: http://localhost:3000

---

## 📊 Demo Walkthrough

1. Upload an image → Helmet compliance + confidence
2. Upload a video → Aggregated helmet analysis
3. Observe temporal warnings
4. Discuss scalability and future extensions

---

## 🔮 Future Scope

- Traffic signal violation detection
- FPS-calibrated speed estimation
- License plate recognition (ANPR)
- Multi-violation policy engine
- Real-time camera feed integration

---

## 🎯 Key Takeaways

- Multimodal (image + video)
- Lightweight & deployable
- Honest AI (no overclaiming)
- Extendable architecture

---

## 👤 Author

**Vishwas**
