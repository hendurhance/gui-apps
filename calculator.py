from tkinter import messagebox
from tkinter import *
from csv import DictWriter
from csv import DictReader
from csv import reader
import pandas as pd
import numpy as np
import string
from tkinter import filedialog
from pathlib import Path


# Defining data methods

# Clear Data
def clearData():
    firstNameEntry.delete(0, END)
    lastNameEntry.delete(0, END)
    gradeEntry.delete(0, END)
    matricEntry.delete(0, END)

# Open imported files
def openFile():
    filename = filedialog.askopenfilename()
    # check if the file selected is csv/excel
    file = Path(filename)
    if file.exists():
        # Check if file is a csv or xlxs file
        if filename.endswith(('.csv', '.xlsx')):
            print("File is: ", filename)
            # Read file and get those needed columns
            # Loop through it and push into data.csv
            with open(filename) as data_file:
                data_reader = reader(data_file, delimiter=",")

                list_of_col_names = []

                for row in data_reader:
                    list_of_col_names.append(row)

                    break
                
                df = pd.read_csv(file, names=['FirstName', 'Grade'])
                print("Stats data: ", df.describe())

            print("List of columns are: ", list_of_col_names[0])

    else:
        print("File does not exists")

# Load data 
def loadData(file: str):
    newList = []
    with open(file, "r") as f:
            reader = DictReader(f, delimiter=",")
            for row in reader:
                name = row["Name"]
                grade = row["Grade"]
                matric = row["Matric"]
                data = {'Name': name, 'Grade': int(grade), 'Matric': int(matric)}
                newList.append(data)
    return newList



def enterData():
    firstName = firstNameEntry.get()
    lastName = lastNameEntry.get()

    # Conditional statement to check if firstName and lastName exits
    if firstName and lastName:
        grade = gradeEntry.get()
        matric = matricEntry.get()

        # Output the following
        print("Name is {firstName} {lastName}".format(
            firstName=firstName, lastName=lastName))
        print("Grade: ", grade)
        print("Matric Number is: ", matric)
        clearData()

        filepath = "data.csv"

        with open(filepath, 'a') as file:
            field_names = ['Name', 'Matric', 'Grade']
            input = DictWriter(file, fieldnames=field_names)
            row = {'Name': firstName + " " + lastName, 'Matric': matric, 'Grade': grade}
            input.writerow(row)

            file.close()

def solveCSV():
    file = "data.csv"
    df = pd.read_csv(file, usecols=['Name', 'Grade'])
    table = df.loc[:, 'Grade']
    students = np.array(df)
    print('Mean: ', np.mean(table))
    print('Maximum Score is: ', max(table))
    print('Minimum Score is: ', min(table))
    print('Median score is: ', solveMedian(file))
    print('Best Student is: ', solveBest(file, max(table)))
    print("Students that score 70 and above are: ", solveMoreOrLess(file, 70, "greater"))
    print("Students that failed are: ", solveMoreOrLess(file, 45, "less"))

# Define stats functions

def solveMedian(file: str):
    newList = []
    with open(file, "r") as f:
            reader = DictReader(f, delimiter=",")
            for row in reader:
                grade = row["Grade"]
                if grade is not None:
                    newList.append(int(row['Grade']))
    newList.sort()
    n = len(newList)
    median = newList[n // 2]
    if n % 2 == 0:
        median = (median + newList[n // 2-1]) / 2
    return median

def solveBest(file: str, best :int):
    newList = []
    with open(file, "r") as f:
            reader = DictReader(f, delimiter=",")
            for row in reader:
                name = row["Name"]
                grade = row["Grade"]
                data = {'Name': name, 'Grade': int(grade)}
                newList.append(data)
    best_student = []
    for i in newList:
        if i['Grade'] >= best:
            best_student.append(i)
    return best_student[0]['Name'] + " with a score of: " + str(best_student[0]['Grade'])

def solveMoreOrLess(file: str, num: int, type: str):
    newList = []
    with open(file, "r") as f:
            reader = DictReader(f, delimiter=",")
            for row in reader:
                name = row["Name"]
                grade = row["Grade"]
                data = {'Name': name, 'Grade': int(grade)}
                newList.append(data)
    solved_data = []
    for i in newList:
        if type == 'greater':
            if i["Grade"] > num:
                solved_data.append(i['Name'])
        elif type == "less":
            if i["Grade"] < num:
                solved_data.append(i['Name'])
    return solved_data

window = Tk()
window.geometry("600x600")
window.title("Student Data Grade Entry App")


frame = Frame(window)
frame.pack()

user_info_frame = LabelFrame(frame, text="Student Details")
user_info_frame.grid(row=0, column=0, padx=20, pady=20)

first_name_label = Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

firstNameEntry = Entry(user_info_frame)
firstNameEntry.grid(row=1, column=0)
lastNameEntry = Entry(user_info_frame)
lastNameEntry.grid(row=1, column=1)

grade_label = Label(user_info_frame, text="Grade")
gradeEntry = Entry(user_info_frame)
grade_label.grid(row=2, column=0)
gradeEntry.grid(row=3, column=0)

matric_label = Label(user_info_frame, text="Matric Number")
matricEntry = Entry(user_info_frame)
matric_label.grid(row=2, column=1)
matricEntry.grid(row=3, column=1)

button = Button(frame, text="Enter Data", command=enterData)
button.grid(row=1, column=0, sticky="news", padx=50, pady=100)

# Import CSV file tkinter
csv_button = Button(frame, text="Import Data", command=openFile)
csv_button.grid(row=2, column=0, sticky="news", padx=50, pady=10)

# Solve Stats data
stats_button = Button(frame, text="Solve Stats", command=solveCSV)
stats_button.grid(row=3, column=0, sticky="news", padx=50, pady=10)

window.mainloop()
