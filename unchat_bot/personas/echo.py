class Persona(object):
    persona = 'echo'
    description = 'Parrot'

    def __init__(self, my_name):
        self.my_name = my_name

    def process_message(self, from_name, to_name, message):
        return "Yea, {0}.  {1}".format(from_name, message)
