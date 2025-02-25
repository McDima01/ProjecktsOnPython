import json
import requests


def load_user_data():
    with open('UserCosts.json', 'r') as file:
        return json.load(file)

'''user_costs = json.loads('UserCosts.json')

print(user_costs)
'''

print(load_user_data())
