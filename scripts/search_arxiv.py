"""Run the fixed arXiv search through the arXiv API, save the raw Atom XML unchanged, and list records first posted on or after 2025-01-01.

Usage: python scripts/search_arxiv.py --query-file protocol/queries/arxiv.txt --label arxiv
Output: searches/raw/<label>_<UTC timestamp>_pNN.atom.xml, searches/raw/<label>_<UTC timestamp>.csv, and a line in searches/SEARCH_LOG.md
"""
import argparse, csv, datetime, pathlib, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom', 'os': 'http://a9.com/-/spec/opensearch/1.1/'}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--query-file', required=True); ap.add_argument('--label', required=True)
    a = ap.parse_args()
    query = pathlib.Path(a.query_file).read_text(encoding='utf8').strip()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%MZ')
    out = pathlib.Path('searches/raw'); out.mkdir(parents=True, exist_ok=True)
    rows, start, total, page = [], 0, None, 0
    while total is None or start < total:
        params = urllib.parse.urlencode({'search_query': query, 'start': start, 'max_results': 200, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
        with urllib.request.urlopen(f'http://export.arxiv.org/api/query?{params}', timeout=60) as r:
            xml = r.read()
        (out / f'{a.label}_{stamp}_p{page:02d}.atom.xml').write_bytes(xml)
        root = ET.fromstring(xml)
        total = int(root.find('os:totalResults', NS).text)
        entries = root.findall('a:entry', NS)
        if not entries: break
        for e in entries:
            doi = e.find('arxiv:doi', NS)
            rows.append({'arxiv_id': e.find('a:id', NS).text.rsplit('/abs/', 1)[-1], 'published': e.find('a:published', NS).text[:10],
                         'title': ' '.join(e.find('a:title', NS).text.split()), 'abstract': ' '.join(e.find('a:summary', NS).text.split()),
                         'authors': '; '.join(x.find('a:name', NS).text for x in e.findall('a:author', NS)),
                         'doi': doi.text if doi is not None else ''})
        start += len(entries); page += 1; time.sleep(3)  # arXiv asks for 3 s between calls
    kept = [r for r in rows if r['published'] >= '2025-01-01']
    csv_path = out / f'{a.label}_{stamp}.csv'
    with open(csv_path, 'w', newline='', encoding='utf8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ['arxiv_id']); w.writeheader(); w.writerows(kept)
    log = pathlib.Path('searches/SEARCH_LOG.md')
    if not log.exists(): log.write_text('| Source | Label | Run (UTC) | Count reported | Records saved | File |\n|---|---|---|---|---|---|\n', encoding='utf8')
    with open(log, 'a', encoding='utf8') as fh:
        fh.write(f'| arXiv | {a.label} | {stamp} | {total} (all dates) | {len(kept)} (from 2025-01-01) | {csv_path.as_posix()} |\n')
    print(f'{a.label}: arXiv reported {total}; downloaded {len(rows)}; kept {len(kept)} from 2025-01-01 -> {csv_path}')

if __name__ == '__main__':
    main()
