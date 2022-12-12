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
        if grade and matric:
            clearData()

            filepath = "data.csv"

            with open(filepath, 'a') as file:
                field_names = ['Name', 'Matric', 'Grade']
                input = DictWriter(file, fieldnames=field_names)
                row = {'Name': firstName + " " + lastName,
                    'Matric': matric, 'Grade': grade+''}
                input.writerow(row)

                file.close()
        else:
            messagebox.showerror(None, 'Grade and Score is required')
    else:
        messagebox.showerror(None, 'Firstname and Lastname is required')


import tkinter as tk

def solveCSV():
    file = "data.csv"
    df = pd.read_csv(file, usecols=['Name', 'Grade'])
    table = df.loc[:, 'Grade']  
    students = np.array(df)
    
    # Create a new Tkinter window
    window = tk.Tk()
    
    # Add a label to the window that displays the mean
    mean_label = tk.Label(window, text="Mean: " + str(np.mean(table)))
    mean_label.pack()
    
    # Add a label to the window that displays the maximum score
    max_label = tk.Label(window, text="Maximum Score: " + str(max(table)))
    max_label.pack()
    
    # Add a label to the window that displays the minimum score
    min_label = tk.Label(window, text="Minimum Score: " + str(min(table)))
    min_label.pack()

    # Add a label to the window that displays the minimum score
    median_label = tk.Label(window, text="Median Score: " + str(solveMedian(file)))
    median_label.pack()

    above_label = tk.Label(window, text="Students that score 70 and above are: " + str(solveMoreOrLess(file, 70, "greater")))
    above_label.pack()

    below_label = tk.Label(window, text="Students that failed are: " + str(solveMoreOrLess(file, 45, "less")))
    below_label.pack()
    
    window.mainloop()

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


def solveBest(file: str, best: int):
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
            best_student.append(i['Name'])
    return ", ".join(best_student)


def solveMoreOrLess(file: str, num: int, type: str):
    newList = {}
    with open(file, "r") as f:
        reader = DictReader(f, delimiter=",")
        for row in reader:
            name = row["Name"]
            grade = row["Grade"]
            newList[name] = int(grade)
    solved_data = []
    for name, grade in newList.items():
        if type == 'greater':
            if grade > num:
                solved_data.append(name)
        elif type == "less":
            if grade < num:
                solved_data.append(name)
    return ", ".join(solved_data)

    
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

# Solve Stats data
stats_button = Button(frame, text="Solve Stats", command=solveCSV)
stats_button.grid(row=3, column=0, sticky="news", padx=50, pady=10)

window.mainloop()
