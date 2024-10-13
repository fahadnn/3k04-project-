import tkinter as tk                        # import tkinter module 
import tksheet                              #import tksheet for charts////
from tkinter import *                       #import tkinter library  
# Following will import tkinter.ttk module and 
# automatically override all the widgets 
# which are present in tkinter module. 
from tkinter.ttk import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create Object root (main window frame)
root = Tk() 

selected_button = None
last_bg = None
#prints out when pacing mode/button selection changes
def abc():
    print("Pacing Mode Changed")
    
def change_selected_button(button):
    abc()
    global selected_button, last_bg
    if selected_button is not None:
        selected_button.config(bg=last_bg)
    selected_button = button
    last_bg = button.cget("bg")
    button.config(bg="orange")

def ResponsiveWidget(widget, *args, **kwargs):
    bindings = {'<Enter>': {'state': 'active'},
                '<Leave>': {'state': 'normal'}}

    w = widget(*args, **kwargs)

    for (k, v) in bindings.items():
        w.bind(k, lambda e, kwarg=v: e.widget.config(**kwarg))

    return w

# Initialize tkinter window with dimensions 100x100             
root.geometry('700x600')                    #size of window
root.title('Pacemaker Pacing Information')  #title of window

#label1
entry1Label = tk.Label(root, text="DCM Communication with Pacemaker: ")
entry1Label.place(x=250, y = 80)  
#label2
entry2Label = tk.Label(root, text="Pacing Mode ")
entry2Label.place(x=30, y = 180)
#label3
entry3Label = tk.Label(root, text="Graph of Pacing Mode ")
entry3Label.place(x=30, y = 280)
#label4
entry4Label = tk.Label(root, text="Programmable Parameters ")
entry4Label.place(x=30, y = 380)

#create button that highlights when pressed for AOO
button1 = ResponsiveWidget(
    tk.Button,
    root,
    text='AOO',
    fg='black',
    activebackground='#B7E3F9',
    activeforeground='black',
    highlightthickness=0,
    relief='flat',
    )
button1.place(x=150, y=180)
button1.config(command=lambda button=button1: change_selected_button(button))

#create button that highlights when pressed for VOO
button2 = ResponsiveWidget(
    tk.Button,
    root,
    text='VOO',
    fg='black',
    activebackground='#B7E3F9',
    activeforeground='black',
    highlightthickness=0,
    relief='flat'
    )   #abc is not calling
button2.place(x=180, y=180)
button2.config(command=lambda button=button2: change_selected_button(button))

#create button that highlights when pressed for AAI
button3 = ResponsiveWidget(
    tk.Button,
    root,
    text='AAI',
    fg='black',
    activebackground='#B7E3F9',
    activeforeground='black',
    highlightthickness=0,
    relief='flat'
    )  
button3.place(x=210, y=180)
button3.config(command=lambda button=button3: change_selected_button(button))

#create button that highlights when pressed for VVI
button4 = ResponsiveWidget(
    tk.Button,
    root,
    text='VVI',
    fg='black',
    activebackground='#B7E3F9',
    activeforeground='black',
    highlightthickness=0,
    relief='flat'
    )   
button4.place(x=240, y=180)
button4.config(command=lambda button=button4: change_selected_button(button))

# Create the main application window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Variable Chart Example")
        self.geometry("600x400")
        
        self.create_chart()

    def create_chart(self):
        # Create a figure for the chart
        fig, ax = plt.subplots(figsize=(5, 4))

        # Create the bar chart
        ax.bar(variables, values, color='skyblue')
        
        # Set labels and title
        ax.set_xlabel('Variables')
        ax.set_ylabel('Values')
        ax.set_title('Bar Chart of Variables')

        # Create a canvas to display the figure
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

mainloop()
