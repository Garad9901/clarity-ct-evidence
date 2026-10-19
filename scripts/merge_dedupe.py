"""Merge the search exports, remove duplicates and prepare blank, blinded screening sheets for the two coding pairs.

Usage:
  python scripts/merge_dedupe.py --pubmed searches/raw/pubmed_main_*.medline.txt --ieee searches/raw/ieee_*.csv \
      --arxiv searches/raw/arxiv_*.csv --prior records/selected.json records/excluded.json records/gandomkar_2022_ref85.json
Outputs (screening/): master_records.csv, dedup_report.md, pilot_<coder>.csv, main_<coder>.csv.
Duplicates: same DOI (case-insensitive), otherwise same normalised title. Seed 20261019 fixes the random split and the pilot draw.
"""
import argparse, csv, glob, json, pathlib, random, re, unicodedata

SEED = 20261019
PAIRS = {'pair1': ['Om_Gawande', 'Aditi_Parshivanikar'], 'pair2': ['Yash_Garad', 'Vikas_Bhowate']}
SHEET_COLS = ['record_id', 'title', 'abstract', 'year', 'doi', 'link', 'decision', 'exclusion_reason', 'notes']

def norm_title(t):
    t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', t)[:150]

def norm_doi(d):
    d = (d or '').strip().lower()
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:\s*)', '', d)

def parse_medline(path):
    recs, cur, key = [], {}, None
    for line in open(path, encoding='utf8'):
        if not line.strip():
            if cur: recs.append(cur); cur = {}; key = None
            continue
        if line[:4].strip() and line[4:6] == '- ':
            key, val = line[:4].strip(), line[6:].rstrip('\n')
            cur.setdefault(key, []).append(val)
        elif key:
            cur[key][-1] += ' ' + line.strip()
    if cur: recs.append(cur)
    out = []
    for r in recs:
        doi = next((x.split(' ')[0] for x in r.get('LID', []) + r.get('AID', []) if x.endswith('[doi]')), '')
        out.append({'source': 'PubMed', 'title': ' '.join(r.get('TI', [''])), 'abstract': ' '.join(r.get('AB', [''])),
                    'year': (r.get('DP', [''])[0])[:4], 'doi': doi, 'pmid': r.get('PMID', [''])[0], 'arxiv_id': ''})
    return out

def parse_ieee(path):
    out = []
    with open(path, encoding='utf-8-sig', newline='') as fh:
        for r in csv.DictReader(fh):
            out.append({'source': 'IEEE Xplore', 'title': r.get('Document Title', ''), 'abstract': r.get('Abstract', ''),
                        'year': r.get('Publication Year', ''), 'doi': r.get('DOI', ''), 'pmid': '', 'arxiv_id': ''})
    return out

def parse_arxiv(path):
    with open(path, encoding='utf8', newline='') as fh:
        return [{'source': 'arXiv', 'title': r['title'], 'abstract': r['abstract'], 'year': r['published'][:4], 'doi': r.get('doi', ''),
                 'pmid': '', 'arxiv_id': r['arxiv_id']} for r in csv.DictReader(fh)]

