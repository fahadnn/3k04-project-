import tkinter


"BUTTONS AND LABELS"

""" def hello():
    print("Hello, motherfucker")
    
    
if __name__ == '__main__':
    window=tkinter.Tk()
    window.title("Tkinter First App")
    window.geometry('600x400')
    
    frame = tkinter.Frame(window)
    frame.pack()
    
    label = tkinter.Label(frame, text='Hello world')
    label.pack()
    button = tkinter.Button(frame, text='Hello world', command=hello)
    button.pack()
    
    window.mainloop() """
    
"======================================================================================================================"

"TEXT ENTRIES"


""" if __name__ == '__main__':
    window=tkinter.Tk()
    window.title("Tkinter First App")
    window.geometry('600x400')
    
    
    label = tkinter.Label(window, text="Hello world", bg="red", fg="yellow")
    label.pack()
    
    textentry = tkinter.Entry(window)
    textentry.pack()
    
    
    window.mainloop() """
    

"USING PACK FOR ALIGNMENT"

""" def computePrice():
    totalPrice = int(priceperitem_entry.get())*int(numberofitems_entry.get())
    totalPrice_entry.insert(0,string=str(totalPrice))
    
window = tkinter.Tk()

priceperitem_label = tkinter.Label(window, text="Price per item")
priceperitem_entry = tkinter.Entry(window)
numberofitems_label = tkinter.Label(window, text="Number of items")
numberofitems_entry = tkinter.Entry(window)
totalPrice_label = tkinter.Label(window, text="Total price:")
totalPrice_entry = tkinter.Entry(window)
calculate_button = tkinter.Button(window, text="Calculate total", command=computePrice)

priceperitem_label.pack()
priceperitem_entry.pack()
numberofitems_label.pack()
numberofitems_entry.pack()
totalPrice_label.pack()
totalPrice_entry.pack()
calculate_button.pack(fill='x') 

window.mainloop() """

window = tkinter.Tk()
window.title("Login form")
window.geometry('340x440')
window.configure(bg='white')


login_label = tkinter.Label(window, text="Login")


#Creating widgets

username_label = tkinter.Label(window, text="Username")
username_entry = tkinter.Entry(window)
password_label = tkinter.Label(window, text="Password")
password_entry = tkinter.Entry(window)
login_button = tkinter.Button(window, text="Login")

#Placing widgets on the screen

login_label.grid(row=0, column=0,columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)

window.mainloop()
