#!/usr/bin/env python
from unchat_bot.bus import Broker
from unchat_bot.util import get_random_name
import importlib
import os
import random
import sys

# Lame non-dynamic list of persona classes to load
PERSONAS = (
    'bleep',
    'knownothing',
    'knowitall'
)

PERSONA_LIBS = {}
for p in PERSONAS:
    libn = 'unchat_bot.personas' + '.' + p
    try:
        PERSONA_LIBS[p] = importlib.import_module(libn)
    except ImportError:
        print("Skipping missing persona {0}".format(libn))


def main():
    amqp_uri = os.getenv('AMQP_URI')

    my_name = get_random_name()

    # Let a random persona be selected
    persona_type = random.choice(list(PERSONA_LIBS.keys()))
    persona = PERSONA_LIBS[persona_type].Persona(my_name=my_name)

    broke = Broker(my_name=my_name,
                   message_processor=persona.process_message,
                   amqp_uri=amqp_uri)

    print("My name is {0} and I am a {1} bot".format(my_name, persona.persona))

    # Go.
    while True:
        try:
            broke.start_consuming()
        except (KeyboardInterrupt, EOFError):
            print("\nAHHHH! YOU KILLED ME!")
            broke.stop_consuming()
            sys.exit(0)

if __name__ == '__main__':
    main()
