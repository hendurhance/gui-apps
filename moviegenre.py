from tkinter import *
import requests
import json
from csv import DictWriter, DictReader, reader, writer
import matplotlib.pyplot as plt
from tkinter import messagebox

class MovieSearcher:
    OMDB_API_URL = 'http://www.omdbapi.com/'
    API_KEY = 'f81b621'
    def __init__(self, parent):
        self.myParent = parent
        self.myContainer1 = LabelFrame(parent, text="Movie Search")
        self.myContainer2 = Frame(parent)
        self.myContainer1.grid(row=0, column=0, padx=50, pady=100)
        self.myContainer2.grid(row=1, column=0, padx=50, pady=10)

        self.label1 = Message(self.myContainer1, text="")

        self.label1.pack()

        self.entryVariable = StringVar()
        self.textbox = Entry(self.myContainer1)
        self.textbox.pack(side=TOP, fill=BOTH)
        self.textbox.bind("<Return>", self.searchMovie)
        self.textbox.focus_set()

        self.label2 = Label(self.myContainer1)
        self.label2["text"] = ""
        self.label2.pack(side=BOTTOM)

        self.label3 = Message(self.myContainer1, text="")
        self.label3.pack()

        self.button1 = Button(self.myContainer2)
        self.button1["text"] = "Search"
        self.button1.pack(side=BOTTOM)
        self.button1.bind("<Button-1>", self.searchMovie)
        textbox = self.textbox

        self.button2 = Button(self.myContainer2)
        self.button2["text"] = "Plot Pie Chart"
        self.button2.pack(side=BOTTOM)
        self.button2.bind("<Button-1>", self.plotPieChart)

    def searchMovie(self, event):
        query = self.textbox.get()
        if len(query)  == 0:
            messagebox.showerror("Error", "An error occurred because the entry is empty")
        else:
            try:
                res = requests.get(self.OMDB_API_URL, params={'apikey': self.API_KEY, 's': query})
                results = json.loads(res.text)["Search"]

                imdbIDs = [result['imdbID'] for result in results]
                genre_count = self.getGenre(imdbIDs)

                self.saveToCSV(genre_count)
            except:
                messagebox.showerror("Error", "An error occurred when fetching the movie you requested.")
    
    def getGenre(self, imdbIDs: list):
        genre_count = {}
        for imdbId in imdbIDs:
            url = f"{self.OMDB_API_URL}?apikey={self.API_KEY}&i={imdbId}"
            response = requests.get(url)
            genres = response.json()["Genre"].split(",")
            for genre in genres:
                genre = genre.strip()
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1

        return genre_count

    def saveToCSV(self, genre_count: dict):
        # read the contents of the CSV file into a dictionary
        with open('movies.csv', 'r') as csv_file:
            read_file = reader(csv_file)
            next(read_file)  # skip the header row
            genre_count_from_file = {row[0]: int(row[1]) for row in read_file}

        # update the dictionary with the new genre counts
        for genre, count in genre_count.items():
            if genre in genre_count_from_file:
                # increment the existing count
                genre_count_from_file[genre] += count
            else:
                # add a new key-value pair
                genre_count_from_file[genre] = count

        # write the updated dictionary back to the CSV file
        with open('movies.csv', 'w', newline='') as csv_file:
            write_file = writer(csv_file)
            write_file.writerow(['Genre', 'Count'])
            for genre, count in genre_count_from_file.items():
                write_file.writerow([genre, count])

    def plotPieChart(self, event):
        genre = []
        count = []
    
        with open('movies.csv', 'r') as movie_file:
            gr_lines = DictReader(movie_file, delimiter=',')
            for i in gr_lines:
                genre.append(i['Genre'])
                count.append(int(i['Count']))
        
        plt.pie(count, labels=genre, autopct='%.2f%%')
        plt.title("Movie Search Genre Result", fontsize=20)
        plt.show()
        

root = Tk()
myapp = MovieSearcher(root)
root.title('Movie Search')
root.mainloop()
