import string
import tkinter as tk
from tkinter import ttk, messagebox
from userDB import create_db, register_user, verify_user

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker")
        self.geometry ("700x600")
        
        create_db()
        
        self.current_frame = None
        self.switch_frame(login_frame)
    
    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = frame(self)
        self.current_frame.pack(fill = "both", expand = True)
                
class registration_frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        #configuring grid layout
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=9) 
        
        #registration page title
        registration_title = ttk.Label(self, text = "Registration", font = ("Arial", 18, "bold"))
        registration_title.grid(row = 0, column = 1, pady = 30)
        
        #username label and entry box
        ttk.Label(self, text = "Username").grid (row = 1, column = 1, pady = None, sticky = "w")
        
        self.username_reg_entry = ttk.Entry(self)
        self.username_reg_entry.grid(row = 2, column = 1, pady = (0,15), sticky = "w"+"e")
        
        #oassword labal and entry box
        ttk.Label(self, text = "Password").grid(row = 3, column = 1, pady = None, sticky = "w")
        
        self.password_reg_entry = ttk.Entry(self, show = "*")
        self.password_reg_entry.grid(row = 4, column = 1, pady = (0,15), sticky = "w"+"e")
        
        #password re-entry labal and entry box
        ttk.Label(self, text = "Re-enter Password").grid(row = 5, column = 1, pady = None, sticky = "w")
        
        self.password_reg_reentry = ttk.Entry(self, show = "*")
        self.password_reg_reentry.grid(row = 6, column = 1, pady = (0,15), sticky = "w"+"e")
        
        #register button
        self.register_button = ttk.Button(self, text = "Register", command = self.register_user)
        self.register_button.grid(row = 7, column = 1)
        
        #registration status message
        self.reg_status = ttk.Label(self, text = " ")
        self.reg_status.grid(row = 8, column = 0, columnspan = 3, pady = None)
        
        #login label and button if already have an account
        ttk.Label(self, text = "Already have an account?").grid(row = 9, column = 1, pady = (30,0))
        
        ttk.Button(self, text = "Login", command = lambda: master.switch_frame(login_frame)).grid(row = 10, column = 1)
    
    #registration validation and adds to database if successful
    def register_user(self):
        username = self.username_reg_entry.get()
        password = self.password_reg_entry.get()
        password_reentry = self.password_reg_reentry.get()
        
        #changes registration status label is updates if there is an error with username or password input
        error_message = self.validate_registration(username, password, password_reentry)
        if error_message:
            self.reg_status.config(text = error_message)
            return
        
        #username and password inputs validated with data in database
        registration_status, error_message = register_user(username, password)
        if registration_status:
            self.reg_status.config(text = error_message)
            self.clear_form()
            self.master.switch_frame(login_frame)
        else:
            self.reg_status.config(text = error_message)
            
    #validates username and password inputs
    def validate_registration(self, username, password, password_reentry):
        if len(username) == 0:
             return "Error, username cannot be empty!"
         
        if any(char.isspace() for char in username):
             return "Error, username cannot contain whitespaces!"
        
        if len(password) < 8:
            return "Error, password must be at least 8 characters long!"
        
        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            return "Error, password must contain at least one uppercase and lowercase letter!"
        
        if not any(char in string.punctuation for char in password):
            return "Error, password must contain at least one special character: !\"#$%&'()*+,-./:;<=>?@[\]^_{|}~`"
        
        if any(char.isspace() for char in password):
            return "Error, password cannot contain whitespaces!"
        
        if password != password_reentry:
            return "Error, passwords do not match!"

        return None
            
    #clears form
    def clear_form(self):
        self.username_reg_entry.delete(0, tk.END)
        self.password_reg_entry.delete(0, tk.END)
        self.password_reg_reentry.delete(0, tk.END)
                        

