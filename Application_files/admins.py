import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
from DATA225utils import make_connection, dataframe_query

main_window = Tk()
main_window.geometry("1366x768")
main_window.title("Retail Administration Interface")

user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()

conn = make_connection(config_file = 'oltp.ini')
cur = conn.cursor()

def generate_employee_id(length):
    numeric_chars = string.digits
    generated_sequence = ''.join(random.choice(numeric_chars) for _ in range(length - 3))
    return 'EMP' + generated_sequence

def is_phone_number_valid(phone_number):
    # Checks if the phone number consists of 10 digits
    if re.match(r"^\d{10}$", phone_number):
        return True
    return False

class LoginPageInterface:
    def __init__(self, main_window=None):
        main_window.geometry("1366x768")
        main_window.resizable(0, 0)
        main_window.title("Retail Manager(ADMIN)")

        self.background_label = Label(main_window)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/admin_login.png")
        self.background_label.configure(image=self.background_image)

        self.username_entry = Entry(main_window)
        self.username_entry.place(relx=0.373, rely=0.273, width=374, height=24)
        self.username_entry.configure(font="-family {Poppins} -size 10", relief="flat", textvariable=user)

        self.password_entry = Entry(main_window)
        self.password_entry.place(relx=0.373, rely=0.384, width=374, height=24)
        self.password_entry.configure(font="-family {Poppins} -size 10", relief="flat", show="*", textvariable=passwd)

        self.login_button = Button(main_window)
        self.login_button.place(relx=0.366, rely=0.685, width=356, height=43)
        self.login_button.configure(relief="flat", overrelief="flat", activebackground="#cf1e13", cursor="hand2",
                                    foreground="black", background="red", font="-family {Poppins SemiBold} -size 20",
                                    borderwidth="0", text="LOGIN", command=self.authenticate_user)
        

    def authenticate_user(self, event=None):
        input_username = user.get()
        input_password = passwd.get()

        query_user = "SELECT * FROM employee WHERE emp_id = %s and password = %s"
        cur.execute(query_user, [input_username, input_password])
        user_data = cur.fetchall()
    
        if user_data:
            if user_data[0][4] == "ADMIN":
                messagebox.showinfo("Login Status", "Login successful.")
                ad_page.username_entry.delete(0, END)
                ad_page.password_entry.delete(0, END)

                main_window.withdraw()
                global admin_window
                global admin_page
                admin_window = Toplevel()
                admin_page = AdministratorInterface(admin_window)
                admin_window.protocol("WM_DELETE_WINDOW", exit_application)
                admin_window.mainloop()
            else:
                messagebox.showerror("Access Denied", "You do not have admin privileges.")

        else:
            messagebox.showerror("Login Failed", "Username or password is incorrect.")
            ad_page.password_entry.delete(0, END)


def exit_application():
    confirmation = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?", parent=main_window)
    if confirmation:
        admin_window.destroy()
        main_window.destroy()

def manage_employees():
    admin_window.withdraw()
    global employee_window
    global employee_page
    employee_window = Toplevel()
    employee_page = EmployeeManagementInterface(employee_window)
    employee_window.protocol("WM_DELETE_WINDOW", exit_application)
    employee_window.mainloop()

def view_invoices():
    admin_window.withdraw()
    global invoice_window
    invoice_window = Toplevel()
    invoice_page = InvoiceManagementInterface(invoice_window)
    invoice_window.protocol("WM_DELETE_WINDOW", exit_application)
    invoice_window.mainloop()

