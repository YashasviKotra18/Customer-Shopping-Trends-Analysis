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
    text="Products Analysis",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

image_image_12 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_12.png"))
image_12 = canvas.create_image(
    56.0,
    31.0,
    image=image_image_12
)


# Data
product_data = [
    ('Accessories', 'Gloves', 2142),
    ('Clothing', 'Skirt', 4136),
    ('Footwear', 'Sneakers', 2000),
    ('Outerwear', 'Coat', 1781)
]

# Extracting labels, categories, and sizes
categories, products, sizes = zip(*product_data)

# Number of categories
num_categories = len(categories)

# Calculate the angle at each position
theta = np.linspace(0.0, 2 * np.pi, num_categories, endpoint=False)

# Create a Figure with a polar subplot
fig_3 = Figure(figsize=(3.5, 2.2), facecolor='#282952', edgecolor='white')
ax = fig_3.add_subplot(111, projection='polar')
ax.set_facecolor('#282952')  # Set the background color of the current Axes

# Plot circular bars resembling loops
bars = ax.bar(theta, sizes, color=plt.cm.viridis(np.arange(num_categories) / num_categories), align='center', alpha=0.7)

# Add labels for each bar using ax.bar_label
ax.bar_label(bars, labels=products, label_type='edge', color='white', fontsize=8, fontweight='bold')

# Set radial gridlines
ax.set_yticklabels([])  # Hide radial tick labels
ax.set_yticks([])  # Hide radial ticks
ax.set_xticks(theta)  # Set the positions of the radial gridlines

# Set category labels
ax.set_xticklabels(categories, color='white')

# Set title
ax.set_title('Top Selling Items', color='white', fontweight='bold')




'''table = ttk.Treeview(master=root, columns=table_columns, show="headings")
print(table.dtype)
for column in table_columns:
    table.heading(column=column, text=column)
    table.column(column=column, width=70)

for row_data in table_data:
    table.insert(parent="", index="end", values=row_data)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#917FB3", fieldbackground="#917FB3", foreground="white")
style.configure("Treeview.Heading", background="#917FB3", fieldbackground="#917FB3", foreground="white")
style.map("Treeview", background=[("selected", "#E5BEEC")])

table.place(x=395, y=225, height=260)'''

cur.execute("SELECT * FROM SalesRollupViews ")
rows = cur.fetchall()

# Assuming you have column names stored in table_columns
table_columns = [column[0] for column in cur.description]
# Create a Treeview widget
table = ttk.Treeview(master=root, columns=table_columns, show="headings")

# Set column headings
for column in table_columns:
    table.heading(column=column, text=column)
    table.column(column=column, width=60)

# Insert rows into the table
for row_data in rows:
    table.insert(parent="", index="end", values=row_data)

# Apply styles to the Treeview widget
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#917FB3", fieldbackground="#917FB3", foreground="black", font=('Arial', 20))
style.configure("Treeview.Heading", background="#917FB3", fieldbackground="#917FB3", foreground="black", font=('Arial', 22))
style.map("Treeview", background=[("selected", "#E5BEEC")])
#style.tag_configure('grid_tag', background='white')
# Place the Treeview widget on the window
table.place(x=150, y=150, height=500, width=900)  # Adjust height and width as needed







def on_dropdown_select(event):
    selected_text = combobox.get()
    print(f"Selected Text: {selected_text}")
    query = f"SELECT * FROM SalesRollupViews WHERE Year = {selected_text}"
    # Execute the query
    cur.execute(query)
    #cur.execute(""" SELECT * FROM SalesRollupViews  where Year = {selected_text} """)
    rows = cur.fetchall()

    # Assuming you have column names stored in table_columns
    table_columns = [column[0] for column in cur.description]
    # Create a Treeview widget
    table = ttk.Treeview(master=root, columns=table_columns, show="headings")

    # Set column headings
    for column in table_columns:
        table.heading(column=column, text=column)
        table.column(column=column, width=60)

    # Insert rows into the table
    for row_data in rows:
        table.insert(parent="", index="end", values=row_data)

    # Apply styles to the Treeview widget
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#917FB3", fieldbackground="#917FB3", foreground="black", font=('Arial', 20))
    style.configure("Treeview.Heading", background="#917FB3", fieldbackground="#917FB3", foreground="black", font=('Arial', 22))
    style.map("Treeview", background=[("selected", "#E5BEEC")])
    #style.tag_configure('grid_tag', background='white')



    # Place the Treeview widget on the window
    table.place(x=150, y=150, height=500, width=900)  # Adjust height and width as needed





# Create a StringVar to store the selected option
selected_option = StringVar()

# Create a Combobox (dropdown menu)
options = [2023, 2022]
combobox = ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
combobox.set("Select an Year")  # Set a default value
combobox.pack(pady=20)

# Bind the <<ComboboxSelected>> event to the on_dropdown_select function
combobox.bind("<<ComboboxSelected>>", on_dropdown_select)





def emp():
    root.withdraw()
    os.system("python cust_demo.py")
    root.deiconify()


import os
from tkinter import *
from tkinter import messagebox


button1 = Button(root)
button1.place(relx=0.92, rely=0.01, width=80, height=55)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="#ffffff")
button1.configure(borderwidth="0")
img2 = PhotoImage(file="./images/bk.png")
button1.configure(image=img2)
button1.configure(command=emp)

#cur.close()
root.resizable(False, False)
root.mainloop()