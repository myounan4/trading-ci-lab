# trading-ci-lab

Minimal daily-bar backtester focused on testing & CI

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

<img width="595" height="192" alt="image" src="https://github.com/user-attachments/assets/ae097a9b-8c78-41d4-aeaa-a63ce64b8f6e" />

