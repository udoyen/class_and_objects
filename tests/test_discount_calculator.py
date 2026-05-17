"""
Key Patterns Used Here:
@pytest.fixture: Reuses setup code (creating products) 
across multiple tests cleanly without mutating the state between tests.

@pytest.mark.parametrize: Runs the same test logic against multiple inputs 
(like testing different user tiers or percentage cutoffs) to avoid duplicating test methods.

Isolation: Every single strategy is isolated and tested independently 
before checking if the DiscountEngine orchestrates them properly.
"""
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
    return Product('Wireless Mouse', 50.0)

@pytest.fixture
def cheap_product():
    return Product('Sticker', 4.0)


# --- Tests for Product ---
def test_product_initialization(standard_product):
    assert standard_product.name == 'Wireless Mouse'
    assert standard_product.price == 50.0

def test_product_string_representation(standard_product):
    assert str(standard_product) == 'Wireless Mouse - $50.0'


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
    assert strategy.apply_discount(standard_product) == 45.0


# --- Tests for FixedAmountDiscount ---
def test_fixed_amount_discount_applicable(standard_product):
    # 50.0 * 0.9 = 45.0, which is > 5.0 (True)
    strategy = FixedAmountDiscount(5)
    assert strategy.is_applicable(standard_product, 'Regular') is True

def test_fixed_amount_discount_not_applicable(cheap_product):
    # 4.0 * 0.9 = 3.6, which is NOT > 5.0 (False)
    strategy = FixedAmountDiscount(5)
    assert strategy.is_applicable(cheap_product, 'Regular') is False

def test_fixed_amount_discount_calculation(standard_product):
    strategy = FixedAmountDiscount(5)
    assert strategy.apply_discount(standard_product) == 45.0


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
    assert strategy.apply_discount(standard_product) == 40.0


# --- Tests for DiscountEngine ---
def test_discount_engine_picks_best_price(standard_product):
    strategies = [
        PercentageDiscount(10),   # Yields 45.0
        FixedAmountDiscount(5),    # Yields 45.0
        PremiumUserDiscount()      # Yields 40.0
    ]
    engine = DiscountEngine(strategies)
    
    # Premium user should get the PremiumUserDiscount (40.0)
    best_price = engine.calculate_best_price(standard_product, 'Premium')
    assert best_price == 40.0

def test_discount_engine_fallback_to_original_price(cheap_product):
    strategies = [
        PercentageDiscount(80),   # Not applicable (>70%)
        FixedAmountDiscount(5),    # Not applicable (Too expensive for a $4 item)
        PremiumUserDiscount()      # Not applicable for 'Regular' tier
    ]
    engine = DiscountEngine(strategies)
    
    # No strategies apply, should return original price
    best_price = engine.calculate_best_price(cheap_product, 'Regular')
    assert best_price == 4.0