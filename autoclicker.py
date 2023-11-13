import threading
from enum import Enum
from pynput import mouse
from pynput.keyboard import Key
import pyautogui
from actions import Action

from keymanager import KeyManager, KeySettings
from listeners import Listeners


class WhichInput(Enum):
    NONE = 0
    MOUSE = 1
    KEYBOARD = 2


class AutoClicker:
    def __init__(self) -> None:
        self.autoclick_thread = None
        self.clicking = False
        self.stop_event = threading.Event()

        self.input_key = None
        self.which_input = WhichInput.NONE

        self.pause_time = 0.1

        self.listeners = Listeners(self.on_click, self.on_keyboard_press)
        self.key_manager = KeyManager(on_quit=self.quit, on_toggle=self.toggle)

        self._pause_time = 0
        self.toggle_key_settings = KeySettings(
            self.key_manager, Action.TOGGLE, Key.insert, "Кнопка кликера"
        )
        self.quit_key_settings = KeySettings(
            self.key_manager, Action.QUIT, Key.end, "Кнопка выхода"
        )

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
        if self.key_manager.has_key(key):
            self.key_manager.execute_key(key)

    def toggle(self):
        self.clicking = not self.clicking

        if self.clicking:
            # Start autoclicking
            self.stop_event.clear()
            self.autoclick_thread = threading.Thread(target=self.autoclick)
            self.autoclick_thread.start()
        else:
            # Stop autoclicking
            self.stop_event.set()

    def quit(self):
        self.stop()

    def make_press(self, key):
        pass

    def start(self, console_log=False):
        if console_log:
            print(
                f"{self.toggle_key_settings.display_name}: {self.toggle_key_settings.key}"
            )
        print(f"{self.quit_key_settings.display_name}: {self.quit_key_settings.key}")

        self.listeners.start()

    def stop(self):
        self.listeners.stop()


if __name__ == "__main__":
    ac = AutoClicker()
    ac.start(console_log=True)
