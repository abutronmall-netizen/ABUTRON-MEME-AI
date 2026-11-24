"""Read-only API. No real transaction or signing endpoints."""
from fastapi import FastAPI
from .portfolio import PaperPortfolio

app = FastAPI(title="ABUTRON MEME AI", version="0.1.0")
portfolio = PaperPortfolio()

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "environment": "paper", "live_trading_enabled": False,
            "stage": "phase1-foundation"}

@app.get("/api/v1/portfolio")
def get_portfolio():
    return {
        "environment": "paper",
        "live_trading_enabled": False,
        "starting_capital_usd": str(portfolio.policy.starting_capital),
        "trading_equity_usd": str(portfolio.trading_equity),
        "profit_reserve_usd": str(portfolio.profit_reserve),
        "total_value_usd": str(portfolio.total_value),
        "drawdown_pct": str(portfolio.drawdown_pct),
        "maximum_drawdown_pct": "30",
        "budgets": {name: {k: str(v) for k, v in portfolio.budgets(name).items()}
                    for name in ("strategy", "execution", "chain")},
        "note": "In-memory demonstration only; persistence and execution are not implemented."
    }
