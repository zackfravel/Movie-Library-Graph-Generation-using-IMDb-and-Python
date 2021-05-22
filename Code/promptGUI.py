# Zack Fravel
# ECE508 - Python Workshop
# Spring 2021
# Final Project
#
# filename: promptGUI.py
#
# description: Implements a simple GUI to be used by the top level program
#   for taking in user information. Gives the user a directory selection dialogue
#   for the program to use as the media folder for generating a list of movies.
#
# library references:
#   https://docs.python.org/3/library/tk.html
#

# Import tkinter for GUI development
import tkinter as tk
from tkinter import filedialog
from tkinter import *

# Configure GUI
promptRoot = tk.Tk()
promptRoot.title('Zack Fravel - Python Workshop - Final Project')
Label(promptRoot).pack()  # Blank Spacer

# Variable to store user's selected media folder
selected_folder = StringVar()


# Function called on each button click
def ask_for_folder():
    # Prompt user to select a directory
    selected_folder.set(filedialog.askdirectory())
    pass


# Function called on each generate graph click
def collect_data():
    folder = selected_folder.get()
    print("Collecting IMDb Data . . . ")
    # Print Selected Folder
    print("Folder: ", folder)
    # Quit GUI window after setting variables to make room for Graph GUI
    promptRoot.destroy()
    pass


# Add Search Button, calls button_clicked()
Button(promptRoot, text="Select Movies Directory", command=ask_for_folder).pack()
Label(promptRoot).pack()  # Blank Spacer

# Add Path Field
Entry(promptRoot, width=120, textvariable=selected_folder).pack()
Label(promptRoot).pack()  # Blank Spacer

# Add Collect Button, calls button_clicked()
Button(promptRoot, text="Collect IMDb Metadata", command=collect_data).pack()
Label(promptRoot).pack()  # Blank Spacer

