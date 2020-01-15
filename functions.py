import gspread
from oauth2client.service_account import ServiceAccountCredentials
from statistics import mean
from savings_calculator import *

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("connection_test").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

#Delete missing semester 1 and 2 for now
#November 7th
#Remove how we do it

def cumulativeReturn(years_ago, initial_contribution, data):
    if years_ago < 1 or years_ago > 92:
        return "Err--Invalid Date Range"
    else:
        row = data[years_ago - 1]
        print("\n"+str(row)+"\n")
        return int(round(initial_contribution * float(row['c_return'])))

def getSampleSpace(start_bound, end_bound):
    years_ago_start = 2019 - int(start_bound)
    years_ago_end = 2019 - int(end_bound)
    space = []
    
    for row in range(years_ago_end - 1, years_ago_start):
        space.append(row)

    return reversed(space)
    

def cumulativeReturnRange(start_bound, end_bound, initial_contribution, annual_contribution):
    if int(end_bound) > 2019 or int(start_bound) < 1926 or (int(end_bound) - int(start_bound)) < 0:
        return "Invalid Range"
    else:
        balance = initial_contribution
        data = list_of_hashes
        space = getSampleSpace(start_bound, end_bound)
        running = 0

        for row in space:
            balance = ((1 + float(data[row]['a_return'])/100) * balance) + annual_contribution * ((1 + float(data[row]['a_return'])/ 100))

        return int(round(balance))

def maxYearReturn(start_bound, end_bound):
    data = list_of_hashes
    space = getSampleSpace(start_bound, end_bound)
    year_storage = None
    percent_storage = None

    for row in space:
        if percent_storage == None or float(data[row]['a_return']) > percent_storage:
            percent_storage = float(data[row]['a_return'])
            year_storage = int(data[row]['year'])
        
    return (year_storage, percent_storage)

def minYearReturn(start_bound, end_bound):
    data = list_of_hashes
    space = getSampleSpace(start_bound, end_bound)
    year_storage = None
    percent_storage = None

    for row in space:
        if percent_storage == None or float(data[row]['a_return']) < percent_storage:
            percent_storage = float(data[row]['a_return'])
            year_storage = int(data[row]['year'])
        
    return (year_storage, percent_storage)

def avgYearReturn(start_bound, end_bound):

    data = list_of_hashes
    space = getSampleSpace(start_bound, end_bound)
    storage = []

    for row in space:
        storage.append(float(data[row]['a_return']))
        print(int(data[row]['a_return']))
        
    return round(mean(storage), 2)

def getReturnProportions(start_bound, end_bound):
    data = list_of_hashes
    space = getSampleSpace(start_bound, end_bound)
    storage = []
    up_years = 0
    down_years = 0

    for row in space:
        if int(data[row]['a_return']) > 0:
            up_years += 1
        elif int(data[row]['a_return']) < 0:
            down_years += 1
        else:
            pass
    
    return (round(round((up_years / (up_years + down_years)),4) * 100,2)  , round(round(1 - (up_years / (up_years +down_years)), 4) * 100,2), up_years, down_years)

def getReturnPercentages(start_bound, end_bound, initial_contribution, annual_contribution):
    """
        Returns % _return on initial, annual, and C(initial && annual)
    """
    data = list_of_hashes
    space = getSampleSpace(start_bound, end_bound)
    annual_contrib_running = 0
    initial_contrib_running = initial_contribution
    base = 0
    balance = initial_contribution
    
    for row in space:
        annual_contrib_running = (annual_contribution+ annual_contrib_running) * ((1 + float(data[row]['a_return'])/ 100))
        initial_contrib_running = initial_contrib_running * (1 + (float(data[row]['a_return'])/100))
        balance = ((1 + float(data[row]['a_return'])/100) * balance) + annual_contribution * ((1 + float(data[row]['a_return'])/ 100))
        base += 1
        total_contrib = initial_contribution + base * annual_contribution

    if annual_contrib_running != 0:
        annual_contrib_running = ((annual_contrib_running) - annual_contribution * base) / total_contrib

    if initial_contrib_running != 0:
        initial_contrib_running = ((initial_contrib_running) - initial_contribution) / initial_contribution

    return {
        "total_contribution" : total_contrib, 
        "end_balance" : round(balance),
        "total_return_percent" : round(100 * (balance - total_contrib) / total_contrib,2), 
        "initial_contribution_return" : round(initial_contrib_running * 100, 2), 
        "annual_contribution_return" : round(annual_contrib_running * 100, 2)
    }
    ##This makes cumulative return redundant. When implementing api calls with this method, be sure to refactor

def testReturnPercentages():
    print(getReturnPercentages(2000, 2018, 1000, 1000))

def testCumulativeReturn():
    years_ago = 2
    initial_c = 1000
    data = list_of_hashes
    print()
    print("Function: testCumulativeReturn")
    print("--")
    print("Years ago: %i" %years_ago)
    print("Initial Contribution: %f" %initial_c)
    print("--")
    print(cumulativeReturn(years_ago, initial_c, data))
    print("--")

def testCumulativeReturnRange():
    start_bound = 1950
    end_bound = 2018
    initial_c = 1000
    annual_c = 100
    print()
    print("Function: testCumulativeReturnRange")
    print("--")
    print("Range: %i, %i" %(start_bound, end_bound))
    print("Initial Contribution: %i" %(initial_c))
    print("--")
    print(cumulativeReturnRange(start_bound, end_bound, initial_c, annual_c))
    print("--")

def testMaxYearReturn():
    start_bound = 1950
    end_bound = 2018
    print(maxYearReturn(start_bound, end_bound))

def testMinYearReturn():
    start_bound = 1950
    end_bound = 2018
    print(maxYearReturn(start_bound, end_bound))


def main():
    #testCumulativeReturn()
    #testCumulativeReturnRange()
    #testMaxYearReturn()
    #testMinYearReturn()
    testReturnPercentages()
    pass

if __name__ == "__main__":
    main()