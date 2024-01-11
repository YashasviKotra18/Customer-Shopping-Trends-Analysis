#==================imports===================
import sqlite3
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
#============================================
from DATA225utils import make_connection, dataframe_query

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import calendar
from decimal import Decimal

conn = make_connection(config_file = 'olap.ini')
cur = conn.cursor()

selected_year = 2023

def execute_stored_procedure(sp,connection, year):
    try:
        cursor = connection.cursor()

        # Assuming 'GetTotalRevenue' is the name of your stored procedure
        cursor.callproc(sp, args=[year])

        # Fetch the result set
        result_set = []
        for result in cursor.stored_results():
            result_set.extend(result.fetchall())

        return result_set

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



def call_view(name):
    # Using placeholders to prevent SQL injection
    cur.execute("SELECT * FROM {}".format(name))

    # Fetching all the results from the executed query
    results = cur.fetchall()

    # Checking if there are any results
    if results:
        result_tuple = results[0]  # Extracting the tuple from the list
        number = result_tuple[0]   # Extracting the number from the tuple

        # Converting the number to a string
        result_string = int(number)
        return result_string
    else:
        return "No results found for the view: {}".format(name)
    
def call_view_rate(name):
    # Using placeholders to prevent SQL injection
    cur.execute("SELECT * FROM {}".format(name))

    # Fetching all the results from the executed query
    results = cur.fetchall()

    # Checking if there are any results
    if results:
        result_tuple = results[0]  # Extracting the tuple from the list
        number = result_tuple[0]   # Extracting the number from the tuple

        # Converting the number to a string
        result_string = round(float(number), 2)
        return result_string
    else:
        return "No results found for the view: {}".format(name)

root = Tk()

root.geometry("1366x768")
root.title("Analytics")
root.configure(bg = "#282952")


canvas = Canvas(
    root,
    bg = "#282952",
    height = 768,
    width = 1366,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1366.0,
    72.0,
    fill="#E5BEEC",
    outline="")

canvas.create_text(
    83.0,
    16.0,
    anchor="nw",
    text="Customer Demographics",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)


