import os
import re
import csv
import random
import string
import numpy as np
import pandas as pd
from decimal import Decimal
from pandas import DataFrame
import matplotlib.pyplot as plt
import calendar
from pathlib import Path


# Tkinter imports
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, scrolledtext as tkst, ttk

# Matplotlib and Pandas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Local imports
from DATA225utils import make_connection, dataframe_query
from tkinter import *



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




def get_total_sales(view_name):

    cursor = conn.cursor()

    # Building the SQL query using the provided view name
    query = f"SELECT * FROM {view_name}"

    # Executing the SQL query to select all records from the specified view
    cursor.execute(query)

    # Fetching all the results from the executed query
    results = cursor.fetchall()

    # Closing the cursor and the database connection
    cursor.close()
    #conn.close()

    result_tuple = results[0]  # Extracting the tuple from the list
    number = result_tuple[0]   # Extracting the number from the tuple

    # Converting the number to a string
    result_string = str(number)
    return result_string


def GetTotalRevenue_f (_year):
    if conn:
        result_set = execute_stored_procedure('GetTotalRevenue',conn, _year)
    return float(result_set[0][0])

def GetToatlCustomers_f (_year):
    if conn:
        result_set = execute_stored_procedure('GetCustomerCountByYear',conn, _year)
    return int(result_set[0][0])




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



root = Tk()

root.geometry("1366x768")
root.title("Analytics")
root.configure(bg = "#2A2F4F")


canvas = Canvas(
    root,
    bg = "#2A2F4F",
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
    text="Revenue Analytics",
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
    text="Revenue",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
)

canvas.create_text(
    396.0,
    117.0,
    anchor="nw",
    text="Customers",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
)

