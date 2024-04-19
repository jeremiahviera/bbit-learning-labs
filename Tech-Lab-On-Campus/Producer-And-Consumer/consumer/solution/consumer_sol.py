from consumer_interface import mqConsumerInterface
import pika
import os
class mqConsumer(mqConsumerInterface):
    


    def __init__(
        self,binding_key: str, exchange_name: str, queue_name: str):
        # Save parameters to class variables
        self.binding_key=binding_key
        self.exchange_name=exchange_name
        self.queue=queue_name

        # Call setupRMQConnection
        self.setupRMQConnection()
       

    def setupRMQConnection(self):
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        channel = connection.channel()
        self.setChannel(channel)

        # Create Queue if not already present
        self.channel.queue_declare(queue=self.queue)

        # Create the exchange if not already present
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)

        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            queue= self.queue,
            routing_key= self.binding_key,
            exchange=self.exchange_name,
        )
##
        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            self.queue, on_message_callback=self.on_message_callback,auto_ack=False
        )
      

    def on_message_callback(self, channel, method_frame, header_frame, body):
        # Acknowledge message
        channel.basic_ack(method_frame.delivery_tag, False)

        #Print message (The message is contained in the body parameter variable)
        print(body)
        pass

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print(" [*] Waiting for messages. To exit press CTRL+C")

        # Start consuming messages
        self.channel.start_consuming()
        pass
    
    def __del__(self):
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")
        
        # Close Channel
        self.channel.close()
        # Close Connection
        self.connection.close()
        
        pass

    def setChannel(self,channel):
        self.channel=channel
