"""
fetch_surveys.py
Pulls survey data from Smartsheet "Conversion Readiness Assessment 2026"
and writes data/surv_recs.json for gen_dash.py.
"""
import os, json, sys, requests

TOKEN    = os.environ.get('SMARTSHEET_TOKEN', '')
SHEET_ID = os.environ.get('SMARTSHEET_SHEET_ID', '2975683629240196')

if not TOKEN:
    print("ERROR: SMARTSHEET_TOKEN not set", file=sys.stderr)
    sys.exit(1)

hdrs = {'Authorization': f'Bearer {TOKEN}'}
print(f"Fetching sheet {SHEET_ID}...")
r = requests.get(f'https://api.smartsheet.com/2.0/sheets/{SHEET_ID}', headers=hdrs)
if not r.ok:
    print(f"ERROR: {r.status_code} {r.text}", file=sys.stderr)
    sys.exit(1)

data   = r.json()
cols   = {c['id']: c['title'] for c in data.get('columns', [])}
print("Columns:", list(cols.values()))

# --- Exact column name map (case-insensitive) ---
def col_id(name):
    name_l = name.lower()
    for cid, title in cols.items():
        if title.lower() == name_l:
            return cid
    # fallback: partial match
    for cid, title in cols.items():
        if name_l in title.lower():
            return cid
    return None

CID = {
    'propid':    col_id('Property ID'),
    'cma_id':    col_id('CMA Property ID'),
    'name':      col_id('Property Name'),
    'address':   col_id('Address'),
    'city':      col_id('City'),
    'state':     col_id('State'),
    'zip':       col_id('Zip'),
    'date':      col_id('Inspection Date'),
    'inspector': col_id('Inspected or Reported By'),
    'email':     col_id('Email Address'),
    'conv_type': col_id('Conversion Type'),
    'parking':   col_id('Parking Lot'),
    'drive':     col_id('Drive Through'),
    'sidewalks': col_id('Sidewalks'),
    'windows':   col_id('Windows'),
    'landscaping':col_id('Landscaping'),
    'trash':     col_id('Trash'),
    'dumpster':  col_id('Dumpster'),
    'entrance':  col_id('Entrance'),
    'exterior':  col_id('Exterior'),
    'signage':   col_id('Signage'),
    'row_num':   col_id('Row Number'),
    'location':  col_id('Location'),
}
print("Mapped:", {k: v for k, v in CID.items() if v})

def cell_val(row_cells, cid):
    if not cid:
        return ''
    for cell in row_cells:
        if cell.get('columnId') == cid:
            return cell.get('displayValue') or cell.get('value') or ''
    return ''

# Load rd_recs for PPM/REM/RD enrichment
rd_map = {}
rd_path = os.path.join(os.path.dirname(__file__), 'data', 'rd_recs.json')
if os.path.exists(rd_path):
    with open(rd_path) as f:
        for rd in json.load(f):
            pid = str(rd.get('PropertyID', '')).strip()
            if pid:
                rd_map[pid] = rd

records = []
for i, row in enumerate(data.get('rows', [])):
    cells = row.get('cells', [])

    propid   = str(cell_val(cells, CID['propid'])).strip()
    name     = str(cell_val(cells, CID['name'])).strip()
    state    = str(cell_val(cells, CID['state'])).strip()
    city     = str(cell_val(cells, CID['city'])).strip()
    address  = str(cell_val(cells, CID['address'])).strip()
    date_val = str(cell_val(cells, CID['date'])).strip()
    inspector= str(cell_val(cells, CID['inspector'])).strip()
    signage  = str(cell_val(cells, CID['signage'])).strip()

    # Skip parent/summary rows that have no property ID or name
    if not propid and not name:
        continue

    # Derive issues count from condition columns
    condition_cols = ['parking','drive','sidewalks','windows','landscaping',
                      'trash','dumpster','entrance','exterior']
    issues = sum(1 for c in condition_cols
                 if cell_val(cells, CID.get(c,'')) not in ('','Excellent ready for day 1.','Nothing new','Looks good','good','N/A'))

    # Derive severity
    if issues == 0:
        severity = 'Green'
    elif issues <= 2:
        severity = 'Yellow'
    else:
        severity = 'Blue'

    # Day 2 detection
    loc = str(cell_val(cells, CID['location'])).lower()
    conv = str(cell_val(cells, CID['conv_type'])).lower()
    has_day2 = 'Yes' if ('day 2' in loc or 'day2' in loc or 'day 2' in conv or 'day2' in conv) else 'No'

    # Normalize date from MM/DD/YY or YYYY-MM-DD
    d = date_val
    if d and '/' in d:
        parts = d.split('/')
        if len(parts) == 3:
            m, dy, y = parts
            y = '20' + y if len(y) == 2 else y
            d = f"{y}-{m.zfill(2)}-{dy.zfill(2)}"

    # RD list enrichment
    rd_info = rd_map.get(propid, {})

    rec = {
        '_i':        i,
        'rownum':    i + 1,
        'propid':    propid,
        'name':      name or str(cell_val(cells, CID['location'])).split('|')[-1].strip(),
        'address':   address,
        'city':      city,
        'state':     state,
        'date':      d,
        'inspector': inspector,
        'severity':  severity,
        'color':     '#78BE20' if severity=='Green' else ('#f59e0b' if severity=='Yellow' else '#3b82f6'),
        'allDone':   'Yes' if issues == 0 else 'No',
        'woReq':     issues,
        'woCreated': '',
        'woComp':    0,
        'woDisp':    0,
        'woCan':     0,
        'issues':    issues,
        'signage':   signage,
        'priScore':  issues,
        'hasDay2':   has_day2,
        'ppm':       rd_info.get('PPM', ''),
        'rem':       rd_info.get('REM', ''),
        'rd':        rd_info.get('RD', ''),
        'rsm':       rd_info.get('RSM', ''),
    }
    records.append(rec)

os.makedirs('data', exist_ok=True)
out = os.path.join(os.path.dirname(__file__), 'data', 'surv_recs.json')
with open(out, 'w') as f:
    json.dump(records, f)

print(f"Wrote {len(records)} survey records to {out}")
# Print date breakdown for debugging
from collections import Counter
dates = Counter(r['date'][:10] for r in records if r['date'])
print("Records by date:", dict(sorted(dates.items())))
