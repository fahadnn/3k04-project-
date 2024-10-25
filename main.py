import string
import tkinter as tk
from tkinter import ttk
from userDB import create_db, register_user, verify_user
from parameterDB import create_parameters_db, save_parameters, get_parameters
import sqlite3

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker")
        self.geometry ("700x600")
        
        create_db() #initialize user login info DB
        create_parameters_db() #User Programmable parameters info DB
        
        self.current_frame = None
        self.user_id = None  # Store the logged-in user ID to associate w/ parameters
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
            return r"Error, password must contain at least one special character: !\"#$%&'()*+,-./:;<=>?@[\]^_{|}~`"
        
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

         # Register button that switches to the registration frame
        self.register_button = ttk.Button(self, text="Register", command=lambda: master.switch_frame(registration_frame))
        self.register_button.grid(row=5, column=1, pady=20)
        
        # Label to display login status (successful or unsuccessful)
        self.login_status = ttk.Label(self, text = " ")
        self.login_status.grid(row=6, column=0, columnspan=2,pady=10)

    #function to allow users to change to desired language in language menu
    def change_language(self, language):
        print(f"Language selected: {language}")

    # Function to display the language menu when the user clicks on the "Language" button
    def show_language_menu(self, event):
        language_menu = tk.Menu(self) # Create a new language menu
        languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]
        
        # Populate the menu with languages
        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        
        # Display the menu at the position of the mouse click    
        language_menu.tk_popup(event.x_root, event.y_root)

    
    # Function to handle the login process
    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        verified, user_id = verify_user(username, password) #unpack the user id and bool that tells if login was success
        
         # Verify the username and password against the database or authentication system
        if verified:
            self.clear_form()
            self.master.user_id = user_id  # Store the logged-in user ID
            self.master.switch_frame(information_frame)
        else:
            self.login_status.config(text = "Login unsuccessful, invalid username and/or password")

    # Function to clear the username and password entry fields
    def clear_form(self):
        self.username_entry.delete(0, tk.END) # Clear the username fiel
        self.password_entry.delete(0, tk.END) # Clear the password field

class information_frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_button = None
        self.last_bg = None

        # Add a communication-status label (active/Inactive)
        self.comm_status_label = ttk.Label(self, text="Inactive", foreground="red")
        self.comm_status_label.grid(row=0, column=1, padx=10, pady=10)  # Position with grid

        # Data for parameter list
        self.parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 
                           'Atrial Pulse Width', 'Ventricular Amplitude', 
                           'Ventricular Pulse Width', 'VRP', 'ARP']
        # Fetch existing values from the database or use defaults
        self.values = self.fetch_existing_parameters()  # Fetch parameters from the database
        self.entries = []  # To store Entry widgets
        self.create_widgets()

#returns the existing parameter values for the user, or returns 1.0 for default value if none xists
    def fetch_existing_parameters(self):
            user_id = self.master.user_id  # Get the logged-in user ID
            #error handling to check that user is logged in and user_id is working correctly
            if user_id is None:
                return "error, it appears that no user is logged in (user_id unavailable)" 
            # Retrieve parameters from the database
            existing_parameters = get_parameters(user_id)
            if existing_parameters:
                return [existing_parameters.get(param, 1.0) for param in self.parameters]
            else:
                return [1.0] * len(self.parameters)  # Default values if no parameters are found
        
    def create_widgets(self):
        # Labels
        tk.Label(self, text="DCM Communication with Pacemaker:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text="Pacing Mode").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text="Graph of Pacing Mode").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text="Programmable Parameters").grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Buttons
        self.create_button('AOO', 1, 1)
        self.create_button('VOO', 1, 2)
        self.create_button('AAI', 1, 3)
        self.create_button('VVI', 1, 4)
        
        # Entry widgets for parameters
        for i, param in enumerate(self.parameters):
            tk.Label(self, text=param).grid(row=6+i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self)
            entry.insert(0, str(self.values[i]))  # Set default value
            entry.grid(row=6+i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        # Button to save values to the database
        save_button = tk.Button(self, text="Save Values", command=self.save_values)
        save_button.grid(row=6+len(self.parameters), column=0, columnspan=2, pady=10)

    def create_button(self, text, row, col):
        button = tk.Button(
            self,
            text=text,
            fg='black',
            bg='lightgray',  # Default background color
            activebackground='#B7E3F9',
            activeforeground='black',
            highlightthickness=0,
            relief='raised',  # Make the button look more clickable
            padx=10,  # Add some padding to make it larger
            pady=5
        )
        button.grid(row=row, column=col, padx=5, pady=5)  # Use grid for button placement

        # Bind mouse enter and leave events for hover effect
        button.bind("<Enter>", lambda e: self.on_hover(button))
        button.bind("<Leave>", lambda e: self.on_leave(button))

        # Configure button command
        button.config(command=lambda btn=button: self.change_selected_button(btn))

# Change color only if the button is not selected, and its bg is not orange (selected button)
    def on_hover(self, button):
        if button != self.selected_button and (button.cget("background") != "orange") : 
            button.config(bg='skyblue')

# Reset color only if the button is not selected and its bg is not orange (selected button)
    def on_leave(self, button):
        if button != self.selected_button and (button.cget("background") != "orange") : 
            button.config(bg='lightgray')

#print a message when pacing mode is changed
    def abc(self):
        print("Pacing Mode Changed")

#set communication with pacemaker status to inactive
    def set_inactive(self): 
        self.comm_status_label.config(text="Inactive", foreground="red")
         
    def change_selected_button(self, button):
        self.abc()
        #set communication status with pacemaker to active when pacing mode button is pressed
        self.comm_status_label.config(text="Active", foreground="green")
        self.after(2000, self.set_inactive)

        if self.selected_button is not None:    #if button is clicked...
            self.selected_button.config(bg="lightgray") #set previously clicked buttons bg to lightgray default
        self.selected_button = button
        button.config(bg="orange") #change selected buttons bg to orange
        
    def save_values(self):
        user_id = self.master.user_id  # Get the logged-in user ID
        if user_id is None:
            print("Error: No user is logged in.")
            return  # Exit the method if user_id is invalid
        
        parameter_values = {}
        for i, entry in enumerate(self.entries):
            param = self.parameters[i]
            value = entry.get()
            try:
                parameter_values[param] = float(value)  # Store each parameter and its value
            except ValueError:
                print(f"Invalid input for {param}: {value}")

        save_parameters(user_id, parameter_values)  # Save all parameters at once
        print("Parameter values saved to database.")

        
        
    '''    
    def save_values(self):
        user_id = self.master.user_id  # Get the logged-in user ID
        
        #check if user_id is available/not null
        if user_id is None:
            print("Error: No user is logged in.")
            return  # Exit the method if user_id is invalid
        
        for i, entry in enumerate(self.entries):
            param = self.parameters[i]
            value = entry.get()
            try:
                save_parameter(user_id, param, float(value))
            except ValueError:
                print(f"Invalid input for {param}: {value}")
            except sqlite3.IntegrityError as e:
                print(f"Database error: {e}")  # Handle the IntegrityError gracefully
        print("Parameter values saved to database.")
    '''       
if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()
    
    
    
    #add save button for programmable parameters list - done
    #perform error handling for if programmable parameter data enteres is out of range
    #make the pacing mode buttons more obvious that they are buttons - done
    #add programmable parameters into the userDB database and attach to each user - done