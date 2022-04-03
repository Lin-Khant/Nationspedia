from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from program_manager import *
import pandas

colors = ["gray", "#000000", "#c6c6c6"]

# Set up the main window
window = Tk()
window.title("Nationspedia")
window.config(bg=colors[0], padx=20, pady=20)
window.geometry("1020x750")

# Read data
try:
    data = pandas.read_csv("countries of the world.csv")
# If the error occured, the app won't crash but only 3 countries and a few data will only be able to searched.
except FileNotFoundError:
    data = create_backup_file()
    messagebox.showwarning("Source data is missing!", "The app is running with the backup file. For the best performance, please close the app. Then, make sure you're in the right directory and the data file was neither renamed nor moved nor deleted.")
finally:
    columns = list(data.columns)

# ----------<<<GUI>>>----------
# Title
main_title = Label(window, text="Nationspedia", font=("Times New Roman", 40, "bold"), fg=colors[1], bg=colors[0])
main_title.grid(row=0, column=0, columnspan=5, pady=(0, 20))

# ---Input Section---
# Input Label
input_label = Label(window, text="Search for a country -", font=("Times New Roman", 18), fg=colors[1], bg=colors[0])
input_label.grid(row=1, column=0, padx=(0, 20), pady=(0, 20))

# Input Box
input_box = Entry(window, fg=colors[1], bg="white", font=("Times New Roman", 20), width=34)
input_box.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=(0, 20))
input_box.focus()

# Clear Button
clear_button = Button(window, text="Clear", font=("Times New Roman", 13, "bold"), fg=colors[1], bg=colors[2], width=10, command=lambda : input_box.delete(0, END))
clear_button.grid(row=1, column=3, padx=(0, 20), pady=(0, 20))

# Search Button
search_button = Button(window, text="Search", font=("Times New Roman", 13, "bold"), fg=colors[1], bg=colors[2], width=10)
search_button.grid(row=1, column=4, pady=(0, 20))

# ---Info Display Section---
# Create the main frame
display_frame = Frame(window, bg=colors[2])
display_frame.grid(row=2, column=2, columnspan=3)

# Create a canvas
display_canvas = Canvas(display_frame, bg=colors[2], width=500, height=537)
display_canvas.pack()

# Create a display box
display_box = Frame(display_canvas, bg=colors[2])

# Add the display box to the canvas
display_canvas.create_window((50, 0), anchor=NW, window=display_box)

# Flag Label
flag_label = Label(display_box, bg=colors[2])
flag_label.grid(row=0, column=0, pady=(20, 20), sticky=N)

# Information Labels
info_labels = []
for i in range(len(columns)):
    text = Label(display_box, font=("Times New Roman", 18), fg="#000000", bg=colors[2])
    text.grid(row=i + 1, column=0, sticky=W)
    info_labels.append(text)

set_up(data, columns, flag_label, info_labels)

# ---Results Section---
# Create the main frame
results_frame = Frame(window, bg=colors[2], padx=20, pady=20)
results_frame.grid(row=2, column=0, columnspan=2, padx=(0, 20))

# Create a scrollable canvas
scroll_canvas = Canvas(results_frame, height=500, bg=colors[2])
scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Create the scrollbar
scrollbar = ttk.Scrollbar(results_frame, orient=VERTICAL, command=scroll_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
scroll_canvas.config(yscrollcommand=scrollbar.set)
scroll_canvas.bind("<Configure>", lambda event: scroll_canvas.config(scrollregion=scroll_canvas.bbox(ALL)))

# Create a scrollbox
scrollbox = Frame(scroll_canvas, bg=colors[2])

# Add the scrollbox to the canvas
scroll_canvas.create_window((0, 0), anchor=NW, window=scrollbox)

# Display the buttons
show_results(scrollbox, data["Country"].to_list())
search_button.config(command=lambda : search(input_box.get(), scrollbox))

window.mainloop()