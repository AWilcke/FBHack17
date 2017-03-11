import os
import sys
import json

import requests
from flask import Flask, request
from witwrap import configure_wit

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
                    message_text = messaging_event["message"]["text"]  # the message's text

                    '''
                    # need to send text to wit
                    wit_out ={
                            'u_id':"12341234123412341234",
                            'stock':"GOOG",
                            'a':"day-high",
                            'b':"52-week-average",
                            'b_type':"variable",
                            'request':"create_alert"
                            }
                    
                    # log(wit_out)
                    # finally send confirmation message
                    wit_out['password'] = os.environ["PHPPASSWORD"]
                    # the send the output to php db
                    r = requests.post("http://www.anyonetrades.com/api.php", data=wit_out, verify=False)
                    log(r)
                    '''
                    send_message(sender_id, "Subscribed you to %s" % "test")

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

@app.route('/notify', methods=['POST'])
def notifyhook():

    data = request.get_json()
    
    log(data)
    # send_message(data['u_id'], data['notif'])

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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
