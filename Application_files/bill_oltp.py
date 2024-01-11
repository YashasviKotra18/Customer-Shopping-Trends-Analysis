# Importing required libraries and modules for the GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from tkinter import scrolledtext as tkst
import random
import string



# Setting UTF-8 encoding
#-*- coding: utf-8 -*-


# Initializing the main window for the application
main_window = Tk()
main_window.geometry("1366x768")
main_window.title("Employee Billing Interface")

# Defining string variables for user input fields
username_var = StringVar()
password_var = StringVar()
first_name_var = StringVar()
last_name_var = StringVar()
new_username_var = StringVar()
# Defining additional string variables for customer and billing details
new_password_var = StringVar()
customer_id_var = StringVar()
customer_feedback_var = StringVar()
total_amount_var = StringVar()
search_bill_number_var = StringVar()
billing_date_var = StringVar()

# Importing database utilities for connectivity
from DATA225utils import make_connection, dataframe_query

# Establishing connection with the database
database_connection = make_connection(config_file='oltp.ini')
database_cursor = database_connection.cursor()

# Function to generate a random bill number
def generate_random_bill_number():
    number_components = string.digits
    generated_number = ''.join(random.choice(number_components) for _ in range(5))
    return generated_number

# Function to validate phone number format
def is_phone_number_valid(phone_number):
    return True  # Placeholder for actual validation logic

# Function to handle user login
def user_login(Event=None):
    global current_user
    entered_username = username_var.get()
    entered_password = password_var.get()

    # Query to check user credentials in the database
    query_user = "SELECT * FROM employee WHERE emp_id = %s and password = %s"
    database_cursor.execute(query_user, [entered_username, entered_password])
    user_data = database_cursor.fetchall()
    
    if user_data:
        messagebox.showinfo("Login Status", "Login successful")
        main_login_page.username_entry.delete(0, 'end')
        main_login_page.password_entry.delete(0, END)

        main_login_page.password_entry.delete(0, 'end')
        main_window.withdraw()

        global billing_window_instance
        global billing_interface
        billing_window_instance = Toplevel()
        billing_interface = BillingInterface(billing_window_instance)
        billing_window_instance.protocol("WM_DELETE_WINDOW", confirm_exit)
        billing_window_instance.mainloop()

    else:
        messagebox.showerror("Login Failed", "Incorrect username or password provided.")
        main_login_page.password_entry.delete(0, 'end')

# Function to handle user logout
def user_logout():
    confirmation = messagebox.askyesno("Confirm Logout", "Do you really want to logout?", parent=billing_window_instance)
    if confirmation:
        billing_window_instance.destroy()
        main_window.deiconify()
        main_login_page.username_entry.delete(0, 'end')
        main_login_page.password_entry.delete(0, 'end')


# Adjusted Class Definition for LoginPage
class RetailLoginPage:
    def __init__(self, primary_window=None):
        primary_window.geometry("1366x768")
        primary_window.resizable(0, 0)
        primary_window.title("Retail Management Portal")

        self.login_background_label = Label(main_window)
        self.login_background_label.place(relx=0, rely=0, width=1366, height=768)
        self.login_background_img = PhotoImage(file="./images/employee_login.png")
        self.login_background_label.configure(image=self.login_background_img)

        self.username_entry = Entry(main_window)
        self.username_entry.place(relx=0.373, rely=0.273, width=374, height=24)
        self.username_entry.configure(font="-family {Poppins} -size 10", relief="flat", textvariable=username_var)

        self.password_entry = Entry(main_window)
        self.password_entry.place(relx=0.373, rely=0.384, width=374, height=24)
        self.password_entry.configure(font="-family {Poppins} -size 10", relief="flat", show="*", textvariable=password_var)

        self.submit_login_button = Button(main_window)
        self.submit_login_button.place(relx=0.366, rely=0.685, width=356, height=43)
        self.submit_login_button.configure(relief="flat", overrelief="flat", activebackground="#D2463E", cursor="hand2")
        self.submit_login_button.configure(foreground="black", background="#D2463E")
        self.submit_login_button.configure(font="-family {Poppins SemiBold} -size 20", borderwidth="0")
        self.submit_login_button.configure(text="LOGIN", command=user_login)