canvas.create_text(
    728.0,
    116.0,
    anchor="nw",
    text="Products Sold",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
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
    text= get_total_sales("Total_Sales"),
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

canvas.create_text(
    237.0,
    126.0,
    anchor="nw",
    text="5.8%",
    fill="#D9FFCA",
    font=("Inter Bold", 20 * -1)
)

canvas.create_text(
    565.0,
    126.0,
    anchor="nw",
    text="9.4%",
    fill="#D9FFCA",
    font=("Inter Bold", 20 * -1)
)

canvas.create_text(
    897.0,
    125.0,
    anchor="nw",
    text="3.6%",
    fill="#D9FFCA",
    font=("Inter Bold", 20 * -1)
)

canvas.create_text(
    237.0,
    151.0,
    anchor="nw",
    text="Past Week",
    fill="#FFFFFF",
    font=("Inter Bold", 7 * -1)
)

canvas.create_text(
    565.0,
    151.0,
    anchor="nw",
    text="Past Week",
    fill="#FFFFFF",
    font=("Inter Bold", 7 * -1)
)

canvas.create_text(
    897.0,
    150.0,
    anchor="nw",
    text="Past Week",
    fill="#FFFFFF",
    font=("Inter Bold", 7 * -1)
)

image_image_8 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_8.png"))
image_8 = canvas.create_image(
    219.0,
    136.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_9.png"))
image_9 = canvas.create_image(
    547.0,
    136.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("./screen_widgets/image_10.png"))
image_10 = canvas.create_image(
    879.0,
    135.0,
    image=image_image_10
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


def call_GetRevenueBySeason(selected_year):
    result_set = execute_stored_procedure('GetRevenueBySeason', conn, selected_year)
    new_list = [(str(item[0]), float(item[1])) for item in result_set]

    # Convert string values to float
    categories, values = zip(*new_list)
    values = [float(value) for value in values]

    # Sort the data by values in descending order
    sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
    categories, values = zip(*sorted_data)

    # Adjust bar width and reduce gaps
    bar_height = 0.2

    # Use plt.subplots to create a Figure and Axes
    fig_2 = Figure(figsize=(3, 2), facecolor="#917FB3")
    ax = fig_2.add_subplot()
    ax.set_facecolor('#917FB3')  # Set the background color of the current Axes

    # Create horizontal bar chart
    bars = ax.barh(categories, values, color='#00d0ff', height=bar_height, align='center')

    # Highlight the highest bar in green
    max_value_index = values.index(max(values))
    bars[max_value_index].set_color('#07d256')

    # Customize the plot
    ax.set_title('By Season', color='white', fontweight='bold')

    # Add total revenue on the side of the graph, aligned right
    for category, value in zip(categories, values):
        ax.text(value, category, f'${value:,.2f}', va='center_baseline', ha='left', fontsize=10, color='yellow')

    # Set the color of category labels to white
    ax.yaxis.set_tick_params(labelcolor='white')
    ax.xaxis.set_tick_params(color='white')

    # Hide x-axis ticks
    ax.set_xticks([])

    # Hide spines
    ax.spines['bottom'].set_color('#917FB3')
    ax.spines['top'].set_color('#917FB3')
    ax.spines['right'].set_color('#917FB3')
    ax.spines['left'].set_color('#917FB3')

    fig_2.tight_layout()

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_2, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=1020, y=330)

def call_GetRevenueByRegion(selected_year):
    result_set = execute_stored_procedure('GetRevenueByRegion', conn, selected_year)
    new_list = [(str(item[0]), float(item[1])) for item in result_set]

    # Convert string values to float
    categories, values = zip(*new_list)
    values = [float(value) for value in values]

    # Sort the data by values in descending order
    sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
    categories, values = zip(*sorted_data)

    # Adjust bar width and reduce gaps
    bar_height = 0.2

    # Use plt.subplots to create a Figure and Axes
    '''fig, ax = plt.subplots(figsize=(1.5, 1), facecolor='#282952', edgecolor='white')
    ax.set_facecolor('#282952')  # Set the background color of the current Axes'''
    fig_5 = Figure(figsize=(3, 2), facecolor="#917FB3")
    ax = fig_5.add_subplot()
    ax.set_facecolor('#917FB3')  # Set the background color of the current Axes

    # Create horizontal bar chart
    bars = ax.barh(categories, values, color='#00d0ff', height=bar_height, align='center')

    # Highlight the highest bar in green
    max_value_index = values.index(max(values))
    bars[max_value_index].set_color('#07d256')

    # Customize the plot
    ax.set_title('By Region', color='white', fontweight='bold')

    # Add total revenue on the side of the graph, aligned right
    for category, value in zip(categories, values):
        ax.text(value, category, f'${value:,.2f}', va='center_baseline', ha='left', fontsize=10, color='yellow')

    # Set the color of category labels to white
    ax.yaxis.set_tick_params(labelcolor='white')
    ax.xaxis.set_tick_params(color='white')

    # Hide x-axis ticks
    ax.set_xticks([])

    # Hide spines
    ax.spines['bottom'].set_color('#917FB3')
    ax.spines['top'].set_color('#917FB3')
    ax.spines['right'].set_color('#917FB3')
    ax.spines['left'].set_color('#917FB3')

    fig_5.tight_layout()

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_5, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=1020, y=550)




def call_GetRevenueByCategory(selected_year):
    result_set = execute_stored_procedure('GetRevenueByCategory', conn, selected_year)
    new_list = [(str(item[0]), float(item[1])) for item in result_set]

    # Convert string values to float
    categories, values = zip(*new_list)
    values = [float(value) for value in values]

    # Sort the data by values in descending order
    sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
    categories, values = zip(*sorted_data)

    # Adjust bar width and reduce gaps
    bar_height = 0.2
    fig_1 = Figure(figsize=(3, 2), facecolor="#917FB3")
    ax = fig_1.add_subplot()
    ax.set_facecolor('#917FB3')  # Set the background color of the current Axes

    # Create horizontal bar chart
    bars = ax.barh(categories, values, color='#00d0ff', height=bar_height, align='center')

    # Highlight the highest bar in green
    max_value_index = values.index(max(values))
    bars[max_value_index].set_color('#07d256')

    # Customize the plot
    ax.set_title('By Category', color='white', fontweight='bold')

    # Add total revenue on the side of the graph, aligned right
    for category, value in zip(categories, values):
        ax.text(value, category, f'${value:,.2f}', va='center_baseline', ha='left', fontsize=10, color='yellow')

    # Set the color of category labels to white
    ax.yaxis.set_tick_params(labelcolor='white')
    #ax.xaxis.set_tick_params(color='white')

    # Hide spines
    ax.spines['bottom'].set_color('#917FB3')
    ax.spines['top'].set_color('#917FB3')
    ax.spines['right'].set_color('#917FB3')
    ax.spines['left'].set_color('#917FB3')
    #ax.xticks([])
    ax.set_xticks([])

    fig_1.tight_layout()

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_1, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=1020, y=105)


    # Create a Matplotlib figure
    fig_4 = Figure(figsize=(1.2, 0.3), facecolor="#917FB3")

    # Add text to the figure
    #text_content = "77345"
    text_content= '$'+str(GetTotalRevenue_f (selected_year))        
    fig_4.text(0.5, 0.5, text_content, ha='center', va='center',fontsize=15,color='white')

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_4, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=45, y=135)

    fig_6 = Figure(figsize=(0.8, 0.3), facecolor="#917FB3")

    # Add text to the figure
    #text_content = "77345"
    text_content= str(GetToatlCustomers_f (selected_year))        
    fig_6.text(0.5, 0.5, text_content, ha='center', va='center',fontsize=15,color='white')

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_6, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=370, y=135)





