import tkinter as tk

def on_button_click():
    print("Button clicked!")

# Create the main window
window = tk.Tk()
window.title("GUI Menu")

# Set the width and height of the window
window.geometry("200x100")  # You can adjust the width and height as needed

# Make the window non-resizable
window.resizable(False, False)

# Create a button
button = tk.Button(window, text="Click me", command=on_button_click)
button.pack(pady=20)

# Start the main loop
window.mainloop()