def parse_prior(path):
    data = json.load(open(path, encoding='utf8'))
    data = data if isinstance(data, list) else [data]
    return [{'source': 'Prior search (evidence-v1.0)', 'title': x.get('title', ''), 'abstract': '', 'year': str(x.get('year') or ''),
             'doi': x.get('doi') or '', 'pmid': '', 'arxiv_id': ''} for x in data]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pubmed', nargs='*', default=[]); ap.add_argument('--ieee', nargs='*', default=[])
    ap.add_argument('--arxiv', nargs='*', default=[]); ap.add_argument('--prior', nargs='*', default=[])
    a = ap.parse_args()
    raw = []
    for pattern_list, fn in ((a.pubmed, parse_medline), (a.ieee, parse_ieee), (a.arxiv, parse_arxiv), (a.prior, parse_prior)):
        for pat in pattern_list:
            for p in sorted(glob.glob(pat)): raw += fn(p)
    per_source = {}
    for r in raw: per_source[r['source']] = per_source.get(r['source'], 0) + 1
    merged, by_doi, by_title = [], {}, {}
    for r in raw:
        d, t = norm_doi(r['doi']), norm_title(r['title'])
        hit = by_doi.get(d) if d else None
        if hit is None and t: hit = by_title.get(t)
        if hit is not None:
            m = merged[hit]
            m['sources'] = sorted(set(m['sources']) | {r['source']})
            for k in ('abstract', 'doi', 'pmid', 'arxiv_id', 'year'):
                if not m[k] and r[k]: m[k] = r[k]
        else:
            hit = len(merged); merged.append({**{k: r[k] for k in ('title', 'abstract', 'year', 'doi', 'pmid', 'arxiv_id')}, 'sources': [r['source']]})
        if d: by_doi[d] = hit
        if t: by_title[t] = hit
    rng = random.Random(SEED)
    order = list(range(len(merged))); rng.shuffle(order)
    for n, i in enumerate(order, 1): merged[i]['record_id'] = f'R{n:04d}'
    merged.sort(key=lambda m: m['record_id'])
    for m in merged:
        m['link'] = (f"https://doi.org/{norm_doi(m['doi'])}" if m['doi'] else
                     f"https://pubmed.ncbi.nlm.nih.gov/{m['pmid']}/" if m['pmid'] else
                     f"https://arxiv.org/abs/{m['arxiv_id']}" if m['arxiv_id'] else '')
    ids = [m['record_id'] for m in merged]
    pilot = set(rng.sample(ids, min(20, len(ids))))
    rest = [i for i in ids if i not in pilot]
    half = {'pair1': set(rest[0::2]), 'pair2': set(rest[1::2])}
    out = pathlib.Path('screening'); out.mkdir(exist_ok=True)
    with open(out / 'master_records.csv', 'w', newline='', encoding='utf8') as fh:
        cols = ['record_id', 'title', 'abstract', 'year', 'doi', 'pmid', 'arxiv_id', 'link', 'sources', 'pilot', 'pair']
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for m in merged:
            pair = 'both (pilot)' if m['record_id'] in pilot else ('pair1' if m['record_id'] in half['pair1'] else 'pair2')
            w.writerow({**{k: m.get(k, '') for k in cols}, 'sources': '; '.join(m['sources']), 'pilot': m['record_id'] in pilot, 'pair': pair})
    blank = {'decision': '', 'exclusion_reason': '', 'notes': ''}
    for pair, coders in PAIRS.items():
        for coder in coders:
            for kind, keep in (('pilot', pilot), ('main', half[pair] | pilot)):
                with open(out / f'{kind}_{coder}.csv', 'w', newline='', encoding='utf8') as fh:
                    w = csv.DictWriter(fh, fieldnames=SHEET_COLS); w.writeheader()
                    for m in merged:
                        if m['record_id'] in keep: w.writerow({**{k: m.get(k, '') for k in SHEET_COLS if k not in blank}, **blank})
    with open(out / 'dedup_report.md', 'w', encoding='utf8') as fh:
        fh.write('# Deduplication report\n\n| Source | Records |\n|---|---|\n')
        for s, n in per_source.items(): fh.write(f'| {s} | {n} |\n')
        fh.write(f'| Total before deduplication | {len(raw)} |\n| Duplicates removed | {len(raw) - len(merged)} |\n| Unique records | {len(merged)} |\n')
        fh.write(f'\nPilot records (screened by all four coders): {len(pilot)}. Pair 1 main: {len(half["pair1"])}. Pair 2 main: {len(half["pair2"])}. Seed {SEED}.\n')
    print(open(out / 'dedup_report.md', encoding='utf8').read())

if __name__ == '__main__':
    main()
