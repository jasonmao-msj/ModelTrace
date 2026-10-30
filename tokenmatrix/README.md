# Token Matrix bank

This fork is the fingerprint bank used by Token Matrix. Production pins `data/unified_bank.json` at a commit.

## Contents

- GPT and Claude reference rows from upstream `xqy2006/ModelTrace` at `6cd4a8ff0f3f4e49d6d6969dd2fbadfa1569fde2`.
- `gpt-6.1-terra`: 72 rows that we collected on 2026-10-30. They come from two Codex subscription accounts (`collector-1` and `collector-2`), with 36 rows from each. We used the upstream `challenge_suite.fingerprint_suite()` prompts, so all 12 environments and 36 challenges are covered. Rows have `config_id: tokenmatrix-collection` and `provider: codex`.
- `gpt-6.1-sol` is not included. Public fork samples confused it with `gpt-6-astra`: with them added, held-out accuracy was 67% for `gpt-6.1-sol`, and `gpt-6-astra` dropped from 94% to 69%.

## Rebuild

```sh
pip install -r requirements.txt
python rebuild_unified_bank.py
cp data/unified_bank.json static/data/unified_bank.json
python tokenmatrix/validate_holdout.py   # leave-one-challenge-out accuracy for GPT 6.x
```

Held-out single-response accuracy for this bank: `gpt-6.1-terra` 98.6%, `gpt-6-luna` 100%, `gpt-6-astra` 94.4% and `gpt-6-sol` 88.9%.
