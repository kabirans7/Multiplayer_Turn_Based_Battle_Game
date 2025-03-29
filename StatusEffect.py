# Base class for status effects.
class StatusEffects:
    # Initialize status effect with name and duration.
    def __init__(self, name, lasting):
        self.name = name  # Name of the effect.
        self.lasting = lasting  # Duration in turns.

    # Execute the status effect on the character.
    def exec_status_effect(self, character):
        pass

    # Called when the effect is removed.
    def remove_status_effect(self, character):
        pass

    # Execute effect logic for one turn and decrement duration.
    def exec_turn(self, character):
        self.exec_status_effect(character)
        self.lasting -= 1
        if self.lasting <= 0:
            self.remove_status_effect(character)
            return False  # Effect expired.
        return True  # Effect still active.

# Poison effect: damages the character each turn.
class Poison(StatusEffects):
    def __init__(self, damage, duration=3):
        super().__init__("Poison", lasting=duration)
        self.damage = damage

    def exec_status_effect(self, character):
        print(f"{character.name} is poisoned! Losing {self.damage} HP this turn.")
        character.health -= self.damage

    def remove_status_effect(self, character):
        if any(isinstance(effect, Poison) for effect in character.status_effects):
            return 
        print(f"{character.name} is no longer poisoned.")

# Stun effect: prevents the character from acting.
class Stun(StatusEffects):
    def __init__(self, duration=2):
        super().__init__("Stun", lasting=duration)

    def exec_status_effect(self, character):
        character.is_stunned = True
        print(f"{character.name} is stunned and cannot act!")

    def remove_status_effect(self, character):
        pass  # No removal message to avoid duplicate output.

# Extra Defense effect: temporarily increases defense.
class ExtraDefense(StatusEffects):
    def __init__(self, defense_boost, duration=3):
        super().__init__("Extra Defense", lasting=duration)
        self.defense_boost = defense_boost

    def exec_status_effect(self, character):
        if self not in character.status_effects:
            character.defense += self.defense_boost
            print(f"{character.name} gains +{self.defense_boost} defense for {self.lasting} turns!")

    def remove_status_effect(self, character):
        if any(isinstance(effect, ExtraDefense) for effect in character.status_effects):
            return 
        character.defense -= self.defense_boost
        print(f"{character.name}'s extra defense has worn off.")
