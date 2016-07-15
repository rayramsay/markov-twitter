import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
       string.
    """

    contents = ""

    for filename in filenames:
        text_file = open(filename)
        contents = contents + text_file.read()
        text_file.close()

    return contents


def make_chains(text_string, n=2):
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

def tweet(chains):
    """Given a dictionary, creates text, processes it, and posts it to twitter.

    Use Python os.environ to get at environmental variables.
    Note: you must run `source secrets.sh` before running this file to make sure
    these environmental variables are set.
    """

    # Set default values for parameters of function.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # Print info about credentials to make sure they're correct.
    # print api.VerifyCredentials()

    # Trim input to 140 characters and posts it. Status is a special module
    # from python-twitter.

    tweeting = True

    while tweeting:

        # Make a new piece of random text.
        text = make_text(chains)

        # Check random text length. If it's too long to tweet, truncate it to
        # 137 characters, and add an ellipsis. 
        if len(text) > 140:
            text = text[:137]
            index = text[::-1].find(' ')
            text = text[:-index-1]
            text = text + '...'

        # Post new tweet to the Internet. 
        status = api.PostUpdate(text)

        # Print just the text of the status.
        print "Your tweet was: \"{}\"".format(status.text)

        # Ask the user if they want to tweet some more.
        user_reply = raw_input("Enter to tweet again [q to quit] > ")

        # If the user entered q/Q, set tweeting flag to False so loop will
        # end. 
        if user_reply.lower() == "q":
            tweeting = False

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Loop over the files and turn them into one long string
big_string = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(big_string)

# Produce random text
random_text = make_text(chains)
print random_text

# Tweets out random text
# tweet(chains)
