from pynput import mouse, keyboard
import pyautogui
import threading


mouse_input = None
clicking = False
quit_key = keyboard.Key.end
stop_event = threading.Event()


def on_click(x, y, button, pressed):
    global mouse_input, clicking
    if pressed:
        print(f"Mouse button {button} clicked at ({x}, {y})")
        mouse_input = button


def autoclick():
    while clicking and not stop_event.is_set():
        x, y = pyautogui.position()
        if mouse_input == mouse.Button.left:
            pyautogui.click()
        elif mouse_input == mouse.Button.right:
            pyautogui.rightClick(x, y)
        elif mouse_input == mouse.Button.middle:
            pyautogui.middleClick(x, y)


def on_press(key):
    global clicking
    if key == keyboard.Key.insert:
        clicking = not clicking
        if clicking:
            # Start autoclicking
            global autoclick_thread
            stop_event.clear()
            autoclick_thread = threading.Thread(target=autoclick)
            autoclick_thread.start()
        else:
            # Stop autoclicking
            stop_event.set()
    elif key == quit_key:
        # Quit the program
        mouse_listener.stop()
        keyboard_listener.stop()
        

pyautogui.PAUSE = 0.01

# Create listeners for mouse events and key presses
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

# Start the listeners
mouse_listener.start()
keyboard_listener.start()

# Wait for the listeners to stop (you can use any other method to keep your program running)
mouse_listener.join()
keyboard_listener.join()
