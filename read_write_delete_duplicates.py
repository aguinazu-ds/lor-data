import json

def readData(filename):
    data = None
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

def writeData(filename, data):
    with open(filename, 'w') as file:
         file.write(format(json.dumps(data, ensure_ascii=False, indent=4)))

def delete_duplicates_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]