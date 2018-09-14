#!/usr/bin/env python
from unchat_bot.bus import Broker
from unchat_bot.util import get_random_name
import importlib
import os
import random
import sys
import argparse

# Lame non-dynamic list of persona classes to load
PERSONAS = (
    'bleep',
    'helpy',
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
    epilog = ("Avatar powered by ARTIFICIAL INTELLIGENCE and DEEP HURTING\n\n"
              "Available Personas:\n\n")
    epilog += "\n\n".join(
        ["\t({0}) {1}".format(
            k, PERSONA_LIBS[k].Persona.description) for k in PERSONAS])

    parser = argparse.ArgumentParser(
        description="UnChat Chat UnBot",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--name', default=None,
                        help='Bot name (Default: Randomly chosen)')
    parser.add_argument('-p', '--persona_type', choices=PERSONAS,
                        default=random.choice(list(PERSONA_LIBS.keys())),
                        help='Choice of cybernetic intelligence module')
    parser.add_argument('--print_received', action='store_true', default=False,
                        help='Display received messages as well as sent')
    parser.add_argument('-a', '--amqp_uri', default=None,
                        help=('AMQP URI to connect with RabbitMQ (Overrides '
                              'AMQP_URI environment variable)'))
    parser.add_argument('--wait_max', type=float, default=2.0,
                        help='Maximum random sleep time (Default: 2)')
    parser.add_argument('--respond_all_percent', type=int, default=50,
                        help=('Percentage of group chats to respond to '
                              '(Default: 50)'))

    args = parser.parse_args()

    my_name = args.name
    if my_name is None:
        my_name = get_random_name()

    persona = PERSONA_LIBS[args.persona_type].Persona(my_name=my_name)

    amqp_uri = os.getenv('AMQP_URI')
    if args.amqp_uri is not None:
        amqp_uri = args.amqp_uri

    if amqp_uri is None:
        sys.stderr.write("No AMQP URI defined!")
        parser.print_help()
        sys.exit(1)

    broker = Broker(my_name=my_name,
                    message_processor=persona.process_message,
                    amqp_uri=amqp_uri,
                    greeting=persona.greeting,
                    wait_max=args.wait_max,
                    respond_all_percent=args.respond_all_percent,
                    print_received=True)

    print("My name is {0} and I am a {1} bot".format(my_name, persona.persona))

    # Go.
    while True:
        try:
            broker.start_consuming()
        except (KeyboardInterrupt, EOFError):
            print("\nAHHHH! YOU KILLED ME!")
            broker.stop_consuming()
            sys.exit(0)

if __name__ == '__main__':
    main()
