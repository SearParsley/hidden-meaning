from Mission import Mission

class Conversation:
    """Manages the conversation history between the player and an NPC."""

    def __init__(self, mission: Mission):
        self._mission = mission
        self._history = list(tuple())

    def add_turn(self, speaker: str, text: str):
        """Adds a turn to the conversation history."""
        self._history.append((speaker, text))

    def get_history(self) -> str:
        """Returns the conversation history as a string."""
        return "\n".join(f"{speaker}: {text}" for speaker, text in self._history)

    def get_mission(self) -> Mission:
        return self._mission