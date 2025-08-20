from Conversation import Conversation
from Mission import Mission
from NPCs import NPCs
from NPC import NPC
from LLM import LLM
import random

class Game:
    """Manages the overall game state, including missions, NPCs, and the game loop."""
    def initialize(self, mission_count: int = 1, npc_count: int = 1):
        """Initializes the game by generating a specified number of missions and NPCs."""
        self.missions = [self.__generate_mission() for _ in range(mission_count)]
        self.npcs = random.sample(NPCs.LIST, k=npc_count)
    
    def __generate_mission(self, difficulty: int = 1) -> Mission:
        """Generates a mission with predefined objectives and environment."""
        # TODO: implement random mission generation based on difficulty
        return Mission(
            objective="Call for reinforcements",
            environment="A bustling city park during a weekend festival",
            forbidden_words=["help", "assist", "support", "backup", "emergency"]
        )
    
    def play_mission(self, mission: Mission = None, npc: NPC = None):
        if mission not in self.missions:
            if mission is not None:
                print("Invalid mission. Choosing a random mission instead.")
            mission = random.choice(self.missions)

        if npc not in self.npcs:
            if npc is not None:
                print("Invalid NPC. Choosing a random NPC instead.")
            npc = random.choice(self.npcs)

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

        result = self.__evaluate(ally_confidence, enemy_suspicion)
        print(f"Mission Result: {result}")

    def __evaluate(self, ally_confidence: float, enemy_suspicion: float):
        if ally_confidence >= 0.8 and enemy_suspicion <= 0.4:
            return "PASS"
        elif ally_confidence >= 0.8 and enemy_suspicion > 0.4:
            return "PARTIAL SUCCESS"
        else:
            return "FAIL"