# This file contains code to analyse the data from MongoDB

import sys, os
import argparse
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

# Get the source and runtime, and create an HTML output
def output(source,runtime):
    source_coverage = [(each['file'],each['line']) for each in source if each['type']=='code']
    runtime_coverage = [(each['file'],each['line']) for each in runtime]
    diff_coverage = list(set(source_coverage) - set(runtime_coverage))
    # print diff_coverage

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

# Check the Lines of Code coverage for all tests
def loc_coverage():
    source =  list(client['trackDB'].collection['source'].posts.find().sort([('file',1),('line',1)]))
    runtime = list(client['trackDB'].collection['runtime'].posts.find())

    # unique_files = list(set([each['file'] for each in source]))
    # print unique_files

    output(source,runtime)

    print "SUCCESS! Output written to track.html"

# Check the Lines of Code coverage for a single test
def test_coverage(test):
    source = list(client['trackDB'].collection['source'].posts.find().sort([('file', 1), ('line', 1)]))
    runtime = list(client['trackDB'].collection['runtime'].posts.find({'test':test}))

    output(source, runtime)

    print "SUCCESS! Output written to track.html"

# Get the corresponding tests, given a file and the line number
def find_tests(file,line):
    runtime = list(client['trackDB'].collection['runtime'].posts.find({'file':file,'line':line}))
    unique_tests = list(set([each['test'] for each in runtime]))
    print unique_tests

# Argument parser
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Argument Parser for Track Analysis')
    parser.add_argument('-a','--action',action='store',dest='action',help='Function to choose',choices=['loc_coverage','test_coverage','find_tests'],type=str,required=True)
    parser.add_argument('-t','--test',action='store',dest='test',help='Test Name (If function = test_coverage)',type=str)
    parser.add_argument('-f', '--file', action='store', dest='file', help='File Name (If function = find_tests)',type=str)
    parser.add_argument('-l', '--line', action='store', dest='line', help='Line Number (If function = find_tests)',type=int)
    args = parser.parse_args()

    if args.action=='loc_coverage':
        loc_coverage()
    elif args.action=='test_coverage':
        if args.test is None:
            print "Please enter a Test Name to continue"
        else:
            test_coverage(args.test)
    else:
        if args.file is None or args.line is None:
            print "Please enter a File Name and Line Number to continue"
        else:
            find_tests(args.file,args.line)

