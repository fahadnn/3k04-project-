import tkinter as tk
from tkinter import ttk

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker")
        self.geometry ("700x600")
        
        self.currentFrame = None
        self.switchFrame(registrationFrame)
    
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
        
        self.registerButton = ttk.Button(self, text = "Register", command = None)
        self.registerButton.pack()
        

if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()