class AdministratorInterface:
    def __init__(self, main_window=None):
        main_window.geometry("1366x768")
        main_window.resizable(0, 0)
        main_window.title("ADMIN Mode")

        self.main_label = Label(admin_window)
        self.main_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/admin.png")
        self.main_label.configure(image=self.background_image)

        self.admin_label = Label(admin_window)
        self.admin_label.place(relx=0.046, rely=0.056, width=62, height=30)
        self.admin_label.configure(font="-family {Poppins} -size 12", foreground="black",
                                   background="#FE6B61", text="ADMIN", anchor="w")

        self.logout_button = Button(admin_window)
        self.logout_button.place(relx=0.035, rely=0.106, width=76, height=23)
        self.logout_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                     cursor="hand2", foreground="black", background="#CF1E14",
                                     font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                     text="Logout", command=self.confirm_logout)

        self.employees_button = Button(admin_window)
        self.employees_button.place(relx=0.338, rely=0.508, width=146, height=63)
        self.employees_button.configure(relief="flat", overrelief="flat", activebackground="#cf1e13",
                                        cursor="hand2", foreground="black", background="#cf1e13",
                                        font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                        text="Employees", command=manage_employees)

        self.invoices_button = Button(admin_window)
        self.invoices_button.place(relx=0.536, rely=0.508, width=146, height=63)
        self.invoices_button.configure(relief="flat", overrelief="flat", activebackground="#cf1e13",
                                       cursor="hand2", foreground="black", background="#cf1e13",
                                       font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                       text="Invoices", command=view_invoices)
        
    def confirm_logout(self):
        confirm_exit = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?", parent=admin_window)
        if confirm_exit:
            admin_window.destroy()
            main_window.deiconify()
            ad_page.username_entry.delete(0, END)
            ad_page.password_entry.delete(0, END)


