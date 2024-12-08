from xarm.wrapper import XArmAPI
import time
from threading import Thread
from pythonosc import udp_client

# Connect to the arm
arm = XArmAPI('192.168.1.155', 18333)

# OSC server details
OSC_IP = "192.168.1.12"  # Replace with the IP of your OSC server
OSC_PORT = 8000       # Replace with the port of your OSC server

# Initialize OSC client
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# Function to send data via OSC
def send_via_osc(address, data):
    """Send data to the given OSC address."""
    osc_client.send_message(address, data)
    print(f"Sent {address}: {data}")
    


# Function to fetch and send xArm information via OSC

def get_arm_info():
    try:
        # Retrieve joint angles
        joint_angles = arm.angles
        if joint_angles is not None:
            send_via_osc("/xarm/joint_angles", joint_angles)

        # Retrieve joint temperatures
        joint_temperatures = arm.temperatures
        if joint_temperatures is not None:
            send_via_osc("/xarm/joint_temperatures", joint_temperatures)

        ft_data = arm.ft_raw_force()  # Call the raw force function
        print(f"ft_raw_force output: {ft_data}")  # Debugging output
 

        # Retrieve servo voltages
        servo_voltages = arm.voltages
        if servo_voltages is not None:
            send_via_osc("/xarm/servo_voltages", servo_voltages)

        # Debugging output
        print("=== xArm Information ===")
        print(f"Joint Angles (degrees): {joint_angles}")
        print(f"Joint Temperatures (°C): {joint_temperatures}")
        print(f"Joint Forces: {ft_data}")
        print(f"Servo Voltages: {servo_voltages}")
        print("=========================\n")

    except Exception as e:
        print(f"Error fetching arm information: {e}")


# Continuous monitoring of the arm's information
def monitor_arm():
    print("Starting monitoring of xArm... Press Ctrl+C to stop.")
    try:
        while True:
            get_arm_info()
            time.sleep(0.1)  # Send data every 1 second
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    finally:
        arm.disconnect()

if __name__ == "__main__":
    # Initialize the arm
    arm.clean_error()
    arm.motion_enable(enable=True)
    arm.set_mode(0)  # Position control mode
    arm.set_state(0)  # Ready state

    # Start monitoring
    monitor_arm()
