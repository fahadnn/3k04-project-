# import tkinter and tksheet package
import tkinter as tk
import tksheet
#import tkinter library
from tkinter import *        
# Following will import tkinter.ttk module and 
# automatically override all the widgets 
# which are present in tkinter module. 
from tkinter.ttk import *
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

#entry value 1
entry1Label = tk.Label(root, text="DCM Communication with Pacemaker: ")
entry1Label.place(x=250, y = 80)  
#entry for value2
entry2Label = tk.Label(root, text="Pacing Mode ")
entry2Label.place(x=30, y = 180)
#entry for value3
entry2Label = tk.Label(root, text="Graph of Pacing Mode ")
entry2Label.place(x=30, y = 280)
#entry for value3
entry2Label = tk.Label(root, text="Programmable Parameters ")
entry2Label.place(x=30, y = 380)

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

sheet = tksheet.Sheet(root)
sheet.grid()
sheet.set_sheet_data([[f"{ri+cj}" for cj in range(4)] for ri in range(1)])
# table enable choices listed below:
sheet.enable_bindings(("single_select",
                       "row_select",
                       "column_width_resize",
                       "arrowkeys",
                       "right_click_popup_menu",
                       "rc_select",
                       "rc_insert_row",
                       "rc_delete_row",
                       "copy",
                       "cut",
                       "paste",
                       "delete",
                       "undo",
                       "edit_cell"))


''' highlight default text in textbox upon clicking it for username field
def in_widget(event):
    event.widget.select_range(0, 'end')

entry11 = Entry(root)
entry11.insert(0, 'sample')
entry11.pack()
entry11.bind('<FocusIn>', in_widget) '''




mainloop()