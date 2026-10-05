# Security considerations

## Non-goals

This project must **not** be used to attack real accounts, websites, or authentication services. Attack modules estimate resistance; they do not implement an operational cracker.

## Password handling

| Control | Implementation |
| --- | --- |
| No database of passwords | SQLite is unused for secrets; none stored |
| No logs of secrets | Flask logs host/port only; query `password=` rejected |
| No URL secrets | `before_request` blocks `password` query params |
| No localStorage of secrets | Only theme preference is persisted |
| History | sessionStorage metadata: timestamp, score, risk, entropy, strength |
| API | Never echoes the password |
| Cache | `Cache-Control: no-store` |

## Headers

`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`.

## Data files

`backend/data/sample/common_passwords.txt` is a public-knowledge trivial list for teaching. Do not commit dumps of real user credentials.

## Threat model (academic)

The local user is trusted. The main risks are accidental persistence (clipboard, screenshots, browser password managers prompting to save). The UI uses `autocomplete="off"` and clears fields after analysis/compare.

## Future work (safe)

Enterprise policy checks on **anonymized** metadata, password-manager integration, privacy-preserving breach lookup. Never harvest credentials or attack third parties.
