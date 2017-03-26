#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request

from gmaps import GoogleMaps
from uber import Uber
from lyft import Lyft

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def webhook():
    #start = str(request.args.get('start'))
    #end = str(request.args.get('end'))
    start = "2184 Pettigrew Drive"
    end ="6816 Turturici Court"
    
    google_maps_results = GoogleMaps(start, end)
    print(google_maps_results)
    uber_results = Uber(google_maps_results[0], google_maps_results[1], google_maps_results[2], google_maps_results[3])
    lyft_results = Lyft(google_maps_results[0], google_maps_results[1], google_maps_results[2], google_maps_results[3])
    res = makeWebhookResult(uber_results, lyft_results)
    return json.dumps(res)


def makeWebhookResult(uber_results, lyft_results):
    speech = "The cost is " + str(uber_results) + " for Uber and $" + str(lyft_results) + " for Lyft."
    
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-price-webhookhandler"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
