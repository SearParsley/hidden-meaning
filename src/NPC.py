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
        env = conversation.get_mission().environment
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

                ENVIRONMENT RULES:
                - Location: {env.name}
                - Description: {env.description}
                - Message Length Limit: {env.message_length_limit} words
                - Forbidden Words: {', '.join(env.forbidden_words)}
                - Noise Level: {int(env.noise_chance * 100)}% chance of message loss
                - Other Rules: {', '.join(f"{k}: {v}" for k, v in env.special_rules.items()) if env.special_rules else "None"}

                If the player:
                - Uses forbidden words: React with subtle concern or confusion
                - Exceeds word limit: Show mild impatience or distraction
                - Uses suspicious phrases: Gradually become more guarded
                
                Keep your responses under {env.message_length_limit} words to match
                the environment's restrictions.

                NPC PROFILE:
                - Name: {self.name}
                - Personality: {self.personality}

                CONVERSATION HISTORY:
                {conversation.get_history()}
                """
            ).strip()
        ).content