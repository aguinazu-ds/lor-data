import json

res = []
seen = set()

def add_entry(res, name, element, type):

    # check if in seen set
    if (name, element, type) in seen:
        return res

    # add to seen set
    seen.add(tuple([name, element, type]))

    # append to results list
    res.append({'name': name, 'element': element, 'type': type})

    return res