# Replicating Smart LED Project

## Introduction

This document provides a step-by-step guide to replicate the Smart LED project, which involves real-time object detection using a webcam and controlling an LED based on the presence of a person and the ambient light level.

## Requirements

### Hardware

- Computer with Python installed
- Arduino board (e.g., Arduino Uno)
- LDR (Light Dependent Resistor)
- Relay module
- LED
- Jumper wires
- Webcam

### Software

- Arduino IDE
- Python 3.x
- OpenCV (cv2)
- NumPy
- PySerial
- imutils


### Arduino Setup

- One leg of the LDR is connected to 5V.
- The other leg of the LDR is connected to one leg of a 1kΩ resistor.
- The other leg of the resistor is connected to ground (GND).
- The common connection between the LDR and the resistor is connected to analog pin A0.
- Additionally, the relay connected to pin 10 controls the LED.
- Open Arduino IDE and upload the provided Arduino code (`smart_led_arduino.ino`) to the Arduino board.

### Python Setup

1. Install Python 3.x from the official website: [Python.org](https://www.python.org/)
2. Install imutils, OpenCV, NumPy, and PySerial using pip:

## Circuit Diagram
![Screenshot 2024-03-10 183445](https://github.com/dev-harshdeep/Smart-LED/assets/148332227/d947bc47-97ae-473e-9eed-6d3df98971bd)

## Running the Project

1. Connect the Arduino board to your computer via USB.
2. Run the Python script (`smart_led.py`) to start the object detection and LED control process.
   ```
   python smart_led.py
   ```

## Conclusion

By following the steps outlined in this document, you should be able to replicate the Smart LED project successfully.
