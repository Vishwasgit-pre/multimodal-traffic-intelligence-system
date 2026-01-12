from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
import tempfile

app = Flask(__name__)

# 🔴 IMPORTANT: SIMPLE GLOBAL CORS (NO ORIGINS FILTER)
CORS(app, supports_credentials=True)

# ------------------- MODEL -------------------
model = tf.keras.models.load_model("helmet_model.h5")
IMG_SIZE = 224

def preprocess_image(img):
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    return np.expand_dims(img, axis=0)

# ------------------- ROUTE -------------------
@app.route("/detect", methods=["POST", "OPTIONS"])
def detect():
    if request.method == "OPTIONS":
        # 🔴 Explicitly handle preflight
        return jsonify({"status": "ok"}), 200

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename.lower()

    # -------- IMAGE --------
    if filename.endswith((".png", ".jpg", ".jpeg")):
        img = cv2.imdecode(
            np.frombuffer(file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        img = preprocess_image(img)
        pred = model.predict(img)[0][0]

        return jsonify({
            "type": "image",
            "result": "NO HELMET 🚨" if pred > 0.5 else "HELMET ✅",
            "confidence": float(pred)
        })

    # -------- VIDEO --------
    elif filename.endswith((".mp4", ".avi", ".mov", ".mkv")):
        temp = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp.name)

        cap = cv2.VideoCapture(temp.name)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 1

        helmet, no_helmet = 0, 0
        idx, processed = 0, 0

        print("\n🎥 VIDEO ANALYSIS STARTED")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if idx % fps == 0:
                processed += 1
                img = preprocess_image(frame)
                pred = model.predict(img)[0][0]

                if pred > 0.5:
                    no_helmet += 1
                    print(f"Frame {processed}: 🚨 NO HELMET")
                else:
                    helmet += 1
                    print(f"Frame {processed}: ✅ HELMET")

            idx += 1

        cap.release()
  

        final = "VIOLATION DETECTED 🚨" if no_helmet > helmet else "NO VIOLATION ✅"

        print("📊 SUMMARY:", final)

        return jsonify({
            "type": "video",
            "frames_processed": processed,
            "helmet_frames": helmet,
            "no_helmet_frames": no_helmet,
            "final_decision": final
        })

    return jsonify({"error": "Unsupported format"}), 400


if __name__ == "__main__":
    # 🔴 Disable reloader (important)
    app.run(port=5000, debug=True, use_reloader=False)
