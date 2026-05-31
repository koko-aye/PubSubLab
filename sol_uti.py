from solace.messaging.resources.queue import Queue
from solace.messaging.messaging_service import MessagingService, RetryStrategy
from solace.messaging.resources.topic import Topic
from solace.messaging.resources.topic_subscription import TopicSubscription
from time import sleep
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.messaging_service import (
    ReconnectionListener,
    ReconnectionAttemptListener,
    ServiceInterruptionListener,
)
import base_uti

max_retries = 20
retry_interval = 10 
current_retry_count = 0

class MyReconnectionAttemptListener(ReconnectionAttemptListener):
    def __init__(self, callback=None):
        self.callback = callback

    def on_reconnecting(self, event):
        print("Solace reconnecting...")
        print(event)

        if self.callback:
            self.callback(event)


class MyReconnectionListener(ReconnectionListener):
    def __init__(self, callback=None):
        self.callback = callback

    def on_reconnected(self, event):
        print("Solace reconnected successfully")
        print(event)

        if self.callback:
            self.callback(event)


class MyServiceInterruptionListener(ServiceInterruptionListener):
    def __init__(self, callback=None):
        self.callback = callback

    def on_service_interrupted(self, event):
        print("Solace service interrupted")
        print(event)

        if self.callback:
            self.callback(event)


def get_connection(host, vpn_name, username, password, on_reconnecting_callback, reconnected_callback, svc_interruption_callback):

    broker_props = {
        "solace.messaging.transport.host":
            host,

        "solace.messaging.service.vpn-name": vpn_name,

        "solace.messaging.authentication.scheme":
            "AUTHENTICATION_SCHEME_BASIC",

        "solace.messaging.authentication.basic.username":
            username,

        "solace.messaging.authentication.basic.password":
            password,
        
        "solace.messaging.tls.trust-store-path": "certs",

        "solace.messaging.tls.cert-validated": True
    }

    messaging_service = (
        MessagingService.builder()
        .from_properties(broker_props)
        .with_reconnection_retry_strategy(
            RetryStrategy.parametrized_retry(max_retries, retry_interval)
        )
        .build()
    )
    messaging_service.add_reconnection_attempt_listener(
        MyReconnectionAttemptListener(on_reconnecting_callback)
    )

    messaging_service.add_service_interruption_listener(
        MyServiceInterruptionListener(svc_interruption_callback)
    )

    messaging_service.add_reconnection_listener(
        MyReconnectionListener(reconnected_callback)
    )

    messaging_service.connect()

    print("Connected to Solace")

    return messaging_service

def disconnect(messaging_service):
    messaging_service.disconnect()
    print("Disconnected from Solace")

def publish_message(messaging_service, topic, message):

    publisher = (
        messaging_service.create_persistent_message_publisher_builder()
        .build()
    )

    publisher.start()

    publisher.publish(
        destination=Topic.of(topic),
        message=message
    )
    print(f"{base_uti.get_singapore_datetime()} - Message published to topic: {topic}")

def start_topic_subscriber(messaging_service, topic, callback, stop_event):

    class MessageProcessor(MessageHandler):

        def on_message(self, message):
            callback(message)
    receiver = (
        messaging_service
        .create_direct_message_receiver_builder()
        .with_subscriptions([
            TopicSubscription.of(topic)
        ])
        .build()
    )

    
    receiver.start()

    receiver.receive_async(MessageProcessor())

    print(f"Subscriber topic: {topic} started")
    input("Press Enter to stop...\n")

    while stop_event.is_set() == False:
        sleep(0.5)
    
    receiver.terminate()

def start_queue_subscriber(messaging_service, queue_name, callback, stop_event):

    class MessageProcessor(MessageHandler):

        def on_message(self, message):
            try:
                callback(message)
                receiver.ack(message)
            except Exception as e:
                print("Processing failed:", e)

    queue = Queue.durable_exclusive_queue(queue_name)
    receiver = (
        messaging_service.create_persistent_message_receiver_builder()
        .build(queue)
    )

    receiver.start()

    receiver.receive_async(MessageProcessor())

    print(f"Subscriber queue: {queue_name} started")
    input("Press Enter to stop...\n")

    while stop_event.is_set() == False:
        sleep(0.5)
    
    receiver.terminate()