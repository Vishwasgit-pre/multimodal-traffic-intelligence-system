from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
import tempfile

app = Flask(__name__)
CORS(app)

# Load trained model
model = tf.keras.models.load_model("helmet_model.h5")

IMG_SIZE = 224
THRESHOLD = 0.5

# ---------- FRAME PREDICTION ----------
def predict_frame(frame):
    frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    frame = frame / 255.0
    frame = np.expand_dims(frame, axis=0)
    pred = model.predict(frame, verbose=0)[0][0]
    return float(pred)

# ---------- MAIN DETECTION API ----------
@app.route("/detect", methods=["POST"])
def detect():
    file = request.files["file"]
    filename = file.filename.lower()

    # ================= IMAGE =================
    if filename.endswith((".jpg", ".jpeg", ".png")):
        img = cv2.imdecode(
            np.frombuffer(file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        pred = predict_frame(img)

        # ✅ CORRECT MAPPING
        if pred < THRESHOLD:
            result = "HELMET"
            confidence = round((1 - pred) * 100, 2)
            rule_status = "COMPLIANT"
        else:
            result = "NO_HELMET"
            confidence = round(pred * 100, 2)
            rule_status = "VIOLATED"

        return jsonify({
            "result": result,
            "confidence": confidence,
            "rule": {
                "name": "Helmet Mandatory Rule (Section 129, Motor Vehicles Act)",
                "status": rule_status
            }
        })

    # ================= VIDEO =================
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        video_path = temp.name

    cap = cv2.VideoCapture(video_path)

    helmet_frames = 0
    no_helmet_frames = 0
    frame_results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        pred = predict_frame(frame)

        # ✅ CORRECT MAPPING
        if pred < THRESHOLD:
            helmet_frames += 1
            frame_results.append("HELMET")
        else:
            no_helmet_frames += 1
            frame_results.append("NO_HELMET")

    cap.release()

    # ✅ SAFE FILE CLEANUP (Windows-safe)
    try:
        os.remove(video_path)
    except:
        pass

    violation = no_helmet_frames > helmet_frames

    rule_status = "VIOLATED" if violation else "COMPLIANT"

    return jsonify({
        "helmet_frames": helmet_frames,
        "no_helmet_frames": no_helmet_frames,
        "violation": violation,
        "rule": {
            "name": "Helmet Mandatory Rule (Section 129, Motor Vehicles Act)",
            "status": rule_status
        },
        "speed_estimation": "Moderate (Indicative)",
        "frame_results": frame_results
    })

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
