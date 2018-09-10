import pika
import random
import time


class Broker(object):
    def __init__(self, my_name, message_processor, exchange_name='unchat',
                 amqp_uri=None):
        """
        Setup a new message broker.

        Args:
            my_name (str) - My name.  Duh.
            message_processor (str) - Function that takes input of to, from,
                                      and a message string and returns a
                                      new string.
            exchange_name (str) - Exchange to bind to.
            amqp_uri (str) - RabbitMQ connection URI
        """
        self.message_processor = message_processor

        # Turn friendly name into a queue name
        self.queue_name = my_name.lower().replace(' ', '_')

        # Create a connection to RabbitMQ and open a channel
        self.connection = pika.BlockingConnection(
            pika.URLParameters(amqp_uri))
        self.channel = self.connection.channel()

        # Create our queue
        self.queue_resource = self.channel.queue_declare(
            queue=self.queue_name, durable=False, auto_delete=True)

        # Ensure the exchange exists
        self.exchange_name = exchange_name
        self.channel.exchange_declare(exchange=exchange_name, durable=True,
                                      passive=True)

        # Set initial bindings to receive messages for us and on the
        # broadcast.
        self.add_binding(self.queue_name + '.#')
        self.add_binding('all.*')

        # To prevent spam-death, upon reception of a message we will
        # wait up to this number of seconds before proceeding.
        self.wait_max = 5.0

    def add_binding(self, routing_key):
        """
        Bind another routing key using our exchange and queue
        """
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_resource.method.queue,
                                routing_key=routing_key)

    def process_message(self, from_route=None, to_route=None, message=""):
        """
        Called by consume with the binding key it was sent to,
        the source name, and the body of new message.  Calls out to
        self.get_response and publishes result appropriately.
        """
        from_name = ' '.join([p.capitalize() for p in
                              from_route.split('.', 1)[0].split('_')])
        if to_route.split('.', 1)[0] == self.queue_name:
            to_name = self.my_name
            routing_key = from_route + '.' + self.queue_name
        else:
            to_name = "Everyone"
            routing_key = 'all.' + self.queue_name

        response = self.message_processor(from_name=from_name, to_name=to_name,
                                          message=message)

        time.sleep(random.random(self.wait_max))
        print("Got: {0} -> {1}: {2}".format(from_name, to_name, message))
        print("Responding: {0} -> {1}: {2}".format(to_name, from_name,
                                                   response))
        self.produce(routing_key=routing_key, message=response)

    def consume(self, channel, method, params, body):
        """
        Consumer callback
        """
        self.process_message(from_route="FROM", to_route="TO", message=body)

    def start_consuming(self):
        """
        Start listening
        """
        self.channel.basic_consume(self.consume, queue=self.queue_name,
                                   no_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        """
        Stop listening.
        """
        self.channel.stop_consuming()

    def produce(self, routing_key, message):
        """
        Send a message
        """
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=routing_key,
                                   body=message,
                                   properties=pika.spec.BasicProperties(
                                       content_type="text/plain"))
