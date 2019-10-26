
#################################################################################
#IMPORTS
#################################################################################
from flask import *
from functions import *

#################################################################################
#GLOBALS
#################################################################################

app = Flask(__name__)

#################################################################################
#FLASK ROUTING
################################################################################

@app.route('/', methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/series_data', methods = ["POST"])
def get_series_data():
    authentication_status = True
    start = int(request.form['start'])
    end = int(request.form['end'])
    initial_contrib = int(request.form['initial_contrib'])
    annual_contrib = int(request.form['annual_contrib'])
    
    end_amount = cumulativeReturnRange(start, end, initial_contrib, annual_contrib)
    maxReturnData = maxYearReturn(start,end)
    minReturnData = minYearReturn(start,end)
    avg_return = avgYearReturn(start, end)
    return_proportions = getReturnProportions(start, end)

    output_params = {
        "authentication_status" : authentication_status,
        "end_amount" : end_amount,
        "avg_return" : avg_return,
        "max_return" : {
            "year" : maxReturnData[0],
            "amount" : maxReturnData [1]
        },
        "min_return" : {
            "year" : minReturnData[0],
            "amount" : minReturnData [1]
        },
        "growth_proportions" : {
            "percent_up_years" : return_proportions[0],
            "percent_down_years" : return_proportions[1],
            "up_years" : return_proportions[2],
            "down_years" : return_proportions[3]
        },
        "contribution" : {
            "total_contribution" : initial_contrib + (annual_contrib * (end - start))
            "return_percent_on_initial" : 
            "return_percent_on_annual" : 
            "return_percent_on_total" :
        }
    }
    print(output_params)

    return jsonify(output_params)

#################################################################################
#MAIN
#################################################################################

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()


