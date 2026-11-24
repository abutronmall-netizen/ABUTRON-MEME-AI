# ABUTRON MEME AI

Autonomous multi-chain hybrid AI meme-coin trading platform — **paper-only development foundation**.

> This repository is not a running autonomous trading system. FOMO automated execution support is unverified. Live trading is prohibited in V1 development.

## Owner-approved configuration

- Initial simulated capital: **$100**
- Strategy budgets: **80% copy trading / 20% autonomous AI**
- Execution budgets: **90% FOMO / 10% dedicated wallets**
- Blockchain budgets: **50% Solana / 25% Base / 25% BNB Chain**
- Eligible realized net gains: **70% reinvest / 30% reserve**, after prior trading-loss recovery
- Maximum peak-to-trough drawdown policy: **30%**
- Worker target: **24 logical workers** (not yet implemented)
- Intelligence target: ML + neural models + agentic coordination (not yet implemented)

Each allocation is a *different dimension of the same trading capital*, not an additional pool.

## Run the current local API

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
uvicorn abutron.api:app --host 127.0.0.1 --port 8000
```

Try `GET /api/v1/health` and `GET /api/v1/portfolio`.

## Tests

```bash
pytest -q
```

Tests are included; see [implementation status](docs/STATUS.md) for verification caveats.

## Safety and known limitations

- **No live order submission, wallet signing or transfer functionality.**
- Read-only API uses an in-memory prototype; persistence and order accounting are not yet built.
- Paper P&L accounting currently accepts only already-completed trade net results through internal Python methods; no trade simulation API exists.
- Cross-chain market discovery and smart-money automation remain planned.
- Keep this repository isolated from ABUTRON FX infrastructure.
