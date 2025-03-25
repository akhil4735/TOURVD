from ultralytics import YOLO
import cv2
import os

# Define the model path
MODEL_DIR = "models/yolo_weights/"
MODEL_PATH = os.path.join(MODEL_DIR, "yolov8n.pt")

# Ensure the directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Download YOLO model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    model.export(format="torchscript")
    os.rename("yolov8n.pt", MODEL_PATH)
else:
    print("Using existing YOLO model.")

# Load the YOLO model
model = YOLO(MODEL_PATH)

class VehicleDetector:
    def __init__(self, model):
        self.model = model
        self.class_names = self.model.names

    def detect_vehicles(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls)
                class_name = self.class_names[class_id]
                confidence = float(box.conf)

                # Only detect vehicles (car, truck, bus, motorcycle)
                if class_name in ["car", "truck", "bus", "motorcycle"]:
                    detections.append({
                        "bbox": (x1, y1, x2, y2),
                        "class_name": class_name,
                        "confidence": confidence,
                    })
        return detections

    def visualize_detections(self, frame, detections):
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            class_name = detection["class_name"]
            confidence = detection["confidence"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame

# Initialize the detector
detector = VehicleDetector(model)

# --- IMAGE PROCESSING ---
image_path = "data/raw/vehicle_image.jpg"
if os.path.exists(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
    else:
        detections = detector.detect_vehicles(image)
        for det in detections:
            print(f"Detected: {det['class_name']} ({det['confidence']:.2f})")
        annotated_image = detector.visualize_detections(image, detections)
        cv2.imshow("Vehicle Detection - Image", annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print(f"Error: Image file not found at {image_path}")

# --- VIDEO PROCESSING ---
video_path = "data/raw/sherbrooke_video.avi"
if os.path.exists(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
    else:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            detections = detector.detect_vehicles(frame)
            annotated_frame = detector.visualize_detections(frame, detections)

            cv2.imshow("Vehicle Detection - Video", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
else:
    print(f"Error: Video file not found at {video_path}")
