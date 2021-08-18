from flask import Flask
from flask import json
import logging

app = Flask(__name__)



@app.route('/status')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    ## log line
    logger.info('Status request successfull')

    return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )

    ## log line
    logger.info('Metrics request successfull')

    return response

@app.route("/")
def hello():

    ## log line
    logger.info('Main request successfull')

    return "Hello World!"

if __name__ == "__main__":
    
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level
    logger.setLevel(logging.DEBUG)

    # define file handler and set formatter
    file_handler = logging.FileHandler('app.log')
    #formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    formatter    = logging.Formatter('%(asctime)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    #logger.basicConfig(filename='app.log',level=logging.DEBUG)

    app.run(host='0.0.0.0')


