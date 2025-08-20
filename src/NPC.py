from Conversation import Conversation
from LLM import LLM
import textwrap

class NPC:
    """Represents a non-player character (NPC) in the game."""

    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality

    def get_response_text(self, conversation: Conversation) -> str:
        """Generates a response from the NPC based on the conversation history and mission parameters."""
        return LLM.model.invoke(
            textwrap.dedent(
                f"""
                INSTRUCTION:
                You are roleplaying as an NPC in a spy-themed game.
                Your task is to have a natural conversation with the player.

                Stay in character based on the NPC's name, personality, and
                current environment. Speak casually and naturally, as though
                you're just having a normal conversation.

                Do not act overly suspicious unless the player says something
                that feels very unnatural.

                Keep responses to 1-3 sentences maximum, so the flow feels like
                a realistic dialogue.

                Include only the dialogue text in your response, not the NPC
                name or any other metadata.

                NPC PROFILE:
                - Name: {self.name}
                - Personality: {self.personality}.
                - Environment: {conversation.get_mission().environment}.

                CONVERSATION HISTORY:
                {conversation.get_history()}
                """
            ).strip()
        ).content