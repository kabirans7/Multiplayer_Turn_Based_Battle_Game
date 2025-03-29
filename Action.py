from abc import ABC, abstractmethod
from StatusEffect import Poison, Stun, ExtraDefense

# Base class for all actions.
class Action(ABC):
    @abstractmethod
    def execute(self, attacker, target=None):
        pass

# Normal attack action.
class AttackAction(Action):
    def execute(self, attacker, target):
        # Normal attack uses a 1.0x multiplier and factors in target defense.
        damage = max(0, (attacker.attack_power * 1.0) - (target.defense * 0.5))
        target.health -= damage
        print(f"{attacker.name} attacks {target.name} for {damage:.1f} damage!")
        if target.health <= 0:
            print(f"{target.name} has been eliminated!")

# Defend action: doubles the character's defense.
class DefendAction(Action):
    def execute(self, attacker, target=None):
        attacker.defense *= 2
        print(f"{attacker.name} is defending! Defense increased.")
        attacker.name = attacker.name+(" (Defending) ")

# Generic special move action with a 1.5x multiplier.
class SpecialMoveAction(Action):
    def execute(self, attacker, target):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        damage = max(10, attacker.attack_power * 1.5)
        target.health -= damage
        print(f"{attacker.name} uses {attacker.spec_move} on {target.name} for {damage:.1f} damage!")
        attacker.special_move_cooldown = 3

# Gladiator's special move: heavy damage with a 2.0x multiplier.
class GladiatorSpecialMove(Action):
    def execute(self, attacker, target):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        damage = max(10, attacker.attack_power * 2.0 - target.defense)
        target.health -= damage
        attacker.special_move_cooldown = 3
        print(f"{attacker.name} uses Titan Smash on {target.name} for {damage:.1f} damage!")

# Voidcaster's special move: magic attack with 1.5x multiplier and applies stun.
class VoidcasterSpecialMove(Action):
    def execute(self, attacker, target):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        damage = max(12, attacker.attack_power * 1.5)
        target.health -= damage 
        target.apply_status_effect(Stun(2))
        attacker.special_move_cooldown = 4
        print(f"{attacker.name} casts Arcane Blast on {target.name} for {damage:.1f} damage! {target.name} is now stunned!")

# Stormstriker's special move: ranged attack with 1.5x multiplier.
class StormstrikerSpecialMove(Action):
    def execute(self, attacker, target):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        damage = max(12, attacker.attack_power * 1.5)
        target.health -= damage
        attacker.special_move_cooldown = 2
        print(f"{attacker.name} uses Piercing Arrow on {target.name} for {damage:.1f} damage!")

# Nightstalker's special move: attack with 1.5x multiplier plus poison.
class NightstalkerSpecialMove(Action):
    def execute(self, attacker, target):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        damage = max(10, attacker.attack_power * 1.5)
        target.health -= damage
        target.status_effects.append(Poison(3))
        attacker.special_move_cooldown = 3
        print(f"{attacker.name} uses Shadow Strike on {target.name} for {damage:.1f} damage! {target.name} is now poisoned!")

# Stoneguard's special move: applies a defensive buff instead of dealing damage.
class StoneguardSpecialMove(Action):
    def execute(self, attacker, target=None):
        if attacker.special_move_cooldown > 0:
            print(f"{attacker.spec_move} is on cooldown for {attacker.special_move_cooldown} more turns!")
            return
        attacker.status_effects.append(ExtraDefense(10, 3))
        attacker.special_move_cooldown = 3
        print(f"{attacker.name} uses Iron Fortress, reducing all damage taken for 3 turns!")
