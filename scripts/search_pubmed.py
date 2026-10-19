"""Run a fixed PubMed search through NCBI E-utilities and save the raw MEDLINE records unchanged.

Usage: python scripts/search_pubmed.py --query-file protocol/queries/pubmed_main.txt --label pubmed_main --email you@example.org
Output: searches/raw/<label>_<UTC timestamp>.medline.txt and a line appended to searches/SEARCH_LOG.md
"""
import argparse, datetime, pathlib, time, urllib.parse, urllib.request, json

BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

def get(url, params):
    q = urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(f'{BASE}{url}?{q}', timeout=60) as r:
                return r.read().decode('utf8')
        except Exception as e:  # network or rate limit: wait and retry
            if attempt == 4: raise
            time.sleep(3 * (attempt + 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--query-file', required=True); ap.add_argument('--label', required=True); ap.add_argument('--email', required=True)
    a = ap.parse_args()
    query = pathlib.Path(a.query_file).read_text(encoding='utf8').strip()
    common = {'db': 'pubmed', 'tool': 'clarity_ct_review', 'email': a.email}
    res = json.loads(get('esearch.fcgi', {**common, 'term': query, 'usehistory': 'y', 'retmode': 'json', 'retmax': 0}))['esearchresult']
    count, webenv, qk = int(res['count']), res['webenv'], res['querykey']
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%MZ')
    out = pathlib.Path('searches/raw'); out.mkdir(parents=True, exist_ok=True)
    path = out / f'{a.label}_{stamp}.medline.txt'
    with open(path, 'w', encoding='utf8') as fh:
        for start in range(0, count, 200):
            fh.write(get('efetch.fcgi', {**common, 'query_key': qk, 'WebEnv': webenv, 'retstart': start, 'retmax': 200,
                                         'rettype': 'medline', 'retmode': 'text'}))
            time.sleep(0.4)
    n_written = sum(1 for line in open(path, encoding='utf8') if line.startswith('PMID-'))
    log = pathlib.Path('searches/SEARCH_LOG.md')
    if not log.exists(): log.write_text('| Source | Label | Run (UTC) | Count reported | Records saved | File |\n|---|---|---|---|---|---|\n', encoding='utf8')
    with open(log, 'a', encoding='utf8') as fh:
        fh.write(f'| PubMed | {a.label} | {stamp} | {count} | {n_written} | {path.as_posix()} |\n')
    print(f'{a.label}: PubMed reported {count}, saved {n_written} -> {path}')
    if n_written != count: print('WARNING: saved count differs from reported count; record this in DEVIATIONS.md')

if __name__ == '__main__':
    main()
