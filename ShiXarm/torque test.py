from xarm.wrapper import XArmAPI
import time

# Verbinding maken met de arm
arm = XArmAPI('192.168.1.155', 18333)

def test_force_data():
    try:
        print("Starting force data test... Press Ctrl+C to stop.")
        while True:
            # Haal de rauwe kracht- en momentgegevens op
            ft_data = arm.ft_raw_force()

            # Zorg ervoor dat de gegevens een lijst zijn
            if isinstance(ft_data, list) and len(ft_data) == 6:
                # Haal de krachten en momenten op uit de lijst
                Fx, Fy, Fz, Mx, My, Mz = ft_data
                print(f"Force/Torque Data: Fx={Fx}, Fy={Fy}, Fz={Fz}, Mx={Mx}, My={My}, Mz={Mz}")
            else:
                print(f"Onverwacht formaat: {ft_data}")

            time.sleep(0.1)  # Update elke 100ms
    except KeyboardInterrupt:
        print("Test gestopt.")
    except Exception as e:
        print(f"Fout bij ophalen kracht data: {e}")
    finally:
        arm.disconnect()

if __name__ == "__main__":
    # Initialiseer de arm
    arm.clean_error()
    arm.motion_enable(enable=True)
    arm.set_mode(0)  # Positiemodus
    arm.set_state(0)  # Klaarstaat

    # Start de test
    test_force_data()
