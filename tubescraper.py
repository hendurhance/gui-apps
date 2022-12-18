from tkinter import *
from bs4 import BeautifulSoup
import requests
import json
from csv import DictWriter
from csv import DictReader
import re
import matplotlib.pyplot as plt


class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        self.myContainer1 = LabelFrame(parent, text="Youtube Search")
        self.myContainer2 = Frame(parent)
        self.myContainer1.grid(row=0, column=0, padx=50, pady=100)
        self.myContainer2.grid(row=1, column=0, padx=50, pady=10)

        self.label1 = Message(self.myContainer1, text="")

        self.label1.pack()

        self.entryVariable = StringVar()
        self.textbox = Entry(self.myContainer1)
        self.textbox.pack(side=TOP, fill=BOTH)
        self.textbox.bind("<Return>", self.searchYoutube)
        self.textbox.focus_set()

        self.label2 = Label(self.myContainer1)
        self.label2["text"] = ""
        self.label2.pack(side=BOTTOM)

        self.label3 = Message(self.myContainer1, text="")
        self.label3.pack()

        self.button1 = Button(self.myContainer2)
        self.button1["text"] = "Search"
        self.button1.pack(side=BOTTOM)
        self.button1.bind("<Button-1>", self.searchYoutube)
        textbox = self.textbox

        self.button2 = Button(self.myContainer2)
        self.button2["text"] = "Plot Pie Chart"
        self.button2.pack(side=BOTTOM)
        self.button2.bind("<Button-1>", self.plotPieChart)

    def searchYoutube(self, event):
        query = self.textbox.get()

        youtube_url = "https://www.youtube.com/results?search_query="+query
        response = requests.request("GET", youtube_url)
        soup = BeautifulSoup(response.text, "html.parser")
        response = soup.find_all("script")[33]
        json_text = re.search(
            'var ytInitialData = (.+)[,;]{1}', str(response)).group(1)
        json_data = json.loads(json_text)

        content = (
            json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
                'sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        )

        youtube_data = []

        for data in content:
            for key, value in data.items():
                if type(value) is dict:
                    for k, v in value.items():
                        if k == "videoId" and len(v) == 11:
                            youtube_data.append({'VideoID': v})

        filepath = "youtube.csv"

        with open(filepath, 'a') as file:
            field_names = ['Query', 'Count']
            input = DictWriter(file, fieldnames=field_names)
            row = {'Query': query, 'Count': len(youtube_data)}
            input.writerow(row)

            file.close()

    def plotPieChart(self, event):
        query_data = []
        count_data = []
        
        with open('youtube.csv', 'r') as youtube_file:
            yt_lines = DictReader(youtube_file, delimiter=',')
            for i in yt_lines:
                query_data.append(i['Query'])
                count_data.append(int(i['Count']))
        
        plt.pie(count_data, labels=query_data, autopct='%.2f%%')
        plt.title("Youtube Query Search Result Count", fontsize=20)
        plt.show()
        

        

    # browser_path = '/usr/bin/firefox %s'
    # textin = self.textbox.get()
    # webbrowser.get(browser_path).open("http://www.google.ca/search?q="+textin)

    # self.myParent.destroy()


root = Tk()
myapp = MyApp(root)
root.title('Search')
root.mainloop()
