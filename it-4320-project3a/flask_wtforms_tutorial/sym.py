import json

def test():
    with open('flask_wtforms_tutorial/symbols.json') as file:
        data = json.load(file)

    symbols = []

    for each in data:
        symbols.append(each["ACT Symbol"])
    
    return symbols
    
