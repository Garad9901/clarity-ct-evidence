"""Agreement and outcome statistics fixed in PROTOCOL.md section 8. No numbers are typed in; everything is read from the coding sheets.

  python scripts/agreement_stats.py kappa  --a sheetA.csv --b sheetB.csv --field decision
  python scripts/agreement_stats.py fleiss --sheets s1.csv s2.csv s3.csv s4.csv --field decision
  python scripts/agreement_stats.py proportion --sheet consensus.csv --field category --positive R E Q
  python scripts/agreement_stats.py rq4 --sheet consensus.csv
"""
import argparse, csv, math, random
from collections import Counter
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

SEED, BOOT, Z = 20261019, 2000, 1.959963984540054

def load(path, field):
    with open(path, encoding='utf8', newline='') as fh:
        return {r['record_id']: (r.get(field) or '').strip().upper() for r in csv.DictReader(fh)}

def cohen(x, y):
    n = len(x); cats = sorted(set(x) | set(y))
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[c] * cy[c] for c in cats) / n ** 2
    return float('nan') if pe == 1 else (po - pe) / (1 - pe)

def kappa_ci(x, y):
    rng = random.Random(SEED); n = len(x); vals = []
    for _ in range(BOOT):
        idx = [rng.randrange(n) for _ in range(n)]
        k = cohen([x[i] for i in idx], [y[i] for i in idx])
        if not math.isnan(k): vals.append(k)
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]

def fleiss(table):
    n = len(table); m = sum(table[0].values()); cats = sorted({c for row in table for c in row})
    p_j = {c: sum(row.get(c, 0) for row in table) / (n * m) for c in cats}
    P_i = [(sum(v * v for v in row.values()) - m) / (m * (m - 1)) for row in table]
    Pbar, Pe = sum(P_i) / n, sum(p * p for p in p_j.values())
    return (Pbar - Pe) / (1 - Pe)

def wilson(k, n):
    p = k / n; d = 1 + Z * Z / n; c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return p, c - h, c + h

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    k = sub.add_parser('kappa'); k.add_argument('--a', required=True); k.add_argument('--b', required=True); k.add_argument('--field', required=True)
    f = sub.add_parser('fleiss'); f.add_argument('--sheets', nargs='+', required=True); f.add_argument('--field', required=True)
    p = sub.add_parser('proportion'); p.add_argument('--sheet', required=True); p.add_argument('--field', required=True); p.add_argument('--positive', nargs='+', required=True)
    r = sub.add_parser('rq4'); r.add_argument('--sheet', required=True)
    a = ap.parse_args()
    if a.cmd == 'kappa':
        A, B = load(a.a, a.field), load(a.b, a.field)
        ids = sorted(i for i in A if i in B and A[i] and B[i])
        x, y = [A[i] for i in ids], [B[i] for i in ids]
        lo, hi = kappa_ci(x, y)
        print(f'{a.field}: n = {len(ids)}, raw agreement = {sum(u == v for u, v in zip(x, y)) / len(ids):.3f}, '
              f'Cohen kappa = {cohen(x, y):.3f} (95% bootstrap CI {lo:.3f} to {hi:.3f})')
    elif a.cmd == 'fleiss':
        sheets = [load(s, a.field) for s in a.sheets]
        ids = sorted(set.intersection(*[set(i for i, v in s.items() if v) for s in sheets]))
        table = [Counter(s[i] for s in sheets) for i in ids]
        print(f'{a.field}: n = {len(ids)} records, {len(sheets)} coders, Fleiss kappa = {fleiss(table):.3f}')
    elif a.cmd == 'proportion':
        S = load(a.sheet, a.field); vals = [v for v in S.values() if v]
        kpos = sum(v in {x.upper() for x in a.positive} for v in vals)
        ph, lo, hi = wilson(kpos, len(vals))
        print(f'{a.field} in {a.positive}: {kpos}/{len(vals)} = {100 * ph:.1f}% (Wilson 95% CI {100 * lo:.1f} to {100 * hi:.1f})')
    elif a.cmd == 'rq4':
        cat, ext = load(a.sheet, 'category'), load(a.sheet, 'ext_test')
        ids = [i for i in cat if cat[i] and ext.get(i) in ('Y', 'N', 'T')]
        t = [[0, 0], [0, 0]]
        for i in ids:
            t[0 if cat[i] in ('R', 'E', 'Q') else 1][0 if ext[i] == 'Y' else 1] += 1
        _, pval = fisher_exact(t)
        orr = odds_ratio(t); ci = orr.confidence_interval(0.95)
        print(f'Assessed beyond examples (rows: yes, no) by external test set (cols: yes, no/temporal): {t}; n = {len(ids)}; '
              f'Fisher two-sided p = {pval:.4f}; OR = {orr.statistic:.2f} (95% CI {ci.low:.2f} to {ci.high:.2f}). '
              f'Studies with ext_test NR are excluded from this test.')

if __name__ == '__main__':
    main()
