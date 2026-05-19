"""
Key Testing Patterns Used:
capsys Built-in Fixture: Your application relies heavily on print() 
statements to announce actions or handle fallback states (like "Invalid email number."). 
We use capsys.readouterr() to inspect the terminal console buffer and assert your script prints the proper textual messages.

Out-of-Bounds Parameterization: The @pytest.mark.parametrize decorator checks four tricky boundary indices 
(0, negative items like -1, immediate upper ceiling bounds, and massive numbers like 99) 
to guarantee your system rejects invalid layout references securely without dropping an unhandled IndexError.

Integration Flow Isolation: test_user_send_and_receive_integration tests the orchestration loop between instances of User, 
Inbox, and Email in a clean sandbox context separate from your production code's main() runner loop execution space.

"""

import pytest
from composition.messaging import User, Email, Inbox  # Replace 'your_module_name' with your actual file name

# --- Fixtures ---
@pytest.fixture
def user_tory():
    return User('Tory')

@pytest.fixture
def user_ramy():
    return User('Ramy')

@pytest.fixture
def sample_email(user_tory, user_ramy):
    return Email(
        sender=user_tory, 
        receiver=user_ramy, 
        subject='Meeting', 
        body='See you at 3 PM.'
    )


# --- Tests for Email Class ---
def test_email_initialization(user_tory, user_ramy, sample_email):
    """Tests if an email constructs its fields and default status cleanly."""
    assert sample_email.sender == user_tory
    assert sample_email.receiver == user_ramy
    assert sample_email.subject == 'Meeting'
    assert sample_email.body == 'See you at 3 PM.'
    assert sample_email.read is False
    assert sample_email.timestamp is not None

def test_mark_as_read(sample_email):
    """Verifies state mutation when marking emails as read."""
    assert sample_email.read is False
    sample_email.mark_as_read()
    assert sample_email.read is True

def test_email_string_representation(sample_email):
    """Ensures string format shows [Unread] and switches to [Read] correctly."""
    assert str(sample_email).startswith('[Unread] From: Tory')
    sample_email.mark_as_read()
    assert str(sample_email).startswith('[Read] From: Tory')


# --- Tests for Inbox Class ---
def test_inbox_initialization():
    """Ensures a fresh inbox starts completely empty."""
    inbox = Inbox()
    assert len(inbox.emails) == 0

def test_receive_email(sample_email):
    """Checks if appending emails into an inbox populates tracking lists."""
    inbox = Inbox()
    inbox.receive_email(sample_email)
    assert len(inbox.emails) == 1
    assert inbox.emails[0] == sample_email


# --- Edge Case Tests: Empty Inbox Operations ---
def test_operations_on_empty_inbox(capsys):
    """Ensures empty inbox routines gracefully log warnings instead of throwing errors."""
    inbox = Inbox()
    
    # 1. Listing an empty inbox
    inbox.list_emails()
    captured = capsys.readouterr()
    assert 'Your inbox is empty.' in captured.out

    # 2. Reading from an empty inbox
    inbox.read_email(1)
    captured = capsys.readouterr()
    assert 'Inbox is empty.' in captured.out

    # 3. Deleting from an empty inbox
    inbox.delete_email(1)
    captured = capsys.readouterr()
    assert 'Inbox is empty.' in captured.out


# --- Edge Case Tests: Invalid Indices (Out of Bounds) ---
@pytest.mark.parametrize("invalid_index", [0, -1, 5, 99])
def test_inbox_boundary_index_errors(capsys, sample_email, invalid_index):
    """Validates that reading or deleting non-existent indices blocks execution safely."""
    inbox = Inbox()
    inbox.receive_email(sample_email)  # Contains exactly 1 email (Index 1 from user standpoint)

    # Test reading out of bounds
    inbox.read_email(invalid_index)
    captured = capsys.readouterr()
    assert 'Invalid email number.' in captured.out

    # Test deleting out of bounds
    inbox.delete_email(invalid_index)
    captured = capsys.readouterr()
    assert 'Invalid email number.' in captured.out


# --- Tests for User Operations (Integration) ---
def test_user_send_and_receive_integration(user_tory, user_ramy):
    """Integration test validating complete E2E delivery mechanics between players."""
    # Inbox should start blank
    assert len(user_ramy.inbox.emails) == 0

    # Send pipeline trigger
    user_tory.send_email(user_ramy, 'Hello', 'Body text here')
    
    # Check assertions on receiver tracking state
    assert len(user_ramy.inbox.emails) == 1
    delivered_email = user_ramy.inbox.emails[0]
    assert delivered_email.subject == 'Hello'
    assert delivered_email.sender == user_tory


def test_user_read_marks_email_as_read_in_place(user_tory, user_ramy):
    """Verifies that reading an email via User proxy alters state across the aggregate model."""
    user_tory.send_email(user_ramy, 'Alert', 'System Check')
    
    # Initially unread
    assert user_ramy.inbox.emails[0].read is False
    
    # Read action via user instance wrapper
    user_ramy.read_email(1)
    
    # Status should swap over
    assert user_ramy.inbox.emails[0].read is True


def test_user_delete_removes_from_sequence(user_tory, user_ramy):
    """Verifies array element trimming and re-indexing mechanics when items drop."""
    user_tory.send_email(user_ramy, 'Email 1', 'First')
    user_tory.send_email(user_ramy, 'Email 2', 'Second')
    
    assert len(user_ramy.inbox.emails) == 2
    
    # Delete the first email item
    user_ramy.delete_email(1)
    
    # Remaining items must compress back down cleanly
    assert len(user_ramy.inbox.emails) == 1
    assert user_ramy.inbox.emails[0].subject == 'Email 2'


def test_display_full_email_execution(capsys, sample_email):
    """Executes the complete print block for displaying a full email."""
    # This executes the print lines inside the Email class
    sample_email.display_full_email()
    
    captured = capsys.readouterr()
    assert '--- Email ---' in captured.out
    assert 'From: Tory' in captured.out
    assert 'To: Ramy' in captured.out
    assert 'Subject: Meeting' in captured.out
    assert 'Body: See you at 3 PM.' in captured.out
    assert sample_email.read is True  # Also verifies it marks as read inline


def test_list_emails_with_populated_inbox(capsys, sample_email):
    """Executes the loop branch inside list_emails when emails exist."""
    inbox = Inbox()
    inbox.receive_email(sample_email)
    
    # Trigger the print sequence loop
    inbox.list_emails()
    
    captured = capsys.readouterr()
    assert 'Your Emails:' in captured.out
    assert '1. [Unread] From: Tory' in captured.out


def test_user_check_inbox_wrapper(capsys, user_tory, user_ramy):
    """Executes the wrapper method for checking an inbox through the User class."""
    user_tory.send_email(user_ramy, 'Ping', 'Test')
    
    # Clear out the print buffer from sending the email
    capsys.readouterr()
    
    # Trigger user check layout
    user_ramy.check_inbox()
    
    captured = capsys.readouterr()
    assert "Ramy's Inbox:" in captured.out
    assert '1. [Unread] From: Tory' in captured.out