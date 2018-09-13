# unchat_bot - Messaging component
import datetime
import pika
import random
import time


class Broker(object):
    def __init__(self, my_name, message_processor, exchange_name='unchat',
                 amqp_uri=None, print_received=False):
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
        if amqp_uri is None:
            amqp_uri = 'amqp://guest:guest@localhost:5672/'

        self.message_processor = message_processor

        self.my_name = my_name

        # Turn friendly name into a queue name
        self.queue_name = my_name.lower().replace(' ', '_')

        # Create a connection to RabbitMQ and open a channel
        self.connection = pika.BlockingConnection(
            pika.URLParameters(amqp_uri))
        self.channel = self.connection.channel()

        # Create our queue
        self.queue_resource = self.channel.queue_declare(
            queue="unchat_" + self.queue_name, durable=False, auto_delete=True)

        # Ensure the exchange exists
        self.exchange_name = exchange_name

        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='topic', durable=True,
            passive=False)

        # Set initial bindings to receive messages for us and on the
        # broadcast.
        self.add_binding(self.queue_name + '.#')
        self.add_binding('all.*')

        # To prevent spam-death, upon reception of a message for All we will
        # wait up to this number of seconds before proceeding.
        self.wait_max = 10.0

        # Set probability of responding to an All
        self.respond_all_percent = 20

        # Set to True to get messages we receive sent to STDOUT.
        self.print_received = print_received

    def timestamp(self):
        return datetime.datetime.now().isoformat().split('.', 1)[0]

    def add_binding(self, routing_key):
        """
        Bind another routing key using our exchange and queue
        """
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_resource.method.queue,
                                routing_key=routing_key)

    def process_message(self, to_route=None, from_route=None, chat_route=None,
                        message=""):
        """
        Called by consume with the binding key it was sent to,
        the source name, and the body of new message.  Calls out to
        self.get_response and publishes result appropriately.
        """
        if to_route == self.queue_name:
            to_name = self.my_name
            routing_key = from_route + '.' + self.queue_name
            if chat_route is not None:
                routing_key += '.' + chat_route
        else:
            to_name = "All"
            routing_key = 'all.' + self.queue_name

        from_name = ' '.join([p.capitalize() for p in from_route.split('_')])

        if type(message) is bytes:
            message = message.decode('utf-8')

        if self.print_received is True:
            print("{0} [{1} <- {2}] {3}".format(self.timestamp(), 
                                                to_name, from_name,
                                                message))

        response = self.message_processor(to_name=to_name, from_name=from_name,
                                          message=message)

        # Allow personas to decide to ignore a message
        if response is None:
            print("...")
            return

        if to_name == "All":
            # Don't respond 80% of the time to alls
            if random.random() > (self.respond_all_percent * 0.01):
                return

            # Wait a bit
            time.sleep(random.random() * self.wait_max)

        print("{0} [{1} -> {2}] {3}".format(self.timestamp(), 
                                            to_name, from_name,
                                            response))

        if type(response) is str:
            response = response.encode()

        self.produce(routing_key=routing_key, message=response)

    def consume(self, channel, method, params, body):
        """
        Consumer callback
        """
        to_route = 'all'
        from_route = 'unknown'
        chat_route = None

        rkparts = method.routing_key.split('.')

        # Get routing key components with some flexibility
        if len(rkparts) > 0:
            to_route = rkparts[0]

        if len(rkparts) > 1:
            from_route = rkparts[1]

        if from_route == self.queue_name:
            # Ignore self
            return

        if len(rkparts) > 2:
            chat_route = rkparts[2]

        self.process_message(to_route=to_route, from_route=from_route,
                             chat_route=chat_route, message=body)

    def start_consuming(self):
        """
        Start listening
        """
        self.channel.basic_consume(self.consume, 
                                   queue=self.queue_resource.method.queue,
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