# Class definition for individual items in the retail system
class RetailItem:
    def __init__(self, item_name, item_price, item_quantity):
        self.name = item_name
        self.price = item_price
        self.quantity = item_quantity

# Class definition for the shopping cart in the retail system
class ShoppingCart:
    def __init__(self):
        self.cart_items = []
        self.item_count = {}

    def add_to_cart(self, item):
        self.cart_items.append(item)

    def remove_from_cart(self):
        if self.cart_items:
            self.cart_items.pop()
    # Method to clear all items from the shopping cart
    def clear_cart(self):
        self.cart_items.clear()

    # Method to calculate the total amount in the cart
    def calculate_total(self):
        total_cost = 0.0
        for item in self.cart_items:
            total_cost += float(item.price) * float(item.quantity)
        return total_cost

    # Method to check if the cart is empty
    def is_cart_empty(self):
        return len(self.cart_items) == 0

    # Method to compile all items in the cart
    def compile_cart_items(self):
        for item in self.cart_items:
            if item.name in self.item_count:
                self.item_count[item.name] += item.quantity
            else:
                self.item_count[item.name] = item.quantity
# Function to handle the application exit process
def confirm_exit():
    user_confirmation = messagebox.askyesno("Confirm Exit", parent=billing_window_instance)
    if user_confirmation:
        billing_window_instance.destroy()
        main_window.destroy()

