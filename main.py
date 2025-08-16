from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
import textwrap

load_dotenv()


class LLM:
    """Encapsulates the language model and related structured output models and prompts."""

    class Ally_Response(BaseModel):
        """Response from the ally character."""
        confidence: float = Field(description="Confidence rating of the ally's interpretation", ge=0.0, le=1.0)

    class Enemy_Response(BaseModel):
        """Response from the enemy character."""
        suspicion: float = Field(description="Suspicion level of the enemy's interpretation", ge=0.0, le=1.0)

    _ally_prompt_template = PromptTemplate.from_template(textwrap.dedent(
        """
        INSTRUCTION:

        You are the player's ally, listening secretly to the conversation.
        Your goal: figure out the hidden message based on the player's messages.

        DO NOT break cover - your output is just an internal note to the game master.

        Hidden message target: {hidden_message}

        Rate your confidence from 0.0 to 1.0 that you have interpreted correctly.

        CONTEXT (may be empty):
        {conversation_history}
        """
        ).strip())
    
    _enemy_prompt_template = PromptTemplate.from_template(textwrap.dedent(
        """
        INSTRUCTION:

        You are an enemy agent listening in to the player's conversation.
        You are trying to detect if the player is conveying a hidden message.

        Rate your suspicion from 0.0 (no suspicion) to 1.0 (fully certain).

        CONTEXT (may be empty):
        {conversation_history}
        """
        ).strip())

    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.5)
    _structured_ally_model = model.with_structured_output(Ally_Response)
    _structured_enemy_model = model.with_structured_output(Enemy_Response)

    @staticmethod
    def get_ally_confidence(conversation_history: str, hidden_message: str):
        ally_prompt = LLM._ally_prompt_template.invoke(
            {
                "hidden_message": hidden_message,
                "conversation_history": conversation_history
            }
        )
        return LLM._structured_ally_model.invoke(ally_prompt).model_dump().get("confidence")

    @staticmethod
    def get_enemy_suspicion(conversation_history: str):
        enemy_prompt = LLM._enemy_prompt_template.invoke(
            {
                "conversation_history": conversation_history
            }
        )
        return LLM._structured_enemy_model.invoke(enemy_prompt).model_dump().get("suspicion")



npc_prompt_template = PromptTemplate.from_template(textwrap.dedent(
    """
    INSTRUCTION:

    You are an NPC in a spy conversation game.
    Personality: {npc_personality}.
    Cover Topic: {cover_topic}.
    Avoid talking about espionage or danger unless suspicious.

    If the player uses forbidden words: {forbidden_words},
    react with mild suspicion.

    You do not know the hidden message. Keep conversation natural but probe if the player sounds odd.
    Respond naturally as the NPC would.

    CONTEXT (may be empty):
    {conversation_history}
    """
    ).strip())



conversation_history = ""
mission = {
    "npc_personality": "Polite but cautious, easily distracted",
    "cover_topic": "Seasonal activities",
    "forbidden_words": ["spy", "secret", "mission", "code"],
    "hidden_message": "Meet at the park at 9:00pm."
}

def evaluate(ally_confidence: float, enemy_suspicion: float):
    if ally_confidence >= 0.8 and enemy_suspicion <= 0.4:
        return "PASS"
    elif ally_confidence >= 0.8 and enemy_suspicion > 0.4:
        return "PARTIAL SUCCESS"
    else:
        return "FAIL"

ally_confidence: float = 0.0
enemy_suspicion: float = 0.0

for turn in range(5):

    npc_prompt = npc_prompt_template.invoke(
        {
            "npc_personality": mission["npc_personality"],
            "cover_topic": mission["cover_topic"],
            "forbidden_words": mission["forbidden_words"],
            "conversation_history": conversation_history
        }
    )

    npc_response = LLM.model.invoke(npc_prompt).content

    print(f"NPC: {npc_response}")
    conversation_history += f"NPC: {npc_response}\n"

    player_input = input("You: ")
    conversation_history += f"Player: {player_input}\n"

    ally_confidence = LLM.get_ally_confidence(conversation_history, mission["hidden_message"])

    print(f"Ally confidence: {ally_confidence}")

    enemy_suspicion = LLM.get_enemy_suspicion(conversation_history)

    print(f"Enemy suspicion: {enemy_suspicion}")

result = evaluate(ally_confidence, enemy_suspicion)
print(f"Mission Result: {result}")