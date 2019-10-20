
#################################################################################
#IMPORTS
#################################################################################
from flask import *
from test import *

#################################################################################
#GLOBALS
#################################################################################

app = Flask(__name__)

#################################################################################
#FLASK ROUTING
#################################################################################

@app.route('/', methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/series_data', methods = ["POST", "GET"])
def get_series_data():
    authentication_status = True
    start = int(request.args['start'])
    end = int(request.args['end'])
    initial_contrib = int(request.args['initial_contrib'])
    annual_contrib = int(request.args['annual_contrib'])
    output = cumulativeReturnRange(start, end, initial_contrib, annual_contrib)

    output_params = {
        "authentication_status" : authentication_status,
        "output" : output
    }

    return jsonify(output_params)

#################################################################################
#MAIN
#################################################################################

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()


