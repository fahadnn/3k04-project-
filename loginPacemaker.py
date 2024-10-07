import tkinter

window=tkinter.Tk()
window.title("PACEMAKER")
window.geometry('700x600')

def change_language(language):
    print(f"Langauge selected: {language}")

def show_language_menu(event):
    language_menu.post(event.x_root, event.y_root) #what is happening here?

#Labels and Entries

welcome_label = tkinter.Label(window, text='Welcome to DCM User Interface for Pacemaker')
username_label = tkinter.Label(window, text="Username")
username_entry = tkinter.Entry(window)
password_label = tkinter.Label(window, text="Password")
password_entry = tkinter.Entry(window)

#Buttons

login_button = tkinter.Button(window, text="Login")
register_button = tkinter.Button(window, text='Register')
language_button = tkinter.Button(window,text="Language")
language_button.bind("<Button-1>", show_language_menu)

#Dropdown (popup) menu

language_menu = tkinter.Menu(window, tearoff=0) #what is happening here?
languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]

for lang in languages:
    language_menu.add_command(label=lang, command=lambda l=lang: change_language(l))


#Layout

welcome_label.grid(row=0, column=0, pady=10, padx=(0,20), sticky="w")
language_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")
username_label.grid(row=1, column=0,columnspan=2, pady=10)
username_entry.grid(row=2, column=0, columnspan=2,pady=10)
password_label.grid(row=3, column=0, columnspan=2,pady=10)
password_entry.grid(row=4, column=0, columnspan=2,pady=10)
login_button.grid(row=5, column=0, columnspan=1, pady=20)
register_button.grid(row=5, column=1, columnspan=1, pady=20)


# Set the grid to expand evenly across columns
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()