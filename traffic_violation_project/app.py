from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # VERY IMPORTANT for React connection

# Load trained model
model = tf.keras.models.load_model("helmet_model.h5")

@app.route("/", methods=["GET"])
def home():
    return "Helmet Detection Backend is Running"

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    try:
        # Load and preprocess image
        img = Image.open(file).convert("RGB")
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict
        prediction = model.predict(img)[0][0]

        if prediction < 0.5:
            return jsonify({"result": "HELMET"})
        else:
            return jsonify({"result": "NO_HELMET"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