class EmployeeManagementInterface:
    def __init__(self, window=None):
        window.geometry("1366x768")
        window.resizable(0, 0)
        window.title("Employee Management")

        self.background_label = Label(employee_window)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/employee.png")
        self.background_label.configure(image=self.background_image)

        self.admin_indicator = Label(employee_window)
        self.admin_indicator.place(relx=0.046, rely=0.055, width=136, height=30)
        self.admin_indicator.configure(font="-family {Poppins} -size 10", foreground="#000000",
                                       background="#cf1e13", text="ADMIN", anchor="w")

        self.time_label = Label(employee_window)
        self.time_label.place(relx=0.9, rely=0.065, width=102, height=36)
        self.time_label.configure(font="-family {Poppins Light} -size 12", foreground="#000000",
                                  background="#cf1e13")

        self.search_entry = Entry(employee_window)
        self.search_entry.place(relx=0.040, rely=0.286, width=240, height=28)
        self.search_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.search_button = Button(employee_window)
        self.search_button.place(relx=0.229, rely=0.289, width=76, height=23)
        self.search_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                     cursor="hand2", foreground="black", background="#CF1E14",
                                     font="-family {Poppins SemiBold} -size 10", borderwidth="0",
                                     text="Search", command=self.find_employee)

        self.logout_button = Button(employee_window)
        self.logout_button.place(relx=0.035, rely=0.106, width=76, height=23)
        self.logout_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                     cursor="hand2", foreground="black", background="#CF1E14",
                                     font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                     text="Logout", command=self.perform_logout)

        self.add_emp_button = Button(employee_window)
        self.add_emp_button.place(relx=0.052, rely=0.432, width=306, height=28)
        self.add_emp_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                      cursor="hand2", foreground="black", background="#CF1E14",
                                      font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                      text="ADD EMPLOYEE", command=self.add_new_employee)
        
        
        self.update_emp_button = Button(employee_window)
        self.update_emp_button.place(relx=0.052, rely=0.5, width=306, height=28)
        self.update_emp_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                      cursor="hand2", foreground="black", background="#CF1E14",
                                      font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                      text="UPDATE EMPLOYEE", command=self.modify_employee)
        
        self.delete_emp_button = Button(employee_window)
        self.delete_emp_button.place(relx=0.052, rely=0.57, width=306, height=28)
        self.delete_emp_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                      cursor="hand2", foreground="black", background="#CF1E14",
                                      font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                      text="DELETE EMPLOYEE", command=self.remove_employee)
        
        self.exit_emp_button = Button(employee_window)
        self.exit_emp_button.place(relx=0.135, rely=0.885, width=76, height=23)
        self.exit_emp_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                      cursor="hand2", foreground="black", background="#CF1E14",
                                      font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                      text="EXIT", command=self.confirm_exit)
        


        # Configuration for Treeview and Scrollbars
        self.horizontal_scrollbar = Scrollbar(employee_window, orient=HORIZONTAL)
        self.vertical_scrollbar = Scrollbar(employee_window, orient=VERTICAL)
        self.employee_treeview = ttk.Treeview(employee_window)
        self.employee_treeview.place(relx=0.307, rely=0.203, width=880, height=550)
        self.employee_treeview.configure(yscrollcommand=self.vertical_scrollbar.set,
                                         xscrollcommand=self.horizontal_scrollbar.set,
                                         selectmode="extended")

        self.employee_treeview.bind("<<TreeviewSelect>>", self.handle_treeview_selection)

        self.vertical_scrollbar.configure(command=self.employee_treeview.yview)
        self.horizontal_scrollbar.configure(command=self.employee_treeview.xview)

        self.vertical_scrollbar.place(relx=0.954, rely=0.203, width=22, height=548)
        self.horizontal_scrollbar.place(relx=0.307, rely=0.924, width=884, height=22)

        # Treeview columns configuration
        self.employee_treeview.configure(columns=("Employee ID", "Employee Name", "Contact No.", "Password", "Designation"))

        self.employee_treeview.heading("Employee ID", text="Employee ID", anchor=W)
        self.employee_treeview.heading("Employee Name", text="Employee Name", anchor=W)
        self.employee_treeview.heading("Contact No.", text="Contact No.", anchor=W)
        self.employee_treeview.heading("Password", text="Password", anchor=W)
        self.employee_treeview.heading("Designation", text="Designation", anchor=W)

        self.employee_treeview.column("#0", stretch=NO, minwidth=0, width=0)
        self.employee_treeview.column("#1", stretch=NO, minwidth=0, width=150)
        self.employee_treeview.column("#2", stretch=NO, minwidth=0, width=200)
        self.employee_treeview.column("#3", stretch=NO, minwidth=0, width=200)
        self.employee_treeview.column("#4", stretch=NO, minwidth=0, width=150)
        self.employee_treeview.column("#5", stretch=NO, minwidth=0, width=150)
        self.populate_employee_data()

    def populate_employee_data(self):
        cur.execute("SELECT * FROM employee")
        employee_data = cur.fetchall()
        for record in employee_data:
            self.employee_treeview.insert("", "end", values=(record))

    def find_employee(self):
        tree_values = []
        for child in self.employee_treeview.get_children():
            tree_values.append(child)
            for value in self.employee_treeview.item(child)["values"]:
                tree_values.append(value)

        employee_id_to_find = self.search_entry.get()
        for item in tree_values:
            if item == employee_id_to_find:
                self.employee_treeview.selection_set(tree_values[tree_values.index(item) - 1])
                self.employee_treeview.focus(tree_values[tree_values.index(item) - 1])
                messagebox.showinfo("Success", f"Employee ID: {employee_id_to_find} found.", parent=employee_window)
                break
        else:
            messagebox.showerror("Not Found", f"Employee ID: {employee_id_to_find} not found.", parent=employee_window)


    selected_items = []
    def handle_treeview_selection(self, event):
        self.selected_items.clear()
        for item in self.employee_treeview.selection():
            if item not in self.selected_items:
                self.selected_items.append(item)

    def remove_employee(self):
        employee_ids = []
        ids_to_remove = []

        if self.selected_items:
            confirm_deletion = messagebox.askyesno("Confirm Deletion", 
                                                   "Are you sure you want to delete the selected employee(s)?", 
                                                   parent=employee_window)
            if confirm_deletion:
                for item in self.selected_items:
                    for value in self.employee_treeview.item(item)["values"]:
                        employee_ids.append(value)
                
                for index, id in enumerate(employee_ids):
                    if index % 7 == 0:
                        ids_to_remove.append(id)

                can_delete = True

                for id in ids_to_remove:
                    if id == "EMP0000":
                        can_delete = False
                        break
                    else:
                        delete_query = "DELETE FROM employee WHERE emp_id = %s"
                        cur.execute(delete_query, [id])
                        conn.commit()

                if can_delete:
                    messagebox.showinfo("Success", "Employee(s) deleted from database.", parent=employee_window)
                    self.selected_items.clear()
                    self.refresh_employee_data()
                else:
                    messagebox.showerror("Error", "Cannot delete master admin.", parent=employee_window)
        else:
            messagebox.showerror("Error", "Please select an employee.", parent=employee_window)

    def modify_employee(self):
        if len(self.selected_items) == 1:
            global update_window
            update_window = Toplevel()
            update_page = EmployeeUpdateInterface(update_window)
            update_window.protocol("WM_DELETE_WINDOW", self.close_update_window)
            global selected_employee_data
            selected_employee_data = []
            for item in self.selected_items:
                selected_employee_data.extend(self.employee_treeview.item(item)["values"])
            
            #update_page.populate_fields(selected_employee_data)
            update_page.name_entry.insert(0, selected_employee_data[1])
            update_page.contact_entry.insert(0, selected_employee_data[2])
            update_page.designation_entry.insert(0, selected_employee_data[3])
            update_page.password_entry.insert(0, selected_employee_data[4])
            update_window.mainloop()
        elif not self.selected_items:
            messagebox.showerror("Error", "Please select an employee to update.")
        else:
            messagebox.showerror("Error", "Only one employee can be updated at a time.")

    def add_new_employee(self):
        global add_window
        add_window = Toplevel()
        add_employee_page = EmployeeAdditionInterface(add_window)
        add_window.protocol("WM_DELETE_WINDOW", self.close_add_window)
        add_window.mainloop()

    def close_add_window(self):
        add_window.destroy()
        self.refresh_employee_data()

    def close_update_window(self):
        update_window.destroy()
        self.refresh_employee_data()

    def refresh_employee_data(self):
        self.employee_treeview.delete(*self.employee_treeview.get_children())
        self.populate_employee_data()

    def confirm_exit(self):
        confirm_exit = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=employee_window)
        if confirm_exit:
            employee_window.destroy()
            employee_window.deiconify()

    def perform_logout(self):
        confirm_logout = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm_logout:
            employee_window.destroy()
            main_window.deiconify()
            LoginPageInterface.clear_login_fields()



