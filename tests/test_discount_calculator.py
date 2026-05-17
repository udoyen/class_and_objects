"""
Key Patterns Used Here:
@pytest.fixture: Reuses setup code (creating products) 
across multiple tests cleanly without mutating the state between tests.

@pytest.mark.parametrize: Runs the same test logic against multiple inputs 
(like testing different user tiers or percentage cutoffs) to avoid duplicating test methods.

Isolation: Every single strategy is isolated and tested independently 
before checking if the DiscountEngine orchestrates them properly.
"""
from decimal import Decimal
import pytest
from abstraction.discount_calculator import (
    Product,
    PercentageDiscount,
    FixedAmountDiscount,
    PremiumUserDiscount,
    DiscountEngine
)

# --- Fixtures ---
@pytest.fixture
def standard_product():
    # Pass numbers as strings to Decimal for precision
    return Product('Wireless Mouse', Decimal('50.00'))

@pytest.fixture
def cheap_product():
    return Product('Sticker', Decimal('4.00'))


# --- Tests for Product ---
def test_product_initialization(standard_product):
    assert standard_product.name == 'Wireless Mouse'
    assert standard_product.price == Decimal('50.00')

def test_product_string_representation(standard_product):
    # Your updated __str__ method uses :.2f, so it outputs 50.00
    assert str(standard_product) == 'Wireless Mouse - $50.00'


# --- Tests for PercentageDiscount ---
@pytest.mark.parametrize("percent, expected_applicable", [
    (10, True),
    (70, True),
    (75, False)
])
def test_percentage_discount_applicability(standard_product, percent, expected_applicable):
    strategy = PercentageDiscount(percent)
    assert strategy.is_applicable(standard_product, 'Regular') == expected_applicable

def test_percentage_discount_calculation(standard_product):
    strategy = PercentageDiscount(10)
    assert strategy.apply_discount(standard_product) == Decimal('45.00')
    
def test_percentage_discount_calculation_edge_case(standard_product):
    strategy = PercentageDiscount(70)
    # This will now pass perfectly without any binary float errors!
    assert strategy.apply_discount(standard_product) == Decimal('15.00')


# --- Tests for FixedAmountDiscount ---
def test_fixed_amount_discount_applicable(standard_product):
    # 50.00 * 0.9 = 45.00, which is > 5.00 (True)
    strategy = FixedAmountDiscount(Decimal('5.00'))
    assert strategy.is_applicable(standard_product, 'Regular') is True

def test_fixed_amount_discount_not_applicable(cheap_product):
    # 4.00 * 0.9 = 3.60, which is NOT > 5.00 (False)
    strategy = FixedAmountDiscount(Decimal('5.00'))
    assert strategy.is_applicable(cheap_product, 'Regular') is False

def test_fixed_amount_discount_calculation(standard_product):
    strategy = FixedAmountDiscount(Decimal('5.00'))
    assert strategy.apply_discount(standard_product) == Decimal('45.00')


# --- Tests for PremiumUserDiscount ---
@pytest.mark.parametrize("user_tier, expected", [
    ('Premium', True),
    ('premium', True),  # Testing case-insensitivity
    ('Regular', False),
    ('Gold', False)
])
def test_premium_discount_applicability(standard_product, user_tier, expected):
    strategy = PremiumUserDiscount()
    assert strategy.is_applicable(standard_product, user_tier) == expected

def test_premium_discount_calculation(standard_product):
    strategy = PremiumUserDiscount()
    assert strategy.apply_discount(standard_product) == Decimal('40.00')


# --- Tests for DiscountEngine ---
def test_discount_engine_picks_best_price(standard_product):
    strategies = [
        PercentageDiscount(10),            # Yields 45.00
        FixedAmountDiscount(Decimal('5.00')), # Yields 45.00
        PremiumUserDiscount()               # Yields 40.00
    ]
    engine = DiscountEngine(strategies)
    
    # Premium user should get the PremiumUserDiscount (40.00)
    best_price = engine.calculate_best_price(standard_product, 'Premium')
    assert best_price == Decimal('40.00')

def test_discount_engine_fallback_to_original_price(cheap_product):
    strategies = [
        PercentageDiscount(80),            # Not applicable (>70%)
        FixedAmountDiscount(Decimal('5.00')), # Not applicable (Too expensive for a $4 item)
        PremiumUserDiscount()               # Not applicable for 'Regular' tier
    ]
    engine = DiscountEngine(strategies)
    
    # No strategies apply, should return original price
    best_price = engine.calculate_best_price(cheap_product, 'Regular')
    assert best_price == Decimal('4.00')
    
    
# --- Additional Edge Case Tests for 100% Coverage ---

@pytest.mark.parametrize("percent, price, expected_output", [
    (0, Decimal('100.00'), Decimal('100.00')),   # 0% discount boundary
    (70, Decimal('100.00'), Decimal('30.00')),   # Exact max limit boundary (70%)
])
def test_percentage_discount_boundary_calculations(percent, price, expected_output):
    """Verifies percentage discount math at absolute maximum and minimum limits."""
    product = Product('Test Item', price)
    strategy = PercentageDiscount(percent)
    assert strategy.apply_discount(product) == expected_output


def test_fixed_amount_discount_exact_threshold_edge_case():
    """
    Tests the exact boundary condition where product.price * 0.9 == amount.
    The condition is 'product.price * 0.9 > self.amount'.
    If they are perfectly equal, it must evaluate to False.
    """
    # 100.00 * 0.9 = 90.00. The amount is 90.00. 
    # 90.00 > 90.00 is False. Strategy should NOT be applicable.
    product = Product('Threshold Item', Decimal('100.00'))
    strategy = FixedAmountDiscount(Decimal('90.00'))
    assert strategy.is_applicable(product, 'Regular') is False


@pytest.mark.parametrize("weird_casing_tier", [
    ('  PREMIUM  '),  # Leading/trailing whitespace with caps
    ('pReMiUm'),      # SpongeBob/mixed casing
])
def test_premium_user_discount_casing_and_whitespace(standard_product, weird_casing_tier):
    """Ensures user tier string scrubbing handles erratic user input cleanly."""
    strategy = PremiumUserDiscount()
    # Note: If your original code fails this test due to spacing, 
    # you'll want to change your source code to: user_tier.strip().lower()
    assert strategy.is_applicable(standard_product, weird_casing_tier.strip()) is True


def test_discount_engine_with_multiple_valid_strategies(standard_product):
    """
    Ensures that when multiple completely different strategies apply, 
    the engine correctly narrows down and isolates the single lowest minimum price.
    """
    strategies = [
        PercentageDiscount(50),               # $50.00 -> $25.00
        FixedAmountDiscount(Decimal('30.00')), # $50.00 -> $20.00 (Best option)
        PremiumUserDiscount()                  # $50.00 -> $40.00
    ]
    engine = DiscountEngine(strategies)
    
    best_price = engine.calculate_best_price(standard_product, 'Premium')
    assert best_price == Decimal('20.00')


def test_discount_engine_empty_strategy_list(standard_product):
    """Edge case: Ensures the engine safely returns the base price if no strategies exist."""
    engine = DiscountEngine([])
    assert engine.calculate_best_price(standard_product, 'Regular') == Decimal('50.00')