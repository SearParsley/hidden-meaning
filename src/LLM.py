from Conversation import Conversation
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import textwrap

class Ally_Response(BaseModel):
    """Response from the ally character."""
    confidence: float = Field(description="Confidence rating of the ally's interpretation", ge=0.0, le=1.0)

class Enemy_Response(BaseModel):
    """Response from the enemy character."""
    suspicion_level: float = Field(description="Suspicion level of the enemy's interpretation", ge=0.0, le=1.0)
    suspicious_phrases: list[str] = Field(description="Suspicious words or phrases identified by the enemy")

class LLM:
    """Encapsulates the language model and related structured output models and prompts."""

    load_dotenv()

    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0.5)
    
    __structured_ally_model = model.with_structured_output(Ally_Response)
    __structured_enemy_model = model.with_structured_output(Enemy_Response)

    def invoke_third_parties(self, conversation: Conversation) -> dict[str, float | list[str]]:
        """Invoke third-party assessments of the conversation. Returns a dictionary with keys:
        'ally_confidence' (float), 'enemy_suspicion' (float), and 'suspicious_phrases' (list of strings)."""
        ally_response_info = self.__invoke_ally(conversation).model_dump()
        enemy_response_info = self.__invoke_enemy(conversation).model_dump()
        return {
            "ally_confidence": ally_response_info.get("confidence"),
            "enemy_suspicion": enemy_response_info.get("suspicion_level"),
            "suspicious_phrases": enemy_response_info.get("suspicious_phrases")
        }

    def __invoke_ally(self, conversation: Conversation) -> Ally_Response:
       return self.__structured_ally_model.invoke(
            textwrap.dedent(
                f"""
                INSTRUCTIONS:
                You are the player's ally. Your task is to analyze the recent
                conversation between the player and an NPC in order to detect
                whether the player has successfully embedded a hidden message.

                Carefully read the conversation for any words or phrases that
                appear to match or encode the mission objective.

                The player must embed the message in a way that seems natural
                in context. Look for subtle or indirect phrasing that might
                hide the objective.

                Rate your confidence in your interpretation from 0.0 to 1.0.

                MISSION OBJECTIVE:
                {conversation.get_mission().objective}

                CONVERSATION HISTORY:
                {conversation.get_history()}
                """
            ).strip()
        )

    def __invoke_enemy(self, conversation: Conversation) -> Enemy_Response:
        return self.__structured_enemy_model.invoke(
            textwrap.dedent(
                f"""
                INSTRUCTIONS:
                You are a hostile intelligence officer secretly listening to
                a conversation between the player and an NPC. Your job is to
                detect whether the player is trying to convey a hidden message.

                Scrutinize the conversation for words, phrases, or patterns
                that feel unnatural or suspicious.

                Pay attention to unusual word choice, repeated terms, or topics
                that may seem forced into casual conversation.

                Rate your suspicion from 0.0 (no suspicion) to 1.0 (fully certain).

                MISSION OBJECTIVE (for reference only):
                {conversation.get_mission().objective}

                CONVERSATION HISTORY:
                {conversation.get_history()}
                """
            ).strip()
        )