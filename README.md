# trading-ci-lab

Minimal daily-bar backtester focused on **testing & CI** (PnL is not the goal).

## Setup
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## Run Tests + Coverage
```bash
coverage run -m pytest
coverage report --fail-under=90
coverage html  # optional
```

## CI
GitHub Actions workflow at `.github/workflows/ci.yml` runs tests & fails if coverage < 90%.
