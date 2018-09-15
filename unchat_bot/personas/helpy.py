# unchat_bot - Lame excuse persona
import os
import random


class Persona(object):
    persona = 'helpy'
    description = 'Helpy: The UnChat helpdesk bot'
    greeting = 'wassup'

    def __init__(self, my_name, excuse_file=None):
        self.my_name = my_name

        if excuse_file is None:
            excuse_file = os.path.join(os.path.dirname(__file__), 'data',
                                       'bofh-excuses.txt')
        self.excuses = open(excuse_file, 'r').readlines()

    def excuse(self):
        return random.choice(self.excuses).capitalize().rstrip()

    def process_message(self, to_name, from_name, message):
        catches = [
            'Obvious.  ',
            'I have found the issue: ',
            'Page 452 of the manual clearly states: ',
            'Sorry.  There is no way to fix it.  '
        ]
        return random.choice(catches) + self.excuse() + ".  I've closed your ticket."

