"""
fetch_surveys.py
Pulls survey data from Smartsheet and writes data/surv_recs.json
in the format expected by gen_dash.py.
"""
import os, json, sys, requests

TOKEN = os.environ.get('SMARTSHEET_TOKEN', '')
SHEET_ID = os.environ.get('SMARTSHEET_SHEET_ID', '2975683629240196')

if not TOKEN:
    print("ERROR: SMARTSHEET_TOKEN not set", file=sys.stderr)
    sys.exit(1)

headers = {'Authorization': f'Bearer {TOKEN}'}
url = f'https://api.smartsheet.com/2.0/sheets/{SHEET_ID}'

print(f"Fetching sheet {SHEET_ID}...")
r = requests.get(url, headers=headers)
if not r.ok:
    print(f"ERROR: {r.status_code} {r.text}", file=sys.stderr)
    sys.exit(1)

data = r.json()
cols = {c['id']: c['title'] for c in data.get('columns', [])}
print("Columns found:", list(cols.values()))

# Flexible column mapper - tries to match by keyword
def find_col(cols_dict, *keywords):
    for cid, title in cols_dict.items():
        t = title.lower().replace(' ', '').replace('_', '').replace('-', '')
        for kw in keywords:
            if kw.lower().replace(' ', '') in t:
                return title
    return None

col_map = {
    'propid':    find_col(cols, 'propertyid', 'propid', 'property id', 'location id'),
    'name':      find_col(cols, 'property name', 'propertyname', 'location name', 'name', 'site'),
    'address':   find_col(cols, 'address', 'addr', 'street'),
    'city':      find_col(cols, 'city'),
    'state':     find_col(cols, 'state', 'st'),
    'date':      find_col(cols, 'inspection date', 'survey date', 'date'),
    'inspector': find_col(cols, 'inspector', 'surveyor', 'assigned', 'technician', 'tech'),
    'severity':  find_col(cols, 'severity', 'priority', 'status'),
    'allDone':   find_col(cols, 'all done', 'alldone', 'complete', 'completed'),
    'woReq':     find_col(cols, 'wo required', 'worequired', 'wo req', 'work order req'),
    'woComp':    find_col(cols, 'wo complete', 'wocomplete', 'wo comp', 'work order comp'),
    'issues':    find_col(cols, 'issues', 'issue', 'problem', 'defect'),
    'signage':   find_col(cols, 'signage', 'sign'),
    'hasDay2':   find_col(cols, 'day 2', 'day2'),
    'ppm':       find_col(cols, 'ppm', 'property manager', 'project manager'),
    'rem':       find_col(cols, 'rem', 'regional', 'engineer'),
    'rd':        find_col(cols, ' rd', 'regional director', 'rd name'),
}

print("Column mapping:", {k: v for k, v in col_map.items() if v})

# Reverse map: column title -> field name
title_to_field = {v: k for k, v in col_map.items() if v}

records = []
for i, row in enumerate(data.get('rows', [])):
    rec = {'rownum': i + 1, '_i': i}
    for cell in row.get('cells', []):
        col_title = cols.get(cell.get('columnId'), '')
        val = cell.get('displayValue') or cell.get('value') or ''
        field = title_to_field.get(col_title)
        if field:
            rec[field] = val
        # Also store raw by title for debugging
        rec[f'_raw_{col_title}'] = val

    # Defaults for missing fields
    for f in ['propid','name','address','city','state','date','inspector',
              'severity','allDone','woReq','woComp','issues','signage',
              'hasDay2','ppm','rem','rd','rsm']:
        rec.setdefault(f, '')
    rec.setdefault('woCreated', '')
    rec.setdefault('woDisp', '')
    rec.setdefault('woCan', '')
    rec.setdefault('color', '#78BE20')
    rec.setdefault('priScore', 0)

    # Normalize severity
    sev = str(rec.get('severity', '')).strip()
    if sev.lower() in ('high', 'red', 'critical'):
        rec['severity'] = 'Blue'
    elif sev.lower() in ('medium', 'yellow', 'warning'):
        rec['severity'] = 'Yellow'
    elif sev.lower() in ('low', 'green', 'ok', 'good', ''):
        rec['severity'] = 'Green'
    # else keep as-is

    records.append(rec)

os.makedirs('data', exist_ok=True)
out = 'data/surv_recs.json'
with open(out, 'w') as f:
    json.dump(records, f)

print(f"Wrote {len(records)} survey records to {out}")
