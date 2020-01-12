import csv



"""

    Get the corresponding row given occupation and location

"""
def getRow(occupation, location):
    with open('savings_calculator.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            if line[1] == location and line[9] == occupation:
                print(line)
                return line
            else:
                pass
        
        return None

"""

Test CSV load speed to ensure efficient page load times

"""        
def speedTest():
    with open('savings_calculator.csv', 'r') as csv_file:
        csv_object = csv.reader(csv_file)

        for line in csv_object:
            print(line)

def main():   
    print(getRow("Occupational Therapists", "Connecticut"))

if __name__ == "__main__":
    main()
