# This file contains the trigger scripts
import inspect
import sys
import trace
from test_a import *
from test_b import *
from pymongo import *

# print __name__
# print __file__
# print inspect.currentframe().f_lineno
# print inspect.trace()

# tracer = trace.Trace()
# tracer.run('test_a()')
# tracer.run('test_b()')
# r = tracer.results()
# print r.write_results(show_missing=True,coverdir="/Users/zthampi/Projects/track/logs/")

# test_a()
# test_b()

# Run a Python command passing local and global scopes
# import __main__
# cmd = """import random
# print \"abc\""""
# exec cmd in __main__.__dict__,__main__.__dict__

# class Track():
#     def __init__(self):
#         self.logs = []
#         self.f = open('/Users/zthampi/Projects/track/output.log','w')
#
#     def run(self,cmd):
#         sys.settrace(self.global_trace)
#         print cmd
#         import __main__
#         scope = __main__.__dict__
#         exec cmd in scope,scope
#         sys.settrace(None)
#
#     def global_trace(self,frame,event,arg):
#         print "######## GLOBAL TRACE : START #########"
#         print frame, frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno
#         # print frame, frame.f_code, frame.f_lineno
#         # print frame.f_back, frame.f_back.f_code, frame.f_back.f_lineno
#         print event
#         print arg
#         print "######## GLOBAL TRACE : END #########"
#         return self.local_trace
#
#     def local_trace(self,frame,event,arg):
#         # print "######## LOCAL TRACE : START #########"
#         # print frame, frame.f_code, frame.f_lineno
#         # print event
#         # print arg
#         # print "######## LOCAL TRACE : END #########"
#         pass
#
#     def close(self):
#         self.f.close()
#
# track = Track()
# track.run('test_a()')
# track.close()

base = '/Users/zthampi/Projects/track'
# f = open('/Users/zthampi/Projects/track/logs/output.log','w')
try:
    # Create MongoDB client
    client = MongoClient('localhost', 27017)
    # Clear data in Collection
    client['trackDB'].collection['runtime'].posts.drop()
except:
    print "ERROR : Mongo DB not running."
    sys.exit(1)

def get_parent(frame):
    while (frame.f_back and 'test_' not in frame.f_back.f_code.co_name):
        frame = frame.f_back
    if frame.f_back is None:
        return None
    else:
        return frame.f_back.f_code.co_name

def local_trace(frame,event,arg):
    # Proceed iff location is in the base location
    if base in frame.f_code.co_filename:
        test = get_parent(frame)
        # Proceed iff the call if part of a test
        if test is not None:
            # f.write(test + " : " + event + " : " + frame.f_code.co_name + " : " + frame.f_code.co_filename + " : " + str(frame.f_lineno) + '\n')
            client['trackDB'].collection['runtime'].posts.insert_one({'test': test, 'event': event, 'function': frame.f_code.co_name, 'file': frame.f_code.co_filename, 'line': frame.f_lineno})

def global_trace(frame,event,arg):
    # Proceed iff location is in the base location
    if base in frame.f_code.co_filename:
        test = get_parent(frame)
        # Proceed iff the call if part of a test
        if test is not None:
            # f.write(test + " : " + event + " : " + frame.f_code.co_name + " : " + frame.f_code.co_filename + " : " + str(frame.f_lineno) + '\n')
            client['trackDB'].collection['runtime'].posts.insert_one({'test': test, 'event': event, 'function': frame.f_code.co_name, 'file': frame.f_code.co_filename, 'line': frame.f_lineno})
    return local_trace

sys.settrace(global_trace)
test_a()
test_b()

# f.close()
sys.settrace(None)