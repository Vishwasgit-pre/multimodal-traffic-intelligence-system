from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
import tempfile
import time

app = Flask(__name__)

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001"
        ]
    }
})

# Load trained model
MODEL_PATH = "helmet_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

IMG_SIZE = 224


# -----------------------------
# Utility: preprocess image
# -----------------------------
def preprocess_image(img):
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# -----------------------------
# Predict single image
# NOTE: Model outputs probability of NO HELMET
# -----------------------------
def predict_image(img):
    img = preprocess_image(img)
    pred = model.predict(img)[0][0]
    return pred


# -----------------------------
# Main detect endpoint
# -----------------------------
@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = file.filename.lower()

    # Create temp file safely (Windows-safe)
    suffix = os.path.splitext(filename)[1]
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file.save(temp.name)
    temp.close()  # IMPORTANT for Windows

    try:
        # ================= IMAGE =================
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img = cv2.imread(temp.name)

            if img is None:
                return jsonify({"error": "Invalid image"}), 400

            pred = predict_image(img)

            # ✅ FIXED LABEL LOGIC
            if pred < 0.5:
                result = "HELMET"
                confidence = (1 - pred) * 100
            else:
                result = "NO HELMET"
                confidence = pred * 100

            return jsonify({
                "type": "image",
                "result": result,
                "confidence": round(confidence, 2)
            })


        # ================= VIDEO =================
        elif filename.endswith((".mp4", ".avi", ".mov")):
            cap = cv2.VideoCapture(temp.name)

            if not cap.isOpened():
                return jsonify({"error": "Invalid video"}), 400

            frame_count = 0
            helmet_frames = 0
            no_helmet_frames = 0

            print("\n🎥 VIDEO ANALYSIS STARTED")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Sample every 10th frame (fast + stable)
                if frame_count % 10 != 0:
                    continue

                pred = predict_image(frame)

                # ✅ FIXED LABEL LOGIC
                if pred < 0.5:
                    helmet_frames += 1
                    print(f"Frame {frame_count}: ✅ HELMET")
                else:
                    no_helmet_frames += 1
                    print(f"Frame {frame_count}: 🚨 NO HELMET")

            cap.release()

            violation = no_helmet_frames > helmet_frames

            return jsonify({
                "type": "video",
                "frames_processed": helmet_frames + no_helmet_frames,
                "helmet_frames": helmet_frames,
                "no_helmet_frames": no_helmet_frames,
                "violation": violation
            })

        else:
            return jsonify({"error": "Unsupported file type"}), 400

    finally:
        # ✅ SAFE CLEANUP (no crash on Windows)
        try:
            time.sleep(0.2)  # allow file handles to close
            if os.path.exists(temp.name):
                os.remove(temp.name)
        except PermissionError:
            print("⚠️ Temp file cleanup skipped (still in use)")



# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
