from random import choice
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # Chain open() to create file object, then read() to create string.
    contents = open(file_path).read()

    return contents


def make_chains(text_string, n):
    """Takes input text as string and length of n-gram as integer; 
    returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2, ...wordn)
    and the value would be a list of the word(s) that follow those n
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita", 2)
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    # Split text_string on whitespace, creating list of words.
    words = text_string.split()

    # Iterate over indices. Use a range of 2 less than number of words (i.e.,
    # len(list)) so that our final key-value pair is made from the last three
    # words.

    for i in range(len(words)-n):

        # Make a tuple n words long to use as a key.
        ngram = []
        for num in range(n):
            ngram.append(words[i + num])

        ngram = tuple(ngram)

        # Check whether the key we just made exists in chains. If not,
        # add it, and set its value to [].
        chains[ngram] = chains.get(ngram, [])

        # Update the key's value to be the word that follows this occurance of
        # the key. ".append" works in place; don't need to use "=".

        chains[ngram].append(words[i+n])

    return chains

def make_capital_keys(chains):
    """Given a dictionary, creates a list of keys that start with a capital.

    Expects dictionary keys to be tuples, and checks capitalization
    of first element in each tuple.

    """
    
    # Start with an empty list to contain keys that start with capital letters.
    cap_keys = []

    # Get list of all keys in chains.
    keys = chains.keys()

    # Iterate over list of keys. If the first item in the tuple is not
    # equivalent to the lowercase version of that item, append it to the list
    # of keys that start with capital letters. 
    for key in keys:
        if key[0] != key[0].lower():
            cap_keys.append(key)

    return cap_keys


def make_text(chains, desired_sentences=2):
    """Takes dictionary of markov chains and desired number of sentences;
    returns random text of desired length."""

    text = ""
    words = []

    # Make a list of starter keys that all begin with a capital letter.
    starter_keys = make_capital_keys(chains)

    # Choose a random key to start with.
    key = choice(starter_keys)

    # Add each element of key tuple to list of words
    for item in key:
        # text = text + ' ' item
        words.append(item)

    # Write the poem
    while desired_sentences > 0:

        # Randomly choose next word from key's value list
        next_word = choice(chains[key])

        # Add next word to list of words
        words.append(next_word)

        # Check whether next_word ends with terminal punctuation. If so, update
        # count of sentences.

        if next_word.endswith(('.','?','!')):
            desired_sentences -= 1

        # Create next key
        key = key[1:] + ( next_word, )

        # Check whether created key exists in passed dictionary.
        # If it doesn't, stop writing.
        if not key in chains:
            break

    # Join all elements in word list into one string
    text = (' ').join(words)

    return text

# Take text file as command line argument
input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, 2)

# Produce random text
random_text = make_text(chains)

print random_text
