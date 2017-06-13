# This file contains code to analyse the data from MongoDB

import sys, os
from pymongo import *

try:
    # Create MongoDB client
    client = MongoClient('localhost', 27017)
except:
    print "ERROR : Mongo DB not running."
    sys.exit(1)

# source = client['trackDB'].collection['source'].posts.find()
# runtime = client['trackDB'].collection['runtime'].posts.find()
#
# for each in source:
#     print each
#
# print source
# print runtime
# print "SUCCESS"

html_prefix = '<!DOCTYPE html><html><title>TRACK</title><head><link rel="stylesheet" type="text/css" href="track.css"><script src="track.js"></script></head><body><h2>TRACK</h2>'
html_postfix = '</body></html>'

# LOC Coverage
def loc_coverage():
    source =  list(client['trackDB'].collection['source'].posts.find().sort([('file',1),('line',1)]))
    runtime = list(client['trackDB'].collection['runtime'].posts.find())

    unique_files = list(set([each['file'] for each in source]))
    print unique_files

    source_coverage = [(each['file'],each['line']) for each in source if each['type']=='code']
    runtime_coverage = [(each['file'],each['line']) for each in runtime]
    diff_coverage = list(set(source_coverage) - set(runtime_coverage))
    print diff_coverage

    f = open('./output/track.html','w')
    f.write(html_prefix)

    current_file = None
    for each in source:
        if current_file is not None and each['file']<>current_file:
            f.write('</table>')
        if current_file is None or each['file']<>current_file:
            current_file = each['file']
            f.write('<table id="{}" cellspacing="0">'.format(current_file))
            f.write('<caption>{}</caption>'.format(current_file))

        if each['type'] == 'blank':
            color = "white"
        elif each['type'] == 'comment':
            color = 'grey'
        elif each['type']=='code' and (each['file'],each['line']) in runtime_coverage:
            color = 'green'
        else:
            color = 'red'
        f.write('<tr><th class="{}">{}</th><td class="{}"><pre>{}</pre></td></tr>'.format(color,each['line'],color,each['code']))

    if current_file is not None:
        f.write('</table>')

    f.write(html_postfix)
    f.close()

    # files = list(set([each['file'] for each in list(client['trackDB'].collection['source'].posts.find({},{'file':1}))]))
    # print files

    # source = [(each['file'],each['line']) for each in list(client['trackDB'].collection['source'].posts.find({'type':'code'},{'file':1, 'line':1}))]
    # print source
    #
    # runtime = [(each['file'],each['line']) for each in list(client['trackDB'].collection['runtime'].posts.find({},{'file':1, 'line':1}))]
    # print runtime
    #
    # diff = list(set(source) - set(runtime))
    # print diff


loc_coverage()

# Test Coverage

# Line Query

# Argument parser