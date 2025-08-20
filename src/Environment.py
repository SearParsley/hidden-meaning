class Environment:
    def __init__(self, name, description, 
                 max_turns=None, 
                 forbidden_words=None, 
                 message_length_limit=None, 
                 cover_keywords=None, 
                 noise_chance=0.0, 
                 special_rules=None):
        """
        Represents a mission environment with certain gameplay restrictions.

        Args:
            name (str): Environment name.
            description (str): Short flavor description.
            max_turns (int): Max number of turns allowed.
            forbidden_words (list[str]): Words that trigger suspicion.
            message_length_limit (int): Max number of words per message.
            cover_keywords (list[str]): Keywords required to appear in a message.
            noise_chance (float): Chance (0.0-1.0) that a message is garbled/lost.
            special_rules (dict): Environment-specific constraints.
        """
        self.name = name
        self.description = description
        self.max_turns = max_turns
        self.forbidden_words = forbidden_words or []
        self.message_length_limit = message_length_limit
        self.cover_keywords = cover_keywords or []
        self.noise_chance = noise_chance
        self.special_rules = special_rules or {}

    def validate_message(self, message: str, turn: int) -> tuple[bool, str]:
        """
        Checks a message against environment restrictions.
        Returns (valid: bool, reason: str).
        """
        words = message.split()

        if self.max_turns is not None and turn > self.max_turns:
            return False, f"Exceeded maximum turns ({self.max_turns})."

        if self.message_length_limit and len(words) > self.message_length_limit:
            return False, f"Message too long (limit: {self.message_length_limit} words)."

        for fw in self.forbidden_words:
            if fw.lower() in message.lower():
                return False, f"Forbidden word used: {fw}"

        if self.cover_keywords:
            if not any(kw.lower() in message.lower() for kw in self.cover_keywords):
                return False, f"Message missing cover keyword (one of {self.cover_keywords})."

        import random
        if random.random() < self.noise_chance:
            return False, "Message lost in environment noise."

        return True, "Message valid."
