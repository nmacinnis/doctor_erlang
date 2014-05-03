import random
import re
import subprocess
import time
import tweepy

from . import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, OTP_SRC_PATH


def get_docs_as_string():
    files = subprocess.check_output(['find', OTP_SRC_PATH, '-name', '*.xml']).split('\n')

    file_lines = []

    files = [file for file in files if file and "notes" not in file ]

    for filename in files:
        file = open(filename)
        lines = file.readlines()
        single_line = ' '.join(lines)
        p_tags = re.findall(r'<p>.*?</p>', single_line)
        p_tags_line = ' '.join(p_tags)
        un_c_data_line = re.sub(r'<!\[CDATA\[', '', p_tags_line)
        un_c_data_line = re.sub(r'\]\]>', '', un_c_data_line)
        untagged_line = re.sub(r'<.*?>', ' ', un_c_data_line)
        line = re.sub(r'\s+', ' ', untagged_line)
        line = re.sub(r' ([\,\.\:\;])', '\1', line)
        file_lines.append(line)
    docstring = ' '.join(file_lines)
    docstring = re.sub(r'\s+', ' ', docstring)
    return docstring


def get_random_segment(docstring):
    start = random.randint(0, len(docstring))
    end = start + 140
    return docstring[start:end]

class Bot(object):
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def do_bot_things(self):
        docstring = get_docs_as_string()
        print len(docstring)
        while True:
            tweet = get_random_segment(docstring)
            print tweet
            self.api.update_status(tweet)
            hours = random.randint(0, 24)
            print 'sleeping', hours, 'hours'
            time.sleep(60*60*12)
            #time.sleep(1)

        #time.sleep(3600) # Sleep for 1 hour
