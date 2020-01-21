
#################################################################################
#IMPORTS
#################################################################################
from flask import *
from functions import *
from flask_cors import CORS
from savings_calculator import *

#################################################################################
#GLOBALS
#################################################################################

app = Flask(__name__)
CORS(app)

#################################################################################
#FLASK ROUTING
################################################################################

@app.route('/', methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/savings', methods = ["GET"])
def savings():
    return render_template("savings.html")

@app.route('/series_data', methods = ["POST"])
def get_series_data():
    authentication_status = True
    start = int(request.form['start'])
    end = int(request.form['end'])
    initial_contrib = int(request.form['initial_contrib'])
    annual_contrib = int(request.form['annual_contrib'])
    
    maxReturnData = maxYearReturn(start,end)
    minReturnData = minYearReturn(start,end)
    avg_return = avgYearReturn(start, end)
    return_proportions = getReturnProportions(start, end)
    return_percentages = getReturnPercentages(start, end, initial_contrib, annual_contrib)

    output_params = {
        "authentication_status" : authentication_status,
        "end_amount" : return_percentages["end_balance"],
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
        "contribution" : return_percentages
    }
    print(output_params)

    return jsonify(output_params)

@app.route('/savings_calculator', methods = ["POST"])
def savings_calculator():
    authentication_status = True
    _state = request.form['state']
    _county = request.form['county']
    _job = request.form['job']

    bls_data = csv.reader(open('savings_calculator.csv', "r"), delimiter=",")
    hud_data = csv.reader(open('hud-data.csv', "r"), delimiter=",")
    
    hudRow = getHUDRow(_county, hud_data)
    blsRow = getBLSRow(_state, _job, bls_data)

    investment_goal = int(request.form['investment_goal'])
    years = int(request.form['years'])
    bedrooms = int(request.form['number_bedrooms'])
    monthly_rent = int(hudRow[3 + bedrooms])
    expense_multiplier = int(request.form['dependents'])
    """
        Note: Change this when you change how jobs data is pulled.
    """
    
    utilities_expenses = int(monthly_rent / 4)
    transportation_expenses = int(monthly_rent / 5)
    insurance_expenses = int(monthly_rent / 7)
    food_expenses = int(monthly_rent / 2)
    misc_expenses = int(monthly_rent / 2)
    monthly_expenses = monthly_rent + utilities_expenses + transportation_expenses + food_expenses + insurance_expenses + food_expenses + misc_expenses

    savings_output = goalMade(int(blsRow[26].replace(',', '')) - (expense_multiplier * (monthly_expenses + 1)) - monthly_rent, investment_goal, years)

    if savings_output[1] == True:
        output_statement = "You're likely to achieve your savings goal."
    else:
        output_statement = "It's unlikely you would achieve your savings goal"

    output_params = {
        "authentication_status" : True,
        "goal_made" : savings_output[1],
        "amount_saved" : int(savings_output[0]),
        "output_statement" : output_statement,
        "years" : years,
        "income" : int(blsRow[26].replace(',', '')) * years,
        "rent" : "$" + str(monthly_rent),
        "utilities" : "$" + str(utilities_expenses),
        "transportation" : "$" + str(transportation_expenses),
        "insurance" : "$" + str(insurance_expenses),
        "food" : "$" + str(food_expenses),
        "monthly_savings" : str(int((investment_goal / years) / 12)),
        "monthly_expenses": "$" + str(monthly_expenses),
        "career": _job,
        "state": _state,
        "monthly_income" : int(int(blsRow[26].replace(",", "")) /12),
        "percentage" : int((int((investment_goal / years) / 12) / int(int(blsRow[26].replace(",", "")) /12)) * 100)
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