image_image_1 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_1.png"))
image_1 = canvas.create_image(
    170.0,
    143.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_2.png"))
image_2 = canvas.create_image(
    170.0,
    364.0,
    image=[]
)

image_image_3 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_3.png"))
image_3 = canvas.create_image(
    830.0,
    364.0,
    image=[]
)

image_image_4 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_4.png"))
image_4 = canvas.create_image(
    498.0,
    364.0,
    image=[]
)

image_image_5 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_5.png"))
image_5 = canvas.create_image(
    498.0,
    143.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_6.png"))
image_6 = canvas.create_image(
    830.0,
    142.0,
    image=image_image_6
)

canvas.create_text(
    68.0,
    117.0,
    anchor="nw",
    text="Customers",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)

canvas.create_text(
    68.0,
    135.0,
    anchor="nw",
    text= call_view('TotalCustomersView'),
    fill="#FFFFFF",
    font=("Inter Bold", 25 * -1)
)
canvas.create_text(
    396.0,
    117.0,
    anchor="nw",
    text="Avg Age",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)

canvas.create_text(
    396.0,
    135.0,
    anchor="nw",
    text= int(call_view('AverageAgeView')),
    fill="#FFFFFF",
    font=("Inter Bold", 25 * -1)
)

canvas.create_text(
    728.0,
    116.0,
    anchor="nw",
    text="Avg Rating",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)

canvas.create_text(
    728.0,
    135.0,
    anchor="nw",
    text=call_view_rate('AverageRatingView'),
    fill="#FFFFFF",
    font=("Inter Bold", 25 * -1)
)


canvas.create_text(
    54.0,
    136.0,
    anchor="nw",
    text= '',
    fill="#FFFFFF",
    font=("Inter Bold", 22 * -1)
)




canvas.create_text(
    382.0,
    136.0,
    anchor="nw",
    text='',
    fill="#FFFFFF",
    font=("Inter Bold", 22 * -1)
)

canvas.create_text(
    714.0,
    135.0,
    anchor="nw",
    text= '',
    fill="#FFFFFF",
    font=("Inter Bold", 22 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_7.png"))
image_7 = canvas.create_image(
    59.0,
    123.0,
    image=image_image_7
)


image_image_11 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_11.png"))
image_11 = canvas.create_image(
    718.0,
    122.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_12.png"))
image_12 = canvas.create_image(
    56.0,
    31.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_13.png"))
image_13 = canvas.create_image(
    386.0,
    123.0,
    image=image_image_13
)


cur.execute("SELECT * FROM datadynamos_wh.GenderCountsPercentageView ")
rows = cur.fetchall()
converted_data = []

for item in rows:
    gender = str(item[0])
    count = int(item[1])
    percentage = float(item[2])

    # Round the percentage to 2 decimal places
    percentage = round(percentage, 2)

    converted_item = (gender, count, percentage)
    converted_data.append(converted_item)

labels, sizes, percentages = zip(*converted_data)
colors = ['#3f8ef4', '#5d4dbe']  # You can adjust the colors as needed

fig_1 = Figure(figsize=(3.5, 2.2), facecolor='#282952', edgecolor='white')
ax = fig_1.add_subplot()
ax.set_facecolor('#282952')

wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', pctdistance=0.79,
                                  startangle=90, counterclock=False,
                                  wedgeprops=dict(width=0.4, edgecolor='#282952'),
                                  colors=colors)

for text in texts + autotexts:
    text.set_color('white')
    text.set_fontweight('bold')
    text.set_fontsize(8)

ax.set_title('Gender Distribution', color='white', fontweight='bold')

fig_1.tight_layout()
# Display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure=fig_1, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=1000, y=105)




# Data
cur.execute("SELECT * FROM datadynamos_wh.ProductCategoryPreferences;")

# Fetch all rows
rows = cur.fetchall()
# Extracting labels, categories, and sizes
labels, categories, sizes = zip(*rows)

# Colors
colors = ['#3f8ef4', '#5d4dbe']  # You can adjust the colors as needed


#fig, axs = plt.subplots(2, 2, figsize=(5, 5), facecolor='#282952', edgecolor='white')
fig_2 = Figure(figsize=(4.4, 4.2), facecolor='#282952', edgecolor='white')
axs = [fig_2.add_subplot(2, 2, i + 1) for i in range(4)]
# Flatten the 2x2 array of subplots for easier indexing
#axs = axs.flatten()

# Iterate through each category and create a pie chart
for i, category in enumerate(set(categories)):
    ax = axs[i]

    # Filter data for the specific category
    category_subset = [(label, size) for label, cat, size in zip(labels, categories, sizes) if cat == category]
    category_labels, category_sizes = zip(*category_subset)

    # Plot the pie chart
    wedges, texts, autotexts = ax.pie(category_sizes, labels=category_labels, autopct='%1.1f%%', pctdistance=0.79,
                                      startangle=90, counterclock=False,
                                      wedgeprops=dict(width=0.4, edgecolor='#282952'),
                                      colors=colors)

    # Set the text color to white

    for text in texts + autotexts:
        text.set_color('yellow')
        text.set_fontweight('bold')
        text.set_fontsize(6)

    # Set title for each subplot
    ax.set_title(f'Category: {category}', color='white', fontweight='bold', fontsize=8)

# Adjust layout to include the legend beside the title
fig_2.tight_layout()

# Display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure=fig_2, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=930, y=320)

##plt.show()





cur.execute("SELECT * FROM AgeGroupCountsView ")

# Fetch all rows
rows = cur.fetchall()

# Extracting labels and values for the bar graph
labels, values = zip(*rows)

# Create a bar graph
fig_3 = Figure(figsize=(7.5, 5.5), facecolor='#282952', edgecolor='white')
ax = fig_3.add_subplot()
ax.set_facecolor('#282952')

bars = ax.bar(labels, values, color='#5d4dbe', width=0.5, edgecolor='white')  # Bar graph with blue color

# Add labels and title to the graph
ax.set_title('Customers Age Distribution', color='white', fontweight='bold')

# Set x and y axis tick labels to white
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
# Rotate x-axis labels for better readability
ax.set_xticklabels(labels, rotation=45, fontweight='bold')
ax.set_yticks([])

# Hide spines
ax.spines['bottom'].set_color('#282952')
ax.spines['top'].set_color('#282952')
ax.spines['right'].set_color('#282952')
ax.spines['left'].set_color('#282952')

# Add horizontal grid lines with low opacity
# ax.grid(axis='y', alpha=0.3)
# Add value annotations inside the bars
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20, str(value), color='white', ha='center',
            va='center', fontweight='bold')



fig_3.tight_layout()
# Display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure=fig_3, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=100, y=200)

import os
from tkinter import *
from tkinter import messagebox

def emp():
    root.withdraw()
    os.system("python roll_up.py")
    root.deiconify()

def dsh():
    root.withdraw()
    os.system("python dashboard.py")
    root.deiconify()

button1 = Button(root)
button1.place(relx=0.92, rely=0.01, width=80, height=55)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="#ffffff")
button1.configure(borderwidth="0")
img2 = PhotoImage(file="./images/nxt.png")
button1.configure(image=img2)
button1.configure(command=emp)

button2 = Button(root)
button2.place(relx=0.8, rely=0.01, width=80, height=55)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(activebackground="#ffffff")
button2.configure(cursor="hand2")
button2.configure(foreground="#ffffff")
button2.configure(background="#ffffff")
button2.configure(borderwidth="0")
img3 = PhotoImage(file="./images/bk.png")
button2.configure(image=img3)
button2.configure(command=dsh)



#cur.close()
root.resizable(False, False)
root.mainloop()