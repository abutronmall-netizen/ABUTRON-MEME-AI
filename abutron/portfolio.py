"""Deterministic paper portfolio accounting; no signing or live execution."""
from dataclasses import dataclass, field
from decimal import Decimal
from .config import CapitalPolicy

D = Decimal
CENT = D("0.01")

def money(value: Decimal) -> Decimal:
    return value.quantize(CENT)

@dataclass
class PaperPortfolio:
    policy: CapitalPolicy = field(default_factory=CapitalPolicy)
    trading_equity: Decimal = field(init=False)
    profit_reserve: Decimal = D("0.00")
    high_watermark: Decimal = field(init=False)
    loss_carryforward: Decimal = D("0.00")
    distributed_profit: Decimal = D("0.00")

    def __post_init__(self) -> None:
        self.trading_equity = self.policy.starting_capital
        self.high_watermark = self.trading_equity

    def budgets(self, dimension: str) -> dict[str, Decimal]:
        if dimension not in ("strategy", "execution", "chain"):
            raise ValueError("Unknown allocation dimension")
        weights = getattr(self.policy, dimension)
        return {name: money(self.trading_equity * weight) for name, weight in weights.items()}

    def record_closed_trade(self, realized_net_pnl: Decimal) -> dict[str, Decimal]:
        """Book fully closed paper-trade net P&L; positive gains first recover prior losses.

        Caller must supply realized P&L net of fees and slippage. This prototype assumes
        no open positions, pending orders, external cashflows, or unsettled executions.
        """
        if not realized_net_pnl.is_finite():
            raise ValueError("Non-finite P&L")
        pnl = money(realized_net_pnl)
        eligible = D("0.00")
        if pnl < 0:
            self.loss_carryforward += -pnl
            self.trading_equity += pnl
        elif pnl > 0:
            recovery = min(pnl, self.loss_carryforward)
            self.loss_carryforward -= recovery
            eligible = pnl - recovery
            # Recovery is retained entirely in trading equity.
            reinvest = money(eligible * self.policy.reinvestment)
            reserve = eligible - reinvest
            self.trading_equity += recovery + reinvest
            self.profit_reserve += reserve
            self.distributed_profit += eligible
        self.high_watermark = max(self.high_watermark, self.trading_equity)
        return {"trading_equity": self.trading_equity, "profit_reserve": self.profit_reserve,
                "loss_carryforward": self.loss_carryforward, "eligible_profit": eligible}

    @property
    def drawdown_pct(self) -> Decimal:
        return (self.high_watermark - self.trading_equity) / self.high_watermark * 100

    @property
    def drawdown_limit_reached(self) -> bool:
        return self.drawdown_pct >= self.policy.maximum_drawdown * 100

    @property
    def total_value(self) -> Decimal:
        return self.trading_equity + self.profit_reserve
