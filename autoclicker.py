import threading
from enum import Enum
from pynput import mouse
from pynput.keyboard import Key, KeyCode, Controller
import pyautogui
from actions import Action

from keymanager import KeyManager, KeySettings
from listeners import Listeners


keyboard = Controller()

class WhichInput(Enum):
    NONE = 0
    MOUSE = 1
    KEYBOARD = 2


class AutoClicker:
    def __init__(self) -> None:
        self.active = False

        self.autoclick_thread = None
        self.stop_event = threading.Event()

        self.input_key = None
        self.which_input = WhichInput.NONE

        self.listeners = Listeners(self.on_click, self.on_press)
        self.key_manager = KeyManager(on_quit=self.quit, on_toggle=self.toggle)

        self.pause_time = 0.1
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

    def autoclick(self):
        match self.which_input:
            case WhichInput.MOUSE:
                # x, y = pyautogui.position()
                while self.active:
                    match self.input_key:
                        case mouse.Button.left:
                            pyautogui.click()
                        case mouse.Button.right:
                            pyautogui.rightClick()
                        case mouse.Button.middle:
                            pyautogui.middleClick()
            case WhichInput.KEYBOARD:
                print(f"{type(self.input_key)} {self.input_key}")
                while self.active:
                    keyboard.press(self.input_key)
            case WhichInput.NONE:
                print("No key pressed")

    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse button {button} clicked at ({x}, {y})")
            self.input_key = button
            self.which_input = WhichInput.MOUSE

    def on_press(self, key: (Key | KeyCode | None)):
        if self.key_manager.has_key(key):
            self.key_manager.execute_key(key)
        else:
            self.input_key = key
            self.which_input = WhichInput.KEYBOARD
            print(f"{key} pressed")

    def toggle(self):
        self.active = not self.active

        if self.active:
            self.autoclick_thread = threading.Thread(target=self.autoclick)
            self.autoclick_thread.start()

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
