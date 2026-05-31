import argparse
import threading
import sol_uti
import base_uti
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.resources.queue import Queue

parser = argparse.ArgumentParser()

parser.add_argument("--host", required=True)
parser.add_argument("--vpn", required=True)
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--topic", required=False)
parser.add_argument("--queue", required=False)
parser.add_argument(
    "--action",
    choices=["connect", "pub", "subOnTopic", "subOnQueue"],
    default="connect",
    help="connect = test connectivity, pub = publish test message, subOnTopic = subscribe on topic, SubOnQueue = subscribe on Queue"
)
args = parser.parse_args()

messaging_service = sol_uti.get_connection(args.host,args.vpn,args.username,args.password)

def on_message(self, payload):
    message = message = payload.get_payload_as_string() if payload is not None else payload
    print(f"Received message: {message}")

def get_active_connection(messaging_service):
    if messaging_service is None or not messaging_service.is_connected:
        print("Connection lost. Reconnecting...")

        try:
            if messaging_service:
                messaging_service.disconnect()
        except Exception:
            pass

        messaging_service = sol_uti.get_connection(args.host,args.vpn,args.username,args.password)

        print("Reconnected.")

    return messaging_service

def test_subscription_on_topic(topic):
    get_active_connection(get_active_connection)
    sol_uti.start_topic_subscriber(messaging_service, topic,on_message,stop_event)   

def test_subscription_on_queue(queue):
    get_active_connection(get_active_connection)
    sol_uti.start_queue_subscriber(messaging_service, queue,on_message,stop_event)
 


if args.action == "connect":
    assert messaging_service.is_connected, "Failed to connect to Solace broker"
    print("Connection test passed.")

elif args.action == "pub":
    if not args.topic:
        print("Topic is required")
        exit(1)
        get_active_connection(get_active_connection)
        sol_uti.publish_message(messaging_service, topic, "Hello, Solace!")
elif args.action == "subOnTopic":
    if not args.topic:
        print("Topic is required")
        exit(1)
    stop_event = threading.Event()
    args=(args.topic)
    get_active_connection(get_active_connection)
    base_uti.start_subscription_thread(test_subscription_on_topic, args,stop_event)

elif args.action == "subOnQueue":
    if not args.queue:
        print("Queue is required")
        exit(1)
    stop_event = threading.Event()
    args=(args.queue)
    base_uti.start_subscription_thread(test_subscription_on_queue, args,stop_event)
    