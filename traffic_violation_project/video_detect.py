import cv2
import numpy as np
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("helmet_model.h5")

IMG_SIZE = 224

def predict_frame(frame):
    frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    frame = frame / 255.0
    frame = np.expand_dims(frame, axis=0)
    prediction = model.predict(frame, verbose=0)[0][0]
    return prediction

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    frame_num = 0
    checked_frames = 0
    no_helmet_frames = 0

    print(f"\nProcessing video: {video_path}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1

        # Process every 5th frame
        if frame_num % 5 != 0:
            continue

        checked_frames += 1
        pred = predict_frame(frame)

        if pred < 0.6:
            no_helmet_frames += 1
            print(f"Frame {frame_num}: ❌ NO HELMET")
        else:
            print(f"Frame {frame_num}: ✅ HELMET")

    cap.release()

    if checked_frames == 0:
        print("No frames processed.")
        return

    ratio = no_helmet_frames / checked_frames
    print(f"No-helmet frame ratio: {ratio:.2f}")

    if ratio > 0.3:
        print("🚨 HELMET VIOLATION DETECTED")
    else:
        print("✅ NO HELMET VIOLATION FOUND")


# ================= MAIN EXECUTION =================

print("\n--- Checking HELMET video ---")
process_video("test_videos/helmet_video.mp4")

print("\n--- Checking NO-HELMET video ---")
process_video("test_videos/no_helmet_video.mp4")
