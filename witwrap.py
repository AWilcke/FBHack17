import os
import re
from wit import Wit

sample = {'msg_id': '281e0caf-9784-47c0-8093-423d35e87faa', '_text': 'Let me know when GOOG hits $500', 'entities': {'number': [{'confidence': 1, 'value': 500, 'type': 'value'}], 'stock': [{'confidence': 1, 'value': 'GOOG', 'type': 'value'}], 'currency': [{'confidence': 1, 'value': '$', 'type': 'value'}], 'change': [{'confidence': 1, 'value': 'reaches', 'type': 'value'}]}}

def get_sample():
    return sample

def configure_wit(actions={}):
    wit_key = os.environ.get('WIT_KEY')
    if wit_key is None:
        raise EnvironmentError("Couldn't retrieve client key")
    wit_here = Wit(access_token=wit_key, actions=actions)
    return wit_here

def test_pm():
    response = sample['entities']
    tupform = [
    (key, dict['value']) for 
        (dicts,key) in [(response[key],key) for key in response] 
    for dict in dicts
    ]
    return dict((x, y) for x, y in tupform)

def parse_message(msg, witstance):
    response = witstance.message(msg)['entities']
    tupform = [
    (key, dict['value']) for 
        (dicts,key) in [(response[key],key) for key in response] 
    for dict in dicts
    ]
    fin = dict((x, y) for x, y in tupform)
    if 'stock' not in fin:
        stock = re.findall('\$([^ ]{3,10})', fin)
        if len(stock) != 1:
            raise KeyError('failed to identify stock name!')
        else:
            fin['stock'] = stock[0]
    return fin

if __name__ == "__main__":
    print(test_pm())