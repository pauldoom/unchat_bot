import random
import re
import time
import wikipedia

# Static time for the know it all to ponder before responding.  Mainly so
# we don't get banned by Wikipedia.
PAUSE = 3.0


class Persona(object):
    persona = 'knowitall'
    description = 'Insufferably arrogant Know It All bot'

    def __init__(self, my_name):
        self.my_name = my_name

    def pick_query(self, message):
        """
        Find the biggest words.  The best words. Minium size is 5 chars.
        Returns one of the top answers.
        """
        wordlist = re.findall(r'(?:^|\W+)([\w]{5,})(?:\W+|$)', message)
        if len(wordlist) == 0:
            return None

        swordlist = sorted(wordlist, key=len, reverse=True)
        return random.choice(swordlist[:int(len(swordlist) * 0.5)])

    def process_message(self, from_name, to_name, message):
        query = self.pick_query(message)

        if query is None:
            # Don't have anything to say.
            return

        # Wait a bit before searching.
        time.sleep(PAUSE)

        results = wikipedia.search(query)

        if len(results) == 0:
            return

        pquery = random.choice(results)

        page = wikipedia.page(pquery)

        # Limit to 1K reponse, chopping the end unceremoniously.
        summary = page.summary[:512]

        return ("Well {0}, on the topic of {1}, did you know this about {2}?  "
                "{3}...".format(from_name, query, pquery, summary))