class EmployeeAdditionInterface:
    def __init__(self, window=None):
        window.geometry("1366x768")
        window.resizable(0, 0)
        window.title("Add Employee")

        self.background_label = Label(add_window)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/add_employee.png")
        self.background_label.configure(image=self.background_image)

        self.time_label = Label(add_window)
        self.time_label.place(relx=0.84, rely=0.065, width=102, height=36)
        self.time_label.configure(font="-family {Poppins Light} -size 12", 
                                  foreground="#000000", background="#cf1e13")

        self.r1 = add_window.register(self.validate_integer)
        self.r2 = add_window.register(self.validate_string)

        self.name_entry = Entry(add_window)
        self.name_entry.place(relx=0.132, rely=0.296, width=374, height=30)
        self.name_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.contact_entry = Entry(add_window)
        self.contact_entry.place(relx=0.132, rely=0.413, width=374, height=30)
        self.contact_entry.configure(font="-family {Poppins} -size 12", 
                                     relief="flat", validate="key", 
                                     validatecommand=(self.r1, "%P"))

        self.designation_entry = Entry(add_window)
        self.designation_entry.place(relx=0.527, rely=0.296, width=374, height=30)
        self.designation_entry.configure(font="-family {Poppins} -size 12", 
                                     relief="flat", validate="key", 
                                     validatecommand=(self.r2, "%P"))

        self.password_entry = Entry(add_window)
        self.password_entry.place(relx=0.527, rely=0.413, width=374, height=30)
        self.password_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.add_button = Button(add_window)
        self.add_button.place(relx=0.408, rely=0.836, width=96, height=34)
        self.add_button.configure(relief="flat", overrelief="flat", 
                                  activebackground="#CF1E14", cursor="hand2", 
                                  foreground="black", background="#CF1E14", 
                                  font="-family {Poppins SemiBold} -size 14", 
                                  borderwidth="0", text="ADD", command=self.add_new_employee)

        self.clear_button = Button(add_window)
        self.clear_button.place(relx=0.526, rely=0.836, width=86, height=34)
        self.clear_button.configure(relief="flat", overrelief="flat", 
                                    activebackground="#CF1E14", cursor="hand2", 
                                    foreground="black", background="#CF1E14", 
                                    font="-family {Poppins SemiBold} -size 14", 
                                    borderwidth="0", text="CLEAR", command=self.clear_employee_fields)

    def validate_integer(self, value):
        if value.isdigit() or value == "":
            return True
        return False

    def validate_string(self, value):
        if value.isalpha() or value == "":
            return True
        return False
    
    def add_new_employee(self):
        employee_name = self.name_entry.get()
        employee_contact = self.contact_entry.get()
        employee_designation = self.designation_entry.get()
        employee_password = self.password_entry.get()

        if employee_name.strip():
            if is_phone_number_valid(employee_contact):
                if employee_designation:
                    if employee_password:
                        employee_id = generate_employee_id(7)
                        insert_query = ("INSERT INTO employee(emp_id, name, contact_num, password, designation) "
                                        "VALUES(%s, %s, %s, %s, %s)")
                        cur.execute(insert_query, [employee_id, employee_name, employee_contact, employee_password, employee_designation])
                        conn.commit()
                        messagebox.showinfo("Success", f"Employee ID: {employee_id} successfully added to the database.", parent=add_window)
                        self.clear_employee_fields()
                    else:
                        messagebox.showerror("Error", "Please enter a password.", parent=add_window)
                else:
                    messagebox.showerror("Error", "Please enter a designation.", parent=add_window)
            else:
                messagebox.showerror("Error", "Invalid phone number.", parent=add_window)
        else:
            messagebox.showerror("Error", "Please enter the employee name.", parent=add_window)

    def clear_employee_fields(self):
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.designation_entry.delete(0, END)