def call_GetMonthlyRevenueByCategory(selected_year):
    import calendar

    result_set = execute_stored_procedure('GetMonthlyRevenueByCategory', conn, selected_year)
    new_list = [(str(item[0]), str(item[1][0:3]), float(item[2])) for item in result_set]

    # Create a dictionary to store data by category
    category_data = {}
    for category, month, value in new_list:
        if category not in category_data:
            category_data[category] = {'months': [], 'values': []}
        category_data[category]['months'].append(month)
        category_data[category]['values'].append(value)

    # Define a custom order for months
    month_order = list(calendar.month_abbr[1:])  # Use the abbreviated month names

    # Sort the months in the custom order
    for category, data in category_data.items():
        data['months'] = sorted(data['months'], key=lambda x: month_order.index(x))

    fig_3 = Figure(figsize=(8.5, 5.5), facecolor="#282952", edgecolor='white')
    ax = fig_3.add_subplot()
    ax.set_facecolor('#282952')  # Set the background color of the current Axes

    for category, data in category_data.items():
        ax.plot(data['months'], data['values'], marker='', label=category)

    # Add labels and title to the graph with white color
    ax.set_xlabel('Month', color='white')
    ax.set_ylabel('Value', color='white')
    ax.set_title('Monthly Values by Category', color='white', fontweight='bold')

    # Rotate x-axis labels for better readability
    #ax.set_xticks(rotation=45, color='white')

    # Set legend and format it with white color
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
    legend = ax.get_legend()
    for text in legend.get_texts():
        text.set_color('white')

    #Set x and y axis tick labels to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_ylim(100, 40000)

    # Hide spines
    ax.spines['bottom'].set_color('#282952')
    ax.spines['top'].set_color('#282952')
    ax.spines['right'].set_color('#282952')
    ax.spines['left'].set_color('#282952')

    fig_3.tight_layout()

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure=fig_3, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=200)


    
    
call_GetRevenueByCategory(selected_year)
call_GetRevenueBySeason(selected_year)
call_GetRevenueByRegion(selected_year)
call_GetMonthlyRevenueByCategory(selected_year)


def switch_year(year):
    # Your backend logic here, e.g., passing the selected year to a function
    print(f"Selected year: {year}")

# Function to handle the radio button selection
def on_radio_button_selected():
    selected_year = year_var.get()
    call_GetRevenueByCategory(selected_year)
    call_GetRevenueBySeason(selected_year)
    call_GetRevenueByRegion(selected_year)
    call_GetMonthlyRevenueByCategory(selected_year)
    
# Initialize a variable to store the selected year

year_var = IntVar()
year_var.set(2023)  # Default to the current year

# Create radio buttons for current year and previous year
current_year_radio = Radiobutton(root, text="Current Year", variable=year_var, value=2023, command=on_radio_button_selected, bg="#E5BEEC", fg="#282952")
previous_year_radio = Radiobutton(root, text="Previous Year", variable=year_var, value=2022, command=on_radio_button_selected, bg="#E5BEEC", fg="#282952")

# Place the radio buttons on the GUI
current_year_radio.pack(pady=10)
previous_year_radio.pack(pady=3)



# Create a Matplotlib figure
fig_4 = Figure(figsize=(1.2, 0.3), facecolor="#917FB3")

# Add text to the figure
#text_content = "77345"
text_content= '$'+str(GetTotalRevenue_f (selected_year))        
fig_4.text(0.5, 0.5, text_content, ha='center', va='center',fontsize=15,color='white')

# Display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure=fig_4, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=45, y=135)

# Create a Matplotlib figure
fig_6 = Figure(figsize=(0.8, 0.3), facecolor="#917FB3")

# Add text to the figure
#text_content = "77345"
text_content= str(GetToatlCustomers_f (selected_year))        
fig_6.text(0.5, 0.5, text_content, ha='center', va='center',fontsize=15,color='white')

# Display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure=fig_6, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=370, y=135)


def emp():
    root.withdraw()
    os.system("python cust_demo.py")
    root.deiconify()

def mn():
    root.withdraw()
    os.system("python main.py")
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
button2.configure(command=mn)


root.resizable(False, False)
root.mainloop()