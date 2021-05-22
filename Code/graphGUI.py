# Zack Fravel
# ECE508 - Python Workshop
# Spring 2021
# Final Project
#
# filename: promptGUI.py
#
# description: Implementation of a simple GUI that allows the user to select
#   which graph edge filter they'd like to apply to the graph being generated.
#   User has the option to generate actor, director, writer, and more graphs.
#
# library references:
#   https://docs.python.org/3/library/tk.html
#

# Import tkinter for GUI development
import tkinter as tk
from tkinter import *

# Configure GUI
graphRoot = tk.Tk()
graphRoot.minsize(450, 150)
graphRoot.title('Zack Fravel - Python Workshop - Final Project')
Label(graphRoot).pack()  # Blank Spacer

# Variable to store user's selected media filter
selected_filter = StringVar()

# Dropdown menu options
options = [
    'Year',
    'Actors',
    'Directors',
    'Writers',
    'Cinematographers',
    'Composers',
    'Producers',
    'Genres',
    'Actors and Directors'
]

# Default option
selected_filter.set("Select a filter")

# Add Dropdown Menu
Label(graphRoot, text="Graph Filter:").pack()
OptionMenu(graphRoot, selected_filter, *options).pack()
Label(graphRoot).pack()  # Blank Spacer


# Function called on each generate graph click
def generate_graph():
    print("Generating Graph. . . ")
    print("Filter: ", selected_filter.get())
    graphRoot.destroy()
    pass


# Add Search Button, calls button_clicked()
Button(graphRoot, text="Generate Graph", command=generate_graph).pack()
Label(graphRoot).pack()  # Blank Spacer
