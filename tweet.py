import sys
import os
import twitter
import markov


def tweet(chains):
    """Given a dictionary, creates text, processes it, and posts it to twitter.

    Uses Python os.environ to get at environmental variables. You must run
    `source twitter_secrets.sh` before running this file to make sure these
    environmental variables are set."""

    try:
        api = twitter.Api(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    except KeyError:
        print "Error: Remember to source your twitter secrets."
        return

    # Print info about credentials to make sure they're correct.
    try:
        api.VerifyCredentials()
        print "Credentials verified."
    except Exception as e:
        print "Credentials cannot be verified:", e
        return

    # Set state variable for REPL.
    tweeting = True
    while tweeting:

        # Make a new piece of random text.
        text = markov.make_text(chains)

        # Check random text length. If it's too long to tweet, truncate it to
        # 137 characters, then go back to the last complete word and add an
        # ellipsis.
        if len(text) > 140:
            text = text[:137]
            index = text[::-1].find(' ')  # reverses string to find first space
            text = text[:-index-1]  # truncates string at that space
            if text.endswith((',', ';')):  # trims any mid-sentence punctuation
                text = text[:-1]
            text = text + '...'

        # Display tweet draft to the user.
        print "Your tweet will be: {}".format(text)
        user_reply = raw_input("Do you want to post it? [y/n] > ")

        if user_reply.lower() == "y":
            # status = api.PostUpdate(text)
            # print "Your tweet was: {}".format(status.text)
            api.PostUpdate(text)
            print "Tweet posted."

        # Ask the user if they want to tweet some more.
        user_reply = raw_input("Hit 'Enter' to tweet again [q to quit] > ")

        # If the user enters q/Q, set tweeting flag to False so loop will end.
        if user_reply.lower() == "q":
            tweeting = False


def command_line_tweet():
    """Tweet Markov-generated text from the command line."""

    # Get the filenames from the user through a command line prompt, ex:
    # python twitter.py genesis.txt gettysburg.txt
    filenames = sys.argv[1:]

    # Loop over the files and turn them into one long string.
    string = markov.open_and_read(filenames)

    # Make Markov chain.
    chains = markov.make_chains(string)

    # Tweet from chain.
    try:
        tweet(chains)
    except IndexError:
        print "Error: Remember to include at least one filename."

if __name__ == "__main__":
    command_line_tweet()
