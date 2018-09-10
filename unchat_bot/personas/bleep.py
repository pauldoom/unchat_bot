# unchat_bot - Worthless.
import random


class Persona(object):
    persona = 'bleep'
    description = 'Menaingless noise.'

    def __init__(self, my_name):
        self.my_name = my_name

    def noise(self):
        return random.choice(['bleep', 'bloop', 'floop', 'buzz', 'bleep',
                              'click', 'Daisy'])

    def process_message(self, to_name, from_name, message):
        return "{0} {1} {2} {3}".format(self.noise(), self.noise(), to_name,
                                        self.noise())
