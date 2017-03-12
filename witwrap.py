# coding=utf-8
import os
import re
from collections import defaultdict

import wolframalpha
from wit import Wit

global kill

wolfsearch = re.compile('\(([A-Z]{2}(?:[^) ]){0,7})\)')

try:
    real_raw_input = vars(__builtins__).get('raw_input', input)
except TypeError:
    pass


def configure_wit(actions=None):
    if actions is None:
        actions = {}
    wit_key = os.environ.get('WIT_KEY')
    wolf_key = os.environ.get('WOLF_KEY')
    if wit_key is None:
        raise EnvironmentError("Couldn't retrieve client key")
    wit_here = Wit(access_token=wit_key, actions=actions)
    if wolf_key is None:
        return wit_here, None
    wolfram = wolframalpha.Client(wolf_key)
    return wit_here, wolfram


def wolfram_whole_request(request):
    (wit, wolf) = configure_wit()
    return wolf.query(request)


def parse_message(msg, clients):
    
    (witstance, wolfstance) = clients
    response = witstance.message(msg)['entities']
    tupform = [
        (key, dic['value']) for
        (dicts, key) in [(response[key], key) for key in response]
        for dic in dicts
        ]
    fin = defaultdict(list)
    for (r, y) in tupform:
        fin[r].append(y)
    if 'average' in fin['metric']:
        fin['metric'] = ['simple moving average' if z == "average" else z for z in fin['metric'] ]
    if 'stock' not in fin:
        if 'utils' in fin:
            return fin
        if 'name' in fin and len(fin['name']) == 1:
            wolres = wolfstance.query(fin['name'] + " stock")
            try:
                wolparse = wolres['pod'][0]['subpod']['plaintext']
                stock = re.findall('([A-Z]{2}(?:[^) ]){1,8})', wolparse)
                if len(stock) == 1:
                    fin['stock'] = stock[0]
            except KeyError:
                pass
        else:
            stock = re.findall('([A-Z](?:[^ a-z]){2,9})', msg)
            if len(stock) != 1:
                company_name = re.findall('^.+ .?([A-Z][a-z]+)(?= )', msg)
                if len(company_name) != 1:
                    raise KeyError('failed to identify stock name!')
                else:
                    wolfresponse = wolfstance.query(company_name[0] + " stock")
                    wolfproc = find_stockcode(wolfresponse)
                    if wolfproc[1]:
                        fin['stock'].append(wolfproc[0])
                    else:
                        raise KeyError('failed to identify stock name!')
            else:
                fin['stock'] = stock[0]
    #print(fin)
    if 'currency' in fin and 'percent' in fin:
        del fin['currency']
    #print(fin)
    global kill
    kill = msg
    vvf = dedictify(process_dict(fin))
    if type(vvf['stock']) is list:
        if len(vvf['stock']) > 1:
            vvf['stock'] = vvf['stock'][-1]
    return vvf


def dedictify(responsedict):
    returndict = {}
    for (k, v) in responsedict.items():
        if len(v) == 1:
            returndict[k] = v[0]
        else:
            returndict[k] = v
    return returndict


def process_dict(responsedict):
    global kill
    less = False
    if 'comparison' in responsedict:
        if "less" in responsedict['comparison']:
            less = True
            for (s, y) in responsedict.items():
                if s != "comparison":
                    if len(y) == 2:
                        responsedict['lesser'].append(y[0])
                        responsedict['greater'].append(y[1])
                        del responsedict[s]
            del responsedict['comparison']
            if 'number' in responsedict:
                if len(responsedict['number']) == 1:
                    loc = kill.find(str(responsedict['number'][0]))
                    if loc > int(len(kill) / 2):
                        responsedict['greater'].append(responsedict['number'][0])
                    else:
                        responsedict['lesser'].append(responsedict['number'][0])
                    del responsedict['number']
        elif "greater" in responsedict['comparison']:
            for (t, y) in responsedict.items():
                if t != "comparison":
                    if len(y) == 2:
                        responsedict['greater'].append(y[0])
                        responsedict['lesser'].append(y[1])
                        del responsedict[t]
            del responsedict['comparison']
            if 'number' in responsedict:
                if len(responsedict['number']) == 1:
                    loc = kill.find(str(responsedict['number'][0]))
                    if loc > int(len(kill) / 2):
                        responsedict['lesser'].append(responsedict['number'][0])
                    else:
                        responsedict['greater'].append(responsedict['number'][0])
                    del responsedict['number']
        else:
            raise NameError("Non-less or greater in comparison")
    if len(responsedict['lesser']) == 1 and responsedict['lesser'] != []:
        if 'metric' in responsedict:
            if less:
                responsedict['lesser'] = [responsedict['metric'][0]] + responsedict['lesser']
            else:
                responsedict['greater'] = [responsedict['metric'][0]] + responsedict['greater']
            del responsedict['metric']
    if type(responsedict['lesser']) is list:
        responsedict['lesser'] = sorted(responsedict['lesser'], reverse=True)
    if type(responsedict['greater']) is list:
        responsedict['greater'] = sorted(responsedict['greater'], reverse=True)
    for (k, v) in responsedict.items():
        if not v:
            del responsedict[k]
    return responsedict


def find_stockcode(wolfdict):
    if isinstance(wolfdict, dict):
        for item in wolfdict.values():
            response = find_stockcode(item)
            if response[1]:
                return response
        return None, False
    elif isinstance(wolfdict, list):
        for item in wolfdict:
            response = find_stockcode(item)
            if response[1]:
                return response
    else:
        if wolfdict is not None:
            searched = wolfsearch.findall(wolfdict)
            if len(searched) == 1:
                return searched[0], True
    return None, False


if __name__ == "__main__":
    rawin = ""
    z = configure_wit()
    while rawin != "exit":
        rawin = real_raw_input(">>>")
        x = (parse_message(rawin, z))
        print(x)