# unchat_bot - Worthless.
import random


class Persona(object):
    persona = 'bleep'
    description = 'Bleep: Malfunctioning nonsense bot.  Yells a lot.'
    greeting = 'Hello World'

    words = ['bleep', 'bloop', 'zing', 'fizz', 'buzz', 'beep',
             'click', 'clunk', 'pop', 'hiss', 'Daisy', 'Dave', '...']

    def __init__(self, my_name):
        self.my_name = my_name

    def noise(self, from_name):
        waccumulator = []
        words = self.words.copy()
        words.append(from_name)
        wc = int(random.random() * 15)
        while wc > 1:
            wc -= 1
            waccumulator.append(random.choice(words))

        return ' '.join(waccumulator).upper()

    def process_message(self, to_name, from_name, message):
        return "{0}!".format(self.noise(from_name))
