import json

with open('1.json', mode='r', encoding='utf=8') as file:
    print(len(json.load(file)['data']))
