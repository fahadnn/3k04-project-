import tkinter as tk
from tkinter import ttk, messagebox
from userDB import createDB, registerUser

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker")
        self.geometry ("700x600")
        
        createDB()
        
        self.currentFrame = None
        self.switchFrame(loginFrame)
    
    def switchFrame(self, frame):
        if self.currentFrame is not None:
            self.currentFrame.destroy()
            
        self.currentFrame = frame(self)
        self.currentFrame.pack(fill = "both", expand = True)
                
class registrationFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text = "Registration").pack()
        
        ttk.Label(self, text = "Username").pack()
        self.usernameEntry = ttk.Entry(self)
        self.usernameEntry.pack()
        
        ttk.Label(self, text = "Password").pack()
        self.passwordEntry = ttk.Entry(self)
        self.passwordEntry.pack()
        
        ttk.Label(self, text = "Re-enter Password").pack()
        self.passwordReentry = ttk.Entry(self)
        self.passwordReentry.pack()
        
        self.registerButton = ttk.Button(self, text = "Register", command = self.registerUser)
        self.registerButton.pack()
        
    def registerUser(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        if registerUser(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Username already exists!")

class loginFrame (ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        
        def change_language(language):
            print(f"Langauge selected: {language}")

        def show_language_menu(event):
            language_menu.post(event.x_root, event.y_root)
        
        ttk.Label(self, text = "Welcome to DCM User Interface for Pacemaker").grid(row=0, column=0, pady=10, padx=(0,20), sticky="w")
        ttk.Label(self, text = "Username").grid(row=1, column=0,columnspan=2, pady=10)
        ttk.Label(self, text = "Password").grid(row=3, column=0, columnspan=2,pady=10)
        
        language_menu = tk.Menu(self, tearoff=0) 
        languages = ["English", "Danish", "Dutch", "French", "German", "Spanish", "Italian", "Swedish"]

        for lang in languages:
            language_menu.add_command(label=lang, command=lambda l=lang: change_language(l))
        
        self.login_button = ttk.Button(self, text = "Login", command = None)
        self.login_button.grid(row=5, column=0, columnspan=1, pady=20)
        
        self.register_button = ttk.Button(self, text = "Register", command = None)
        self.register_button.grid(row=5, column=1, columnspan=1, pady=20)
        
        self.language_button = ttk.Button(self, text = "Login", command = self.bind("<Button-1>", show_language_menu))
        self.language_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")
    
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=2, column=0, columnspan=2,pady=10)
        
        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(row=4, column=0, columnspan=2,pady=10)
        
        
        # def login_user(self):
        #     username = self.username_entry.get()
        #     password = self.password_entry.get()
            
        #     if login_user(username, password):
        #         messagebox.showinfo("Success", "Login successful!")
        #         self.clear_form()
        #     else:
        #         messagebox.showerror("Error", "Username already exists!")
            
        # def register_user(self):
        #     username = self.username_entry.get()
        #     password = self.password_entry.get()
            
        #     if register_user(username, password):
        #         messagebox.showinfo("Success", "Registration successful!")
        #         self.clear_form()
        #     else:
        #         messagebox.showerror("Error", "Username already exists!")
                

            


            
if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()