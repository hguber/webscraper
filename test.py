print(len(l3))
for x in l2:
    if x < datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
        l3.append(x)
pickle_save(l3, "save")
for x in l2:
    if x == datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
        globaldate = l2.index(x)