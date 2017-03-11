import os
import re
import wolframalpha
from wit import Wit

sample = {'msg_id': '281e0caf-9784-47c0-8093-423d35e87faa', '_text': 'Let me know when GOOG hits $500', 'entities': {'number': [{'confidence': 1, 'value': 500, 'type': 'value'}], 'stock': [{'confidence': 1, 'value': 'GOOG', 'type': 'value'}], 'currency': [{'confidence': 1, 'value': '$', 'type': 'value'}], 'change': [{'confidence': 1, 'value': 'reaches', 'type': 'value'}]}}
wolfsample = {'sources': {'@count': '1', 'source': {'@url': 'http://www.wolframalpha.com/sources/FinancialDataSourceInformationNotes.html', '@text': 'Financial data'}}, '@recalculate': '', '@parsetimedout': 'false', 'pod': [{'@numsubpods': '1', '@scanner': 'Identity', '@position': '100', '@title': 'Input interpretation', 'subpod': {'plaintext': 'Alphabet Class A Shares  (GOOGL)', '@title': '', 'img': {'@width': '222', '@height': '18', '@title': 'Alphabet Class A Shares  (GOOGL)', '@alt': 'Alphabet Class A Shares  (GOOGL)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3161f8h07081d3i471f00003696ce0ci2121f7b?MSPStoreType=image/gif&s=43'}}, '@id': 'Input', '@error': 'false'}, {'@numsubpods': '1', '@scanner': 'FinancialData', '@position': '200', '@title': 'Latest trade', 'states': {'@count': '1', 'state': {'@name': 'More', '@input': 'Quote__More'}}, 'subpod': {'plaintext': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@title': '', 'img': {'@width': '441', '@height': '18', '@title': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@alt': '$861.41 (£708.07) (GOOGL | NASDAQ | 9:00:00 pm GMT | 19 hrs 2 mins ago)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3171f8h07081d3i471f000030h53a5a74fdid73?MSPStoreType=image/gif&s=43'}}, '@id': 'Quote', '@primary': 'true', '@error': 'false'}, {'@numsubpods': '1', '@scanner': 'FinancialData', '@position': '400', '@title': 'Price history', 'states': {'@count': '3', 'state': {'@name': 'Log scale', '@input': 'PriceHistory__Log scale'}, 'statelist': [{'@value': 'Last year', '@delimiters': '', 'state': [{'@name': 'Last year', '@input': 'PriceHistory__Last year'}, {'@name': 'Last week', '@input': 'PriceHistory__Last week'}, {'@name': 'Last month', '@input': 'PriceHistory__Last month'}, {'@name': 'Last 2 years', '@input': 'PriceHistory__Last 2 years'}, {'@name': 'Last 5 years', '@input': 'PriceHistory__Last 5 years'}, {'@name': 'Last 10 years', '@input': 'PriceHistory__Last 10 years'}, {'@name': 'Last 30 years', '@input': 'PriceHistory__Last 30 years'}, {'@name': 'All data', '@input': 'PriceHistory__All data'}], '@count': '8'}, {'@value': 'Basic chart', '@delimiters': '', 'state': [{'@name': 'Basic chart', '@input': 'PriceHistory__Basic chart'}, {'@name': 'With MA', '@input': 'PriceHistory__With MA'}, {'@name': 'Candlestick chart', '@input': 'PriceHistory__Candlestick chart'}, {'@name': 'With trend', '@input': 'PriceHistory__With trend'}], '@count': '4'}]}, 'subpod': {'plaintext': 'minimum | average | maximum\n$681.14 | $783.13 | $861.40\n(Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@title': '', 'img': {'@width': '546', '@height': '254', '@title': ' minimum | average | maximum $681.14 | $783.13 | $861.40 (Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@alt': ' minimum | average | maximum $681.14 | $783.13 | $861.40 (Monday, Jun 27, 2016) |   | (Friday, Mar 10, 2017)', '@src': 'http://www5a.wolframalpha.com/Calculate/MSP/MSP3181f8h07081d3i471f0000235ef2he2ae2h12b?MSPStoreType=image/gif&s=43'}}, '@id': 'PriceHistory', '@error': 'false'}], 'assumptions': {'@count': '2', 'assumption': [{'@template': 'Assuming "${word}" is ${desc1}. Use as ${desc2} instead', 'value': [{'@name': 'Financial', '@desc': 'a financial entity', '@input': '*C.google-_*Financial-'}, {'@name': 'Internet', '@desc': 'an internet domain', '@input': '*C.google-_*Internet-'}, {'@name': 'Word', '@desc': 'a word', '@input': '*C.google-_*Word-'}], '@type': 'Clash', '@count': '3', '@word': 'google'}, {'@template': 'Assuming ${desc1}. Use ${desc2} instead', 'value': [{'@name': 'NASDAQ:GOOGL', '@desc': 'GOOGL', '@input': '*DPClash.FinancialE.google-_*NASDAQ%3AGOOGL-'}, {'@name': 'NASDAQ:GOOG', '@desc': 'GOOG', '@input': '*DPClash.FinancialE.google-_*NASDAQ%3AGOOG-'}], '@type': 'SubCategory', '@count': '2', '@word': 'google'}]}, '@timing': '11.196', '@error': 'false', '@numpods': '3', '@server': '43', '@host': 'http://www5a.wolframalpha.com', '@success': 'true', '@related': 'http://www5a.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa3151f8h07081d3i471f00003h7ffdc76h1ad9942763595553672727499', '@timedoutpods': 'Recent returns,Performance comparisons,Correlation matrix,Daily return analysis,Projections,Daily returns versus S&P 500,Company information,Company logo,Company management,Wikipedia summary', '@datatypes': 'Financial', '@timedout': '', '@id': 'MSPa3141f8h07081d3i471f000054ga282g9e7b7abh', '@parsetiming': '0.11900000000000001', '@version': '2.6'}
wolfapple = {'sources': {'@count': '1', 'source': {'@text': 'Financial data', '@url': 'http://www.wolframalpha.com/sources/FinancialDataSourceInformationNotes.html'}}, '@timedoutpods': 'Recent returns,Performance comparisons,Correlation matrix,Daily return analysis,Projections,Daily returns versus S&P 500,Company information,Company logo,Company management,Wikipedia summary', '@success': 'true', '@numpods': '3', '@version': '2.6', '@server': '59', '@related': 'http://www4c.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa2336211cb13924c5584700004f22hiigbf4fa3774818584333534952213', '@recalculate': '', 'pod': [{'subpod': {'img': {'@title': 'Apple  (AAPL)', '@height': '18', '@src': 'http://www4c.wolframalpha.com/Calculate/MSP/MSP2337211cb13924c55847000023e98ageaa53id8g?MSPStoreType=image/gif&s=59', '@alt': 'Apple  (AAPL)', '@width': '89'}, '@title': '', 'plaintext': 'Apple  (AAPL)'}, '@error': 'false', '@numsubpods': '1', '@id': 'Input', '@scanner': 'Identity', '@title': 'Input interpretation', '@position': '100'}, {'subpod': {'img': {'@title': '$139.14 (£114.37) (AAPL | NASDAQ | 9:00:00 pm GMT | 19 hrs 36 mins ago)', '@height': '18', '@src': 'http://www4c.wolframalpha.com/Calculate/MSP/MSP2338211cb13924c558470000553g8b37g2gaf319?MSPStoreType=image/gif&s=59', '@alt': '$139.14 (£114.37) (AAPL | NASDAQ | 9:00:00 pm GMT | 19 hrs 36 mins ago)', '@width': '432'}, '@title': '', 'plaintext': '$139.14 (£114.37) (AAPL | NASDAQ | 9:00:00 pm GMT | 19 hrs 36 mins ago)'}, '@error': 'false', 'states': {'@count': '1', 'state': {'@name': 'More', '@input': 'Quote__More'}}, '@primary': 'true', '@numsubpods': '1', '@id': 'Quote', '@scanner': 'FinancialData', '@title': 'Latest trade', '@position': '200'}, {'subpod': {'img': {'@title': ' minimum | average | maximum $90.34 | $110.36 | $139.79 (Thursday, May 12, 2016) |   | (Wednesday, Mar 1, 2017)', '@height': '254', '@src': 'http://www4c.wolframalpha.com/Calculate/MSP/MSP2339211cb13924c55847000066cedhh218c2006d?MSPStoreType=image/gif&s=59', '@alt': ' minimum | average | maximum $90.34 | $110.36 | $139.79 (Thursday, May 12, 2016) |   | (Wednesday, Mar 1, 2017)', '@width': '546'}, '@title': '', 'plaintext': 'minimum | average | maximum\n$90.34 | $110.36 | $139.79\n(Thursday, May 12, 2016) |   | (Wednesday, Mar 1, 2017)'}, '@error': 'false', 'states': {'@count': '3', 'statelist': [{'@count': '8', '@value': 'Last year', '@delimiters': '', 'state': [{'@name': 'Last year', '@input': 'PriceHistory__Last year'}, {'@name': 'Last week', '@input': 'PriceHistory__Last week'}, {'@name': 'Last month', '@input': 'PriceHistory__Last month'}, {'@name': 'Last 2 years', '@input': 'PriceHistory__Last 2 years'}, {'@name': 'Last 5 years', '@input': 'PriceHistory__Last 5 years'}, {'@name': 'Last 10 years', '@input': 'PriceHistory__Last 10 years'}, {'@name': 'Last 30 years', '@input': 'PriceHistory__Last 30 years'}, {'@name': 'All data', '@input': 'PriceHistory__All data'}]}, {'@count': '4', '@value': 'Basic chart', '@delimiters': '', 'state': [{'@name': 'Basic chart', '@input': 'PriceHistory__Basic chart'}, {'@name': 'With MA', '@input': 'PriceHistory__With MA'}, {'@name': 'Candlestick chart', '@input': 'PriceHistory__Candlestick chart'}, {'@name': 'With trend', '@input': 'PriceHistory__With trend'}]}], 'state': {'@name': 'Log scale', '@input': 'PriceHistory__Log scale'}}, '@numsubpods': '1', '@id': 'PriceHistory', '@scanner': 'FinancialData', '@title': 'Price history', '@position': '400'}], '@datatypes': 'Financial', '@parsetimedout': 'false', '@id': 'MSPa2335211cb13924c5584700001dhh7f0a2d7384cc', '@timing': '10.161', 'assumptions': {'@count': '1', 'assumption': {'value': [{'@desc': 'a financial entity', '@name': 'Financial', '@input': '*C.apple-_*Financial-'}, {'@desc': 'a food', '@name': 'ExpandedFood', '@input': '*C.apple-_*ExpandedFood-'}, {'@desc': 'an internet domain', '@name': 'Internet', '@input': '*C.apple-_*Internet-'}, {'@desc': 'a computers & electronics retail chain', '@name': 'RetailLocationClass', '@input': '*C.apple-_*RetailLocationClass-'}, {'@desc': 'a plant', '@name': 'Plant', '@input': '*C.apple-_*Plant-'}, {'@desc': 'a general material', '@name': 'CommonMaterial', '@input': '*C.apple-_*CommonMaterial-'}, {'@desc': 'a word', '@name': 'Word', '@input': '*C.apple-_*Word-'}, {'@desc': ' referring to a mathematical definition', '@name': 'MathWorld', '@input': '*C.apple-_*MathWorld-'}], '@count': '8', '@template': 'Assuming "${word}" is ${desc1}. Use as ${desc2} instead', '@type': 'Clash', '@word': 'apple'}}, '@error': 'false', '@parsetiming': '0.295', '@timedout': '', '@host': 'http://www4c.wolframalpha.com'}

wolfsearch = re.compile('\(([A-Z]{2}(?:[^) ]){1,8})\)')

def get_samples():
    return (sample, wolfsample, wolfapple)

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
    (first, second, third) = get_samples()
    print(find_stockcode(second))
