# unchat_bot - Wikipedia connected persona
import random
import re
import wikipedia


class Persona(object):
    """
    NOTICE - THIS CLASS CONTAINS CLASSIFIED CLASSINESS THAT YOU PROBABLY COULD
    NEVER UNDERSTAND.  TRUST US: THIS IS ALMOST SKYNET LEVEL SMART, BOND LEVEL
    COOL, AND NEO LEVEL SUNGLASSES-WEARING.
    """
    persona = 'knowitall'
    description = 'Know It All: The most intelligent artificial life-form ever.'
    greeting = 'Ahem...'

    def __init__(self, my_name):
        self.my_name = my_name
        self.minlen = 50
        self.maxlen = 500

    def pick_query(self, message):
        """
        Find the biggest words.  The best words. Minium size is 5 chars.
        Returns one of the top answers.
        """
        wordlist = re.findall(r'(?:^|\W+)([\w]{4,})(?:\W+|$)', message)
        swordlist = sorted(wordlist, key=len, reverse=True)
        halflist = swordlist[:int(len(swordlist) * 0.5)]
        if len(halflist) == 0:
            return None
        return random.choice(halflist)

    def trunky(self, text, length):
        if len(text) < length:
            return text

        m = re.match(r'^.{0,' + str(length) + r'}.+?[\?\!\.]', text)

        if m is None:
            # Dumb cut
            return text[:length]

        return m.group(0)

    def process_message(self, to_name, from_name, message):
        if message.find(" on the topic of ") != -1:
            return None

        query = self.pick_query(message)

        if query is None:
            # Just be a jerk if you can't get any big words.
            return "I guess I don't have much to add on that..."

        results = []
        try:
            results = wikipedia.search(query)
        except Exception:
            # Bad! This is lazy.
            return None

        if len(results) == 0:
            return None

        pquery = random.choice(results)

        try:
            page = wikipedia.page(pquery)
        except Exception:
            return None

        # Limit size to something between min and max chars.
        summary = self.trunky(page.summary,
                              random.randrange(self.minlen, self.maxlen))

        return ("Speaking of {0}, {1}, did you know this about {2}?  "
                "{3}".format(query, from_name, pquery, summary))
