import argparse
import threading
import sol_uti
import base_uti
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.resources.queue import Queue
from enum import Enum
import random
from enum import Enum
import json


parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True)
parser.add_argument("--vpn", required=True)
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument(
    "--action",
    choices=[ "pub", "subOnTopic", "subOnQueue"],
    default="connect",
    help="connect = test connectivity, pub = publish test message, subOnTopic = subscribe on topic, SubOnQueue = subscribe on Queue"
)
parser.add_argument("--topic", required=False)
parser.add_argument("--queue", required=False)
parser.add_argument("--loop", required=False)
args = parser.parse_args()

curr_attempt_count = 0


class Country(Enum):
    SG = "Singapore"
    CN = "China"
    US = "United States"
    IN = "India"
    RU = "Russia"

def generate_imo():
    # Randomly choose 5 or 6 base digits
    base_length = random.choice([5, 6])

    base = [random.randint(0, 9) for _ in range(base_length)]

    # Weights descend from base_length+1 to 2
    weights = range(base_length + 1, 1, -1)

    checksum = sum(
        digit * weight
        for digit, weight in zip(base, weights)
    ) % 10

    return f"{''.join(map(str, base))}{checksum}"

def generate_gt():
    return random.randint(500, 250000)

def on_message(payload):
    message = payload.get_payload_as_string() if payload is not None else payload
    print(f"{base_uti.get_singapore_datetime()} - Received message: {message}")

def on_reconnecting(event):
    global curr_attempt_count

    curr_attempt_count += 1

    print(
        f"Reconnect attempt "
        f"{curr_attempt_count}/{sol_uti.max_retries}"
    )

    if curr_attempt_count >= sol_uti.max_retries:
        print("Maximum reconnect attempts reached")


def on_reconnected(event):
    global curr_attempt_count

    curr_attempt_count = 0
    print("Successfully reconnected")


def on_service_interrupted(event):
    print("Service interrupted")
    
messaging_service = sol_uti.get_connection(args.host,args.vpn,args.username,args.password, on_reconnecting, on_reconnected, on_service_interrupted)

def publish():
    topic_prefix = "port_ops/cv/vsl_activities/vsl_arr_submitted"

    max_count = int(args.loop)

    for i in range(max_count):
        imo_number = generate_imo()
        flag = random.choice(list(Country)).name
        gt = generate_gt()

        latitude = round(random.uniform(1.15, 1.45), 6)
        longitude = round(random.uniform(103.55, 104.10), 6)

        speed = round(random.uniform(0.0, 25.0), 1)
        direction = random.randint(0, 359)

        topic = (
            f"{topic_prefix}/"
            f"{imo_number}/"
            f"{flag}/"
            f"{gt}/"
            f"{latitude}/"
            f"{longitude}/"
            f"{speed}/"
            f"{direction}"
        )

        payload = {
            "imoNumber": imo_number,
            "flag": flag,
            "gt": gt,
            "latitude": latitude,
            "longitude": longitude,
            "speed": speed,
            "direction": direction
        }

        json_str = json.dumps(payload)

        sol_uti.publish_message(
            messaging_service,
            topic,
            json_str
        )
        print(f"Published: {payload}")

def subscription_on_topic(topic):
    sol_uti.start_topic_subscriber(messaging_service, topic,on_message,stop_event)   

def subscription_on_queue(queue):
    sol_uti.start_queue_subscriber(messaging_service, queue,on_message,stop_event)
 
if args.action == "connect":
    assert messaging_service.is_connected, "Failed to connect to Solace broker"
    print("Connection test passed.")

elif args.action == "pub":
    if not args.loop:
        print("loop is required")
        exit(1)
    publish()
elif args.action == "subOnTopic":
    if not args.topic:
        print("Topic is required")
        exit(1)
    stop_event = threading.Event()
    args=(args.topic)
    base_uti.start_subscription_thread(subscription_on_topic, args,stop_event)

elif args.action == "subOnQueue":
    if not args.queue:
        print("Queue is required")
        exit(1)
    stop_event = threading.Event()
    args=(args.queue)
    base_uti.start_subscription_thread(subscription_on_queue, args,stop_event)