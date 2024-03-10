import cv2
import datetime
import imutils
import numpy as np
import serial
import time

def send_command(ser, command):
    """Send a command to the Arduino via serial communication."""
    ser.write(command.encode())

def main():
    """Main function to perform real-time object detection and LED control."""
    # Initialize variables
    curr = time.time()
    arduino_port = 'COM7' # Specify the port where the Arduino is connected
    ser = serial.Serial(arduino_port, 9600, timeout=1)
    ledstate = False
    ldrstate = False
    
    # List of classes for object detection
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    
    # Load pre-trained model for object detection
    protopath = "MobileNetSSD_deploy.prototxt"
    modelpath = "MobileNetSSD_deploy.caffemodel"
    detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
    
    # Start video capture
    cap = cv2.VideoCapture(1)  # Initialize video capture from the second camera device (in my case index 1 , but can also be 0 in your case)
    fps_start_time = datetime.datetime.now()
    total_frames = 0

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()
        
        # Resize frame for faster processing
        frame = imutils.resize(frame, width=600)
        total_frames += 1

        # Extract frame dimensions
        (H, W) = frame.shape[:2]

        # Preprocess frame for object detection
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)

        # Pass preprocessed frame to object detector
        detector.setInput(blob)
        person_detections = detector.forward()

        # Check if a person is detected
        person_detected = False
        for i in np.arange(0, person_detections.shape[2]):
            confidence = person_detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(person_detections[0, 0, i, 1])
                if CLASSES[idx] == "person":
                    person_detected = True
                    (startX, startY, endX, endY) = (int(person_detections[0, 0, i, 3] * W),
                                                    int(person_detections[0, 0, i, 4] * H),
                                                    int(person_detections[0, 0, i, 5] * W),
                                                    int(person_detections[0, 0, i, 6] * H))
                    # Draw bounding box around the person
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    break
        
        # Read the serial data from the Arduino
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("LDR_VALUE"):
                ldr_value = int(line.split(":")[1])
                print("Received LDR value:", ldr_value)
                # Control LED based on LDR value
                if ldr_value < 50:
                    if not ledstate:  # If LED is off, turn it on
                        send_command(ser, "PIN_ON\n")
                        print("LED on - Low light")
                        ledstate = True
                else:
                    if ledstate and time.time() - curr > 2:  # If LED is on and sufficient light for 2 seconds, turn it off
                        send_command(ser, "PIN_OFF\n")
                        print("LED off - Sufficient light")
                        ledstate = False

        # Control LED based on presence of person
        if person_detected:
            curr = time.time()
            if not ledstate:  # If LED is off, turn it on
                send_command(ser, "PIN_ON\n")
                print("LED on - Person detected")
                ledstate = True
        else:
            if ledstate and time.time() - curr > 2 and ldr_value > 50:  # If LED is on and no person detected for 2 seconds, turn it off
                send_command(ser, "PIN_OFF\n")
                print("LED off - Person not detected")
                ledstate = False
        
        # Display FPS on the frame
        fps_end_time = datetime.datetime.now()
        time_diff = fps_end_time - fps_start_time
        if time_diff.seconds == 0:
            fps = 0.0
        else:
            fps = (total_frames / time_diff.seconds)

        fps_text = "FPS: {:.2f}".format(fps)
        cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

        # Display frame
        cv2.imshow("Application", frame)

        # Check for user input to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
