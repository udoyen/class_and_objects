from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

class Product:
    # Use Decimal for price instead of float
    def __init__(self, name: str, price: Decimal) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        # F-strings automatically respect the format on Decimal objects
        return f'{self.name} - ${self.price:.2f}'

class DiscountStrategy(ABC):
    @abstractmethod
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def apply_discount(self, product: Product) -> Decimal:
        pass # pragma: no cover

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: int) -> None:
        self.percent = percent

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return self.percent <= 70

    def apply_discount(self, product: Product) -> Decimal:
        # Convert percent to a Decimal fraction and perform exact math
        discount_factor = Decimal(1) - (Decimal(self.percent) / Decimal(100))
        calculated = product.price * discount_factor
        
        # Quantize rounds exactly to 2 decimal places using standard financial rounding
        return calculated.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class FixedAmountDiscount(DiscountStrategy):
    # Use Decimal for the fixed discount amount
    def __init__(self, amount: Decimal) -> None:
        self.amount = amount

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        # 0.9 becomes Decimal('0.9')
        return product.price * Decimal('0.9') > self.amount

    def apply_discount(self, product: Product) -> Decimal:
        return product.price - self.amount

class PremiumUserDiscount(DiscountStrategy):
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return user_tier.lower() == 'premium'

    def apply_discount(self, product: Product) -> Decimal:
        # 0.8 becomes Decimal('0.8')
        calculated = product.price * Decimal('0.8')
        return calculated.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class DiscountEngine:
    def __init__(self, strategies: list[DiscountStrategy]) -> None:
        self.strategies = strategies

    def calculate_best_price(self, product: Product, user_tier: str) -> Decimal:
        prices = [product.price]

        for strategy in self.strategies:
            if strategy.is_applicable(product, user_tier):
                discounted = strategy.apply_discount(product)
                prices.append(discounted)

        return min(prices)

if __name__ == '__main__': # pragma: no cover
    # CRITICAL: Always pass numeric values as strings to Decimal to preserve accuracy
    product = Product('Wireless Mouse', Decimal('50.00'))
    user_tier = 'Premium'

    strategies = [
        PercentageDiscount(10),
        FixedAmountDiscount(Decimal('5.00')),
        PremiumUserDiscount()
    ]

    engine = DiscountEngine(strategies)
    best_price = engine.calculate_best_price(product, user_tier)
    print(f"Best price for {product.name} for {user_tier} user: ${best_price:.2f}")