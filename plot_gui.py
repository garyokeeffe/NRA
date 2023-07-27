import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from api_wrappers.nsa_wrapper import download_unfiltered_nostr_data
from api_wrappers.openai_wrapper import embedding_annotate
from helpers.text_helpers import generate_formatted_query_object
from helpers.misc_helpers import save, load, initial_semantic_focus
from api_wrappers.chromadb_wrapper import set_up_database, upload_embeddings_to_database, get_random_note

# Load pre-processed notes
notes_with_embeddings = load("notes_with_embeddings")

# Set up database and upload embeddings
database = set_up_database()
upload_embeddings_to_database(database, notes_with_embeddings)

# Initialize semantic focus
semantic_focus = initial_semantic_focus('npub10mgeum509kmlayzuvxhkl337zuh4x2knre8ak2uqhpcra80jdttqqvehf6')

# Create the main window
root = tk.Tk()
root.title("Nostr Recommendation System")

# Create a Text widget to display the note
note_text = tk.Text(root, width=80, height=20)
note_text.pack(pady=10)

# Function to open hyperlink
def open_hyperlink(event):
    webbrowser.open(current_url)

note_text.tag_config("bold", font=("TkDefaultFont", 10, "bold"))

# Initialize counters
likes = 0
dislikes = 0
skips = 0

# Initialize an empty list to store the fractions
fractions = []

# Create the plot outside the function
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)  # Create the canvas, but don't pack it


# Function to calculate the fractions and update the plot
def update_plot():
    global ax, canvas
    total = likes + dislikes + skips
    ax.clear()  # Clear the previous plot
    if total > 0:
        fractions.append([likes/total, dislikes/total, skips/total])
        ax.plot(np.array(fractions))
        ax.legend(['Likes', 'Dislike', 'Skip'])
    else:
        ax.plot([])  # Create an empty plot
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM)  # Pack the canvas here


def display_new_note():
    global query_result
    global current_url
    query_result = get_random_note(database, semantic_focus)
    note_text.delete(1.0, tk.END)
    result_dict = generate_formatted_query_object(query_result)
    current_url = result_dict['link']
    note_text.insert(tk.END, "Link: ", "bold")
    note_text.insert(tk.END, current_url + "\n\n")
    note_text.insert(tk.END, "Author: ", "bold")
    note_text.insert(tk.END, result_dict['author'] + "\n\n")
    note_text.insert(tk.END, "Content: \n", "bold")
    note_text.insert(tk.END, result_dict['documents'])
    note_text.tag_add("hyperlink", "1.6", "1.end")
    note_text.tag_config("hyperlink", foreground="blue", underline=True)
    note_text.tag_bind("hyperlink", "<Button-1>", open_hyperlink)

# Function to handle the 'Like' button
def like_note():
    global semantic_focus
    global likes
    semantic_focus  = [.9*x + .1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
    likes += 1
    display_new_note()
    root.after(100, update_plot)
    print("Liked note.")

# Function to handle the 'Dislike' button
def dislike_note():
    global semantic_focus
    global dislikes
    semantic_focus  = [1.1*x + -.1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
    dislikes += 1
    display_new_note()
    root.after(100, update_plot)
    print("Disliked note.")

# Function to handle the 'Skip' button
def skip_note():
    global skips
    skips += 1
    display_new_note()
    root.after(100, update_plot)
    print("Skipped note.")

# Function to exit the program when the window is closed
def exit_program():
    sys.exit()

root.protocol("WM_DELETE_WINDOW", exit_program)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Create the buttons
like_button = tk.Button(button_frame, text="Like", command=like_note)
like_button.pack(side=tk.RIGHT, padx=20)

dislike_button = tk.Button(button_frame, text="Dislike", command=dislike_note)
dislike_button.pack(side=tk.LEFT, padx=20)

skip_button = tk.Button(button_frame, text="Skip", command=skip_note)
skip_button.pack( padx=20)


display_new_note()
update_plot()
root.mainloop()

