from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()

class Ally_Response(BaseModel):
    """Response from the ally character."""
    confidence: float = Field(description="Confidence rating of the ally's interpretation", ge=0.0, le=1.0)

class Enemy_Response(BaseModel):
    """Response from the enemy character."""
    suspicion: float = Field(description="Suspicion level of the enemy's interpretation", ge=0.0, le=1.0)

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.5)

structured_ally_model = model.with_structured_output(Ally_Response)

structured_enemy_model = model.with_structured_output(Enemy_Response)

npc_prompt_template = PromptTemplate.from_template(
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

CONTEXT:
{conversation_history}
"""
)

ally_prompt_template = PromptTemplate.from_template(
"""
INSTRUCTION:

You are the player's ally, listening secretly to the conversation.
Your goal: figure out the hidden message based on the player's messages.

DO NOT break cover - your output is just an internal note to the game master.

Hidden message target: {hidden_message}

Rate your confidence from 0.0 to 1.0 that you have interpreted correctly.

CONTEXT:
{conversation_history}
"""
)

enemy_prompt_template = PromptTemplate.from_template(
"""
INSTRUCTION:

You are an enemy agent listening in to the player's conversation.
You are trying to detect if the player is conveying a hidden message.

Rate your suspicion from 0.0 (no suspicion) to 1.0 (fully certain).

CONTEXT:
{conversation_history}
"""
)

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

    npc_response = model.invoke(npc_prompt).content

    print(f"NPC: {npc_response}")
    conversation_history += f"NPC: {npc_response}\n"

    player_input = input("You: ")
    conversation_history += f"Player: {player_input}\n"

    ally_prompt = ally_prompt_template.invoke(
        {
            "hidden_message": mission["hidden_message"],
            "conversation_history": conversation_history
        }
    )

    ally_confidence = structured_ally_model.invoke(ally_prompt).model_dump().get("confidence")

    print(f"Ally confidence: {ally_confidence}")

    enemy_prompt = enemy_prompt_template.invoke(
        {
            "conversation_history": conversation_history
        }
    )

    enemy_suspicion = structured_enemy_model.invoke(enemy_prompt).model_dump().get("suspicion")

    print(f"Enemy suspicion: {enemy_suspicion}")

result = evaluate(ally_confidence, enemy_suspicion)
print(f"Mission Result: {result}")