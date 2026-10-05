# PasswordGuard test notes

Frontend tests live as lightweight Node checks. Backend tests use pytest from the repository root:

```bash
cd backend && source venv/bin/activate
PYTHONPATH=. pytest ../tests/backend -q
```
