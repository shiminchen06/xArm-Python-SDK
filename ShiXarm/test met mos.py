from xarm.wrapper import XArmAPI
import time
import serial
import threading

# Connect to the arm
arm = XArmAPI('192.168.1.155', 18333)

# Connect to Arduino
arduino = serial.Serial(port='/dev/cu.usbmodem34B7DA661E382', baudrate=9600, timeout=1)  # Adjust port for your system
time.sleep(2)  # Wait for Arduino to initialize

# Function to read data from Arduino
def read_sensor_data():
    if arduino.in_waiting > 0:  # Check if data is available
        try:
            data = arduino.readline().decode('utf-8').strip()  # Read and decode data
            return float(data)  # Convert to float for comparison
        except ValueError:
            print("Invalid sensor data received.")
            return None
    return None



# Function to move the arm to a specific position
def move_arm_to_position(x, y, z, roll, pitch, yaw, speed=50, wait=False, radius=5):
    arm.set_position(x, y, z, roll, pitch, yaw, speed=speed, wait=wait, radius=radius)
    print(f"Arm moved to position: x={x}, y={y}, z={z}, roll={roll}, pitch={pitch}, yaw={yaw}")

# Ensure robot is ready for operation
arm.motion_enable(enable=True)
arm.set_state(0)

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

# Main loop to monitor Arduino and move the arm
try:
    while True:
        sensor_value = read_sensor_data()
        if sensor_value is not None:
            print(f"Sensor Value: {sensor_value}")
            if sensor_value > 60:
                print("Sensor value exceeded threshold, moving arm to position 1")
                # Move arm to position 1
                move_arm_to_position(
                    x=234.424637, y=-223.125153, z=86.248451,  # Replace with desired coordinates
                    roll=-3.112597, pitch=-0.018961, yaw=-0.946951,
                    speed=150, wait=False, radius=5
                )
                # Uncomment the line to control the gripper when sensor value exceeds threshold
                # arm.open_lite6_gripper()
            else:
                print("Sensor value below threshold, moving arm to position 2")
                # Move arm to position 2
                move_arm_to_position(
                    x=221, y=-185.5, z=64.7,  # Replace with desired coordinates
                    roll=-178.7, pitch=-5.7, yaw=-54.3,
                    speed=150, wait=False, radius=5
                )
                


                # Uncomment the line to control the gripper when sensor value is below threshold
                # arm.close_lite6_gripper()
        else:
            print("No valid sensor data received.")
        time.sleep(1)  # Check sensor value every second
        
        
        
        
except KeyboardInterrupt:
    print("Exiting program.")
    arm.disconnect()
 