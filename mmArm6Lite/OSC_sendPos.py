import time
from pythonosc import udp_client
from threading import Thread
from xarm.wrapper import XArmAPI

# OSC server details (replace with your OSC server's IP and port)
OSC_IP = "192.168.1.10"  # Change to the actual IP of your OSC server
OSC_PORT = 8000       # Change to the actual port of your OSC server

# Initialize OSC client
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# Function to send position data via OSC
def send_position_via_osc(position):
    """Send end-effector position data via OSC"""
    if len(position) >= 3:
        x, y, z = position[:3]
        osc_client.send_message("/xarm/position", [x, y, z])
        print(f"Sent position via OSC: x={x}, y={y}, z={z}")
    else:
        print("Invalid position data, not enough values:", position)

# Function to stream position data continuously
def stream_position_data(arm):
    """Continuously fetch and send the current position of the arm in real-time"""
    while True:
        pos_data = arm.get_position()
        if isinstance(pos_data, tuple):
            code, position = pos_data
            if code == 0 and position:
                send_position_via_osc(position)
            else:
                print(f"Error code: {code}, position data: {position}")
        else:
            print(f"Unexpected data type: {type(pos_data)}")
        time.sleep(0.05)

# Function to perform circular movement x times with adjusted settings
def perform_circular_motion(arm, repetitions=3):
    """Perform a circular movement with adjusted parameters 'repetitions' times"""
    # Define two poses for the circular movement with a larger radius
    pose1 = [150, 100, 150, -180, 0, 0]  # First point of the arc
    pose2 = [300, 100, 150, -180, 0, 0]  # Second point of the arc

    # Reduced speed and acceleration (30%)
    speed = 200 * 0.3  # 30% of 200
    mvacc = 1000 * 0.3  # 30% of 1000

    # Circular movement 'percent' should be moderate (try 50-100)
    percent = 50  # Circular arc length

    for i in range(repetitions):
        print(f"Starting circular movement iteration {i+1}")
        ret = arm.move_circle(pose1=pose1, pose2=pose2, percent=percent, speed=speed, mvacc=mvacc, wait=True)
        if ret != 0:
            print(f"Error during circular movement iteration {i+1}: {ret}")
        else:
            print(f"Circular movement iteration {i+1} completed")
        time.sleep(0.5)  # Short pause between movements

# Main program to initialize the arm and start streaming position data
def main():
    # Replace with your xArm Lite's IP address
    arm_ip = "192.168.1.155"  
    arm = XArmAPI(arm_ip)

    # Enable motion and set the state
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    # Test: Send a test message via OSC to verify the connection is working
    osc_client.send_message("/xarm/test", "Test message sent!")
    print("Test OSC message sent")

    # Start streaming position data in a separate thread
    position_thread = Thread(target=stream_position_data, args=(arm,))
    position_thread.daemon = True  # Ensure the thread exits when the program ends
    position_thread.start()

    # Move the arm to home position before starting
    arm.move_gohome(wait=True)

    # Perform circular motion 5 times with adjusted settings
    perform_circular_motion(arm, repetitions=5)

    # Return to home position
    arm.move_gohome(wait=True)

    # Stop the arm and disconnect
    arm.disconnect()

if __name__ == "__main__":
    main()
