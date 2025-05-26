import paho.mqtt.client as mqtt
import json
import uuid

# MQTT Broker settings
MQTT_BROKER = "localhost"  # Change to your Mosquitto server IP if not local
MQTT_PORT = 1883

# Topics
PUB_TOPIC = "/a1ZNnqHo7Cu/70756475313335/user/sub_sdk"  # Upper computer sends commands here
SUB_TOPIC = "/a1ZNnqHo7Cu/70756475313335/user/pub_sdk"  # Upper computer receives updates here

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

def send_command(client, msgType, body, target="70756475313335", source="master", vn=None, vc=None, groupId=None):
    message = {
        "msgId": str(uuid.uuid4()),
        "msgType": msgType,
        "source": source,
        "body": body,
        "target": target
    }
    if vn is not None:
        message["vn"] = vn
    if vc is not None:
        message["vc"] = vc
    if groupId is not None:
        message["groupId"] = groupId
    client.publish(PUB_TOPIC, json.dumps(message, ensure_ascii=False))
    print(f"[Sent] {msgType} -> {PUB_TOPIC}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print("Upper Computer Simulation Started")
    print("Commands:")
    print("1: Move to coordinate")
    print("2: Cancel move")
    print("3: Move to point")
    print("4: Cancel point move")
    print("5: Charge")
    print("6: Cancel charge")
    print("q: Quit")

    while True:
        cmd = input("\nEnter command: ").strip()
        if cmd == "1":
            x = float(input("X: "))
            y = float(input("Y: "))
            z = float(input("Z: "))
            send_command(client, "/move/any", {"x": x, "y": y, "z": z}, vn="1.3.3", vc=0)
        elif cmd == "2":
            send_command(client, "/move/cancelAny", None, target="90037142992d")
        elif cmd == "3":
            point = input("Point name: ")
            send_command(client, "/move/dest", point, vn="1.3.3", vc=0)
        elif cmd == "4":
            point = input("Point name: ")
            body = {"destination": {"name": point, "type": "table"}}
            send_command(client, "cancelCall", body, source="OpenPlatform")
        elif cmd == "5":
            send_command(client, "/move/charge", None)
        elif cmd == "6":
            send_command(client, "/move/cancelCharge", None)
        elif cmd.lower() == "q":
            break
        else:
            print("Unknown command.")

    client.loop_stop()
    client.disconnect() 