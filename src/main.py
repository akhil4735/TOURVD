# import cv2
# import os
# from imageprocessing.vehicledetection import VehicleDetector
# from imageprocessing.vehicleclassification import VehicleClassifier

# # Paths
# VIDEO_PATH = "data/raw/sherbrooke_video.avi"  # Update with actual video source
# MODEL_PATH_DETECTION = "models/yolo_weights/yolov8n.pt"
# MODEL_PATH_CLASSIFICATION = "models/custom_models/vehicle_classifier.pth"

# # Initialize models
# detector = VehicleDetector(model_path=MODEL_PATH_DETECTION)
# classifier = VehicleClassifier(model_path=MODEL_PATH_CLASSIFICATION)

# def process_frame(frame):
#     """
#     Process a video frame: detect and classify vehicles.
    
#     Args:
#         frame (numpy.ndarray): Input frame.
    
#     Returns:
#         numpy.ndarray: Frame with detection and classification results.
#     """
#     # Detect vehicles
#     detections = detector.detect_vehicles(frame)

#     for detection in detections:
#         x1, y1, x2, y2 = detection["bbox"]
#         cropped_vehicle = frame[y1:y2, x1:x2]  # Crop detected vehicle

#         # Classify vehicle type
#         vehicle_type = classifier.classify_vehicle(cropped_vehicle)
#         detection["class_name"] = vehicle_type  # Update class name

#         # Draw bounding boxes & labels
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         label = f"{vehicle_type} ({detection['confidence']:.2f})"
#         cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#     return frame

# def main():
#     # Check if video exists
#     if not os.path.exists(VIDEO_PATH):
#         print(f"Error: Video file not found at {VIDEO_PATH}")
#         return

#     cap = cv2.VideoCapture(VIDEO_PATH)
    
#     if not cap.isOpened():
#         print("Error: Could not open video file")
#         return

#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break

#         # Process frame
#         processed_frame = process_frame(frame)

#         # Display result
#         cv2.imshow("Vehicle Detection & Classification", processed_frame)

#         # Exit on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
