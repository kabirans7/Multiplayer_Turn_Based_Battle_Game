import time
from Character import Gladiator, Voidcaster, Stormstriker, Nightstalker, Stoneguard
from StatusEffect import Poison, Stun, ExtraDefense
from CharacterFactory import CharacterFactory
from Action import AttackAction, DefendAction, SpecialMoveAction, GladiatorSpecialMove, VoidcasterSpecialMove, StormstrikerSpecialMove, NightstalkerSpecialMove, StoneguardSpecialMove

# Manages game flow and turn-based battle.
class BattleManager:
    # Initialize with a list of player objects.
    def __init__(self, players):
        self.players = players  # List of all players.
        self.turn_order = list(players)  # Order of turns.

    # Main battle loop until one player remains.
    def start_battle(self):
        print("\nLET THE BATTLE COMMENCE!")
        time.sleep(2)
        while len(self.get_alive_players()) > 1:
            for player in self.turn_order[:]:  # Iterate over a copy to avoid modification issues.
                if player.health <= 0:
                    continue  # Skip dead players.
                self.process_turn(player)
                if len(self.get_alive_players()) == 1:
                    break  # End battle if one player remains.
        winner = self.get_alive_players()[0]
        print(f"\nGame Over! {winner.name} is the winner!")

    # Return a list of players that are still alive.
    def get_alive_players(self):
        return [player for player in self.players if player.health > 0]

    # Process an individual player's turn.
    def process_turn(self, player):
        if player.health <= 0:
            return  # Do nothing if the player is dead.
        # Reset defense if defending.
        if " (Defending) " in player.name:
             player.defense /= 2
             player.name = player.name.replace(" (Defending) ", "")
        print(f"\n{player.name}'s turn!")
        # Process status effects (which may modify behavior).
        player.process_status_effects()
        # Skip turn if stunned.
        if any(isinstance(effect, Stun) for effect in player.status_effects):
            return
        # Display current battle status.
        print("\nCurrent Battle Status:")
        for p in self.players:
            print(f"{p.name} - HP: {p.health}")
        # Show available actions.
        print("\nChoose an action:")
        print("[1] Attack")
        print("[2] Defend")
        if player.special_move_cooldown == 0:
            print("[3] Special Move")
        else:
            print(f"[3] Special Move (Cooldown: {player.special_move_cooldown} turns)")
        # Get and validate player's choice.
        while True:
            try:
                choice = int(input("Enter action (1, 2, or 3): ").strip())
                if choice == 3 and player.special_move_cooldown > 0:
                    print(f"{player.name}'s special move is on cooldown!")
                    continue
                if choice in [1, 2, 3]:
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        # Execute the chosen action.
        if choice == 1:
            target = self.choose_target(player)
            player.attack_enemy(target)
        elif choice == 2:
            player.defend_yourself()
        elif choice == 3:
            if isinstance(player, Stoneguard):
                action = StoneguardSpecialMove()
                action.execute(player)  # Stoneguard's special move does not require a target.
            else:
                target = self.choose_target(player)
                if isinstance(player, Gladiator):
                    action = GladiatorSpecialMove()
                elif isinstance(player, Voidcaster):
                    action = VoidcasterSpecialMove()
                elif isinstance(player, Stormstriker):
                    action = StormstrikerSpecialMove()
                elif isinstance(player, Nightstalker):
                    action = NightstalkerSpecialMove()
                else:
                    action = SpecialMoveAction()  # Fallback if needed.
                action.execute(player, target)
        # Remove players that have been eliminated.
        self.players = [p for p in self.players if p.health > 0]
        time.sleep(2)

    # Allow the player to choose a target from alive opponents.
    def choose_target(self, player):
        """Allows a player to choose a valid target from alive players."""
        alive_players = [p for p in self.get_alive_players() if p != player]
        if not alive_players:
            return None  # No valid targets.
        print("\nSelect a target:")
        for idx, opponent in enumerate(alive_players):
            print(f"[{idx+1}] {opponent.name} - HP: {opponent.health}")
        while True:
            try:
                choice = int(input("Enter target number: ")) - 1
                if 0 <= choice < len(alive_players):
                    return alive_players[choice]
            except ValueError:
                pass
            print("Invalid selection, try again.")

# Main function to initialize and start the game.
def main():
    print("Initializing game...")
    selected_characters = set()
    total_players_allowed = 3
    players = []
    character_options = {
        "1": "Gladiator",
        "2": "Voidcaster",
        "3": "Stormstriker",
        "4": "Nightstalker",
        "5": "Stoneguard"
    }
    character_descriptions = {
        "1": "\nThe Gladiator is a generalist fighter with solid physical damage. \nTheir special move, Titan Smash, deals extra damage with a cooldown.",
        "2": "\nThe Voidcaster has high attack power and deals heavy magic damage. \nTheir special move, Arcane Blast, hits both opponents and stuns them.",
        "3": "\nThe Stormstriker deals solid ranged damage, but is weak up close. \nTheir special move, Piercing Arrow, ignores defense.",
        "4": "\nThe Nightstalker deals very high physical damage and applies status effects, but is very frail. \nTheir special move, Shadow Strike, inflicts poison.",
        "5": "\nThe Stoneguard is very defensive with low attack power. \nTheir special move, Iron Fortress, increases defense for 3 turns."
    }
    # Loop for character selection.
    while len(players) < total_players_allowed:
        print("\nChoose your character:")
        for key, name in character_options.items():
            print(f"[{key}] {name}")
        user_in = input("Select a character: ").strip()
        if user_in in character_options:
            if user_in in selected_characters:
                print("Character already chosen. Please select a different one.") #Cannot choose the same character
                continue
            character_name = character_options[user_in]
            # Display character description.
            print(character_descriptions[user_in])
            # Confirm selection.
            confirm = input(f"Confirm choosing {character_name}? \n[1] Return \n[2] Proceed \nSelect: ").strip()
            if confirm == "1":
                continue
            elif confirm == "2":
                player_character = CharacterFactory.create_character(character_name)
                players.append(player_character)
                selected_characters.add(user_in)
                print(f"You have chosen {character_name}!")
        else:
            print("Invalid choice. Please select a valid number.")
    print("\nLoading...")
    time.sleep(3)
    print("\nAll characters have been selected! The battle is about to begin!")
    battle_manager = BattleManager(players)
    battle_manager.start_battle()

# Main Program
if __name__ == "__main__":
    main()
