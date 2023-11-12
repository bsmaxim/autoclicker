from typing import Literal
from pynput import mouse, keyboard
from pynput.keyboard import Key
import pyautogui
import threading
from enum import Enum

class WHICH_INPUT(Enum):
    NONE = 0
    MOUSE = 1
    KEYBOARD = 2


class AutoClicker:
    def __init__(self) -> None:
        self.clicking = False
        self.stop_event = threading.Event()
        
        self.quit_key = keyboard.Key.end
        self.input_key = None
        self.which_input = WHICH_INPUT.NONE
        # self._pause_time = 0
        
        self._toggle_key = None
        
        self.toggle_key = keyboard.Key.insert
        self.pause_time = 0.1
    
    @property
    def pause_time(self):
        return self._pause_time
    
    @pause_time.setter
    def pause_time(self, new_time):
        if isinstance(new_time, (int, float)):
            self._pause_time = new_time
            pyautogui.PAUSE = new_time
        else:
            raise ValueError("Pause time must be an int or float.")
    
    
    @property
    def toggle_key(self):
        return self._toggle_key
    
    @toggle_key.setter
    def toggle_key(self, new_key: Key):
        if isinstance(new_key, Key):
            self._toggle_key = new_key
        else:
            raise ValueError("Toggle key must be an Key.")

    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse button {button} clicked at ({x}, {y})")
            self.input_key = button

    def autoclick(self):
        while self.clicking and not self.stop_event.is_set():
            x, y = pyautogui.position()
            if self.input_key == mouse.Button.left:
                pyautogui.click()
            elif self.input_key == mouse.Button.right:
                pyautogui.rightClick(x, y)
            elif self.input_key == mouse.Button.middle:
                pyautogui.middleClick(x, y)

    def on_keyboard_press(self, key):
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
            self.stop()
    
    
    def make_press(self, key):
        pass

    def start(self, console_log=False):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_press)
        
        
        if console_log:
            print(f"Кнопка кликера: {self.toggle_key}")
            print(f"Кнопка выхода: {self.quit_key}")
        
        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.mouse_listener.join()
        self.keyboard_listener.join()
    
    
    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

if __name__ == "__main__":
    ac = AutoClicker()
    ac.start(console_log=True)
