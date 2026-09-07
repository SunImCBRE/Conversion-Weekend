"""
convert_wo.py
Reads data/wo_data.csv OR data/wo_data.xlsx → writes data/wo_recs.json.
Drop the latest work order export into data/ on GitHub; the next
Action run will auto-detect and rebuild the dashboard.

Supports the standard CBRE WO export format with columns:
  WorkOrderNumber, Priority, Status, PCode Description, AssignedVendorName,
  Assigned Employee Name, DateEnteredSite, PCode Number, ProblemDescription,
  Building ID, Building Description, City, State, BidAmount, CBRE NON-CBRE, etc.
"""
import csv, json, os, sys

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CSV_SRC  = os.path.join(DATA_DIR, 'wo_data.csv')
XLSX_SRC = os.path.join(DATA_DIR, 'wo_data.xlsx')
OUT      = os.path.join(DATA_DIR, 'wo_recs.json')

# --- Detect source file ---
if os.path.exists(XLSX_SRC):
    src_type = 'xlsx'
    print("Found wo_data.xlsx")
elif os.path.exists(CSV_SRC):
    src_type = 'csv'
    print("Found wo_data.csv")
else:
    print("No wo_data.csv or wo_data.xlsx in data/ — skipping WO conversion")
    sys.exit(0)

# --- Load rows ---
if src_type == 'xlsx':
    try:
        import openpyxl
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl', '-q'])
        import openpyxl
    wb = openpyxl.load_workbook(XLSX_SRC, data_only=True)
    ws = wb.active
    raw_rows = list(ws.iter_rows(values_only=True))
    if not raw_rows:
        print("XLSX is empty"); sys.exit(0)
    headers = [str(c).strip() if c is not None else '' for c in raw_rows[0]]
    rows = [{headers[i]: (str(v).strip() if v is not None else '') for i, v in enumerate(raw)} for raw in raw_rows[1:]]
else:
    with open(CSV_SRC, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print("CSV is empty"); sys.exit(0)
    headers = list(rows[0].keys())

print(f"Loaded {len(rows)} rows, {len(headers)} columns")

# --- Flexible column finder (exact match first, then partial) ---
def find_col(hdrs, *candidates):
    h_map = {h.lower().replace(' ','').replace('_','').replace('#','').replace('/','').replace('-',''): h for h in hdrs}
    for c in candidates:
        c_l = c.lower().replace(' ','').replace('_','').replace('#','').replace('/','').replace('-','')
        if c_l in h_map:
            return h_map[c_l]
    # partial fallback
    for c in candidates:
        c_l = c.lower().replace(' ','').replace('_','').replace('#','').replace('/','').replace('-','')
        for norm, orig in h_map.items():
            if c_l in norm or norm in c_l:
                return orig
    return None

CM = {
    'wo':        find_col(headers, 'WorkOrderNumber', 'WO Number', 'Work Order'),
    'building':  find_col(headers, 'Building Description', 'BuildingDescription', 'Property Name', 'Site Name'),
    'buildingId':find_col(headers, 'Building ID', 'BuildingID', 'Property ID'),
    'city':      find_col(headers, 'City'),
    'state':     find_col(headers, 'State'),
    'priority':  find_col(headers, 'Priority'),
    'status':    find_col(headers, 'Status'),
    'scope':     find_col(headers, 'CBRE NON-CBRE', 'CBRE/NON-CBRE', 'Scope'),
    'group':     find_col(headers, 'PCode Description', 'PCodeDescription', 'Category', 'Group', 'Service Type'),
    'amount':    find_col(headers, 'BidAmount', 'Bid Amount', 'SplitAmount', 'Amount', 'Cost'),
    'date':      find_col(headers, 'DateEnteredSite', 'Date Entered Site', 'DateEntered', 'Date Entered', 'Open Date'),
    'vendor':    find_col(headers, 'AssignedVendorName', 'Assigned Vendor Name', 'Vendor Name', 'Vendor'),
    'assignee':  find_col(headers, 'Assigned Employee Name', 'AssignedEmployeeName', 'Assignee'),
    'pcode':     find_col(headers, 'PCode Number', 'PCodeNumber', 'Problem Code'),
    'probDesc':  find_col(headers, 'ProblemDescription', 'Problem Description', 'Description', 'Notes'),
    'cbre':      find_col(headers, 'CBRE NON-CBRE', 'CBRE/NON-CBRE', 'CBRE'),
}
print(f"Mapped: { {k:v for k,v in CM.items() if v} }")
missing = [k for k,v in CM.items() if not v]
if missing:
    print(f"Warning — could not map: {missing}")

def g(row, field):
    col = CM.get(field)
    return str(row.get(col, '') or '').strip() if col else ''

records = []
for i, row in enumerate(rows):
    wo_num = g(row, 'wo')
    if not wo_num:
        continue

    # Day 2 detection: check ProblemDescription or Description for "day 2"
    desc = g(row, 'probDesc').lower()
    day2 = any(kw in desc for kw in ('day 2', 'day2', 'd2 -', ' d2 '))

    # Normalize date — keep just date portion (strip time)
    raw_date = g(row, 'date')
    date_out = raw_date.split(' ')[0] if raw_date else ''

    # Normalize amount
    amt = g(row, 'amount').replace('$','').replace(',','').strip()

    rec = {
        '_i':        i,
        'wo':        wo_num,
        'building':  g(row, 'building'),
        'buildingId':g(row, 'buildingId'),
        'city':      g(row, 'city'),
        'state':     g(row, 'state'),
        'priority':  g(row, 'priority'),
        'status':    g(row, 'status'),
        'scope':     g(row, 'scope'),
        'group':     g(row, 'group'),
        'day2':      day2,
        'amount':    amt,
        'date':      date_out,
        'vendor':    g(row, 'vendor'),
        'assignee':  g(row, 'assignee'),
        'pcode':     g(row, 'pcode'),
        'probDesc':  g(row, 'probDesc'),
        'cbre':      g(row, 'cbre'),
    }
    records.append(rec)

os.makedirs(DATA_DIR, exist_ok=True)
with open(OUT, 'w') as f:
    json.dump(records, f)

print(f"Wrote {len(records)} WO records to {OUT}")
from collections import Counter
print("By state:", dict(sorted(Counter(r['state'] for r in records if r['state']).items())))
print("By status:", dict(sorted(Counter(r['status'] for r in records if r['status']).items())))
