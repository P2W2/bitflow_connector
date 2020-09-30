import bernhard

c = bernhard.Client(host='localhost', port=5555)
q = c.query('host = "peewee-ThinkPad"')
#print(q)
for e in q:
    print(e)
