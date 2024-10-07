import tkinter as tk
from tkinter import ttk

class pacemaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ("Pacemaker")
        self.geometry ("700x600")
        
        self.currentFrame = None
    
    def switchFrame(self, frame):
        if self.currentFrame is not None:
            self.currentFrame.destroy()
            
        self.currentFrame = frame(self)
        self.currentFrame.pack(fill = "both", expand = True)
                

if __name__ == "__main__":
    app = pacemaker()
    app.mainloop()