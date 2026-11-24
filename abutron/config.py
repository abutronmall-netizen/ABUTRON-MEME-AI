"""Owner-approved, immutable V1 allocation defaults."""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Mapping

D = Decimal

@dataclass(frozen=True)
class CapitalPolicy:
    starting_capital: Decimal = D("100.00")
    strategy: Mapping[str, Decimal] = field(default_factory=lambda: {
        "copy_trading": D("0.80"), "autonomous_ai": D("0.20")
    })
    execution: Mapping[str, Decimal] = field(default_factory=lambda: {
        "fomo": D("0.90"), "dedicated_wallets": D("0.10")
    })
    chain: Mapping[str, Decimal] = field(default_factory=lambda: {
        "solana": D("0.50"), "base": D("0.25"), "bnb_chain": D("0.25")
    })
    reinvestment: Decimal = D("0.70")
    profit_reserve: Decimal = D("0.30")
    maximum_drawdown: Decimal = D("0.30")

    def __post_init__(self) -> None:
        for name in ("strategy", "execution", "chain"):
            allocations = getattr(self, name)
            if not allocations or any(amount < 0 or amount > 1 for amount in allocations.values()):
                raise ValueError(f"Invalid {name} allocation")
            if sum(allocations.values(), D("0")) != D("1"):
                raise ValueError(f"{name} allocation must total 100%")
        if self.reinvestment + self.profit_reserve != D("1"):
            raise ValueError("Profit distribution must total 100%")
        if self.starting_capital <= 0 or not D("0") < self.maximum_drawdown < D("1"):
            raise ValueError("Invalid starting capital or drawdown")
