import os
import re
import wolframalpha
from wit import Wit

sample = {'msg_id': '281e0caf-9784-47c0-8093-423d35e87faa', '_text': 'Let me know when GOOG hits $500', 'entities': {'number': [{'confidence': 1, 'value': 500, 'type': 'value'}], 'stock': [{'confidence': 1, 'value': 'GOOG', 'type': 'value'}], 'currency': [{'confidence': 1, 'value': '$', 'type': 'value'}], 'change': [{'confidence': 1, 'value': 'reaches', 'type': 'value'}]}}
wolfsample = {'sources': {'@count': '1', 'source': {'@url': 'http://www.wolframalpha.com/sources/FinancialDataSourceInformationNotes.html', '@text': 'Financial data'}}, '@recalculate': '', '@parsetimedout': 'false', 'pod': [{'@numsubpods': '1', '@scanner': 'Identity', '@position': '100', '@title': 'Input interpretation', 'subpod': {'plaintext': 'Alphabet Class A Shares  (GOOGL)', '@title': '', 'img': {'@width': '222', '@height': '18', '@title': 'Alphabet Class A Shares  (GOOGL)', '@alt': 'Alphabet Class A Shares  (GOOGL)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3161f8h07081d3i471f00003696ce0ci2121f7b?MSPStoreType=image/gif&s=43'}}, '@id': 'Input', '@error': 'false'}, {'@numsubpods': '1', '@scanner': 'FinancialData', '@position': '200', '@title': 'Latest trade', 'states': {'@count': '1', 'state': {'@name': 'More', '@input': 'Quote__More'}}, 'subpod': {'plaintext': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@title': '', 'img': {'@width': '441', '@height': '18', '@title': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@alt': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3171f8h07081d3i471f000030h53a5a74fdid73?MSPStoreType=image/gif&s=43'}}, '@id': 'Quote', '@primary': 'true', '@error': 'false'}, {'@numsubpods': '1', '@scanner': 'FinancialData', '@position': '400', '@title': 'Price history', 'states': {'@count': '3', 'state': {'@name': 'Log scale', '@input': 'PriceHistory__Log scale'}, 'statelist': [{'@value': 'Last year', '@delimiters': '', 'state': [{'@name': 'Last year', '@input': 'PriceHistory__Last year'}, {'@name': 'Last week', '@input': 'PriceHistory__Last week'}, {'@name': 'Last month', '@input': 'PriceHistory__Last month'}, {'@name': 'Last 2 years', '@input': 'PriceHistory__Last 2 years'}, {'@name': 'Last 5 years', '@input': 'PriceHistory__Last 5 years'}, {'@name': 'Last 10 years', '@input': 'PriceHistory__Last 10 years'}, {'@name': 'Last 30 years', '@input': 'PriceHistory__Last 30 years'}, {'@name': 'All data', '@input': 'PriceHistory__All data'}], '@count': '8'}, {'@value': 'Basic chart', '@delimiters': '', 'state': [{'@name': 'Basic chart', '@input': 'PriceHistory__Basic chart'}, {'@name': 'With MA', '@input': 'PriceHistory__With MA'}, {'@name': 'Candlestick chart', '@input': 'PriceHistory__Candlestick chart'}, {'@name': 'With trend', '@input': 'PriceHistory__With trend'}], '@count': '4'}]}, 'subpod': {'plaintext': 'minimum | average | maximum\n$681.14 | $783.13 | $861.40\n(Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@title': '', 'img': {'@width': '546', '@height': '254', '@title': ' minimum | average | maximum $681.14 | $783.13 | $861.40 (Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@alt': ' minimum | average | maximum $681.14 | $783.13 | $861.40 (Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3181f8h07081d3i471f0000235ef2he2ae2h12b?MSPStoreType=image/gif&s=43'}}, '@id': 'PriceHistory', '@error': 'false'}], 'assumptions': {'@count': '2', 'assumption': [{'@template': 'Assuming "${word}" is ${desc1}. Use as ${desc2} instead', 'value': [{'@name': 'Financial', '@desc': 'a financial entity', '@input': '*C.google-_*Financial-'}, {'@name': 'Internet', '@desc': 'an internet domain', '@input': '*C.google-_*Internet-'}, {'@name': 'Word', '@desc': 'a word', '@input': '*C.google-_*Word-'}], '@type': 'Clash', '@count': '3', '@word': 'google'}, {'@template': 'Assuming ${desc1}. Use ${desc2} instead', 'value': [{'@name': 'NASDAQ:GOOGL', '@desc': 'GOOGL', '@input': '*DPClash.FinancialE.google-_*NASDAQ%3AGOOGL-'}, {'@name': 'NASDAQ:GOOG', '@desc': 'GOOG', '@input': '*DPClash.FinancialE.google-_*NASDAQ%3AGOOG-'}], '@type': 'SubCategory', '@count': '2', '@word': 'google'}]}, '@timing': '11.196', '@error': 'false', '@numpods': '3', '@server': '43', '@host': 'http://www5a.wolframalpha.com', '@success': 'true', '@related': 'http://www5a.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa3151f8h07081d3i471f00003h7ffdc76h1ad9942763595553672727499', '@timedoutpods': 'Recent returns,Performance comparisons,Correlation matrix,Daily return analysis,Projections,Daily returns versus S&P 500,Company information,Company logo,Company management,Wikipedia summary', '@datatypes': 'Financial', '@timedout': '', '@id': 'MSPa3141f8h07081d3i471f000054ga282g9e7b7abh', '@parsetiming': '0.11900000000000001', '@version': '2.6'}

def get_samples():
    return (sample, wolfsample)

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

def test_pm():
    response = sample['entities']
    tupform = [
    (key, dict['value']) for 
        (dicts,key) in [(response[key],key) for key in response] 
    for dict in dicts
    ]
    return dict((x, y) for x, y in tupform)

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

if __name__ == "__main__":
    print(test_pm())
    