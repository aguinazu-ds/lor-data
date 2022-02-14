import json

def write_to_json(lst, fn):
    with open(fn, 'a', encoding='utf-8') as file:
        for item in lst:
            x = json.dumps(item, indent=4)
            file.write(x + '\n')
