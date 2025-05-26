import paho.mqtt.client as mqtt
import json
import uuid
import time
import threading

# MQTT Broker settings
MQTT_BROKER = "localhost"  # Change to your Mosquitto server IP if not local
MQTT_PORT = 1883

# Topics
PUB_TOPIC = "/a1ZNnqHo7Cu/70756475313335/user/pub_sdk"  # Robot publishes here
SUB_TOPIC = "/a1ZNnqHo7Cu/70756475313335/user/sub_sdk"  # Robot subscribes here

# Robot state
robot_state = {
    "angle": 0.0,
    "x": 0.0,
    "y": 0.0,
    "robotGoState": "Idle"
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(SUB_TOPIC)
    print(f"Subscribed to {SUB_TOPIC}")

def on_message(client, userdata, msg):
    print(f"\n[Received] Topic: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Error parsing message:", e)
        print(msg.payload)

def simulate_robot(client):
    while True:
        # Simulate robot state updates
        robot_state["angle"] += 0.1
        robot_state["x"] += 0.1
        robot_state["y"] += 0.1
        robot_state["robotGoState"] = "Arriving"

        # Publish robot state
        message = {
            "body": {
                "angle": robot_state["angle"],
                "x": robot_state["x"],
                "y": robot_state["y"]
            },
            "groupId": "default",
            "from": "",
            "msgId": str(uuid.uuid4()),
            "msgType": "notifyRobotPose",
            "source": "70756475313335",
            "sourceType": "",
            "target": "any"
        }
        client.publish(PUB_TOPIC, json.dumps(message, ensure_ascii=False))
        #print(f"[Robot] Published state: {json.dumps(message, indent=2, ensure_ascii=False)}")
        time.sleep(0.1)  # Update every 5 seconds

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    # Start robot simulation in a separate thread
    robot_thread = threading.Thread(target=simulate_robot, args=(client,))
    robot_thread.daemon = True
    robot_thread.start()

    print("Robot Simulation Started")
    print("Press Ctrl+C to exit")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()
        client.disconnect()
