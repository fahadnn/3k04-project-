import string
import tkinter as tk
from tkinter import ttk
from userDB import create_db, register_user, verify_user
from parameterDB import create_parameters_db, save_parameters, get_parameters
from serial_com import serialCommunication 

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker GUI")
        # Set the window size and position it at the top-left corner
        self.geometry("1000x800+0+0")  # width=1200, height=800, X=0, Y=0
        
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
        
        #password labal and entry box
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
        error_message = self._validate_registration(username, password, password_reentry)
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
    def _validate_registration(self, username, password, password_reentry):
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
        ttk.Label(self, text="Welcome to DCM User Interface for Pacemaker", foreground="red", font=("Helvetica", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        ttk.Label(self, text="Username", foreground="red", font=("Helvetica", 14, "bold")).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Password", foreground="red", font=("Helvetica", 14, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
       
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
        
        # Create a Style object
        self.style = ttk.Style()
        
        # Configure the style for Login Button (Red)
        self.style.configure("Login.TButton",
                             background="yellow",
                             foreground="red",
                             font=("Helvetica", 12, "bold"),
                             padding=10)
        
        # Configure the style for Register Button (Yellow)
        self.style.configure("Register.TButton",
                             background="yellow",
                             foreground="red",
                             font=("Helvetica", 12, "bold"),
                             padding=10)
        
        # Create Login Button
        self.login_button = ttk.Button(self, text="Login", style="Login.TButton", command=self.login_user)
        self.login_button.grid(row=5, column=0, pady=20)
        
        # Create Register Button
        self.register_button = ttk.Button(self, text="Register", style="Register.TButton", command=lambda: master.switch_frame(registration_frame))
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
        self.data = [0] * 19             # data list of 19 elements [0] to [18]
        self.function_code = None           # function_code data byte 
        self.sync = 0x16                    # Sync byte is 0x16 or 22 in decimal
        self.comm_status_label = None       # Variable for Active/ Inactive text based on comm w/ pacemaker
        self.comm = serialCommunication()   # Init. Object of serialCommunication Class
        self.pacing_mode = 0                # Default pacing mode is 0 (no pacing) 
        self.selected_button = None
        self.last_bg = None
        # Names for Programmable Parameter list
        self.parameters = ['Hysteresis', 'Rate Smoothing', 'Reaction Time', 'Response Factor', 
                           'Recovery Time', 'Lower Rate Limit', 'Upper Rate Limit', 'Max Sensor Rate', 'VRP', 'ARP', 
                           'PVARP', 'AV Amp Reg', 'AV Pulse Width', 'Atrial Sensitivity', 'Ventricular Sensitivity', ] 
        self.values = self.fetch_existing_parameters()      # Fetch existing user values from the database or use defaults
        self.entries = []                                   # To store Textbox in GUI
        self.create_widgets()                               # Create GUI elements
        self.update_comm_status()       # Check comm to update Comm Activity label
        
    def update_comm_status(self):       # Opens serial port then Check the communication status and updates the label
        self.comm.open_conn()           # Open serial port
        if (self.comm.is_connected()):  # returns True if connected
            self.comm_status_label.config(text="Active", foreground="green", font=("Helvetica", 12, "bold"))  
        else:
            self.comm_status_label.config(text="Inactive", foreground="red", font=("Helvetica", 12, "bold"))

    def fetch_existing_parameters(self):   # returns the saved user parameter values, or defaults to 0
        user_id = self.master.user_id  # Get the logged-in user ID
        if user_id is None:            # Confirm that user is logged in & provided a user ID
            return "error, it appears that no user is logged in (user_id unavailable)" 
        existing_parameters = get_parameters(user_id)   # Retrieve parameters from the database
        if existing_parameters:
            return [existing_parameters.get(param, 0) for param in self.parameters]
        else:
            return [0] * len(self.parameters) 
        
    def create_widgets(self):
        # Labels
        tk.Label(self, text="DCM Communication with Pacemaker: ", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")        
        self.comm_status_label = ttk.Label(self, text="Inactive", foreground="red", font=("Helvetica", 14, "bold")) # communication-status label
        self.comm_status_label.grid(row=0, column=5, columnspan = 2, padx=10, pady=6)
        tk.Label(self, text="Pacing Mode: ", font=("Helvetica", 14, "bold")).grid(row=1, column=0, columnspan=3, padx=2, pady=2)
        tk.Label(self, text="Graph of Pacing Mode: ", font=("Helvetica", 14, "bold")).grid(row=2, column=3, columnspan=4, padx=2, pady=2)
        ttk.Label(self, text="Programmable Parameters: ", foreground="red", font=("Helvetica", 14, "bold")).grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="w")
        
        # Create Pacing Mode Buttons
        pacing_modes = ['AOO', 'VOO', 'AAI', 'VVI', 'AOOR', 'VOOR', 'AAIR', 'VVIR', 'DOOR', 'DDDR']
        for idx, mode in enumerate(pacing_modes):
            self.create_button(mode, 1, idx + 4, width=5, height=1, font=("Helvetica", 12, "bold"), padx=1, pady=2)

        # Save Button used to store values in the database
        save_button = tk.Button(self, text="Save Values", command=self.save_values,
                        relief="raised", bd=3, font=("Helvetica", 12),
                        padx=2, pady=8, bg="lightblue", fg="red")
        save_button.grid(row=8 + len(self.parameters), column=1, padx=8, pady=4)   
        # Send_data button used to send packet of data, then ask for echo and receive the echo for confirmation
        send_button = tk.Button(self, text="Send Data", command=self.send_values,
                        relief="raised", bd=3, font=("Helvetica", 12),
                        padx=2, pady=8, bg="lightblue", fg="red")
        send_button.grid(row=8 + len(self.parameters), column=0, padx=8, pady=4)
        
        for i, param in enumerate(self.parameters):         # Create Labels & Textbox's for inputting Parameter Values
            tk.Label(self, text=param, font=("Helvetica", 12, "bold")).grid(row=6+i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self)
            entry.insert(0, str(self.values[i]))            # Fill Textbox's with saved values for the user
            entry.grid(row=6+i, column=1, padx=5, pady=5)
            self.entries.append(entry)

    def create_button(self, text, row, col, width, height, font, padx, pady):    # Create pacing mode buttons to choose a mode
        button = tk.Button(
            self,
            text=text,
            width=width,
            height=height,
            font=font,
            fg='red',
            bg='lightgray',                       # Default background color
            activebackground='#B7E3F9',
            activeforeground='black',
            highlightthickness=0,
            relief='raised',                      # Make the button look more clickable
            padx=padx,                            # Add some padding to make it larger
            pady=pady
        )
        button.grid(row=row, column=col)  # Use grid for button placement
        # Bind mouse enter and leave events for hover effect
        button.bind("<Enter>", lambda e: self.on_hover(button))
        button.bind("<Leave>", lambda e: self.on_leave(button))
        # use lambda fxn to capture text of the button when it is clicked
        button.config(command=lambda btn=button: self.change_selected_button(btn, text))

    def on_hover(self, button): # Highlight button if its not orange (most recently selected)
        if button != self.selected_button and (button.cget("background") != "orange") : 
            button.config(bg='skyblue')
    def on_leave(self, button): # Un-Highlight button if its not orange
        if button != self.selected_button and (button.cget("background") != "orange") : 
            button.config(bg='lightgray')
    def abc(self):              # print a message when pacing mode is changed
        print("Pacing Mode Changed") 
    def change_selected_button(self, button, text):     # Change most recently selected button to orange
        self.abc()                                      # print a message when pacing mode is changed
        if self.selected_button is not None:            # if button is clicked...
            self.selected_button.config(bg="lightgray") # set previously clicked buttons bg to gray default      
        self.selected_button = button                   # Make recently clicked button the selected_button
        button.config(bg="orange")                      # change selected_buttons bg to orange
        self.set_pacing_mode(text)          # Pass text of recently clicked button
        
    def set_pacing_mode(self, text):       # Map pacing modes to data list
        if text == "VOO":
            self.pacing_mode = 1  # mode = 1 for VOO
            print("Pacing Mode Changed to VOO")
        elif text == "AOO":
            self.pacing_mode = 2  # mode = 2 for AOO
            print("Pacing Mode Changed to AOO")
        elif text == "VVI":
            self.pacing_mode = 3
            print("Pacing Mode Changed to VVI")
        elif text == "AAI":
            self.pacing_mode = 4
            print("Pacing Mode Changed to AAI")
        elif text == "AOOR":
            self.pacing_mode = 5
            print("Pacing Mode Changed to AOOR")
        elif text == "VOOR":
            self.pacing_mode = 6
            print("Pacing Mode Changed to VOOR")
        elif text == "AAIR":
            self.pacing_mode = 7
            print("Pacing Mode Changed to AAIR")
        elif text == "VVIR":
            self.pacing_mode = 8
            print("Pacing Mode Changed to VVIR")
        elif text == "DOOR":
            self.pacing_mode = 9
            print("Pacing Mode Changed to DOOR")
        elif text == "DDDR":
            self.pacing_mode = 10
            print("Pacing Mode Changed to DDDR")
        else:
            print(f"Unknown pacing mode. self.pacing_mode = {self.pacing_mode} ")
            return
        self.data[2] = self.pacing_mode
        
    def send_values(self):     # Send & Echo 37 bit packet to pacemaker using serial_com methods
        function_code = 0                   #send params (0x00 in hex) 
        self.data[0] = 22                        #sync(0x16) is 22 in decimal
        self.data[1] = function_code             #send parameter fxn code
        self.data[2] = self.pacing_mode          #may already be set in set_pacing_mode
        #                     19-5 = 14
        for i in range ( (len(self.data)) - 5 ):     #fill data list from [3] to [35], [36] is checksum
            self.data[i+3] = self.values[i]
            print(self.data[i])
        if (len(self.data) > 19):
            print("Error in send_values data list has too many indices")
            return
        
        self.comm.send_packet(function_code, self.data, self.pacing_mode)  # send packet to write parameters from dcm to pacemaker (function_code=0x00)
        
        function_code = 1                                # echo params (0x01 in hex)
        self.data[1] = function_code                     # echo packet fxn code
        self.comm.send_packet(function_code, self.data, self.pacing_mode)  # send packet to echo parameters from dcm to pacemaker (function_code=0x01)
        self.comm.receive_packet()                       # receive back/print the echo of the params that were just sent
        
    def save_values(self):      # Save parameter values in GUI text box's to parameter database
        user_id = self.master.user_id               # Get the logged in user's ID
        if user_id is None:                         # Exit the method if user_id is invalid
            print("Error: No user is logged in.")
            return
        
        parameter_values = {}                       # create empty dictionary for parameter values
        
        for i, entry in enumerate(self.entries):    # validate each parameter entry in GUI textbox
            param = self.parameters[i]
            value = entry.get()
            try:     # Attempt to convert the input to a float, handle invalid input by exiting save
                value = float(value)
            except ValueError:
                print(f"Invalid input for {param}: {value}")
                return
            if (i == 0) and (not (0 <= value <= 50)):           # Check if the value is within the valid range (50 <= value <= 125)
                print(f"Error: '{param}' value '{value}' is out of the valid range (0-50). Please input a valid value before saving.")
                return                                          # Prevent saving if value is out of the range
            if (i == 1) and (not (0 <= value <= 25)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (0-25). Please input a valid value before saving.")
                return
            if (i == 2) and (not (10 <= value <= 50)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (10-50). Please input a valid value before saving.")
                return
            if (i == 3) and (not (1 <= value <= 16)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (1-16). Please input a valid value before saving.")
                return
            if (i == 4) and (not (2 <= value <= 16)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (2-16). Please input a valid value before saving.")
                return
            if (i == 5) and (not (30 <= value <= 50)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (30-50). Please input a valid value before saving.")
                return
            if (i == 6) and (not (50 <= value <= 175)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (50-175). Please input a valid value before saving.")
                return
            if (i == 7) and (not (50 <= value <= 175)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (50-175). Please input a valid value before saving.")
                return
            if (i == 8) and (not (150 <= value <= 500)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (150-500). Please input a valid value before saving.")
                return
            if (i == 9) and (not (150 <= value <= 500)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (150-500). Please input a valid value before saving.")
                return
            if (i == 10) and (not (150 <= value <= 500)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (150-500). Please input a valid value before saving.")
                return
            if (i == 11) and (not (0 <= value <= 7.0)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (0-7.0). Please input a valid value before saving.")
                return    
            if (i == 12) and (not (0.1 <= value <= 1.0)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (0.1-1.0). Please input a valid value before saving.")
                return
            if (i == 13) and (not (0.25 <= value <= 0.75)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (0.25-0.75). Please input a valid value before saving.")
                return
            if (i == 14) and (not (1.0 <= value <= 10)):         
                print(f"Error: '{param}' value '{value}' is out of the valid range (1.0-10). Please input a valid value before saving.")
                return
            
        parameter_values[param] = value                 # Store the validated parameter value
        save_parameters(user_id, parameter_values)      # If all parameters are valid, save them to the database
        print("Parameter values saved to database.")

if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()

    #perform error handling for if programmable parameter data enteres is out of range