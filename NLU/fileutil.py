import json

def save_dict(name,dict):#.txt
    with open(name, 'w') as outfile:
        json.dump(dict, outfile)

def restore_dict(filename):#.txt
    with open(filename) as json_file:
        dict = json.load(json_file)
        return dict