class EmployeeUpdateInterface:
    def __init__(self, window=None):
        window.geometry("1366x768")
        window.resizable(0, 0)
        window.title("Update Employee")

        self.background_label = Label(update_window)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.update_image = PhotoImage(file="./images/update_employee.png")
        self.background_label.configure(image=self.update_image)

        self.time_label = Label(update_window)
        self.time_label.place(relx=0.84, rely=0.065, width=102, height=36)
        self.time_label.configure(font="-family {Poppins Light} -size 12", 
                                  foreground="#000000", background="#cf1e13")

        self.validate_integer = update_window.register(self.validate_integer_input)
        self.validate_string = update_window.register(self.validate_string_input)

        self.name_entry = Entry(update_window) 
        self.name_entry.place(relx=0.132, rely=0.296, width=374, height=30)
        self.name_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.contact_entry = Entry(update_window)
        self.contact_entry.place(relx=0.132, rely=0.413, width=374, height=30)
        self.contact_entry.configure(font="-family {Poppins} -size 12", 
                                     relief="flat", validate="key", 
                                     validatecommand=(self.validate_integer, "%P"))

        self.password_entry = Entry(update_window)
        self.password_entry.place(relx=0.527, rely=0.296, width=374, height=30)
        self.password_entry.configure(font="-family {Poppins} -size 12", 
                                     relief="flat", validate="key", 
                                     validatecommand=(self.validate_string, "%P"))

        self.designation_entry = Entry(update_window)
        self.designation_entry.place(relx=0.527, rely=0.413, width=374, height=30)
        self.designation_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.update_button = Button(update_window)
        self.update_button.place(relx=0.408, rely=0.836, width=96, height=34)
        self.update_button.configure(relief="flat", overrelief="flat", 
                                     activebackground="#CF1E14", cursor="hand2", 
                                     foreground="black", background="#CF1E14", 
                                     font="-family {Poppins SemiBold} -size 14", 
                                     borderwidth="0", text="UPDATE", command=self.execute_update)

        self.clear_button = Button(update_window)
        self.clear_button.place(relx=0.526, rely=0.836, width=86, height=34)
        self.clear_button.configure(relief="flat", overrelief="flat", 
                                    activebackground="#CF1E14", cursor="hand2", 
                                    foreground="black", background="#CF1E14", 
                                    font="-family {Poppins SemiBold} -size 14", 
                                    borderwidth="0", text="CLEAR", command=self.clear_update_fields)
        
    def execute_update(self):
        employee_name = self.name_entry.get()
        employee_contact = self.contact_entry.get()
        employee_designation = self.designation_entry.get()
        employee_password = self.password_entry.get()
      
        if employee_name.strip():
            if is_phone_number_valid(employee_contact):
                if employee_designation:
                    if employee_password:
                        employee_id = selected_employee_data[0]
                        update_query = ("UPDATE employee SET name = %s, contact_num = %s, password = %s, designation = %s "
                                        "WHERE emp_id = %s")
                        cur.execute(update_query, [employee_name, employee_contact, employee_password, employee_designation, employee_id])
                        conn.commit()
                        messagebox.showinfo("Success", f"Employee ID: {employee_id} successfully updated in the database.", parent=employee_window)
                        selected_employee_data.clear()
                        employee_page.refresh_employee_data()
                        update_window.destroy()
                    else:
                        messagebox.showerror("Error", "Please enter a password.")                    
                else:
                    messagebox.showerror("Error", "Please enter a designation.")
            else:
                messagebox.showerror("Error", "Invalid phone number.")
        else:
            messagebox.showerror("Error", "Please enter the employee name.")

    def clear_update_fields(self):
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.designation_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def validate_integer_input(self, value):
        return value.isdigit() or value == ""

    def validate_string_input(self, value):
        return value.isalpha() or value == ""



