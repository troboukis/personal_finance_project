import tkinter as tk

def update_label():
    var.set("Hello, Tkinter!")  # Update the StringVar value

root = tk.Tk()

# Create a StringVar
var = tk.StringVar()

# Set an initial value
var.set("Click the button to change this text.")

# Create a label and link it to the StringVar
label = tk.Label(root, textvariable=var)
label.pack()

# Create a button that when clicked will update the StringVar
button = tk.Button(root, text="Update", command=update_label)
button.pack()

root.mainloop()