# Class definition for the billing interface window
class BillingInterface:
    def __init__(self, window=None):
        window.geometry("1366x768")
        window.resizable(0, 0)
        window.title("Advanced Billing System")

        self.background_label = Label(billing_window_instance)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/retail_mngmnt.png")
        self.background_label.configure(image=self.background_image)
        self.user_message_label = Label(billing_window_instance)
        self.user_message_label.place(relx=0.038, rely=0.055, width=136, height=30)
        self.user_message_label.configure(font="-family {Poppins} -size 10", foreground="#000000", background="#ffffff")
        self.user_message_label.configure(text=username_var, anchor="w")

        
        self.customer_id_entry = Entry(billing_window_instance)
        self.customer_id_entry.place(relx=0.509, rely=0.23, width=240, height=24)
        self.customer_id_entry.configure(font="-family {Poppins} -size 12", relief="flat", textvariable=customer_id_var)
        self.customer_review_entry = Entry(billing_window_instance)
        self.customer_review_entry.place(relx=0.791, rely=0.23, width=240, height=24)
        self.customer_review_entry.configure(font="-family {Poppins} -size 12", relief="flat", textvariable=customer_feedback_var)

        self.bill_search_entry = Entry(billing_window_instance)
        self.bill_search_entry.place(relx=0.102, rely=0.23, width=240, height=24)
        self.bill_search_entry.configure(font="-family {Poppins} -size 12", relief="flat", textvariable=search_bill_number_var)

        self.search_button = Button(billing_window_instance)
        self.search_button.place(relx=0.031, rely=0.104, width=76, height=23)
        self.search_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.search_button.configure(foreground="black", background="#CF1E14")
        self.logout_button = Button(billing_window_instance)
        self.logout_button.place(relx=0.031, rely=0.104, width=76, height=23)
        self.logout_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.logout_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 12", borderwidth="0")
        self.logout_button.configure(text="Logout", command=user_logout)

        self.search_bill_button = Button(billing_window_instance)
        self.search_bill_button.place(relx=0.315, rely=0.234, width=76, height=23)
        self.search_bill_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.search_bill_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 12", borderwidth="0")
        self.search_bill_button.configure(text="Search", command=self.search_for_bill)

        self.generate_bill_button = Button(billing_window_instance)
        self.generate_bill_button.place(relx=0.048, rely=0.885, width=86, height=25)
        self.generate_bill_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.generate_bill_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.generate_bill_button.configure(text="Total", command=self.calculate_total_bill)

        self.clear_cart_button = Button(billing_window_instance)
        self.clear_cart_button.place(relx=0.141, rely=0.885, width=84, height=25)
        self.clear_cart_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.clear_cart_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.clear_cart_button.configure(text="Generate", command=self.initiate_bill_generation)

        self.reset_interface_button = Button(billing_window_instance)
        self.reset_interface_button.place(relx=0.230, rely=0.885, width=86, height=25)
        self.reset_interface_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.reset_interface_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.reset_interface_button.configure(text="Clear", command=self.reset_bill)

        self.print_bill_button = Button(billing_window_instance)
        self.print_bill_button.place(relx=0.322, rely=0.885, width=86, height=25)
        self.print_bill_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.print_bill_button.configure(overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.print_bill_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.print_bill_button.configure(text="Exit", command=confirm_exit)

        self.add_product_button = Button(billing_window_instance)
        self.add_product_button.place(relx=0.098, rely=0.734, width=86, height=26)
        self.add_product_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.add_product_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.add_product_button.configure(text="Add To Cart", command=self.add_product_to_cart)

        self.remove_product_button = Button(billing_window_instance)
        self.remove_product_button.place(relx=0.274, rely=0.734, width=84, height=26)
        self.remove_product_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.remove_product_button.configure(foreground="black", background="#CF1E14", font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.remove_product_button.configure(text="Clear", command=self.clear_product_selections)

        self.modify_product_button = Button(billing_window_instance)
        self.modify_product_button.place(relx=0.194, rely=0.734, width=68, height=26)
        self.modify_product_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2")
        self.modify_product_button.configure(activebackground="#CF1E14", cursor="hand2", foreground="black", background="#CF1E14")
        self.modify_product_button.configure(font="-family {Poppins SemiBold} -size 10", borderwidth="0")
        self.modify_product_button.configure(text="Remove", command=self.remove_selected_product)

        font_for_text = ("Poppins", "8")
        self.category_combobox = ttk.Combobox(billing_window_instance)
        self.category_combobox.place(relx=0.035, rely=0.408, width=477, height=26)

        query_for_category = "SELECT Category FROM Items"
        database_cursor.execute(query_for_category)
        categories_result = database_cursor.fetchall()
        unique_categories = []
        for category in categories_result:
            if category[0] not in unique_categories:
                unique_categories.append(category[0])
        self.category_combobox.configure(values=unique_categories)
        self.category_combobox.configure(state="readonly")
        self.category_combobox.configure(font="-family {Poppins} -size 8")
        self.category_combobox.option_add("*TCombobox*Listbox.font", font_for_text)
        self.category_combobox.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")

        self.item_combobox = ttk.Combobox(billing_window_instance)
        self.item_combobox.place(relx=0.035, rely=0.479, width=477, height=26)
        self.item_combobox.configure(font="-family {Poppins} -size 8")
        self.item_combobox.option_add("*TCombobox*Listbox.font", font_for_text)
        self.item_combobox.configure(state="disabled")

        self.subitem_combobox = ttk.Combobox(billing_window_instance)
        self.subitem_combobox.place(relx=0.035, rely=0.551, width=477, height=26)
        self.subitem_combobox.configure(state="disabled")
        self.subitem_combobox.configure(font="-family {Poppins} -size 8")
        self.subitem_combobox.option_add("*TCombobox*Listbox.font", font_for_text)

        self.quantity_entry = ttk.Entry(billing_window_instance)
        self.quantity_entry.place(relx=0.035, rely=0.629, width=477, height=26)
        self.quantity_entry.configure(font="-family {Poppins} -size 8", foreground="#000000", state="disabled")

        self.billing_scrolltext = tkst.ScrolledText(window)
        self.billing_scrolltext.place(relx=0.439, rely=0.586, width=695, height=275)
        self.billing_scrolltext.configure(borderwidth=0, font="-family {Podkova} -size 8", state="disabled")

        self.category_combobox.bind("<<ComboboxSelected>>", self.handle_category_selection)

    def handle_category_selection(self, Event):
        self.item_combobox.configure(state="readonly")
        self.item_combobox.set('')
        self.subitem_combobox.set('')
        # Handling the selection of a category to populate sub-categories or items
        query_for_items = "SELECT DISTINCT ItemName FROM Items WHERE Category = %s"
        database_cursor.execute(query_for_items, (self.category_combobox.get(),))
        items_result = database_cursor.fetchall()
        unique_items = []
        for item in items_result:
            if item[0] not in unique_items:
                unique_items.append(item[0])

        self.item_combobox.configure(values=unique_items)
        self.item_combobox.bind("<<ComboboxSelected>>", self.handle_item_selection)
        self.subitem_combobox.configure(state="disabled")

    def handle_item_selection(self, Event):
        self.subitem_combobox.configure(state="readonly")
        self.subitem_combobox.set('')
        query_for_subitems = "SELECT distinct color FROM datadynamos_db.Items i join datadynamos_db.ItemDetails id on i.Item_ID = id.Item_ID where category = %s and ItemName = %s"
        database_cursor.execute(query_for_subitems, [self.category_combobox.get(), self.item_combobox.get()])
        subitems_result = database_cursor.fetchall()
        unique_subitems = []
        # Populating the subitem combobox based on the item selection
        for subitem in subitems_result:
            unique_subitems.append(subitem[0])

        self.subitem_combobox.configure(values=unique_subitems)
        self.subitem_combobox.bind("<<ComboboxSelected>>", self.handle_subitem_selection)
        self.quantity_entry.configure(state="disabled")

    def handle_subitem_selection(self, Event):
        self.quantity_entry.configure(state="normal")
        self.stock_label = Label(billing_window_instance)
        self.stock_label.place(relx=0.033, rely=0.664, width=82, height=26)
        self.stock_label.configure(font="-family {Poppins} -size 8", anchor="w")

        selected_product = self.subitem_combobox.get()
        # Assuming 1 as a placeholder for stock quantity. This should be dynamically fetched based on actual stock.
        #self.stock_label.configure(text="In Stock: {}".format(1), background="#ffffff", foreground="#333333")

    shopping_cart = ShoppingCart()
    def add_product_to_cart(self):
        self.billing_scrolltext.configure(state="normal")
        current_text = self.billing_scrolltext.get('1.0', 'end')
        if 'Total' not in current_text:
            selected_item = self.item_combobox.get()
            if selected_item:
                selected_quantity = self.quantity_entry.get()
                query_for_price = """
                    SELECT distinct Purchase_Amount  FROM datadynamos_db.Items i \
                            join datadynamos_db.ItemDetails id on i.Item_ID = id.Item_ID \
                            join datadynamos_db.Purchases p on i.Item_ID = p.Item_ID \
                            where  ItemName = %s limit 1
                """
                database_cursor.execute(query_for_price, [selected_item])
                price_results = database_cursor.fetchall()
                available_stock = 1  # Placeholder for stock quantity
                item_price = int(price_results[0][0])
                selling_price = item_price * int(selected_quantity)
                retail_item = RetailItem(selected_item, item_price, selected_quantity)

                self.shopping_cart.add_to_cart(retail_item)
                self.billing_scrolltext.configure(state="normal")
                bill_entry = "{}\t\t\t\t\t\t{}\t\t\t\t\t\t{}\n".format(selected_item, selected_quantity, selling_price)
                self.billing_scrolltext.insert('insert', bill_entry)
                self.billing_scrolltext.configure(state="disabled")

    def remove_selected_product(self):
        if not self.shopping_cart.is_cart_empty():
            self.billing_scrolltext.configure(state="normal")
            current_text = self.billing_scrolltext.get('1.0', 'end')
            if 'Total' not in current_text:
                try:
                    self.shopping_cart.remove_from_cart()
                except IndexError:
                    messagebox.showerror("Error", "The cart is already empty", parent=billing_window_instance)
                else:
                    updated_bill_text = self.billing_scrolltext.get('1.0', 'end').split("\n")
                    new_bill_text = updated_bill_text[:-3]
                    self.billing_scrolltext.delete('1.0', 'end')
                    for line in new_bill_text:
                        self.billing_scrolltext.insert('insert', line + "\n")
                    # Adding a newline for visual separation in the bill text
                    self.billing_scrolltext.insert('insert', '\n')
                    self.billing_scrolltext.configure(state="disabled")
            else:
                try:
                    self.shopping_cart.remove_from_cart()
                except IndexError:
                    messagebox.showerror("Error", "The cart is empty", parent=billing_window_instance)
                else:
                    current_bill_lines = self.billing_scrolltext.get('1.0', 'end').split("\n")
                    updated_bill_lines = []
                    for line in current_bill_lines:
                        if line and 'Total' not in line:
                            updated_bill_lines.append(line)
                            updated_bill_lines.pop()  # Remove the last item from the list
                            self.billing_scrolltext.delete('1.0', 'end')
                    for updated_line in updated_bill_lines[:-1]:
                        self.billing_scrolltext.insert('insert', updated_line + "\n")
                        self.billing_scrolltext.insert('insert', updated_line + "\n")
                        self.billing_scrolltext.insert('insert', '\n')
                        self.billing_scrolltext.configure(state="disabled")
        else:
            messagebox.showerror("Error", "Please add a product before attempting removal.", parent=billing_window_instance)

    def initialize_welcome_message(self):
        self.customer_name_text = Text(billing_window_instance)
        self.customer_name_text.place(relx=0.514, rely=0.452, width=176, height=30)
        self.customer_name_text.configure(font="-family {Podkova} -size 10", borderwidth=0, background="#ffffff")

        self.customer_phone_text = Text(billing_window_instance)
        self.customer_phone_text.place(relx=0.894, rely=0.452, width=90, height=30)
        self.customer_phone_text.configure(font="-family {Podkova} -size 10", borderwidth=0, background="#ffffff")
        self.bill_number_text = Text(billing_window_instance)
        self.bill_number_text.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_number_text.configure(font="-family {Podkova} -size 10", borderwidth=0, background="#ffffff")

        self.bill_date_text = Text(billing_window_instance)
        self.bill_date_text.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_text.configure(font="-family {Podkova} -size 10", borderwidth=0, background="#ffffff")

    def calculate_total_bill(self):
        if self.shopping_cart.is_cart_empty():
            messagebox.showerror("Error", "Please add a product to the cart before calculating the total.", parent=billing_window_instance)
        else:
            self.billing_scrolltext.configure(state="normal")
            current_bill_text = self.billing_scrolltext.get('1.0', 'end')
            if 'Total' not in current_bill_text:
                self.billing_scrolltext.configure(state="normal")
                bill_divider = "\n\n\n" + ("─" * 61)
                self.billing_scrolltext.insert('insert', bill_divider)
                total_amount = "\nTotal\t\t\t\t\t\t\t\t\t\t\tRs. {}".format(self.shopping_cart.calculate_total())
                self.billing_scrolltext.insert('insert', total_amount)
                lower_divider = "\n" + ("─" * 61)
                self.billing_scrolltext.insert('insert', lower_divider)
                self.billing_scrolltext.configure(state="disabled")
            else:
                return

    bill_generation_state = 1
    def initiate_bill_generation(self):
        if self.bill_generation_state == 1:
            current_bill_content = self.billing_scrolltext.get('1.0', 'end')
            self.initialize_welcome_message()
            if customer_id_var.get() == "":
                messagebox.showerror("Error", "Please enter the customer's id.", parent=billing_window_instance)
            elif customer_feedback_var.get() == "":
                messagebox.showerror("Error", "Please enter a customers review.", parent=billing_window_instance)
            elif not is_phone_number_valid(customer_feedback_var.get()):
                messagebox.showerror("Error", "Please enter a valid phone number.", parent=billing_window_instance)
            elif self.shopping_cart.is_cart_empty():
                messagebox.showerror("Error", "The shopping cart is empty.", parent=billing_window_instance)
            else:
                if 'Total' not in current_bill_content:
                    self.calculate_total_bill()
                    self.initiate_bill_generation()
                else:
                    self.customer_name_text.insert('end', customer_id_var.get())
                    self.customer_name_text.configure(state="disabled")

                    self.customer_phone_text.insert('end', customer_feedback_var.get())
                    self.customer_phone_text.configure(state="disabled")

                    random_bill_number = generate_random_bill_number()
                    self.bill_number_text.insert('end', random_bill_number)
                    self.bill_number_text.configure(state="disabled")
                    current_bill_date = str(date.today())

                    self.bill_date_text.insert('end', current_bill_date)
                    self.bill_date_text.configure(state="disabled")

                    # Establishing a database connection for bill data insertion
                    database_connection = make_connection(config_file='oltp.ini')
                    database_cursor = database_connection.cursor()

                    total_bill_amount = self.shopping_cart.calculate_total()
                    bill_insert_query = ("INSERT INTO datadynamos_db.Purchases(Purchase_ID, Purchase_Date, Customer_ID, ReviewRating, Purchase_Amount,Purchase_frequency) VALUES(%s, %s, %s, %s, %s,%s)")
                    database_cursor.execute(bill_insert_query, [random_bill_number, current_bill_date, customer_id_var.get(), customer_feedback_var.get(), total_bill_amount, 4])
                    database_connection.commit()
                    messagebox.showinfo("Success", "The bill has been successfully generated.", parent=billing_window_instance)
                    self.customer_id_entry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.customer_review_entry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.bill_generation_state = 0
        else:
            return

    def reset_bill(self):
        self.initialize_welcome_message()
        self.customer_id_entry.configure(state="normal")
        self.customer_review_entry.configure(state="normal")
        self.customer_id_entry.delete(0, 'end')
        self.customer_review_entry.delete(0, 'end')
        self.bill_search_entry.delete(0, 'end')
        self.customer_name_text.configure(state="normal")
        self.customer_phone_text.configure(state="normal")
        self.bill_number_text.configure(state="normal")
        self.bill_date_text.configure(state="normal")
        self.billing_scrolltext.configure(state="normal")
        self.customer_name_text.delete('1.0', 'end')
        self.customer_phone_text.delete('1.0', 'end')
        self.bill_number_text.delete('1.0', 'end')
        self.bill_date_text.delete('1.0', 'end')
        self.billing_scrolltext.delete('1.0', 'end')
        self.customer_name_text.configure(state="disabled")
        self.customer_phone_text.configure(state="disabled")
        self.bill_number_text.configure(state="disabled")
        self.bill_date_text.configure(state="disabled")
        self.billing_scrolltext.configure(state="disabled")
        self.shopping_cart.clear_cart()
        self.bill_generation_state = 1

    def clear_product_selections(self):
        self.quantity_entry.delete(0, 'end')
        self.category_combobox.configure(state="normal")
        self.item_combobox.configure(state="normal")
        self.subitem_combobox.configure(state="normal")
        self.category_combobox.delete(0, 'end')
        self.item_combobox.delete(0, 'end')
        self.subitem_combobox.delete(0, 'end')
        self.item_combobox.configure(state="disabled")
        self.subitem_combobox.configure(state="disabled")
        self.quantity_entry.configure(state="disabled")
        try:
            self.stock_label.configure(foreground="#ffffff")
        except AttributeError:
            pass

    def search_for_bill(self):
        bill_search_query = "SELECT Purchase_ID,Purchase_Date,Purchase_Amount,ReviewRating FROM Purchases WHERE Purchase_ID = %s"
        database_cursor.execute(bill_search_query, [search_bill_number_var.get().strip()])
        bill_results = database_cursor.fetchall()
        if bill_results:
            self.reset_bill()
            self.initialize_welcome_message()
            self.customer_name_text.insert('end', bill_results[0][2])
            self.customer_name_text.configure(state="disabled")
            self.customer_phone_text.insert('end', bill_results[0][3])
            self.customer_phone_text.configure(state="disabled")

            self.bill_number_text.insert('end', bill_results[0][0])
            self.bill_number_text.configure(state="disabled")

            self.bill_date_text.insert('end', bill_results[0][1])
            self.bill_date_text.configure(state="disabled")

            self.billing_scrolltext.configure(state="normal")
            self.billing_scrolltext.configure(state="disabled")

            self.customer_id_entry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.customer_review_entry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.bill_generation_state = 0

        else:
            messagebox.showerror("Error", "No bill found with the provided information.", parent=billing_window_instance)



main_login_page = RetailLoginPage(main_window)
main_window.bind("<Return>", user_login)
main_window.mainloop()



