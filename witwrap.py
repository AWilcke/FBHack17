import os
import re
import wolframalpha
from wit import Wit

wolfsearch = re.compile('\(([A-Z]{2}(?:[^) ]){1,8})\)')


def configure_wit(actions={}):
    wit_key = os.environ.get('WIT_KEY')
    wolf_key = os.environ.get('WOLF_KEY')
    if wit_key is None:
        raise EnvironmentError("Couldn't retrieve client key")
    wit_here = Wit(access_token=wit_key, actions=actions)
    if wolf_key is None:
        return (wit_here, None)
    wolfram = wolframalpha.Client(wolf_key)
    return (wit_here, wolfram)

def wolfram_whole_request(request):
    (wit, wolf) = configure_wit()
    return wolf.query(request)

def parse_message(msg, clients):
    (witstance, wolfstance) = clients
    response = witstance.message(msg)['entities']
    tupform = [
    (key, dict['value']) for 
        (dicts,key) in [(response[key],key) for key in response] 
    for dict in dicts
    ]
    fin = dict((x, y) for x, y in tupform)
    if 'stock' not in fin:
        if 'name' in fin and len(fin['name']) == 1:
            wolres = wolfstance.query(fin['name'])
            try:
                wolparse = wolres['pod'][0]['subpod']['plaintext']
                stock = re.findall('([A-Z]{2}(?:[^) ]){1,8})', wolparse)
            except:
                pass
        else:
            stock = re.findall('\$([A-Z](?:[^ ]){2,9})', msg)
            if len(stock) != 1:
                raise KeyError('failed to identify stock name!')
            else:
                fin['stock'] = stock[0]
    if 'currency' in fin and 'percent' in fin:
        del fin['currency']
    return fin

def find_stockcode(wolfdict):
    if isinstance(wolfdict, dict):
        for item in wolfdict.values():
            response = find_stockcode(item)
            if response[1]:
                return response
        return (None, False)
    elif isinstance(wolfdict, list):
        for item in wolfdict:
            response = find_stockcode(item)
            if response[1]:
                return response
    else:
        searched = wolfsearch.findall(wolfdict)
        if len(searched) == 1:
            return (searched[0], True)
    return (None, False)

if __name__ == "__main__":
    rawin = ""
    z = configure_wit()
    while (rawin != "exit"):
        rawin = raw_input(">>>")
        try:
            print(parse_message(rawin, z))
        except Exception as e: 
            print(str(e))
            pass