class InvoiceManagementInterface:
    def __init__(self, window=None):
        window.geometry("1366x768")
        window.resizable(0, 0)
        window.title("Invoices")

        self.background_label = Label(invoice_window)
        self.background_label.place(relx=0, rely=0, width=1366, height=768)
        self.background_image = PhotoImage(file="./images/invoices.png")
        self.background_label.configure(image=self.background_image)

        self.admin_label = Label(invoice_window)
        self.admin_label.place(relx=0.046, rely=0.055, width=136, height=30)
        self.admin_label.configure(font="-family {Poppins} -size 10", foreground="#000000",
                                   background="#cf1e13", text="ADMIN", anchor="w")

        self.time_label = Label(invoice_window)
        self.time_label.place(relx=0.9, rely=0.065, width=102, height=36)
        self.time_label.configure(font="-family {Poppins Light} -size 12", 
                                  foreground="#000000", background="#cf1e13")

        self.search_entry = Entry(invoice_window)
        self.search_entry.place(relx=0.040, rely=0.286, width=240, height=28)
        self.search_entry.configure(font="-family {Poppins} -size 12", relief="flat")

        self.search_button = Button(invoice_window)
        self.search_button.place(relx=0.229, rely=0.289, width=76, height=23)
        self.search_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                     cursor="hand2", foreground="black", background="#CF1E14",
                                     font="-family {Poppins SemiBold} -size 10", borderwidth="0",
                                     text="Search", command=self.search_inv)

        self.logout_button = Button(invoice_window)
        self.logout_button.place(relx=0.035, rely=0.106, width=76, height=23)
        self.logout_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                     cursor="hand2", foreground="black", background="#CF1E14",
                                     font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                     text="Logout", command=self.Logout)

        self.delete_invoice_button = Button(invoice_window)
        self.delete_invoice_button.place(relx=0.052, rely=0.432, width=306, height=28)
        self.delete_invoice_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                             cursor="hand2", foreground="black", background="#CF1E14",
                                             font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                             text="DELETE INVOICE", command=self.delete_invoice)

        self.exit_button = Button(invoice_window)
        self.exit_button.place(relx=0.135, rely=0.885, width=76, height=23)
        self.exit_button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14",
                                   cursor="hand2", foreground="black", background="#CF1E14",
                                   font="-family {Poppins SemiBold} -size 12", borderwidth="0",
                                   text="EXIT", command=self.Exit)

        self.horizontal_scrollbar = Scrollbar(invoice_window, orient=HORIZONTAL)
        self.vertical_scrollbar = Scrollbar(invoice_window, orient=VERTICAL)
        self.invoice_treeview = ttk.Treeview(invoice_window)
        self.invoice_treeview.place(relx=0.307, rely=0.203, width=880, height=550)
        self.invoice_treeview.configure(yscrollcommand=self.vertical_scrollbar.set, 
                                        xscrollcommand=self.horizontal_scrollbar.set,
                                        selectmode="extended")

        self.invoice_treeview.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.vertical_scrollbar.configure(command=self.invoice_treeview.yview)
        self.horizontal_scrollbar.configure(command=self.invoice_treeview.xview)

        self.vertical_scrollbar.place(relx=0.954, rely=0.203, width=22, height=548)
        self.horizontal_scrollbar.place(relx=0.307, rely=0.924, width=884, height=22)

        self.invoice_treeview.configure(columns=("Bill Number", "Date", "Customer ID", "Customer Review"))

        self.invoice_treeview.heading("Bill Number", text="Bill Number", anchor=W)
        self.invoice_treeview.heading("Date", text="Date", anchor=W)
        self.invoice_treeview.heading("Customer ID", text="Customer ID", anchor=W)
        self.invoice_treeview.heading("Customer Review", text="Customer Review", anchor=W)

        self.invoice_treeview.column("#0", stretch=NO, minwidth=0, width=0)
        self.invoice_treeview.column("#1", stretch=NO, minwidth=0, width=219)
        self.invoice_treeview.column("#2", stretch=NO, minwidth=0, width=219)
        self.invoice_treeview.column("#3", stretch=NO, minwidth=0, width=219)
        self.invoice_treeview.column("#4", stretch=NO, minwidth=0, width=219)

        self.DisplayData()


    def DisplayData(self):
        cur.execute("SELECT Purchase_ID,Purchase_Date,Customer_ID,ReviewRating FROM Purchases")
        fetch = cur.fetchall()
        for data in fetch:
            self.invoice_treeview.insert("", "end", values=(data))

    sel = []
    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.invoice_treeview.selection():
            if i not in self.sel:
                self.sel.append(i)
        
    def delete_invoice(self):
        val = []
        to_delete = []

        if len(self.sel)!=0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoice(s)?", parent=invoice_window)
            if sure == True:
                for i in self.sel:
                    for j in self.invoice_treeview.item(i)["values"]:
                        val.append(j)
                
                for j in range(len(val)):
                    if j%5==0:
                        to_delete.append(val[j])
                
                for k in to_delete:
                    delete = "DELETE FROM Purchases WHERE Purchase_ID = %s"
                    cur.execute(delete, [k])
                    conn.commit()

                messagebox.showinfo("Success!!", "Invoice(s) deleted from database.", parent=invoice_window)
                self.sel.clear()
                self.invoice_treeview.delete(*self.invoice_treeview.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!","Please select an invoice", parent=invoice_window)

    def search_inv(self):
        val = []
        for i in self.invoice_treeview.get_children():
            val.append(i)
            for j in self.invoice_treeview.item(i)["values"]:
                val.append(j)
        #print('valsss')  
        #print(val[0])
        to_search = self.search_entry.get()
        for search in val:
            if search==to_search:
                self.invoice_treeview.selection_set(val[val.index(search)-1])
                self.invoice_treeview.focus(val[val.index(search)-1])
                messagebox.showinfo("Success!!", "Bill Number: {} found.".format(self.search_entry.get()), parent=invoice_window)
                break
        else: 
            messagebox.showerror("Oops!!", "Bill Number: {} not found.".format(self.search_entry.get()), parent=invoice_window)


    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            invoice_window.destroy()
            main_window.deiconify()
            ad_page.search_entry.delete(0, END)
            ad_page.entry2.delete(0, END)

    def Exit(self):
        sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=invoice_window)
        if sure == True:
            invoice_window.destroy()
            admin_window.deiconify()


ad_page = LoginPageInterface(main_window)
main_window.bind("<Return>", LoginPageInterface.authenticate_user)
main_window.mainloop()
