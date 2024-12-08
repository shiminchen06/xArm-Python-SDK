from xarm.wrapper import XArmAPI
import time
import serial
import threading

# Connect to the arm
arm = XArmAPI('192.168.1.155', 18333)

# Connect to Arduino
# arduino = serial.Serial(port='/dev/cu.usbmodem34B7DA661E382', baudrate=9600, timeout=1)  # Adjust port for your system
# time.sleep(2)  # Wait for Arduino to initialize

# Function to read data from Arduino
# def read_sensor_data():
#     if arduino.in_waiting > 0:  # Check if data is available
#         try:
#             data = arduino.readline().decode('utf-8').strip()  # Read and decode data
#             return float(data)  # Convert to float for comparison
#         except ValueError:
#             print("Invalid sensor data received.")
#             return None
#     return None

# Ensure robot is ready for operation
arm.motion_enable(enable=True)
arm.set_state(0)

# # Function to get and print the current position
def print_position():
    while True:
        # Get the position from the arm
        code, current_position = arm.get_position(is_radian=False)  # Ensure units are not in radians
        if code == 0 and len(current_position) == 6:  # Check for success
            print("Current Position:")
            print("x =", current_position[0], ",y =", current_position[1], ",z =", current_position[2])
            print(",roll =", current_position[3], ",pitch =", current_position[4], ",yaw =", current_position[5],",")
        else:
            print("Failed to retrieve position. Error code:", code)
        time.sleep(10)  # Print position every 3 seconds
        
# Start a thread to continuously print the current position
position_thread = threading.Thread(target=print_position, daemon=True)
position_thread.start()
while True:
    time.sleep(1)  # Keep the main program alive