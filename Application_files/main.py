import os
from tkinter import Tk, Label, Button, PhotoImage, messagebox

def close_application():
    user_confirmation = messagebox.askyesno("Confirm Exit", "Do you really want to exit?", parent=app_window)
    if user_confirmation:
        app_window.destroy()

def open_dashboard():
    app_window.withdraw()
    os.system("python dashboard.py")
    app_window.deiconify()

def open_admin_panel():
    app_window.withdraw()
    os.system("python admins.py")
    app_window.deiconify()

def open_billing_system():
    app_window.withdraw()
    os.system("python bill_oltp.py")
    app_window.deiconify()

# Set up the main application window
app_window = Tk()
app_window.geometry("1366x768")
app_window.title("Sales Trends Analytics")
app_window.resizable(False, False)
app_window.protocol("WM_DELETE_WINDOW", close_application)

# Background label configuration
background_label = Label(app_window)
background_label.place(relx=0, rely=0, width=1366, height=768)
background_img = PhotoImage(file="./images/Main_Page.png")
background_label.configure(image=background_img)

button1 = Button(app_window)
button1.place(relx=0.032, rely=0.51, width=120, height=90)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="#ffffff")
button1.configure(borderwidth="0")
img2 = PhotoImage(file="./images/ana.png")
button1.configure(image=img2)
button1.configure(command=open_dashboard)

button2 = Button(app_window)
button2.place(relx=0.3, rely=0.51, width=120, height=90)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(activebackground="#ffffff")
button2.configure(cursor="hand2")
button2.configure(foreground="#ffffff")
button2.configure(background="#ffffff")
button2.configure(borderwidth="0")
img3 = PhotoImage(file="./images/2.png")
button2.configure(image=img3)
button2.configure(command=open_admin_panel)


button3 = Button(app_window)
button3.place(relx=0.16, rely=0.51, width=120, height=90)
button3.configure(relief="flat")
button3.configure(overrelief="flat")
button3.configure(activebackground="#ffffff")
button3.configure(cursor="hand2")
button3.configure(foreground="#ffffff")
button3.configure(background="#ffffff")
button3.configure(borderwidth="0")
img4 = PhotoImage(file="./images/1.png")
button3.configure(image=img4)
button3.configure(command=open_billing_system)



app_window.mainloop()

