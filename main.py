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
        
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=9) 
        # self.grid_rowconfigure(0, weight=1)     # Empty space above title
        # self.grid_rowconfigure(6, weight=1)   
        
        registration_title = ttk.Label(self, text = "Registration", font = ("Arial", 18, "bold"))
        registration_title.grid(row = 0, column = 1, pady = 30)
        
        ttk.Label(self, text = "Username").grid (row = 1, column = 1, pady = None, sticky = "w")
        
        self.username_reg_entry = ttk.Entry(self)
        self.username_reg_entry.grid(row = 2, column = 1, pady = (0,15), sticky = "w"+"e")
        
        ttk.Label(self, text = "Password").grid(row = 3, column = 1, pady = None, sticky = "w")
        
        self.password_reg_entry = ttk.Entry(self, show = "*")
        self.password_reg_entry.grid(row = 4, column = 1, pady = (0,15), sticky = "w"+"e")
        
        ttk.Label(self, text = "Re-enter Password").grid(row = 5, column = 1, pady = None, sticky = "w")
        
        self.password_reg_reentry = ttk.Entry(self, show = "*")
        self.password_reg_reentry.grid(row = 6, column = 1, pady = (0,15), sticky = "w"+"e")
        
        self.register_button = ttk.Button(self, text = "Register", command = self.register_user)
        self.register_button.grid(row = 7, column = 1)
        
        self.reg_status = ttk.Label(self, text = " ")
        self.reg_status.grid(row = 8, column = 0, columnspan = 3, pady = None)
        
        ttk.Label(self, text = "Already have an account?").grid(row = 9, column = 1, pady = (30,0))
        
        ttk.Button(self, text = "Login", command = lambda: master.switch_frame(login_frame)).grid(row = 10, column = 1)
    
    def register_user(self):
        username = self.username_reg_entry.get()
        password = self.password_reg_entry.get()
        password_reentry = self.password_reg_reentry.get()
        
        error_message = self.validate_registration(username, password, password_reentry)
        if error_message:
            self.reg_status.config(text = error_message)
            return
                   
        registration_status, error_message = register_user(username, password)
        if registration_status:
            self.reg_status.config(text = error_message)
            self.clear_form()
            self.master.switch_frame(login_frame)
        else:
            self.reg_status.config(text = error_message)
            
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
            
    def clear_form(self):
        self.username_reg_entry.delete(0, tk.END)
        self.password_reg_entry.delete(0, tk.END)
        self.password_reg_reentry.delete(0, tk.END)
                        

class login_frame (ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
            
        ttk.Label(self, text = "Welcome to DCM User Interface for Pacemaker").grid(row=0, column=0, pady=10, padx=(0,20), sticky="w")
        ttk.Label(self, text = "Username").grid(row=1, column=0,columnspan=2, pady=10)
        ttk.Label(self, text = "Password").grid(row=3, column=0, columnspan=2,pady=10)
        
        language_menu = tk.Menu(self, tearoff=0) 
        languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]

        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: change_language(l))
        
        self.login_button = ttk.Button(self, text = "Login", command = self.login_user)
        self.login_button.grid(row=5, column=0, columnspan=1, pady=20)
        
        self.register_button = ttk.Button(self, text = "Register", command = lambda: master.switch_frame(registration_frame))
        self.register_button.grid(row=5, column=1, columnspan=1, pady=20)
        
        self.language_button = ttk.Button(self, text = "Login", command = self.bind("<Button-1>", language_menu))
        self.language_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")
    
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=2, column=0, columnspan=2,pady=10)
        
        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(row=4, column=0, columnspan=2,pady=10)
        
    def change_language(language):
        print(f"Langauge selected: {language}")

    def show_language_menu(event):
        language_menu.post(event.x_root, event.y_root)
    
    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if verify_user(username, password):
            messagebox.showinfo("Success", "Login successful! [PLACEHOLDER]")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Invalid username or password![PLACEHOLER]")
            
    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
            
if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()