# Methodology

## Theoretical entropy vs real-world strength

Search-space entropy is computed as

\[
H = L \times \log_2(R)
\]

where \(L\) is length and \(R\) is the detected character pool (lowercase 26, uppercase 26, digits 10, specials ~33, plus a conservative Unicode allowance).

This is an **upper bound** for uniformly random strings. Humans select non-uniform passwords, so a string with high \(H\) can still be weak if it contains `qwerty`, a year, or a dictionary word.

Shannon entropy of the observed character distribution is reported as a second reference; it is also not a complete model of attacker behavior.

## Scoring

The 0–100 score is a weighted blend of:

- length, complexity (character classes), entropy, uniqueness
- dictionary resistance, pattern resistance, predictability, attack-resistance composite

It is an **analytical estimate**, not a cryptographic proof. UI copy states this explicitly.

Bands: 0–20 VERY WEAK, 21–40 WEAK, 41–60 MODERATE, 61–80 STRONG, 81–100 VERY STRONG.

## Pattern detection

Sequential alphabets/digits, repeated characters and substrings, keyboard rows, years (1950–2039), common suffixes, and leetspeak substitutions are detected and returned as structured findings.

## Dictionary analysis

Exact match, de-leet match, substring common-word detection, and 3-gram Jaccard similarity against a local educational list. Risk: HIGH / MEDIUM / LOW / VERY_LOW.

## Attack-resistance estimates

| Model | Idea |
| --- | --- |
| Dictionary | Penalize exact/common-word hits |
| Rule-based | Penalize years, suffixes, leet, short mangling |
| Pattern | Invert predictability score |
| Brute force | Scale with theoretical bits, then discount predictability and dictionary hits |

Illustrative offline rate: \(10^9\) guesses/second. No hashes of user passwords are cracked; no remote logins are attempted.

## zxcvbn

Used only as an optional benchmark field. Feature extraction and scoring are independent.
