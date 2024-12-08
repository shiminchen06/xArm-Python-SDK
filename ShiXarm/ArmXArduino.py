from xarm.wrapper import XArmAPI
import time
import serial


# Connect to the arm
arm = XArmAPI('192.168.1.155', 18333)

# Connect to Arduino
arduino = serial.Serial(port='/dev/cu.usbmodem34B7DA661E382', baudrate=9600, timeout=1)  # Adjust port for your system
time.sleep(2)  # Wait for Arduino to initialize

#ensure serial monitor in arduino IDE is closed

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

# Main loop to monitor Arduino and move the arm
try:
    while True:
        sensor_value = read_sensor_data()
        if sensor_value is not None:
            print(f"Sensor Value: {sensor_value}")
            if sensor_value > 60:
                print("Sensor value exceeded threshold, moving arm to position 1")
                move_arm_to_position(
                    x=234.424637, y=-223.125153, z=86.248451,  # Replace with desired coordinates
                    roll=-3.112597, pitch=-0.018961, yaw=-0.946951,
                    speed=150, wait=False, radius=5
                )
            else:
                print("Sensor value below threshold, moving arm to position 2")
                move_arm_to_position(
                    x=231.172562, y=201.517502, z=381.067108,  # Replace with desired coordinates
                    roll=3.129562, pitch=-0.002496, yaw=-0.305295,
                    speed=150, wait=False, radius=5
                )
        else:
            print("No valid sensor data received.")
        time.sleep(1)  # Check sensor value every second
except KeyboardInterrupt:
    print("Exiting program.")
    arm.disconnect()
