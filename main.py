
#################################################################################
#IMPORTS
#################################################################################
from flask import *

#################################################################################
#GLOBALS
#################################################################################

app = Flask(__name__)

#################################################################################
#FLASK ROUTING
#################################################################################

@app.route('/', methods = ["POST"])
def index():
    if request.form["authenticator"] == "test":
        authentication_status = True
    else:
        authentication_status = False

    output_params = {
        "authentication_status" : authentication_status
    }

    return jsonify(output_params)

@app.route('/series_data', methods = ["POST"])
def get_series_data():
    if request.form["authenticator"] == "test":
        authentication_status = True
    else:
        authentication_status = False

    output_params = {
        "authentication_status" : authentication_status
    }

    return jsonify(output_params)

#################################################################################
#MAIN
#################################################################################

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()


