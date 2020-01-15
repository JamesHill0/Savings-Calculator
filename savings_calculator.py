 #!/usr/bin/python

import csv
import sys

#input number you want to search
#read csv, and split on "," the line
imported_file = csv.reader(open('savings_calculator.csv', "r"), delimiter=",")
hud_data = csv.reader(open('hud-data.csv', "r"), delimiter=",")

def getBLSRow(location_input, career_input, csv_file):
    #loop through csv list
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if location_input == row[1] and career_input == row[9]:
            print(row)
            return row

def getHUDRow(location_input, csv_file):
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if location_input == row[2]:
            print(row)
            return row

def getBLSLocationInputs(csv_file):
    locations = []
    states = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virgin Island','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    for row in csv_file:
        if str(row[1]) in states:
            locations.append(str(row[1]))
    
    return set(locations)

def getBLSCareerInputs(csv_file):
    careers = []
    for row in csv_file:
        careers.append(row[9])
    
    return set(careers)
    
def getHUDLocationInputs(csv_file):
    locations = []
    for row in csv_file:
        locations.append(row[2])

    return set(locations)

def goalMade(annual_contribution, end_amount, years):
    counter = 0
    contrib = annual_contribution
    marker = None
    for x in range(0,years):
        counter += contrib
        counter *= 1.1
        contrib *= 1.03
        if counter >= end_amount and marker == None:
            marker = int(x)
    print(counter)
    print(end_amount)
    return [counter, bool(counter >= end_amount), marker]

def testGetBLSRow():
    getBLSRow("Alabama","Accountants and Auditors", imported_file)

def testGetHUDRow():
    getHUDRow("Gadsden, AL MSA", hud_data)

def testGetBLSLocationInputs():
    print(getBLSLocationInputs(imported_file))

def testGetBLSCareerInputs():
    print(getBLSCareerInputs(imported_file))

def testGetHUDLocationInputs():
    print(getHUDLocationInputs(hud_data))

def main():
    testGetBLSRow()
    testGetHUDRow()
    testGetBLSCareerInputs()
    #testGetBLSLocationInputs()
    #testGetHUDLocationInputs()

if __name__ == "__main__":
    main()