class login_frame (ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        # Set the frame to be responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)  # Extra row for better spacing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Add labels, entries, and buttons with grid layout
        ttk.Label(self, text="Welcome to DCM User Interface for Pacemaker").grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        ttk.Label(self, text="Username").grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Password").grid(row=3, column=0, columnspan=2, pady=10)
        
        # Language menu
        language_menu = tk.Menu(self, tearoff=0)
        languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]

        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        
        self.language_button = ttk.Button(self, text="Language")
        self.language_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        self.language_button.bind("<Button-1>", self.show_language_menu)

        # Username and Password entries
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Login and Register buttons
        self.login_button = ttk.Button(self, text="Login", command=self.login_user)
        self.login_button.grid(row=5, column=0, pady=20)

        self.register_button = ttk.Button(self, text="Register", command=lambda: master.switch_frame(registration_frame))
        self.register_button.grid(row=5, column=1, pady=20)
        
        self.login_status = ttk.Label(self, text = " ")
        self.login_status.grid(row=6, column=0, columnspan=2,pady=10)

    #function to allow users to change to desired language in language menu
    def change_language(self, language):
        print(f"Language selected: {language}")

    def show_language_menu(self, event):
        language_menu = tk.Menu(self)
        languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]
        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        language_menu.tk_popup(event.x_root, event.y_root)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if verify_user(username, password):
            self.clear_form()
            self.master.switch_frame(information_frame)
        else:
            self.login_status.config(text = "Login unsuccessful, invalid username and/or password")

    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


class information_frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.selected_button = None
        self.last_bg = None
        
        # Add a communication-status label (active/Inactive)
        self.comm_status_label = ttk.Label(self, text="Inactive", foreground="red")
        self.comm_status_label.place(x=550, y=80)  # Position 
        
        # Data for parameter list
        self.parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 'Atrial Pulse Width', 
                           'Ventricular Amplitude', 'Ventricular Pulse Width', 'VRP', 'ARP']
        self.values = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        
        self.create_widgets()
        self.create_table()

    def create_widgets(self):
        # Labels
        tk.Label(self, text="DCM Communication with Pacemaker:").place(x=250, y=80)
        tk.Label(self, text="Pacing Mode").place(x=30, y=180)
        tk.Label(self, text="Graph of Pacing Mode").place(x=30, y=280)
        tk.Label(self, text="Programmable Parameters").place(x=30, y=380)

        # Buttons
        self.create_button('AOO', 150, 180)
        self.create_button('VOO', 180, 180)
        self.create_button('AAI', 210, 180)
        self.create_button('VVI', 240, 180)

    #create button instance, place the button on gui, call 
    #change_selected_button method when clicked
    def create_button(self, text, x, y):
        button = tk.Button(
            self,
            text=text,
            fg='black',
            activebackground='#B7E3F9',
            activeforeground='black',
            highlightthickness=0,
            relief='flat',
        )
        button.place(x=x, y=y)
        button.config(command=lambda btn=button: self.change_selected_button(btn))

#Print a message to the terminal upon changing pacing mode
    def abc(self):
        print("Pacing Mode Changed")
        
#method to set label back to inactive, for when we add the logic (ASSIGNMENT2)
    def set_inactive(self): 
        self.comm_status_label.config(text="Inactive", foreground="red")

#Manages the selection/highlight state of the pacing mode buttons 
    def change_selected_button(self, button):
        self.abc()      #Print message to indicate new pacing mode
        
        # Update communication status label to "Active" upon pacing mode selection (FOR NOW/ASSIGNMENT1)
        self.comm_status_label.config(text="Active", foreground="green")
        # Simulate a delay for communication (for demo purposes, REPLACE WITH LOGIC FOR ASSIGNMENT2)
        self.after(2000, self.set_inactive)  # Set it back to inactive after 2 seconds
        
        #if theres a previously selected button, reset the buttons background to original state
        if self.selected_button is not None:
            self.selected_button.config(bg=self.last_bg)    
        #update selectedbutton to the most currently clicked button
        #and make its background orange
        self.selected_button = button
        self.last_bg = button.cget("bg")
        button.config(bg="orange")

    def create_table(self):
        # Create a Frame for the table
        table_frame = tk.Frame(self)
        table_frame.place(x=30, y=430, width=640, height=150)  # Adjust dimensions as needed

        # Create a Treeview widget
        tree = ttk.Treeview(table_frame, columns=("Programmable Parameter", "Value"), show='headings')
        
        # Define column headings
        tree.heading("Programmable Parameter", text="Programmable Parameter")
        tree.heading("Value", text="Value")

        # Set column widths
        tree.column("Programmable Parameter", width=200)
        tree.column("Value", width=100)

        # Insert data into the table
        for param, value in zip(self.parameters, self.values):
            tree.insert("", tk.END, values=(param, value))

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pack the Treeview widget
        tree.pack(fill=tk.BOTH, expand=True)
            
if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()