from tkinter import *
import sqlite3
import os.path
from os import path
from tkinter import messagebox

def login_signup_click():
    global username_input
    global pword_input
    global pword_conf_input

    # Create new DB or connect to existing one
    conn = sqlite3.connect("usernames_and_passwords.db")
    c = conn.cursor()

    #Execute DB query and assign username and pword variables
    c.execute('''SELECT username FROM usernames_and_passwords WHERE username=?''',
              (username_input.get(),))
    user_query_tuple = c.fetchone()

    if user_query_tuple is not None:
        user_query_str = user_query_tuple[0]

    c.execute('''SELECT password FROM usernames_and_passwords WHERE username=?''',
              (username_input.get(),))
    pword_query_tuple = c.fetchone()

    if pword_query_tuple is not None:
        pword_query_str = pword_query_tuple[0]

    #****New users****
    #Insert user details into DB if new user
    if new_button["state"] == "disabled" and pword_input.get() == pword_conf_input.get() and user_query_tuple is None:

        c.execute("INSERT INTO usernames_and_passwords VALUES (:username, :password)",
                  {
                      "username": username_input.get(),
                      "password": pword_input.get()
                  })
        conn.commit()
        messagebox.showinfo("Success", "Your account has been created.")

    #Passwords don't match
    elif new_button["state"] == "disabled" and pword_input.get() != pword_conf_input.get() and user_query_tuple is None:
        messagebox.showwarning("Password error", "Passwords do not match. Please try again.")

    #Username already exists
    elif new_button["state"] == "disabled" and pword_input.get() == pword_conf_input.get() and user_query_tuple is not None:
        messagebox.showwarning("Username taken", "Username already exists. Please try another.")

    #****Existing users****
    elif new_button["state"] == "normal":

        #Username does not exist
        if user_query_tuple is None:
            messagebox.showinfo("Username not in database", "Username not in database. Please try again.")

        #Password doesn't match
        elif pword_query_str != str(pword_input.get()):
            #Username and pword don't match
            messagebox.showinfo("Incorrect password", "Password incorrect. Please try again.")

        #Everything matches
        elif pword_query_str == str(pword_input.get()):
            #Username and pword match
            messagebox.showinfo("Success", "You are now logged in.")

        #Catch-all warning
        else:
            messagebox.showwarning("Undefined error", "Something went wrong. Please restart.")

    #Catch-all warning
    else:
        messagebox.showwarning("Undefined error", "Something went wrong. Please restart.")

    records = ""
    c.execute("SELECT *, oid FROM usernames_and_passwords")
    records = c.fetchall()

    conn.close()

def create_db():
    # Create new DB or connect to existing one
    conn = sqlite3.connect("usernames_and_passwords.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE usernames_and_passwords (
        username text,
        password text
        )""")
    conn.commit()
    conn.close()

def setup_existing_user_gui():
    global username_input
    global pword_input
    global pword_conf_input

    #Set title
    root.title("Log in as existing user")

    # Inputs
    username_input = Entry(root, width=20)
    username_input.insert(0, "")
    pword_input = Entry(root, width=20)
    pword_input.insert(0, "")
    pword_conf_input = Entry(root, width=20)
    pword_conf_input.insert(0, "")

    # Labels
    username_label = Label(root, text="Username: ")
    password_label = Label(root, text="Password: ")
    password_conf_label = Label(root, text="Confirm password: ")

    # Displaying
    login_signup_button.configure(state=NORMAL)
    login_signup_button.configure(text="Log in")
    new_button.grid(row=1, column=2)
    existing_button.configure(state=DISABLED)
    new_button.configure(state=NORMAL)
    username_label.grid(row=2, column=1,  pady=(100, 5))
    password_label.grid(row=3, column=1)
    username_input.grid(row=2, column=2, pady=(100, 5))
    pword_input.grid(row=3, column=2, pady=5)
    password_conf_label.grid(row=4, column=1, pady=5)
    pword_conf_input.grid(row=4, column=2)
    pword_conf_input.configure(state=DISABLED)

def setup_new_user_gui():

    global username_input
    global pword_input
    global pword_conf_input

    #Set title
    root.title("Create new user")

    # Inputs
    username_input = Entry(root, width=20)
    username_input.insert(0, "")
    pword_input = Entry(root, width=20)
    pword_input.insert(0, "")
    pword_conf_input = Entry(root, width=20)
    pword_conf_input.insert(0, "")

    # Labels
    username_label = Label(root, text="Username: ")
    password_label = Label(root, text="Password: ")
    password_conf_label = Label(root, text="Confirm password: ")

    # Displaying
    login_signup_button.configure(state=NORMAL)
    login_signup_button.configure(text="Sign up")
    existing_button.grid(row=1, column=1)
    new_button.configure(state=DISABLED)
    existing_button.configure(state=NORMAL)
    username_label.grid(row=2, column=1, pady=(100, 5))
    password_label.grid(row=3, column=1, pady=5)
    password_conf_label.grid(row=4, column=1)
    username_input.grid(row=2, column=2, pady=(100, 5))
    pword_input.grid(row=3, column=2)
    pword_conf_input.grid(row=4, column=2, pady=5)
    pword_conf_input.configure(state=NORMAL)

def view_db_click():
    # Create new DB or connect to existing one
    conn = sqlite3.connect("usernames_and_passwords.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM usernames_and_passwords")
    records = c.fetchall()
    conn.commit()
    conn.close()

def setup_gui():
    global username_input
    global pword_input
    global pword_conf_input
    global new_button
    global login_signup_button
    global existing_button
    global root

    # Tkinter set up
    root = Tk()
    root.title("New or existing page")
    root.geometry("500x400")

    # Buttons
    new_button = Button(root, text="New user", command=setup_new_user_gui, padx=30, pady= 5)
    existing_button = Button(root, text="Existing user", command=setup_existing_user_gui, padx=30, pady= 5)
    login_signup_button = Button(root, text="Log in / Sign up", command=login_signup_click, padx=30, pady= 5)
    view_db_button = Button(root, text="View DB", command=view_db_click)

    # Displaying
    new_button.grid(row=1, column=2)
    existing_button.grid(row=1, column=1)
    login_signup_button.grid(row=5, column=2, pady = (100, 5))
    # view_db_button.grid(row=5, column=1)
    login_signup_button.configure(state=DISABLED)

    mainloop()

#********Runtime starts here*********

if not path.exists("usernames_and_passwords.db"):
    create_db()

setup_gui()