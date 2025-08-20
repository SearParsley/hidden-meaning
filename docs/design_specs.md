# Hidden Meaning Design Specs

## Summary

This is a game in which the player attempts to embed hidden messages within a regular conversation, while an enemy spy is listening in.

## Core gameplay loop

1. **Mission Briefing**: Player gets the following:
    1. The hidden message to convey
    2. Rules on forbidden words/phrases
    3. Conversation cover topic
2. **Dialogue Phase**: Player chats with NPC(s) in natural language
3. **Interpretation Phase**: AI "listens" from multiple perspectives:
    1. Ally
    2. Bystander
    3. Enemy Agent
4. **Outcome**: AI evaluates the following:
    1. Did the ally recieve the intended message?
    2. Did the enemy detect it?
    3. Did the player stay within topic and tone restrictions?
5. **World Update**: NPC trust changes, mission progress updates, possible complications

## LLM Agent Roles

### Scenario Generator Agent

- Creates location, NPC traits, cover topic, and forbidden words/phrases
- Adds random "complications" like interruptions or topic shifts

example output:

```json
{
    "location": "Cafe in Lisbon",
    "npc_personality": "Suspicious and detail-oriented",
    "cover_topic": "local cuisine",
    "forbidden_words": ["bridge", "code", "agent", "meet"],
    "hidden_message": "Meet at Bridge 47 at midnight",
}
```

### Conversation NPC Agent

- Maintains small talk
- Reacts naturally to player responses
- Can steer conversation toward or away from sensetive areas
- May "probe" if suspicious

### Interpretation Agents

- **Ally Interpreter**: Tries to decode the hidden message from the player's phrasing
- **Neutral Listener**: Judges conversation for normalcy
- **Enemy Listener**: Looks for signs of hidden info or unusual phrasing

## Success Evaluation Logic

- **Pass**: Ally correctly interprets AND enemy sees nothing unusual
- **Partial Success**: Ally gets the message but enemy is suspicious
- **Fail**: Ally misinterprets OR enemy identifies message

## Technical Skeleton

- LLM Core: Handles NPC dialogue and multi-perspective interpretation
- Conversation State: Tracks player responses, NPC suspicion level, ally confidence
- Mission State: Stores current message, constraints, and success/failure
- Agent Framework: LangChain, to run scenario -> conversation -> evaluation loop
- Memory: Short-term (current conversation) + long-term (past mission reports)
