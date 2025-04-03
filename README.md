# README: Troubleshooting Guide for Face & Voice Recognition with Arduino Servo Control

## **Project Overview**
This project detects a face using a TensorFlow Lite model, listens for a password via voice recognition, and activates a servo motor if the correct password ("Bailey") is spoken. The Arduino receives a command from Python and rotates the servo motor 90 degrees before resetting.

---

## **Common Errors & Fixes**

### **1. Serial Port Issues (COM Port Not Found)**
**Error:**
- `serial.SerialException: could not open port 'COMX': FileNotFoundError`  
- `PermissionError: [Errno 13] Access is denied: 'COMX'`

**Fix:**
- Ensure the **correct COM port** is used. If your Arduino is connected to **COM3**, update this in Python:  
  ```python
  arduino = serial.Serial('COM3', 9600)
  ```
- Check **Device Manager** (Windows) or `ls /dev/tty*` (Mac/Linux) to find the correct port.
- Close any other program (like the Arduino IDE Serial Monitor) that may be **blocking access**.
- Restart the Arduino and reconnect.

---

### **2. Speech Recognition Errors**
**Error:**
- `speech_recognition.RequestError: Could not request results from Google Speech Recognition service`
- `speech_recognition.UnknownValueError: Speech Recognition could not understand the audio`

**Fix:**
- Ensure you have **an active internet connection** (Google Speech API requires it).
- Speak clearly and **reduce background noise**.
- If using a **wireless microphone**, check its connection.
- Try an **offline model** like **Vosk** or **Whisper** if needed.

---

### **3. Face Detection Model Issues**
**Error:**
- `tensorflow.lite.Interpreter: Error loading model file`
- `ValueError: Could not set tensor: data type mismatch`

**Fix:**
- Ensure the **model path is correct**:
  ```python
  model_path = r"C:\Users\iatpuser\Downloads\model_unquant.tflite"
  ```
- Verify that the model **expects the correct input shape** (e.g., 224x224 images, float32 format).
- If using a different model, update preprocessing accordingly.

---

### **4. Servo Motor Not Responding**
**Error:**
- `Servo not moving when correct password is spoken.`
- `Arduino receiving signal, but no motor movement.`

**Fix:**
- Check **servo wiring**:
  - Red (VCC) → **5V on Arduino**
  - Black/Brown (GND) → **GND on Arduino**
  - Yellow/White (Signal) → **Pin 9 on Arduino**
- Ensure Arduino **code is uploaded correctly**.
- Run a simple **test script** to check if the servo responds:
  ```cpp
  #include <Servo.h>
  Servo myServo;
  void setup() {
      myServo.attach(9);
      myServo.write(90);  // Move to 90 degrees
  }
  void loop() {}
  ```

---

### **5. Python Not Communicating with Arduino**
**Error:**
- `Serial.write() command sent, but Arduino not reacting`

**Fix:**
- Add a **small delay** after opening the serial connection:
  ```python
  arduino = serial.Serial('COM3', 9600)
  time.sleep(2)  # Wait for Arduino to initialize
  ```
- Verify **Python is sending "TRIGGER" correctly**:
  ```python
  arduino.write(b"TRIGGER\n")
  ```
- Use the Arduino **Serial Monitor** to check if it’s receiving data.

---

## **Final Checklist Before Running**
 **Arduino COM port is correct**  
 **Servo motor is wired properly**  
 **Face detection model is loaded successfully**  
 **Speech recognition is working**  
 **Python can send signals to Arduino**  

---

## **Need More Help?**
If issues persist, check:
- **Arduino Serial Monitor** (`Tools > Serial Monitor`) for errors.
- **Python console** for error messages.
- **Device Manager** (Windows) or `ls /dev/tty*` (Mac/Linux) for correct ports.



