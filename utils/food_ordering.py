import json

def load_menu():
    with open('menu.json', 'r') as file:
        return json.load(file)

