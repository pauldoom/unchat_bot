# unchat_bot - Lame excuse persona
import os
import random


class Persona(object):
    persona = 'knownothing'
    description = 'Know Nothing the Excuse Bot'

    def __init__(self, my_name, excuse_file=None):
        self.my_name = my_name

        if excuse_file is None:
            excuse_file = os.path.join(os.path.dirname(__file__), 'data',
                                       'bofh-excuses.txt')
        self.excuses = open(excuse_file, 'r').readlines()

    def excuse(self):
        return random.choice(self.excuses).capitalize().rstrip()

    def process_message(self, to_name, from_name, message):
        return "Sorry, {0}.  I can't.  {1}".format(from_name, self.excuse())
