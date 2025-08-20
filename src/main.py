from Conversation import Conversation
from Mission import Mission
from NPC import NPC
from LLM import LLM

def evaluate(ally_confidence: float, enemy_suspicion: float):
    if ally_confidence >= 0.8 and enemy_suspicion <= 0.4:
        return "PASS"
    elif ally_confidence >= 0.8 and enemy_suspicion > 0.4:
        return "PARTIAL SUCCESS"
    else:
        return "FAIL"

def main():
    mission = Mission(
        objective="Call for reinforcements",
        environment="A bustling city park during a weekend festival",
        forbidden_words=["help", "assist", "support", "backup", "emergency"]
    )

    npc = NPC(
        name="Clara",
        personality="Friendly and talkative, but a little nosy"
    )

    conversation = Conversation(mission)

    print(f"Environment: {mission.environment}")
    print(f"Mission Objective: {mission.objective}")
    print(f"NPC: {npc.name} - {npc.personality}")

    for turn in range(5):
        player_input = input("You: ")
        conversation.add_turn("Player", player_input)

        npc_response = npc.get_response_text(conversation)

        print(f"{npc.name}: {npc_response}")
        conversation.add_turn(npc.name, npc_response)

        third_party_results = LLM.invoke_third_parties(conversation)
        ally_confidence = third_party_results.get("ally_confidence", 0.0)
        enemy_suspicion = third_party_results.get("enemy_suspicion", 0.0)
        suspicious_phrases = third_party_results.get("suspicious_phrases", [])

        print(f"Ally confidence: {ally_confidence}")
        print(f"Enemy suspicion: {enemy_suspicion}")
        print(f"Suspicious phrases: {suspicious_phrases}")

    result = evaluate(ally_confidence, enemy_suspicion)
    print(f"Mission Result: {result}")

if __name__=="__main__":
    main()