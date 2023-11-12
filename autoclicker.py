from typing import Literal
from pynput import mouse, keyboard
import pyautogui
import threading


class AutoClicker:
    def __init__(self) -> None:
        self.mouse_input = None
        self.clicking = False
        self.stop_event = threading.Event()
        
        self.quit_key = keyboard.Key.end
        self.toggle_key = keyboard.Key.insert
        self.pause_time = 0.01
        
        self.change_toggle_key(keyboard.Key.insert)
        self.change_pause_time(self.pause_time)

        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

    def on_click(self, x, y, button, pressed):
        global mouse_input, clicking
        if pressed:
            print(f"Mouse button {button} clicked at ({x}, {y})")
            mouse_input = button

    def autoclick(self):
        while self.clicking and not self.stop_event.is_set():
            x, y = pyautogui.position()
            if mouse_input == mouse.Button.left:
                pyautogui.click()
            elif mouse_input == mouse.Button.right:
                pyautogui.rightClick(x, y)
            elif mouse_input == mouse.Button.middle:
                pyautogui.middleClick(x, y)

    def on_press(self, key):
        if key == self.toggle_key:
            self.clicking = not self.clicking
            if self.clicking:
                # Start autoclicking
                self.stop_event.clear()
                self.autoclick_thread = threading.Thread(target=self.autoclick)
                self.autoclick_thread.start()
            else:
                # Stop autoclicking
                self.stop_event.set()
        elif key == self.quit_key:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

    def change_toggle_key(self, new_key: Literal):
        self.toggle_key = new_key
        print(f"Changed toggle key to: {self.toggle_key}")

    def change_pause_time(self, time: float):
        self.pause_time = time
        pyautogui.PAUSE = self.pause_time

    def start(self):
        print("aboba")
        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.mouse_listener.join()
        self.keyboard_listener.join()

if __name__ == "__main__":
    ac = AutoClicker()
    ac.start()
