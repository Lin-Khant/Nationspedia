from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas

data = None
columns = []
flag = None
text_labels = []
buttons = []

# Backup File
def create_backup_file():
    # Only the first 3 countries in alphabetical order and their corresponding regions will be put in the backup file.
    new_data = {
        "Country" : ["Afghanistan", "Albania", "Algeria"],
        "Region" : ["ASIA (EX. NEAR EAST)", "EASTERN EUROPE", "NORTHERN AFRICA"]
    }
    data_frame = pandas.DataFrame(new_data)
    data_frame.to_csv("countries of the world.csv", index=False)

    return pandas.read_csv("countries of the world.csv")

# Import required data, column names and widgets from the main file
def set_up(dataframe, column_names, flag_label, labels):
    global data, columns, flag, text_labels
    data = dataframe
    columns = column_names
    flag = flag_label
    text_labels = labels

# Display result buttons
def show_results(container, countries):           
    for i in range(len(countries)):
        btn = Button(container, text=countries[i], font=("Times New Roman", 14), fg="#000000", padx=50, pady=10, width=28)
        btn.grid(row=i, column=0, pady=(0, 20))
        set_command(btn)
        buttons.append(btn)

# Search
def search(input, container):
    searched_countries = [country for country in data["Country"] if input.lower().strip() in country.lower()]

    # Destroy all existing results every time the user searches.
    global buttons
    for btn in buttons:
        btn.destroy()

    # And display the new results that matches with the user's search.
    show_results(container, searched_countries)

    # If the list weren't empty, do this.
    try:
        display(searched_countries[0])
    # If it was empty, an error (List index out of range) will occur. Then, do this.
    except IndexError:
        flag.config(image=None)
        flag.image = None
        for label in text_labels:
            label.config(text='')
        messagebox.showinfo("Oops!", f"None of the results matched with the country, '{input}'.")

# Display the data of each country
def display(country_name):
    selected_data = data[data.Country == country_name]

    try:
        flag_source = ImageTk.PhotoImage(Image.open(f"./flags_240px/{country_name}.png"))
    except FileNotFoundError:
        flag.config(image=None)
        flag.image = None
        messagebox.showerror("Flag source is missing!", "Sorry, couldn't find the flag source. National flag can't be displayed.")
    else:    
        flag.config(image=flag_source)  # <-- Sometimes, photo images might not appeared just by doing this.
        flag.image = flag_source    # <-- To solve that, it needs to assign the photo image directly into the 'image' attribute of the flag label.
    finally:
        for i in range(len(text_labels)):
            text_labels[i].config(text=f"{columns[i]} : {selected_data[columns[i]].to_list()[0]}")

# A handy trick to set different commands for 225 result buttons
def set_command(button):
    button.config(command=lambda : display(button["text"]))