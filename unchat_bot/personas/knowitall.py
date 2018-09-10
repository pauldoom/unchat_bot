# unchat_bot - Wikipedia connected persona
import random
import re
import wikipedia


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
        swordlist = sorted(wordlist, key=len, reverse=True)
        halflist = swordlist[:int(len(swordlist) * 0.5)]
        if len(halflist) == 0:
            return None
        return random.choice(halflist)

    def process_message(self, to_name, from_name, message):
        if message.find(" on the topic of ") != -1:
            return None

        query = self.pick_query(message)

        if query is None:
            # Just be a jerk if you can't get any big words.
            query = 'inane prattle'

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

        # Limit to 1K reponse, chopping the end unceremoniously.
        summary = page.summary[:512]

        return ("Well {0}, on the topic of {1}, did you know this about {2}?  "
                "{3}...".format(from_name, query, pquery, summary))
