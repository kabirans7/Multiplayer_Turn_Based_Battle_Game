from abc import ABC, abstractmethod
from StatusEffect import Poison, Stun, ExtraDefense
from Action import AttackAction, DefendAction, GladiatorSpecialMove, VoidcasterSpecialMove, StormstrikerSpecialMove, NightstalkerSpecialMove, StoneguardSpecialMove

# Base class for all characters in the game.
class Character(ABC):
    # Initialize character with attributes.
    def __init__(self, name: str, health: int, abilities: str, spec_move: str, attack_power: int, defense: int):
        self.name = name
        self.health = health
        self.status_effects = []  # List of active status effects.
        self.abilities = abilities
        self.spec_move = spec_move
        self.attack_power = attack_power
        self.defense = defense
        self.special_move_cooldown = 0  # Cooldown counter for special move.

    # Abstract method for performing a special move.
    @abstractmethod
    def do_special_moves(self, opponent):
        pass

    # Execute a normal attack on an opponent.
    def attack_enemy(self, opponent):
        action = AttackAction()
        action.execute(self, opponent)

    # Execute a defend action.
    def defend_yourself(self):
        action = DefendAction()
        action.execute(self)

    # Apply a status effect if not already present.
    def apply_status_effect(self, effect):
        if not any(isinstance(e, type(effect)) for e in self.status_effects):
            self.status_effects.append(effect)
            print(f"{self.name} is now affected by {effect.name}!")

    # Process all active status effects at the start of a turn.
    def process_status_effects(self):
        active_effects = []
        for effect in self.status_effects[:]:
            effect.exec_turn(self)  # Execute effect logic and print its message.
            if effect.lasting > 0:
                active_effects.append(effect)
            else:
                print(f"{self.name} is no longer affected by {effect.name}.")
        self.status_effects = active_effects  # Update active effects list.

    # Check if the special move is ready.
    def special_move_ready(self):
        return self.special_move_cooldown == 0

    # Decrement cooldown counters and process status effects.
    def decrement_cooldowns(self):
        if self.special_move_cooldown > 0:
            self.special_move_cooldown -= 1
        self.process_status_effects()

# Concrete character classes with their specific special moves.
class Gladiator(Character):
    def do_special_moves(self, opponent):
        action = GladiatorSpecialMove()
        action.execute(self, opponent)

class Voidcaster(Character):
    def do_special_moves(self, opponent):
        action = VoidcasterSpecialMove()
        action.execute(self, opponent)

class Stormstriker(Character):
    def do_special_moves(self, opponent):
        action = StormstrikerSpecialMove()
        action.execute(self, opponent)

class Nightstalker(Character):
    def do_special_moves(self, opponent):
        action = NightstalkerSpecialMove()
        action.execute(self, opponent)

class Stoneguard(Character):
    def do_special_moves(self, opponent):
        action = StoneguardSpecialMove()
        action.execute(self)

