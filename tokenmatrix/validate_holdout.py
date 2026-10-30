"""Hold out each challenge_id, rebuild, and score held-out GPT 6.x rows with the single-response predictor."""
import json, sys, collections
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from bank_builder import build_bank, read_rows
from fingerprint import robust_score_numbers
from pathlib import Path
rows = []
for fam, name, path in [('gpt','GPT','data/gpt_reference.jsonl'),('claude','Claude','data/claude_reference.jsonl')]:
    rows += [{**r,'family_id':fam,'family_name':name} for r in read_rows(Path(path))]
targets = sys.argv[1:] or ['gpt-6.1-terra','gpt-6-sol','gpt-6-astra','gpt-6-luna']
conf = collections.defaultdict(collections.Counter)
for hold in sorted({r['challenge_id'] for r in rows}):
    train = [r for r in rows if r['challenge_id'] != hold]
    bank = build_bank(train)
    ids = bank['robust']['model_order']
    for r in rows:
        if r['challenge_id'] == hold and r['source'] in targets:
            s = robust_score_numbers(r['numbers'], bank)['fused']
            conf[r['source']][ids[max(range(len(s)), key=s.__getitem__)]] += 1
for m in targets:
    c = conf[m]; n = sum(c.values())
    print(m, 'n=%d acc=%.3f' % (n, c[m]/n if n else 0), dict(c.most_common(4)))
