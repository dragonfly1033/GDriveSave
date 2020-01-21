from backup import *

test_string = 'test bkuptst.py lastlast'

print(test_string)

service, gdserv, docs = get_values()
save(__file__,service, docs)

