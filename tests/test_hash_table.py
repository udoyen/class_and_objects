import pytest
from hash_table.hash_table import HashTable  # Adjust this import path to match your layout

# --- Fixtures ---
@pytest.fixture
def empty_table():
    """Provides a fresh, empty HashTable instance for each test."""
    return HashTable()

@pytest.fixture
def populated_table():
    """Provides a HashTable pre-populated with unique entries and colliding entries."""
    ht = HashTable()
    # "cat" hash: 99 + 97 + 116 = 312
    ht.add("cat", "Meow")
    # "act" hash: 97 + 99 + 116 = 312 (Collides with "cat"!)
    ht.add("act", "Theater")
    # "dog" hash: 100 + 111 + 103 = 314 (Unique hash)
    ht.add("dog", "Bark")
    return ht


# --- User Story 1: Initialization Tests ---
def test_hash_table_initialization(empty_table):
    """Ensures a new instance sets up an empty internal collection dictionary."""
    assert hasattr(empty_table, 'collection')
    assert isinstance(empty_table.collection, dict)
    assert len(empty_table.collection) == 0


# --- User Story 2: Hashing Strategy ---
def test_hash_method_computes_unicode_sum(empty_table):
    """Verifies hash calculation matches the sum of individual character ord values."""
    # 'A' (65) + 'B' (66) = 131
    assert empty_table.hash("AB") == 131
    # 'c' (99) + 'a' (97) + 't' (116) = 312
    assert empty_table.hash("cat") == 312


# --- User Story 3: Addition and Collision Resolution ---
def test_add_stores_key_value_in_nested_dict(empty_table):
    """Tests if adding an item creates a nested dictionary under the computed hash key."""
    empty_table.add("dog", "Bark")
    target_hash = empty_table.hash("dog")  # 314
    
    # Structure must be: collection = { 314: {"dog": "Bark"} }
    assert target_hash in empty_table.collection
    assert isinstance(empty_table.collection[target_hash], dict)
    assert empty_table.collection[target_hash]["dog"] == "Bark"

def test_add_handles_collisions_with_nested_chaining(empty_table):
    """Edge Case: Anagrams producing identical hashes must coexist inside the same bucket dictionary."""
    empty_table.add("cat", "Meow")
    empty_table.add("act", "Theater")
    
    cat_hash = empty_table.hash("cat")
    act_hash = empty_table.hash("act")
    
    # Confirm they actually cause a collision
    assert cat_hash == act_hash
    
    # Both must survive inside the same bucket index without overwriting one another
    assert len(empty_table.collection[cat_hash]) == 2
    assert empty_table.collection[cat_hash]["cat"] == "Meow"
    assert empty_table.collection[cat_hash]["act"] == "Theater"


# --- User Story 4: Value Lookup ---
def test_lookup_returns_correct_value(populated_table):
    """Tests if looking up a clean or colliding key extracts its accurate value."""
    assert populated_table.lookup("dog") == "Bark"
    assert populated_table.lookup("cat") == "Meow"
    assert populated_table.lookup("act") == "Theater"

def test_lookup_non_existent_key_returns_none(populated_table):
    """Edge Case: Searching for a key that was never added should return None cleanly."""
    assert populated_table.lookup("bird") is None


# --- User Story 5: Removal ---
def test_remove_deletes_key_value_pair(populated_table):
    """Verifies that removing a key safely deletes it from the internal bucket storage mapping."""
    populated_table.remove("dog")
    assert populated_table.lookup("dog") is None

def test_remove_retains_collided_siblings(populated_table):
    """Edge Case: Dropping a colliding key must not accidentally wipe out other items in that same bucket."""
    shared_hash = populated_table.hash("cat")
    
    # Drop one of the colliding pair entries
    populated_table.remove("cat")
    
    # "cat" should be gone, but "act" must safely remain intact inside that bucket array
    assert populated_table.lookup("cat") is None
    assert populated_table.lookup("act") == "Theater"
    assert shared_hash in populated_table.collection

def test_remove_non_existent_key_does_not_raise_error(populated_table):
    """Edge Case: Requesting deletion for a non-existent key fails silently without throwing errors."""
    try:
        populated_table.remove("dinosaur")
    except Exception as exc:
        pytest.fail(f"remove() raised an unexpected error on a missing key: {exc}")