from Environment import Environment

class Mission:
    """Defines the mission parameters for the game."""

    def __init__(self, objective: str, environment: Environment):
        self.objective = objective
        self.environment = environment
