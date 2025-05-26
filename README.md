# MQTT Robot Simulation Demo

This demo simulates a robot, a server (Mosquitto MQTT broker), and an upper computer using MQTT for communication.

## Prerequisites

- Ubuntu/Linux (or any OS with Mosquitto support)
- Python 3.6+
- `paho-mqtt` Python library

## Installation

### 1. Install Mosquitto

On Ubuntu/Linux, run:
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

Start Mosquitto:
```bash
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

Check if Mosquitto is running:
```bash
sudo systemctl status mosquitto
```

### 2. Install Python Dependencies

Install the `paho-mqtt` library:
```bash
pip install paho-mqtt
```

## Project Structure

- `mqtt_robot_demo.py`: Simulates the robot, subscribing to commands and publishing state updates.
- `mqtt_upper_computer_demo.py`: Simulates the upper computer, sending commands and receiving robot state updates.

## MQTT Topics

- **Robot Publishes**: `/a1ZNnqHo7Cu/70756475313335/user/pub_sdk`
- **Robot Subscribes**: `/a1ZNnqHo7Cu/70756475313335/user/sub_sdk`
- **Upper Computer Publishes**: `/a1ZNnqHo7Cu/70756475313335/user/sub_sdk`
- **Upper Computer Subscribes**: `/a1ZNnqHo7Cu/70756475313335/user/pub_sdk`

## How to Run

### 1. Start Mosquitto

Ensure Mosquitto is running:
```bash
sudo systemctl start mosquitto
```

### 2. Run the Robot Simulation

Open a terminal and run:
```bash
python mqtt_robot_demo.py
```

The robot will:
- Subscribe to commands.
- Publish state updates every 5 seconds.

### 3. Run the Upper Computer Simulation

Open another terminal and run:
```bash
python mqtt_upper_computer_demo.py
```

The upper computer will:
- Subscribe to robot state updates.
- Provide a command-line menu to send commands.

### 4. Interact with the Demo

- In the upper computer terminal, use the menu to send commands (e.g., navigation, cancel, charge).
- Observe the robot terminal for state updates.

## Example Commands

- **Move to Coordinate**:
  - Enter `1` and provide X, Y, Z coordinates.
- **Cancel Move**:
  - Enter `2`.
- **Move to Point**:
  - Enter `3` and provide the point name.
- **Cancel Point Move**:
  - Enter `4` and provide the point name.
- **Charge**:
  - Enter `5`.
- **Cancel Charge**:
  - Enter `6`.
- **Quit**:
  - Enter `q`.

## Testing with Mosquitto Clients

### Subscribe to Robot State

```bash
mosquitto_sub -h localhost -t "/a1ZNnqHo7Cu/70756475313335/user/pub_sdk" -v
```

### Publish a Command

```bash
mosquitto_pub -h localhost -t "/a1ZNnqHo7Cu/70756475313335/user/sub_sdk" -m '{"msgType":"/move/any","body":{"x":0.1,"y":0.1,"z":0.1}}'
```

## Troubleshooting

- **Connection Issues**: Ensure Mosquitto is running and accessible.
- **Topic Issues**: Topics are created dynamically. No explicit creation is needed.
- **Firewall**: If testing remotely, ensure port 1883 is open.

## Next Steps

- Extend the demo with additional features (e.g., task status, charging status).
- Use Mosquitto's ACL for access control if needed.

## License

This project is open-source and available under the MIT License. # mosquito_test
