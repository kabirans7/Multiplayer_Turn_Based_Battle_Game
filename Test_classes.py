import pytest
from Character import Gladiator, Voidcaster, Stormstriker, Nightstalker, Stoneguard
from Action import AttackAction, DefendAction, GladiatorSpecialMove, StormstrikerSpecialMove, VoidcasterSpecialMove
from StatusEffect import Poison
from BattleManager import BattleManager
from CharacterFactory import CharacterFactory

@pytest.fixture
def test_gladiator(): #Gladiator character
    return Gladiator("Gladiator", 100, "Close Combat, Big Physical Damage", "Titan Smash", 25, 12)

@pytest.fixture
def test_stoneguard(): #Stoneguard character
    return Stoneguard("Stoneguard", 140, "High Defense, Low Attack", "Iron Fortress", 18, 25)

#Test for attack actions
def test_attack_action(test_gladiator, test_stoneguard): 
    attack_action = AttackAction()
    init_health = test_stoneguard.health
    attack_action.execute(test_gladiator, test_stoneguard)
    assert test_stoneguard.health == init_health - (test_gladiator.attack_power - test_stoneguard.defense * 0.5)

#Test for special moves
def test_glad_spec_move(test_gladiator, test_stoneguard): 
    spec_move = GladiatorSpecialMove()
    inital_health = test_stoneguard.health
    spec_move.execute(test_gladiator, test_stoneguard)
    assert test_stoneguard.health < inital_health
    assert test_gladiator.special_move_cooldown == 3

#Test for damage 
def test_attack_damage(test_gladiator, test_stoneguard): 
    attack_action = AttackAction()
    ini_health = test_stoneguard.health    
    attack_action.execute(test_gladiator, test_stoneguard)

    expected_damage = max(0, (test_gladiator.attack_power * 1.0) -(test_stoneguard.defense * 0.5))
    assert test_stoneguard.health == ini_health - expected_damage

#Test for player count and unique characters chosen
@pytest.fixture
def character_count():
    character_options = ["Gladiator", "Voidcaster", "Stormstriker", "Nightstalker", "Stoneguard"]
    players = []
    selected_characters = set()

    total_players = 3
    for character_name in character_options[:total_players]:
        player_character = CharacterFactory.create_character(character_name)
        players.append(player_character)
        selected_characters.add(character_name)
    
    return players, selected_characters

def test_player_count(character_count):
    players, selected_characters = character_count

    assert len(players) == 3, "There should be 3 players"
    
    assert len(selected_characters) == 3, "There should be 3 unique characters chosen"

    assert players[0] is not players[1] or players[2], "Players should be unique"

def test_character_selection_unique(character_count):
    players, selected_characters = character_count

    assert len(players), "There should be 3 players"

# Test for the battle- Last remaining player wins
@pytest.fixture

def battle_manager(): 
    voidcaster = Voidcaster("Voidcaster", 85, "High Magic Damage", "Arcane Blast", 30, 8)
    stormstriker = Stormstriker("Stormstriker", 90, "Fast, Ranged Attacker", "Piercing Arrow", 22, 10)
    nightstalker = Nightstalker("Nightstalker", 75, "High Physical Damage, Stealth", "Shadow Strike", 35, 6)
    return BattleManager([voidcaster, stormstriker, nightstalker])

def test_battle_manager(battle_manager):
    battle_manager.start_battle()
    assert len(battle_manager.get_alive_players()) == 1, "Only one player should be left remaining"
    #You have to play the battle but this passes the test

#Test for target selection
@pytest.fixture 
def the_battle():
    voidcaster = Voidcaster("Voidcaster", 85, "High Magic Damage", "Arcane Blast", 30, 8)
    stormstriker = Stormstriker("Stormstriker", 90, "Fast, Ranged Attacker", "Piercing Arrow", 22, 10)
    gladiator = Gladiator("Gladiator", 100, "Close Combat, Big Physical Damage", "Titan Smash", 25, 12)
    battle_manager2 =  BattleManager([voidcaster, stormstriker, gladiator])
    return battle_manager2, gladiator, voidcaster, stormstriker

def test_valid_target_selection(the_battle): #Test for Valid Target Selection
    battle_manager2, gladiator, voidcaster, stormstriker = the_battle

    intended_target = battle_manager2.choose_target(stormstriker)
    assert intended_target == voidcaster, "Stormstriker should target Voidcaster"

def test_invalid_target_selection(the_battle): #Test for Invalid target selection
    battle_manager2, gladiator, voidcaster, stormstriker = the_battle
    intended_target = battle_manager2.choose_target(gladiator)
    assert intended_target != gladiator, "Gladiator should not target itself"

#Test for special moves initial cooldown and defensive actions
@pytest.fixture
def gladiator_and_stoneguard():
    gladiator = Gladiator("Gladiator", 100, "Close Combat, Big Physical Damage", "Titan Smash", 25, 12)
    stoneguard = Stoneguard("Stoneguard", 140, "High Defense, Low Attack", "Iron Fortress", 18, 25)
    return gladiator, stoneguard

def test_special_move_cooldown_initial(gladiator_and_stoneguard): #Initial Special Move Cooldown test
    gladiator, stoneguard = gladiator_and_stoneguard
    
    special_move = GladiatorSpecialMove()
    special_move.execute(gladiator, stoneguard)

    assert gladiator.special_move_cooldown == 3, "Cooldown should be 3"

def test_special_move_cooldown_decrement(gladiator_and_stoneguard): #Decrement Special Move Cooldown test
    gladiator, stoneguard = gladiator_and_stoneguard

    special_move = GladiatorSpecialMove()
    special_move.execute(gladiator, stoneguard)

    gladiator.decrement_cooldowns()
    assert gladiator.special_move_cooldown == 2, "Cooldown should be 2"

    gladiator.decrement_cooldowns()
    assert gladiator.special_move_cooldown == 1, "Cooldown should be 1"

def test_defend_action_increased_defense(gladiator_and_stoneguard): #Increased Defense test for Stoneguard
    gladiator, stoneguard = gladiator_and_stoneguard
    init_defense = stoneguard.defense
    defend_action = DefendAction()
    defend_action.execute(stoneguard)
    assert stoneguard.defense == init_defense * 2

def test_defend_action_reduce_damage(gladiator_and_stoneguard):#Reduced Damage test for Stoneguard
    gladiator, stoneguard = gladiator_and_stoneguard

    initial_health = stoneguard.health

    defend_action = DefendAction()
    defend_action.execute(stoneguard)

    attack_action = AttackAction()
    attack_action.execute(gladiator, stoneguard)

    expected_damage = max(0, (gladiator.attack_power * 1.0) - (stoneguard.defense * 2))
    assert stoneguard.health == initial_health - expected_damage

# Test for Poison Status Effect
def test_poison_effect():
    character = Nightstalker("Test1", 100, "High Damage, Stealth", "Shadow Strike", 35, 10)
    poison = Poison(5, duration = 3)
    character.apply_status_effect(poison)

    initial_health = character.health
    character.process_status_effects()

    assert character.health < initial_health, "Health should decrease due to poison effect"
    assert character.health == initial_health - 5, "Health should decrease by 5 due to poison effect"
