from xarm.wrapper import XArmAPI
import time
import serial
import threading
import os

# Connect to the arm
arm = XArmAPI('192.168.1.155', 18333)

# # Connect to Arduino
# arduino = serial.Serial(port='/dev/cu.usbmodem34B7DA661E382', baudrate=9600, timeout=1)  # Adjust port for your system
# time.sleep(2)  # Wait for Arduino to initialize

# # Function to read data from Arduino
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

# Function to get and print the current position
def print_position():
    while True:
        # Get the position from the arm
        code, current_position = arm.get_position(is_radian=False)  # Ensure units are not in radians
        if code == 0 and len(current_position) == 6:  # Check for success
            print("Current Position:")
            print(f"x = {current_position[0]:.2f}, y = {current_position[1]:.2f}, z = {current_position[2]:.2f}")
            print(f"roll = {current_position[3]:.2f}, pitch = {current_position[4]:.2f}, yaw = {current_position[5]:.2f}")
        else:
            print("Failed to retrieve position. Error code:", code)
        time.sleep(3)  # Print position every 3 seconds

# Start a thread to continuously print the current position
position_thread = threading.Thread(target=print_position, daemon=True)
position_thread.start()


 
arm.set_position(
            x=206.3, y=4.3, z=471.6,
            roll=179.9, pitch=1.4, yaw=86,
            speed=150, wait=True, radius=5,
            is_radian=False
        )  
   
def loop_movements(repetitions=2):
     for i in range(repetitions):  # Loop for the specified number of repetitions  

        # Move to Position 1
        arm.set_position(
                    x=194.4, y=-77.1, z=151,
                    roll=95.6, pitch=13.8, yaw=82.4,
                    speed=150, wait=True, radius=5,
                    is_radian=False
                )
                

                # Move to Position 2
                
        arm.set_position( 
                    x=198.5, y=88.5, z=154.6,
                    roll=93.9, pitch=-16.7, yaw=94,
                    speed=150, wait=True, radius=5,
                    is_radian=False
                )

# Call the function to perform 5 repetitions
loop_movements(repetitions=2)

arm.set_position(
            x=206.3, y=4.3, z=471.6,
            roll=179.9, pitch=1.4, yaw=86,
            speed=150, wait=True, radius=5,
            is_radian=False
        ) 
        

       





# # Wait a bit for movement to complete
# time.sleep(2)

# # Check current position
# code, current_position = arm.get_position(is_radian=False)
# print("Current Position:", current_position)




# try:
#     while True:
#         sensor_value = read_sensor_data()
#         if sensor_value is not None:
#             print(f"Sensor Value: {sensor_value}")
#             if sensor_value > 60:
#                 # Ensure the arm is in a proper state before playback
#                 arm.set_state(0)
#                 if arm.load_trajectory(trajectory_file1):
#                     print("Trajectory loaded successfully.")
#                     arm.playback_trajectory(trajectory_file1)
#                 else:
#                     print("Failed to load trajectory.")
#             else:
#                 print("Sensor value below threshold, moving arm to initial position.")
#                 move_to_position(positions["position4"])
#                 arm.close_lite6_gripper()  # Adjust gripper function as needed
#         else:
#             print("No valid sensor data received.")
#         time.sleep(1)  # Check sensor value every second
# except KeyboardInterrupt:
#     print("Exiting program.")
#     arm.disconnect()

# # Keep the main program alive
# while True:
#     time.sleep(1)
