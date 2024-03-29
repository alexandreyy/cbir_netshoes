'''
Segmentation service.
'''

from flask import Flask, request, jsonify
from search_mx import Matcher
import requests
import os
import shutil


# Create Flask application.
app = Flask(__name__)
matcher = Matcher("../../grupo2storage2/features/dnn/features_mx.pickle",
                  "../../grupo2storage2/features/dnn/skus_mx.pickle")


@app.route('/matcher-mx', methods=['POST'])
def matcherHandler():
    """ Match an image from url.
    """

    # Load data from json.
    try:
        content = request.json

        url = content["url"]

        r = requests.get(url, stream=True)
        tempfile = '/tmp/{0}'.format(os.path.basename(url))

        with open(tempfile, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('calling matcher')
        skus = matcher.match(tempfile)

        os.remove(tempfile)

        # Set result.
        json_data = {"skus": skus}

    except Exception as e:
        print(e)
        json_data = {
            "url": "",
            "error": "Invalid json data."}

    result = jsonify(json_data)
    return result


# Run service on port 8090.
app.run(host='0.0.0.0', port=8090)
