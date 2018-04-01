import sys
from random import choice


VERBOSE = True


def open_and_read(filenames):
    """Given a list of files, open them, read the text, and return one long
    string."""

    contents = ""

    for filename in filenames:
        text_file = open(filename)
        if VERBOSE:
            print(filename+" opened")
        contents = contents + text_file.read() + ' '
        text_file.close()

    return contents


def make_chains(text_string, n=2):
    """Takes input text as string and length of n-gram as integer (default 2);
    returns dictionary of markov chains.

    Each key is a tuple n-words long and each value is a list of the word(s)
    that follow that key in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita", 2)
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi'): ['there']}
    """

    chains = {}

    # Split text_string on whitespace, creating list of words.
    words = text_string.split()

    # Iterate over indices using range of n less than the total number of words
    # so that the final key-value pair is made from the last n + 1 words.
    for i in range(len(words) - n):

        # Make a tuple n-words long to use as a key.
        key = []
        for num in range(n):
            key.append(words[i + num])
        key = tuple(key)

        # Check whether the key we just made exists in chains. If not,
        # add it, and set its value to [].
        # Update the key's value to include the word that follows this
        # occurrence of the key.
        chains.setdefault(key, []).append(words[i + n])

    return chains


def make_capital_keys(chains):
    """Given a dictionary, creates a list of keys that start with a capital.

    Expects dictionary keys to be tuples, and checks capitalization
    of first element in each tuple."""

    # Start with an empty list to contain keys that start with capital letters.
    cap_keys = []

    # Iterate over keys. If the first item in the tuple is not equivalent to the
    # lowercase version of that item, append it to the list of keys that start
    # with capital letters.
    for key in iter(chains.keys()):
        if key[0] != key[0].lower():
            cap_keys.append(key)

    return cap_keys


def make_starter_keys(chains, starter_word):
    """Given a dictionary and starter string, creates a list of keys that start
    with that word and don't end with terminal punctuation."""

    starter_keys = []

    for key in iter(chains.keys()):
        if key[0] == starter_word and key[-1][-1] not in [".", "?", "!"]:
            starter_keys.append(key)

    if VERBOSE:
        print(starter_keys)

    return starter_keys


def make_text(chains, starter_keys, desired_sentences=2):
    """Takes dictionary of markov chains, list of starter keys, and desired
    number of sentences; returns random text of desired length."""

    words = []

    # Choose a random key to start with.
    key = choice(starter_keys)

    # Add each element of first key tuple to list of words.
    for item in key:
        words.append(item)

    # Write the new text.
    while desired_sentences > 0:

        # Randomly choose next word from key's value list.
        next_word = choice(chains[key])

        # Add next word to list of words.
        words.append(next_word)

        # Check whether next_word ends with terminal punctuation. If so, update
        # count of sentences.
        if next_word.endswith(('.', '?', '!')):
            desired_sentences -= 1

        # Create next key. We're adding tuples together.
        key = key[1:] + (next_word,)

        # Check whether created key exists in passed dictionary.
        # If it doesn't, stop writing.
        if not key in chains:
            break

    # Join all elements in word list into one string.
    text = " ".join(words)

    return text


def command_line_markov():
    """Returns random text."""

    # Get the filenames, starter word (default cap_keys), and desired number of
    # sentences (default 2) from the user through a command line prompt, ex:
    # python markov.py -sent=3 -start=Holmes -files=scandal.txt,mountains.txt

    # Set default values.
    desired_sentences = 2
    starter_word = None
    filenames = None

    # Loop over arguments and check if flag.
    for arg in sys.argv:
        if arg.startswith('-'):
            # If this is the desired sentences flag, set desired sentences.
            if arg[1:].startswith("sent"):
                desired_sentences = int(arg.split("=")[1])
                if VERBOSE:
                    print("Desired sentences: " + str(desired_sentences))
            # If this is the starter word flag, set starter word.
            if arg[1:].startswith("start"):
                starter_word = arg.split("=")[1]
                if VERBOSE:
                    print("Starter word: " + starter_word)
            # If this is the files flag, set filenames.
            if arg[1:].startswith("files"):
                filenames = arg.split("=")[1].split(",")
                if VERBOSE:
                    print("Filenames: " + str(filenames))

    if not filenames:
        raise Exception("Remember to include file names, like this: -files=scandal.txt,mountains.txt")

    # Loop over the files and turn them into one long string.
    string = open_and_read(filenames)

    # Make Markov chains.
    chains = make_chains(string)

    # Make starter keys with either desired word or capitals.
    if starter_word:
        starters = make_starter_keys(chains, starter_word)
    else:
        starters = make_capital_keys(chains)

    # Produce random text.
    random_text = make_text(chains, starters, desired_sentences)

    return random_text


if __name__ == "__main__":
    print(command_line_markov())
