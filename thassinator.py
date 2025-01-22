import face_recognition
import cv2
import os
import numpy as np
import time

class FrameProcessor:
    def __init__(self, known_face_encodings, known_face_names):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.last_results = []
        self.frame_count = 0
        self.process_every_n_frames = 2  # Process every nth frame
        
    def process_frame(self, frame):
        self.frame_count += 1
        
        # Skip frames to improve performance
        if self.frame_count % self.process_every_n_frames != 0:
            return self.last_results
            
        try:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert to RGB
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces with optimized parameters
            face_locations = face_recognition.face_locations(rgb_small_frame, 
                                                          model="hog",
                                                          number_of_times_to_upsample=1)
            
            if not face_locations:
                self.last_results = []
                return []

            # Get face encodings with optimized parameters
            face_encodings = face_recognition.face_encodings(rgb_small_frame, 
                                                           face_locations,
                                                           num_jitters=1,
                                                           model="small")

            results = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                status = "ACCESS DENIED"
                confidence = 0

                if len(self.known_face_encodings) > 0:
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    min_distance = face_distances[best_match_index]
                    
                    if min_distance < 0.6:
                        name = self.known_face_names[best_match_index]
                        status = "ACCESS GRANTED"
                    
                    confidence = (1 - min_distance) * 100

                # Scale coordinates back to original size
                scale = 4  # Since we resized to 0.25
                top *= scale
                right *= scale
                bottom *= scale
                left *= scale

                results.append({
                    "location": (top, right, bottom, left),
                    "name": name,
                    "status": status,
                    "confidence": round(confidence, 1)
                })

            self.last_results = results
            return results
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return self.last_results

def load_known_faces(known_faces_dir):
    """Load known faces with optimized parameters"""
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(known_faces_dir):
        print(f"Creating known_faces directory at {known_faces_dir}")
        os.makedirs(known_faces_dir)
        return known_face_encodings, known_face_names

    print("\nLoading face database...")
    
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        person_encodings = []
        image_files = [f for f in os.listdir(person_dir) 
                      if f.lower().endswith(('jpg', 'jpeg', 'png'))]
        
        if not image_files:
            continue
            
        print(f"Processing {person_name}...")
        
        for file_name in image_files:
            try:
                image_path = os.path.join(person_dir, file_name)
                image = face_recognition.load_image_file(image_path)
                # Resize image for faster processing
                small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
                encodings = face_recognition.face_encodings(small_image, 
                                                         num_jitters=1,
                                                         model="small")
                
                if encodings:
                    person_encodings.append(encodings[0])
                    print(f"  Processed {file_name}")
                
            except Exception as e:
                print(f"  Error processing {file_name}: {str(e)}")
                continue

        if person_encodings:
            average_encoding = np.mean(person_encodings, axis=0)
            known_face_encodings.append(average_encoding)
            known_face_names.append(person_name)
            print(f"Successfully loaded {len(person_encodings)} images for {person_name}")

    print(f"\nFace database loaded successfully! {len(known_face_names)} people in database.")
    return known_face_encodings, known_face_names

def main():
    try:
        print("Initializing face recognition system...")
        known_faces_dir = "known_faces"
        
        # Load face database
        known_face_encodings, known_face_names = load_known_faces(known_faces_dir)
        
        # Initialize frame processor
        frame_processor = FrameProcessor(known_face_encodings, known_face_names)

        # Initialize video capture
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            raise Exception("Could not open webcam")

        # Set video capture properties
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_capture.set(cv2.CAP_PROP_FPS, 30)
        video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        print("\nPress 'q' to quit")
        
        fps_counter = []

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Calculate FPS
            current_time = time.time()
            fps_counter = [t for t in fps_counter if t > current_time - 1]
            fps_counter.append(current_time)
            fps = len(fps_counter)

            # Process frame
            results = frame_processor.process_frame(frame)

            # Draw results
            for result in results:
                top, right, bottom, left = result["location"]
                color = (0, 255, 0) if result["status"] == "ACCESS GRANTED" else (0, 0, 255)
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                
                # Modified to only show access status
                label = result['status']
                cv2.putText(frame, label, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            # Display FPS
            cv2.putText(frame, f"FPS: {fps}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        print("Cleaning up...")
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()