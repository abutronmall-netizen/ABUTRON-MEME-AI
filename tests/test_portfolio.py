from decimal import Decimal as D
import pytest
from abutron.config import CapitalPolicy
from abutron.portfolio import PaperPortfolio

def test_initial_budget_dimensions_are_not_additive():
    p = PaperPortfolio()
    assert p.budgets("strategy") == {"copy_trading": D("80.00"), "autonomous_ai": D("20.00")}
    assert p.budgets("execution") == {"fomo": D("90.00"), "dedicated_wallets": D("10.00")}
    assert p.budgets("chain") == {"solana": D("50.00"), "base": D("25.00"), "bnb_chain": D("25.00")}
    assert p.total_value == D("100.00")

def test_net_profit_70_30_distribution():
    p = PaperPortfolio()
    outcome = p.record_closed_trade(D("50.00"))
    assert outcome["eligible_profit"] == D("50.00")
    assert p.trading_equity == D("135.00")
    assert p.profit_reserve == D("15.00")
    assert p.total_value == D("150.00")

def test_loss_recovery_precedes_distribution():
    p = PaperPortfolio()
    p.record_closed_trade(D("-20.00"))
    assert p.loss_carryforward == D("20.00")
    p.record_closed_trade(D("15.00"))
    assert p.trading_equity == D("95.00")
    assert p.profit_reserve == D("0.00")
    p.record_closed_trade(D("15.00"))
    assert p.loss_carryforward == D("0.00")
    assert p.trading_equity == D("107.00")
    assert p.profit_reserve == D("3.00")

def test_peak_to_trough_drawdown():
    p = PaperPortfolio()
    p.record_closed_trade(D("-30.00"))
    assert p.drawdown_pct == D("30.0")
    assert p.drawdown_limit_reached

def test_invalid_allocations_rejected():
    with pytest.raises(ValueError):
        CapitalPolicy(strategy={"copy_trading": D("0.50"), "autonomous_ai": D("0.20")})

def test_no_live_trading_routes():
    from fastapi.testclient import TestClient
    from abutron.api import app
    client = TestClient(app)
    assert client.get("/api/v1/health").json()["live_trading_enabled"] is False
    assert client.get("/api/v1/portfolio").json()["environment"] == "paper"
    assert client.post("/api/v1/orders").status_code == 404
