# Password Security Evaluation and Attack-Resistance Analysis

Academic full-stack platform that evaluates password security **without storing plaintext passwords**. The interface is a dark cybersecurity dashboard; the backend combines custom feature extraction, entropy modeling, dictionary/pattern heuristics, educational attack-resistance estimates, and a scikit-learn classifier.

## Problem statement

People routinely choose passwords that look complex but remain predictable. Theoretical entropy overstates security when the secret contains dictionary words, years, keyboard walks, or common suffixes. This project measures those gaps and explains them for teaching and viva demonstration.

## Objectives

- Analyze composition, entropy, patterns, and dictionary similarity in memory only.
- Estimate resistance to dictionary, rule-based, pattern, and brute-force *models* (not live attacks).
- Classify strength with a trained Random Forest (compared against Logistic Regression and Decision Tree).
- Present results on a professional dashboard with charts, recommendations, and privacy guarantees.

## Features

- Analyze, attack-resistance, ML insights, comparison, history, improvement simulator
- Score 0–100 and labels: VERY WEAK → VERY STRONG
- Demo analysis so the dashboard is never empty
- Dark/light theme (theme preference only is persisted)
- Session history of **metadata only**

## Architecture

```text
Frontend (React + Vite)
   |
   | REST /api
   ↓
Flask Backend
   ├── Feature extraction
   ├── Entropy analysis
   ├── Pattern detection
   ├── Dictionary analysis
   ├── Attack-resistance estimates
   ├── ML prediction
   └── Recommendation engine
```

See `docs/architecture.md`.

## Technologies

Python 3, Flask, pandas, numpy, scikit-learn, joblib, zxcvbn (benchmark only), React, Vite, Tailwind CSS, Recharts, Lucide.

## ML methodology

Synthetic passwords are generated, labeled by the project's scoring engine, then used to train three models. The best model (preferring Random Forest when competitive) is serialized with joblib. Metrics are written to `backend/models/evaluation.json` and shown on ML Insights. See `docs/ml.md`.

## Dataset methodology

No leaked credential dumps. Training uses synthetic strings. The local dictionary is a textbook-style list of trivial passwords (`password`, `123456`, `qwerty`, …) in `backend/data/sample/`.

## Attack-resistance methodology

Scores are heuristic estimates from length, character pool, dictionary similarity, and pattern detections. Brute-force time uses \(H = L \times \log_2(R)\) and an illustrative \(10^9\) guesses/second. **No authentication systems are targeted.** See `docs/methodology.md` and `docs/security.md`.

## Installation

Requires Python 3.10+, Node.js 18+, and macOS/Linux.

```bash
chmod +x run.sh
./run.sh
```

`run.sh` creates a venv, installs Python deps, trains the model if missing, starts Flask on `127.0.0.1:5001`, and starts Vite on `http://127.0.0.1:5173`.

### Running the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python ml/train_model.py   # first time
PYTHONPATH=. python app.py
```

### Running the frontend

```bash
cd frontend
npm install
npm run dev
```

Copy `.env.example` to `backend/.env` only if you need to override host/port.

## Testing

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest ../tests/backend -q
cd ../frontend && npm test
```

## Screenshots

Run the app locally and capture the Dashboard, Analyze, Attack Analysis, and ML Insights pages for the report.

## Security considerations

- Passwords are not stored, logged, placed in URLs, or returned in API responses.
- History stores only timestamp, score, risk, entropy, and strength in `sessionStorage`.
- Analysis is educational; it is not a cracking toolkit.

## Limitations

- Theoretical entropy ≠ real-world guessability.
- Dictionary coverage is a small demo list.
- ML labels come from the same heuristic engine (supervised consistency, not an external ground truth).
- Offline guess-rate assumptions are illustrative.

## Future enhancements

Password manager integration, enterprise policy analysis on anonymized data, privacy-preserving breach notification, transformer-based estimators, adaptive risk scoring, compliance reporting. Do not implement credential harvesting or attacks on third-party accounts.

## Team / author

[Your Name] — Final-year engineering / academic demonstration project.
