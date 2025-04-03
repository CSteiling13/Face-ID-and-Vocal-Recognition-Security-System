import cv2
import numpy as np
import tensorflow as tf
import speech_recognition as sr
import time
import serial  # Import serial library

import cv2
import numpy as np
import tensorflow as tf
import speech_recognition as sr
import time
import serial

# Connect to Arduino on COM3
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for Arduino to initialize

# Path to your TensorFlow Lite model
model_path = r"C:\Users\iatpuser\Downloads\model_unquant.tflite"

# Load the TensorFlow Lite model for face detection
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize webcam
cap = cv2.VideoCapture(0)

def preprocess_frame(frame):
    # Resize the frame to match the model input size (224x224 is an example)
    resized_frame = cv2.resize(frame, (224, 224))
    normalized_frame = resized_frame / 255.0  # Normalize pixel values
    return np.expand_dims(normalized_frame, axis=0).astype(np.float32)

def detect_face(frame):
    processed_frame = preprocess_frame(frame)
    
    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], processed_frame)
    
    # Run inference
    interpreter.invoke()

    # Get the output tensor (example: probability of a face)
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Assuming the output gives a confidence score for face detection
    confidence = output_data[0][0]
    
    return confidence

def listen_for_password():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("What is the password?")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise levels
        audio = recognizer.listen(source)  # Listen for speech

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio).lower()
        print("Heard:", text)
        
        if "bailey" in text:
            print("Correct password! Rotating motor.")
            return True
        else:
            print("Incorrect password.")
            return False

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return False
    except sr.RequestError as e:
        print(f"Request error from Google API; {e}")
        return False

def trigger_motor():
    arduino.write(b"TRIGGER\n")  # Send trigger command to Arduino
    print("Motor rotated 90 degrees!")  # Debugging message

# Main loop
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    confidence = detect_face(frame)
    
    if confidence > 0.5:  # Assuming 0.5 as threshold for detecting face
        print("Face detected!")
        if listen_for_password():  # If correct password is given
            trigger_motor()
            break  # Exit after detecting face and correct password
    else:
        print("No face detected.")
    
    cv2.imshow("Webcam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
