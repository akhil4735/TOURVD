from ultralytics import YOLO
import cv2
import os

# Define YOLO model path
MODEL_DIR = "models/yolo_weights/"
MODEL_PATH = os.path.join(MODEL_DIR, "yolov8n.pt")
os.makedirs(MODEL_DIR, exist_ok=True)

# Load YOLO Model
model = YOLO(MODEL_PATH)

class VehicleDensityCalculator:
    def __init__(self):
        self.model = model
        self.class_names = self.model.names  # Class names (e.g., car, bus, truck, etc.)

    def count_vehicles(self, frame):
        results = self.model(frame)

        # Initialize vehicle counts
        vehicle_counts = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorcycle": 0
        }

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                class_name = self.class_names[class_id]

                if class_name in vehicle_counts:
                    vehicle_counts[class_name] += 1

        return vehicle_counts

    def display_density(self, frame, vehicle_counts):
        """Display vehicle count for each type separately."""
        y_offset = 50  # Start position for text display
        for vehicle, count in vehicle_counts.items():
            text = f"{vehicle.capitalize()}: {count}"
            cv2.putText(frame, text, (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            y_offset += 40  # Move text down for next vehicle type
        return frame

# Process video
if __name__ == "__main__":
    calculator = VehicleDensityCalculator()
    video_path = "data/raw/sherbrooke_video.avi"

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        vehicle_counts = calculator.count_vehicles(frame)
        frame = calculator.display_density(frame, vehicle_counts)

        print(f"Vehicle Counts: {vehicle_counts}")  # Print vehicle count in terminal

        cv2.imshow("Vehicle Density Calculation", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
