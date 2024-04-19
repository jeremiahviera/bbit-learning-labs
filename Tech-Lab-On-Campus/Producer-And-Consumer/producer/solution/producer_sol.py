import pika
import os
from producer_interface import mqProducerInterface
class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        
        self.setupRMQConnection()
        
    def setupRMQConnection(self):
    # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)

    # Establish Channel
        self.channel = self.connection.channel()

    # Create the exchange if not already present
        exchange = self.channel.exchange_declare(exchange="Exchange Name")

        pass

    def publishOrder(self, message: str):
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange="Exchange Name",
            routing_key="Routing Key",
            body="Message",
        )

        # Close Channel
        # Close Connection
        self.channel.close()
        self.connection.close()
    
        pass


