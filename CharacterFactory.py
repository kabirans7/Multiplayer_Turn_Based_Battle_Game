from Character import Gladiator, Voidcaster, Stormstriker, Nightstalker, Stoneguard

# Factory class to create character objects.
class CharacterFactory:
    @staticmethod
    def create_character(character_name):
        character_classes = {
            "Gladiator": lambda: Gladiator("Gladiator", 100, "Close Combat, Big Physical Damage", "Titan Smash", 25, 12),
            "Voidcaster": lambda: Voidcaster("Voidcaster", 85, "High Magic Damage", "Arcane Blast", 30, 8),
            "Stormstriker": lambda: Stormstriker("Stormstriker", 90, "Fast, Ranged Attacker", "Piercing Arrow", 22, 10),
            "Nightstalker": lambda: Nightstalker("Nightstalker", 75, "High Physical Damage, Stealth", "Shadow Strike", 35, 6),
            "Stoneguard": lambda: Stoneguard("Stoneguard", 140, "High Defense, Low Attack", "Iron Fortress", 18, 25),
        }
        if character_name in character_classes:
            return character_classes[character_name]()
        else:
            raise ValueError(f"Invalid character type: {character_name}")
