import sys
import os
import twitter
import markov


def tweet(chains):
    """Given a dictionary, creates text, processes it, and posts it to twitter.

    Uses Python os.environ to get at environmental variables. You must run
    `source twitter_secrets.sh` before running this file to make sure these
    environmental variables are set."""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # Print info about credentials to make sure they're correct.
    # print "Verifying credentials...\n", api.VerifyCredentials()

    # Set state variable for REPL.
    tweeting = True

    # Trim input to 140 characters and post it. `Status` is a special module
    # from python-twitter.

    while tweeting:

        # Make a new piece of random text.
        text = markov.make_text(chains)

        # Check random text length. If it's too long to tweet, truncate it to
        # 137 characters, then go back to the last complete word and add an
        # ellipsis.
        if len(text) > 140:
            text = text[:137]
            index = text[::-1].find(' ')
            text = text[:-index-1]
            text = text + '...'

        # Post new tweet to the Internet.
        status = api.PostUpdate(text)

        # Print just the text of the status.
        print "Your tweet was: {}".format(status.text)

        # Ask the user if they want to tweet some more.
        user_reply = raw_input("Enter to tweet again [q to quit] > ")

        # If the user entered q/Q, set tweeting flag to False so loop will end.
        if user_reply.lower() == "q":
            tweeting = False


def command_line_tweet():
    """Tweet Markov-generated text from the command line."""

    # Get the filenames from the user through a command line prompt, ex:
    # python twitter.py genesis.txt gettysburg.txt
    filenames = sys.argv[1:]

    # Loop over the files and turn them into one long string.
    string = markov.open_and_read_file(filenames)

    # Make Markov chain.
    chains = markov.make_chains(string)

    # Tweet from chain.
    tweet(chains)


if __name__ == "__main__":
    command_line_tweet()
