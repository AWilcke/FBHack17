import os
import sys
import json

import requests
from flask import Flask, request
from witwrap import configure_wit, parse_message

app = Flask(__name__)
w = configure_wit()

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    except:
                        send_message(sender_id, "Sorry, this format is not supported.")
                        return "ok", 200

                    wit_out = parse_message(message_text, w)

                    log(wit_out)

                    wit_out['password'] = os.environ["PHPPASSWORD"]
                    wit_out['u_id'] = sender_id

                    # adding rule
                    if wit_out.has_key('change'):
                        
                        if wit_out.has_key('percent'):
                            wit_out['type'] = 'percent'

                        elif wit_out['change'] == 'reaches':
                            wit_out['type'] = 'absolute'

                        elif wit_out['change'] == 'up' or wit_out['change'] == 'down':
                            wit_out['type'] = 'relative'

                        if wit_out.has_key('metric'):
                            wit_out['a'] = key_to_lang(wit_out.pop(wit_out['metric']))
                            
                            # if needs time, add it
                            if wit_out['a'] == 'move' or wit_out['a'] == 'weight':
                                if len(wit_out['number'])<2:
                                    wit_out['a'] += '10'
                                else:
                                    wit_out['a'] += str(wit_out['number'][0])
                        else:
                            wit_out['a'] = 'value'

                        wit_out['b'] = wit_out['number'][-1]

                        log(wit_out)

                        r = requests.post("http://www.anyonetrades.com/api/create_alert.php", 
                                data=wit_out, verify=False)
                        send_message(sender_id, r.text)

                    elif wit_out.has_key('lesser') and wit_out.has_key('greater'):
                        
                        wit_out['type'] = 'variables'

                        if type(wit_out['greater']) == list:
                            wit_out['a'] = key_to_lang(wit_out['greater'][0]) + str(wit_out['greater'][1])
                        else:
                            wit_out['a'] = key_to_lang(wit_out['greater']) + '10'

                        if type(wit_out['lesser']) == list:
                            wit_out['b'] = key_to_lang(wit_out['lesser'][0]) + str(wit_out['lesser'][1])
                        else:
                            wit_out['b'] = key_to_lang(wit_out['lesser']) + '10'

                        log(wit_out)

                        r = requests.post("http://www.anyonetrades.com/api/create_alert.php", 
                                data=wit_out, verify=False)
                        send_message(sender_id, r.text)

                    # getting stats
                    elif wit_out.has_key('utils'):
                        r = requests.post("http://www.anyonetrades.com/api/get_alerts.php", 
                                data=wit_out, verify=False).json()
                        send_message(sender_id, "You have %s alerts. For more info, visit %s" % (r['num'],r["url"]))
                    
                    # querying current values
                    elif wit_out.has_key('stock') and wit_out.has_key('metric'):
                        s = "%s %s" % (wit_out['stock'], wit_out['metric'])

                        wit_out['metric'] = key_to_lang(wit_out['metric'])
                        if (wit_out['metric'] == 'move' or wit_out['metric'] == 'weight'):
                            if not wit_out.has_key('number'):
                                wit_out['number'] = 10
                            s += " over %s days" % (wit_out['number'])
                            wit_out['metric'] += str(wit_out['number'])


                        log(wit_out)

                        r = requests.post("http://www.anyonetrades.com/api/get_info.php", 
                                data=wit_out, verify=False).text

                        s += " is %s" % (r)
                        send_message(sender_id, s)

                    else:
                        send_message(sender_id, "Sorry, couldnt quite figure that out, would you mind rephrasing?")

    return "ok", 200

@app.route('/notify', methods=['POST'])
def notifyhook():

    data = request.json
    send_message(data['u_id'], data['notif'])
    return "ok", 200

@app.route('/update', methods=['POST'])
def updatehook():

    data = request.json

    sender_id = data["u_id"]        # the facebook ID of the person sending you the message
    message_text = data["query"]  # the message's text

    # need to send text to wit
    wit_out = parse_message(message_text, w)

    log(wit_out)

    wit_out['password'] = os.environ["PHPPASSWORD"]

    if wit_out.has_key('change'):
        # then send the output to php db
        r = requests.post("http://www.anyonetrades.com/api/create_alert.php", 
                data=wit_out, verify=False).json()
        send_message(sender_id, "Subscribed you to %s" % r)

    else:
        return "Failed", 400

    return "ok", 200


    
def send_message(recipient_id, message_text):

    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def key_to_lang(key):
    if key == 'weighted moving average':
        return 'weight'
    elif key == 'simple moving average':
        return 'move'
    else:
        return key

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
