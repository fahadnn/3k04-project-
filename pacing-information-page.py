import tkinter as tk
from tkinter import ttk

class PacemakerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('700x600')
        self.root.title('Pacemaker Pacing Information')
        
        self.selected_button = None
        self.last_bg = None
        # Data for parameter list
        self.parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 'Atrial Pulse Width', 
                           'Ventricular Amplitude', 'Ventricular Pulse Width', 'VRP', 'ARP']
        self.values = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        
        self.create_widgets()
        self.create_table()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="DCM Communication with Pacemaker:").place(x=250, y=80)
        tk.Label(self.root, text="Pacing Mode").place(x=30, y=180)
        tk.Label(self.root, text="Graph of Pacing Mode").place(x=30, y=280)
        tk.Label(self.root, text="Programmable Parameters").place(x=30, y=380)

        # Buttons
        self.create_button('AOO', 150, 180)
        self.create_button('VOO', 180, 180)
        self.create_button('AAI', 210, 180)
        self.create_button('VVI', 240, 180)

    def create_button(self, text, x, y):
        button = tk.Button(
            self.root,
            text=text,
            fg='black',
            activebackground='#B7E3F9',
            activeforeground='black',
            highlightthickness=0,
            relief='flat',
        )
        button.place(x=x, y=y)
        button.config(command=lambda btn=button: self.change_selected_button(btn))

    def abc(self):
        print("Pacing Mode Changed")

    def change_selected_button(self, button):
        self.abc()
        if self.selected_button is not None:
            self.selected_button.config(bg=self.last_bg)
        self.selected_button = button
        self.last_bg = button.cget("bg")
        button.config(bg="orange")

    def create_table(self):
        # Create a Frame for the table
        table_frame = tk.Frame(self.root)
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
    root = tk.Tk()
    app = PacemakerApp(root)
    root.mainloop()