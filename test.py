import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

def cumulativeReturnRange(start_bound, end_bound, initial_contribution, annual_contribution, data):
    if int(end_bound) > 2019 or int(start_bound) < 1926 or (int(end_bound) - int(start_bound)) < 0:
        return "Invalid Range"
    else:
        years_ago_start = 2019 - int(start_bound)
        years_ago_end = 2019 - int(end_bound)
        print(years_ago_start)
        print(years_ago_end)
        balance = initial_contribution
        for row in range(years_ago_end - 1, years_ago_start):
            balance = ((1 + float(data[row]['a_return'])/100) * balance) + annual_contribution
        return int(round(balance))


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
    start_bound = 2000
    end_bound = 2018
    initial_c = 1000
    annual_c = 100
    data = list_of_hashes
    print()
    print("Function: testCumulativeReturnRange")
    print("--")
    print("Range: %i, %i" %(start_bound, end_bound))
    print("Initial Contribution: %i" %(initial_c))
    print("Annual Contribution: %i" %(annual_c))
    print("--")
    print(cumulativeReturnRange(start_bound, end_bound, initial_c, annual_c, data))
    print("--")

def main():
    testCumulativeReturnRange()

if __name__ == "__main__":
    main()