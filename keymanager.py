from typing import Callable, Dict, Union
from pynput.keyboard import Key

from actions import Action



class KeySettings:
    # pylint: disable=too-few-public-methods
    def __init__(self, key_manager, action, key, display_name):
        self.key_manager = key_manager
        self.action = action
        self.display_name = display_name
        self.key = key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        if isinstance(new_key, Key):
            self._key = new_key
            self.key_manager.change_key(self.action, new_key)
        else:
            raise ValueError(
                f"{self.action.name.lower().capitalize()} key must be an instance of Key."
            )


class KeyManager:
    def __init__(self, on_toggle: Callable, on_quit: Callable) -> None:
        # Mapping from Action to Key (or str)
        self.action_to_key_map: Dict[Action, Union[Key, str]] = {}

        # Mapping from Key (or str) to Action
        self.key_to_action_map: Dict[Union[Key, str], Action] = {}

        self.init_keys()

        self.on_toggle = on_toggle
        self.on_quit = on_quit

    def init_keys(self):
        self.change_key(Action.TOGGLE, Key.insert)
        self.change_key(Action.QUIT, Key.end)

    def has_key(self, key: Union[Key, str]) -> bool:
        return key in self.key_to_action_map

    def change_key(self, action: Action, key: Union[Key, str]):
        """Change the key associated with the specified action."""
        if action in self.action_to_key_map:
            # Retrieve the current key associated with the action
            action_key = self.action_to_key_map[action]

            # Remove the current key from the key_to_action_map
            del self.key_to_action_map[action_key]

        # Update both mappings with the new key
        self.key_to_action_map[key] = action
        self.action_to_key_map[action] = key

    def execute_key(self, key: Union[Key, str]):
        """Execute the action associated with the specified key."""
        try:
            action = self.key_to_action_map[key]
            match action:
                case Action.TOGGLE:
                    self.on_toggle()
                case Action.QUIT:
                    self.on_quit()
                case _:
                    print(f"Unhandled action: {action}")
        except KeyError:
            print(f"No action associated with the key: {key}")
