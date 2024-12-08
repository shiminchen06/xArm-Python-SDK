import time
import random
from threading import Thread
from pythonosc import udp_client
from xarm.wrapper import XArmAPI  # Only used when not in simulation mode

# OSC server details
OSC_IP = "127.0.0.1"  # IP address of the receiving OSC server
OSC_PORT = 8000       # Port of the receiving OSC server

# Initialize OSC client
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# Function to send data via OSC
def send_via_osc(address, data):
    """Send data to the given OSC address."""
    osc_client.send_message(address, data)
    print(f"Sent {address}: {data}")

# Simulated xArmAPI for testing without a physical robot
class SimulatedXArmAPI:
    """Simulates the xArmAPI for testing without a physical xArm."""
    
    def get_servo_angle(self):
        """Simulate fetching joint angles."""
        joint_angles = [random.uniform(-180, 180) for _ in range(6)]
        return {"code": 0, "data": joint_angles}

    def get_position(self):
        """Simulate fetching Cartesian position."""
        position = [random.uniform(200, 400), random.uniform(-200, 200), random.uniform(100, 300), 
                    random.uniform(-180, 180), random.uniform(-180, 180), random.uniform(-180, 180)]
        return (0, position)

    def get_servo_angle(self, is_radian=False, is_velocity=False):
        """Simulate fetching joint velocities."""
        joint_velocities = [random.uniform(-1, 1) for _ in range(6)]
        return {"code": 0, "data": joint_velocities}

    def get_servo_torque(self):
        """Simulate fetching joint torques."""
        joint_torques = [random.uniform(-10, 10) for _ in range(6)]
        return {"code": 0, "data": joint_torques}

    def get_state(self):
        """Simulate robot state (moving, stopped, etc.)."""
        state = random.choice([0, 1, 2, 3])  # 0=stopped, 1=moving, etc.
        return {"code": 0, "data": state}

    def get_mode(self):
        """Simulate operation mode."""
        mode = random.choice([0, 1, 2])  # 0=position mode, 1=velocity mode, etc.
        return {"code": 0, "data": mode}

    def get_servo_temperature(self):
        """Simulate joint temperatures."""
        temperatures = [random.uniform(30, 60) for _ in range(6)]
        return {"code": 0, "data": temperatures}

    def motion_enable(self, enable):
        """Simulate enabling motion."""
        print(f"Simulated motion enable: {enable}")

    def set_mode(self, mode):
        """Simulate setting mode."""
        print(f"Simulated mode set to: {mode}")

    def set_state(self, state):
        """Simulate setting state."""
        print(f"Simulated state set to: {state}")

    def move_gohome(self, wait=True):
        """Simulate moving to home position."""
        print("Simulated move to home position")

    def disconnect(self):
        """Simulate disconnection."""
        print("Simulated disconnection from xArm")

# Fetch all xArm features (joint angles, position, velocity, etc.)
def fetch_and_send_xarm_features(arm):
    """Fetch and send various xArm features via OSC."""
    while True:
        # Joint angles
        joint_data = arm.get_servo_angle()
        if isinstance(joint_data, dict) and joint_data['code'] == 0:
            joint_angles = joint_data['data']
            send_via_osc("/xarm/joints", joint_angles)

        # Cartesian position (end-effector position)
        position_data = arm.get_position()
        if isinstance(position_data, tuple):
            code, position = position_data
            if code == 0:
                send_via_osc("/xarm/position", position)

        # Joint velocities
        velocity_data = arm.get_servo_angle(is_radian=False, is_velocity=True)
        if isinstance(velocity_data, dict) and velocity_data['code'] == 0:
            joint_velocities = velocity_data['data']
            send_via_osc("/xarm/velocity", joint_velocities)

        # Joint torques
        torque_data = arm.get_servo_torque()
        if isinstance(torque_data, dict) and torque_data['code'] == 0:
            joint_torques = torque_data['data']
            send_via_osc("/xarm/torque", joint_torques)

        # Robot state (moving, stopped, etc.)
        state_data = arm.get_state()
        if isinstance(state_data, dict) and state_data['code'] == 0:
            robot_state = state_data['data']
            send_via_osc("/xarm/state", robot_state)

        # Mode (e.g., position control mode, velocity control mode)
        mode_data = arm.get_mode()
        if isinstance(mode_data, dict) and mode_data['code'] == 0:
            robot_mode = mode_data['data']
            send_via_osc("/xarm/mode", robot_mode)

        # Joint temperatures (if applicable)
        temp_data = arm.get_servo_temperature()
        if isinstance(temp_data, dict) and temp_data['code'] == 0:
            joint_temperatures = temp_data['data']
            send_via_osc("/xarm/temperature", joint_temperatures)

        time.sleep(0.1)  # Send updates every 100ms

# Main program to initialize the xArm (real or simulated) and start streaming
def main(simulation_mode=False):
    """Main function to initialize xArm and start streaming data via OSC."""
    if simulation_mode:
        print("Running in simulation mode")
        arm = SimulatedXArmAPI()
    else:
        print("Running with real xArm")
        arm_ip = "192.168.1.155"  # Replace with your real xArm's IP
        arm = XArmAPI(arm_ip)
        arm.motion_enable(enable=True)
        arm.set_mode(0)
        arm.set_state(0)

    # Start streaming all xArm features in a separate thread
    feature_thread = Thread(target=fetch_and_send_xarm_features, args=(arm,))
    feature_thread.daemon = True  # Ensure the thread exits when the program ends
    feature_thread.start()

    # Move the arm to home position before starting (simulated or real)
    arm.move_gohome(wait=True)

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

    # Disconnect the arm (simulated or real)
    arm.disconnect()

if __name__ == "__main__":
    main(simulation_mode=True)  # Set to False to use real xArm
