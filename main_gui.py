import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox, font

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
root.title("Notes Reviewer")

# Create a Text widget to display the note
note_text = tk.Text(root, width=80, height=20)
note_text.pack(pady=10)

# Function to open hyperlink
def open_hyperlink(event):
    start = note_text.index("@current wordstart")
    end = note_text.index("@current wordend")
    url = note_text.get(start, end)
    webbrowser.open(url)

note_text.tag_config("bold", font=("TkDefaultFont", 10, "bold"))

# Function to display a new note
# Function to display a new note
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


# Function to open hyperlink
def open_hyperlink(event):
    webbrowser.open(current_url)  # Modify this line



# Function to handle the 'Like' button
def like_note():
    global semantic_focus
    semantic_focus  = [.9*x + .1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
    display_new_note()

# Function to handle the 'Dislike' button
def dislike_note():
    global semantic_focus
    semantic_focus  = [1.1*x + -.1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
    display_new_note()

# Function to handle the 'Skip' button
def skip_note():
    display_new_note()


# Function to exit the program when the window is closed
def exit_program():
    sys.exit()

root.protocol("WM_DELETE_WINDOW", exit_program)

# Create the buttons
like_button = tk.Button(root, text="Like", command=like_note)
like_button.pack(side=tk.RIGHT, padx=20)

dislike_button = tk.Button(root, text="Dislike", command=dislike_note)
dislike_button.pack(side=tk.LEFT, padx=20)

skip_button = tk.Button(root, text="Skip", command=skip_note)
skip_button.pack(pady=20)

# Display the first note
display_new_note()

# Start the main loop
root.mainloop()
