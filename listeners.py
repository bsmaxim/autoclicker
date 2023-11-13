from pynput import mouse, keyboard


class Listeners:
    def __init__(self, on_click, on_press) -> None:
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.keyboard_listener = keyboard.Listener(on_press=on_press)

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.mouse_listener.join()
        self.keyboard_listener.join()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
