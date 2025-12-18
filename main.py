import requests
from bs4 import BeautifulSoup
from tkinter import *
import json
import os

# #################### UI ##########################
BACKGROUND = "#23252f"
TEXT = "#efefef"
NEON_GREEN = "#64ed85"
PLACEHOLDER = "Enter Movie Name, Rank, or Rating"
DATA_FILE = "movies.json"

window = Tk()
window.title("Movie Search Tool")
window.minsize(700, 500)
window.config(bg=BACKGROUND)


window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(4, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(10, weight=8)

movie_frame = Frame(window, bg=BACKGROUND, bd=2, relief="groove")
movie_frame.grid(column=0, row=0)


# #################### User Input ##########################
def search_movie():

    user_input = entry.get().title()

    for movie in movies:
        if user_input in movie["title"]:
            title_label.config(text=f"{movie['title']}")
            rating_label.config(text=f"Worldwide Gross: {movie['worldwide_gross']}")
            votes_label.config(text=f"Domestic Gross: {movie['domestic_gross']}")
            year_label.config(text=f"Year: {movie['year']}")
            rank_label.config(text=f"Rank: {movie['rank']}")
            return  # stop after finding the movie
    else:
        title_label.config(text="The movie you searched for isn't on the list")
        rating_label.config(text="Worldwide Gross: N/A")
        votes_label.config(text="Domestic Gross: N/A")
        year_label.config(text="Year: N/A")
        rank_label.config(text="Rank: N/A")


title = Label(text="Top Lifetime Grosses", font=("Arial", 30, "bold"))
title.grid(column=1, row=1, columnspan=3, sticky="ew", pady=40)

sub_text = Label(
    text="Search for a keyword", font=("Arial", 15), bg=BACKGROUND, fg=TEXT
)
sub_text.grid(column=2, row=2, pady=10)


entry = Entry(width=35, fg="gray")
entry.insert(0, PLACEHOLDER)
entry.grid(column=2, row=3, ipady=5)


def clear_placeholder(event):
    # Only clear if placeholder is present
    if entry.get() == PLACEHOLDER:
        entry.delete(0, END)
        entry.config(fg="black")


entry.bind("<FocusIn>", clear_placeholder)


search_btn = Button(
    text="Search",
    pady=5,
    padx=10,
    font=("Arial", 13),
    command=search_movie,
)
search_btn.grid(column=2, row=4, pady=8)


title_label = Label(
    window, text="Title: N/A", font=("Arial", 18, "bold"), bg=BACKGROUND, fg=NEON_GREEN
)
title_label.grid(row=6, column=1, columnspan=3, sticky="ew", pady=30)


rating_label = Label(
    window,
    text="Worldwide Gross: N/A",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Arial", 12),
)
rating_label.grid(row=7, column=1, sticky="w", pady=10)


year_label = Label(window, text="Year: N/A", bg=BACKGROUND, fg=TEXT, font=("Arial", 12))
year_label.grid(row=7, column=3, sticky="e", pady=10)


votes_label = Label(
    window,
    text="Domestic Gross: N/A",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Arial", 12),
)
votes_label.grid(row=8, column=1, sticky="w", pady=10)


rank_label = Label(window, text="Rank: N/A", bg=BACKGROUND, fg=TEXT, font=("Arial", 12))
rank_label.grid(row=8, column=3, sticky="e", pady=10)


# #################### Web scraping ##########################
def get_movies_data():
    url = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/"

    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    movies = []
    for row in rows:
        cols = row.find_all("td")
        movie = {
            "rank": cols[0].text.strip(),
            "title": cols[1].text.strip(),
            "worldwide_gross": cols[2].text.strip(),
            "domestic_gross": cols[3].text.strip(),
            "year": cols[-1].text.strip(),
        }
        movies.append(movie)

    return movies


# #################### Check if data exists ##########################
if os.path.exists(DATA_FILE):

    with open(DATA_FILE) as file:
        movies = json.load(file)

else:
    movies = get_movies_data()
    with open(DATA_FILE, "w") as file:
        json.dump(movies, file, indent=4)


# #############################################
window.mainloop()
