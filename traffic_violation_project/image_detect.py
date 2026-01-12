import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sys

MODEL_PATH = "helmet_model.h5"

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]

    if prediction < 0.5:
        return "✅ HELMET DETECTED"
    else:
        return "🚨 HELMET VIOLATION DETECTED"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_detect.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    result = predict_image(img_path)
    print(result)
