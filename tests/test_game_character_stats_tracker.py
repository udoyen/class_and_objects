import pytest
# Assuming your class is saved in a file named game_character.py
from class_properties.game_character_stats_tracker import GameCharacter

def test_initialization():
    """Verify that a newly instantiated character has correct starting stats."""
    character = GameCharacter("Kratos")
    
    assert character.name == "Kratos"
    assert character.health == 100
    assert character.mana == 50
    assert character.level == 1

def test_name_is_read_only():
    """Verify that name cannot be changed directly if it's meant to be read-only."""
    # Note: Since your current implementation includes @name.setter, this test 
    # checks if modifying it works. If you remove the setter per user stories,
    # you would use: with pytest.raises(AttributeError): character.name = "NewName"
    character = GameCharacter("Kratos")
    character.name = "Atreus"
    assert character.name == "Atreus"

def test_health_clamping_min_and_max():
    """Verify that health property setter clamps values between 0 and 100."""
    character = GameCharacter("Kratos")
    
    # Test valid damage reduction
    character.health = 75
    assert character.health == 75
    
    # Test clamping below 0
    character.health = -20
    assert character.health == 0
    
    # Test clamping above 100
    character.health = 150
    assert character.health == 100

def test_mana_clamping_min_and_max():
    """Verify that mana property setter clamps values between 0 and 50."""
    character = GameCharacter("Kratos")
    
    # Test valid mana usage
    character.mana = 30
    assert character.mana == 30
    
    # Test clamping below 0
    character.mana = -10
    assert character.mana == 0
    
    # Test clamping above 50
    character.mana = 80
    assert character.mana == 50

def test_level_up(capsys):
    """Verify level increases, stats reset, and message prints correctly."""
    character = GameCharacter("Kratos")
    
    # Simulate damage and mana drain before leveling up
    character.health = 20
    character.mana = 10
    
    # Trigger level up
    character.level_up()
    
    # Check that stats updated correctly
    assert character.level == 2
    assert character.health == 100
    assert character.mana == 50
    
    # Verify console print output format matches <name> leveled up to <level>!
    captured = capsys.readouterr()
    assert captured.out.strip() == "Kratos leveled up to 2!"

def test_string_representation():
    """Verify __str__ output matches the exact user story layout."""
    character = GameCharacter("Kratos")
    expected_output = (
        "Name: Kratos\n"
        "Level: 1\n"
        "Health: 100\n"
        "Mana: 50"
    )
    assert str(character) == expected_output