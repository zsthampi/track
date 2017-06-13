# The file contains code to parse the source content and store details in MongoDB
import sys, os
from pymongo import *
import re

try:
    # Create MongoDB client
    client = MongoClient('localhost', 27017)
    # Drop data in Collection
    client['trackDB'].collection['source'].posts.drop()
except:
    print "ERROR : Mongo DB not running."
    sys.exit(1)

base = '/Users/zthampi/Projects/track/source/'
for filename in os.listdir(base):
    if re.match(r'^.*(\.py)$',filename):
        f = open(base+filename)
        for index,line in enumerate(f.readlines()):
            if re.match(r'\s*$',line):
                type = 'blank'
            elif re.match(r'^\s*(#.*)?$',line):
                type = 'comment'
            else:
                type = 'code'
            client['trackDB'].collection['source'].posts.insert_one({'type': type, 'line': index+1, 'file': base+filename, 'code': line})


