import json

import os
_base = os.path.join(os.path.dirname(__file__), 'data')
with open(os.path.join(_base, 'wo_recs.json')) as f: WO = f.read()
with open(os.path.join(_base, 'surv_recs.json')) as f: SV = f.read()
with open(os.path.join(_base, 'team_recs.json')) as f: TM = f.read()
with open(os.path.join(_base, 'rd_recs.json')) as f: RD = f.read()

HTML = """<title>Fifth Third Conversion Weekend</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0d1117;--card:#161b22;--card2:#1c2128;--border:#2a3040;
  --53g:#006033;--53g2:#1B6539;--53gl:#78BE20;--53n:#003087;
  --yellow:#f59e0b;--red:#ef4444;--blue:#3b82f6;--teal:#14b8a6;
  --text:#d1fae5;--muted:#6b8f72;--white:#f0fdf4;
}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
header{background:linear-gradient(135deg,#001f5b 0%,#003087 40%,#006033 100%);padding:0 26px;display:flex;align-items:center;gap:14px;height:58px;box-shadow:0 2px 20px #00000077}
.logo{background:#fff;border-radius:7px;padding:5px 11px;font-weight:900;font-size:1rem;color:#003087;letter-spacing:-.5px}
header h1{font-size:1.05rem;font-weight:700;color:#fff;letter-spacing:.3px}
.hdr-sub{font-size:.72rem;color:#93c5fd;margin-left:2px}
.hdr-r{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:3px}
.hdr-badge{background:#78BE2022;border:1px solid #78BE2066;color:#78BE20;padding:2px 10px;border-radius:20px;font-size:.7rem;font-weight:700}
.hdr-ts{font-size:.68rem;color:#93c5fd}
.tabs{display:flex;background:var(--card);border-bottom:1px solid var(--border);padding:0 20px;gap:0}
.tab{padding:12px 20px;cursor:pointer;font-size:.82rem;font-weight:600;color:var(--muted);border-bottom:3px solid transparent;transition:.15s;white-space:nowrap}
.tab.active{color:var(--53gl);border-bottom-color:var(--53gl)}
.tab:hover:not(.active){color:var(--text)}
.page{display:none;padding:20px}
.page.active{display:block}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:11px;margin-bottom:20px}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:9px;padding:15px 16px;position:relative;overflow:hidden}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent,var(--53gl))}
.kpi .val{font-size:1.85rem;font-weight:800;line-height:1;color:var(--white)}
.kpi .lbl{font-size:.67rem;color:var(--muted);margin-top:5px;text-transform:uppercase;letter-spacing:.5px}
.kpi .sub{font-size:.7rem;color:var(--muted);margin-top:2px}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:13px;margin-bottom:20px}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:9px;padding:15px}
.chart-card h3{font-size:.68rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.8px;margin-bottom:11px}
.cw{position:relative;height:200px}
.cw.tall{height:260px}
.filters{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px;align-items:center}
.filters select,.filters input{background:var(--card2);border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:6px;font-size:.77rem;outline:none}
.filters select:focus,.filters input:focus{border-color:var(--53gl)}
.badge{display:inline-block;padding:2px 7px;border-radius:20px;font-size:.66rem;font-weight:700;white-space:nowrap}
.bg{background:#00603322;color:#78BE20}.by{background:#f59e0b22;color:#f59e0b}
.br{background:#ef444422;color:#ef4444}.bb{background:#3b82f622;color:#3b82f6}
.bgr{background:#6b8f7222;color:#6b8f72}.bdn{background:#00308722;color:#93c5fd}
.tbl-w{overflow-x:auto;border-radius:8px;border:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:.74rem}
thead{background:var(--card2)}
th{padding:9px 10px;text-align:left;font-weight:700;color:var(--muted);text-transform:uppercase;font-size:.63rem;letter-spacing:.5px;white-space:nowrap;border-bottom:1px solid var(--border)}
td{padding:8px 10px;border-bottom:1px solid #1c2128;white-space:nowrap;vertical-align:middle}
tr:hover td{background:#78BE2008}
td[contenteditable=true]{cursor:text}
td[contenteditable=true]:focus{background:#00603322;outline:1px solid var(--53gl);border-radius:3px}
.pg{display:flex;gap:7px;align-items:center;margin-top:11px;font-size:.76rem;color:var(--muted)}
.pg button{background:var(--card2);border:1px solid var(--border);color:var(--text);padding:4px 11px;border-radius:6px;cursor:pointer;font-size:.73rem}
.pg button:hover{border-color:var(--53gl);color:var(--53gl)}
.save-btn{background:var(--53g);color:#fff;border:none;padding:7px 15px;border-radius:7px;cursor:pointer;font-size:.77rem;font-weight:600}
.save-btn:hover{background:var(--53gl);color:#000}
.exp-btn{background:var(--card2);color:var(--text);border:1px solid var(--border);padding:6px 13px;border-radius:6px;cursor:pointer;font-size:.75rem}
.exp-btn:hover{border-color:var(--53gl);color:var(--53gl)}
.dl{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}
.dl .item{display:flex;align-items:center;gap:4px;font-size:.68rem;color:var(--muted)}
.dl .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.pb{background:var(--border);border-radius:20px;height:6px;overflow:hidden;margin-top:4px}
.pf{height:100%;border-radius:20px;transition:.4s}
.sr{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid var(--border)}
.sr:last-child{border:none}
.sr .nm{font-size:.76rem}
.sr .vl{font-size:.8rem;font-weight:700;color:var(--white)}
.twoCol{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:20px}
/* Modal */
.mo{display:none;position:fixed;inset:0;background:#000000bb;z-index:2000;align-items:center;justify-content:center;padding:16px}
.mo.open{display:flex}
.mc{background:var(--card);border:1px solid var(--border);border-radius:12px;width:100%;max-width:820px;max-height:88vh;overflow-y:auto;padding:22px;position:relative}
.mc h2{font-size:1rem;color:var(--white);margin-bottom:3px}
.mc .ms{font-size:.75rem;color:var(--muted);margin-bottom:16px}
.mc-x{position:absolute;top:14px;right:16px;background:none;border:none;color:var(--muted);font-size:1.3rem;cursor:pointer;line-height:1}
.mc-x:hover{color:var(--red)}
.mg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.mf{background:var(--card2);border-radius:6px;padding:9px 12px}
.mf-l{font-size:.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}
.mf-v{font-size:.79rem;color:var(--white);word-break:break-word;white-space:normal}
.ms-sec{margin-top:14px}
.ms-sec h4{font-size:.68rem;color:var(--53gl);text-transform:uppercase;letter-spacing:.8px;margin-bottom:7px;padding-bottom:5px;border-bottom:1px solid var(--border)}
.wchip{display:inline-block;background:var(--card2);border:1px solid var(--border);border-radius:5px;padding:2px 8px;margin:2px;font-size:.7rem;cursor:pointer}
.wchip:hover{border-color:var(--53gl);color:var(--53gl)}
.day2-chip{background:#f59e0b18;border:1px solid #f59e0b44;color:#f59e0b;display:inline-block;padding:1px 7px;border-radius:4px;font-size:.63rem;font-weight:700;margin-left:5px}
@media(max-width:680px){.twoCol{grid-template-columns:1fr}.mg{grid-template-columns:1fr}}
</style>

<header>
  <div class="logo" style="padding:4px 8px;background:#fff;border-radius:6px;display:flex;align-items:center"><img src="https://www.53.com/content/dam/fifth-third/brand/logos/53-logo.svg" alt="Fifth Third Bank" style="height:28px;width:auto" onerror="this.parentElement.innerHTML='5/3'"></div>
  <div>
    <div style="display:flex;align-items:baseline;gap:8px">
      <h1>Fifth Third Conversion Weekend</h1>
    </div>
    <span class="hdr-sub">Day 1 Readiness Dashboard &nbsp;·&nbsp; CBRE Property Management</span>
  </div>
  <div class="hdr-r">
    <span class="hdr-badge">&#128197; Sep 4–7, 2026</span>
    <span class="hdr-ts" id="ts"></span>
  </div>
</header>

<div class="tabs">
  <div class="tab active" onclick="nav('ov',this)">&#9724; Overview</div>
  <div class="tab" onclick="nav('wo',this)">Work Orders</div>
  <div class="tab" onclick="nav('sv',this)">Field Surveys</div>
  <div class="tab" onclick="nav('tm',this)">Team Assignments</div>
  <div class="tab" onclick="nav('dt',this)">Data Tables</div>
  <div class="tab" onclick="nav('la',this)">&#128202; Live Assessments</div>
</div>

<!-- OVERVIEW -->
<div class="page active" id="ov">
  <div class="kpis" id="ov_kpis"></div>
  <div class="charts">
    <div class="chart-card"><h3>Work Orders by Scope</h3><div class="cw"><canvas id="cScope"></canvas></div><div class="dl" id="scopeDL"></div></div>
    <div class="chart-card"><h3>WO Status Breakdown</h3><div class="cw"><canvas id="cStatus"></canvas></div></div>
    <div class="chart-card"><h3>Survey Severity</h3><div class="cw"><canvas id="cSev"></canvas></div><div class="dl" id="sevDL"></div></div>
    <div class="chart-card"><h3>Daily Activity — Conversion Weekend</h3><div class="cw"><canvas id="cDaily"></canvas></div></div>
    <div class="chart-card"><h3>Work Orders by State</h3><div class="cw"><canvas id="cState"></canvas></div></div>
    <div class="chart-card"><h3>Survey WO Pipeline</h3><div class="cw"><canvas id="cPipe"></canvas></div></div>
  </div>
  <div class="twoCol">
    <div class="chart-card"><h3>WO Categories</h3><div id="grpList"></div></div>
    <div class="chart-card"><h3>Survey Coverage by State</h3><div id="stList"></div></div>
  </div>
</div>

<!-- WORK ORDERS -->
<div class="page" id="wo">
  <div class="kpis" id="wo_kpis"></div>
  <div class="charts">
    <div class="chart-card"><h3>Priority Distribution</h3><div class="cw"><canvas id="cPri"></canvas></div></div>
    <div class="chart-card"><h3>Categories (Horizontal)</h3><div class="cw tall"><canvas id="cGrp"></canvas></div></div>
  </div>
  <div class="filters">
    <select id="wf_st" onchange="fWO()"><option value="">All States</option></select>
    <select id="wf_sc" onchange="fWO()"><option value="">All Scopes</option></select>
    <select id="wf_pr" onchange="fWO()"><option value="">All Priorities</option></select>
    <select id="wf_ss" onchange="fWO()"><option value="">All Statuses</option></select>
    <select id="wf_d2" onchange="fWO()"><option value="">Day 1 &amp; Day 2</option><option value="1">Day 2 Only</option><option value="0">Day 1 Only</option></select>
    <input id="wf_q" placeholder="Search WO #, building, city, vendor..." oninput="fWO()" style="min-width:200px">
    <button class="exp-btn" onclick="xWO()">&#8659; CSV</button>
  </div>
  <div class="tbl-w"><table><thead><tr>
    <th>WO #</th><th>Building</th><th>City</th><th>St</th><th>Pri</th>
    <th>Status</th><th>Scope</th><th>Category</th><th>D2?</th><th>Amount</th><th>Date</th><th></th>
  </tr></thead><tbody id="woTb"></tbody></table></div>
  <div class="pg"><button onclick="woP(-1)">&#8592;</button><span id="woPI"></span><button onclick="woP(1)">&#8594;</button></div>
</div>

<!-- SURVEYS -->
<div class="page" id="sv">
  <div class="kpis" id="sv_kpis"></div>
  <div class="charts">
    <div class="chart-card"><h3>Daily Survey Volume</h3><div class="cw"><canvas id="cSvD"></canvas></div></div>
    <div class="chart-card"><h3>Issues Identified by State</h3><div class="cw"><canvas id="cSvSt"></canvas></div></div>
  </div>
  <div class="filters">
    <select id="sf_st" onchange="fSV()"><option value="">All States</option></select>
    <select id="sf_sv" onchange="fSV()"><option value="">All Severities</option><option>Green</option><option>Yellow</option><option>Blue</option></select>
    <select id="sf_dt" onchange="fSV()"><option value="">All Dates</option></select>
    <select id="sf_d2" onchange="fSV()"><option value="">Any Day 2 Status</option><option value="1">Has Day 2 Issues</option><option value="0">No Day 2 Issues</option></select>
    <select id="sf_ppm" onchange="fSV()"><option value="">All PPMs</option></select>
    <select id="sf_rem" onchange="fSV()"><option value="">All REMs</option></select>
    <select id="sf_rd" onchange="fSV()"><option value="">All RDs</option></select>
    <input id="sf_q" placeholder="Search property, city, inspector..." oninput="fSV()" style="min-width:200px">
    <button class="exp-btn" onclick="xSV()">&#8659; CSV</button>
  </div>
  <div class="tbl-w"><table><thead><tr>
    <th>#</th><th>Property</th><th>City</th><th>St</th><th>Date</th><th>Inspector</th>
    <th>PPM</th><th>REM</th><th>RD</th>
    <th>Severity</th><th>D2?</th><th>WOs Req</th><th>Done</th><th>All Done</th><th>Signage</th><th></th>
  </tr></thead><tbody id="svTb"></tbody></table></div>
  <div class="pg"><button onclick="svP(-1)">&#8592;</button><span id="svPI"></span><button onclick="svP(1)">&#8594;</button></div>
</div>

<!-- TEAM ASSIGNMENTS -->
<div class="page" id="tm">
  <div class="kpis" id="tm_kpis"></div>
  <div class="charts">
    <div class="chart-card"><h3>Properties per Assignee (Top 15)</h3><div class="cw tall"><canvas id="cTmA"></canvas></div></div>
    <div class="chart-card"><h3>Properties per State</h3><div class="cw"><canvas id="cTmS"></canvas></div></div>
  </div>
  <div class="filters">
    <select id="tf_st" onchange="fTM()"><option value="">All States</option></select>
    <select id="tf_tm" onchange="fTM()"><option value="">All Teams</option></select>
    <input id="tf_q" placeholder="Search name, property, city..." oninput="fTM()" style="min-width:200px">
    <button class="exp-btn" onclick="xTM()">&#8659; CSV</button>
  </div>
  <div class="tbl-w"><table><thead><tr>
    <th>Team</th><th>Assigned To</th><th>Property ID</th><th>CMA ID</th><th>Property Name</th><th>Address</th><th>City</th><th>St</th><th>Ownership</th>
  </tr></thead><tbody id="tmTb"></tbody></table></div>
  <div class="pg"><button onclick="tmP(-1)">&#8592;</button><span id="tmPI"></span><button onclick="tmP(1)">&#8594;</button></div>
</div>

<!-- DATA TABLES (EDITABLE) -->
<div class="page" id="dt">
  <div style="display:flex;gap:9px;margin-bottom:13px;align-items:center;flex-wrap:wrap">
    <div class="tab active" id="dt_wo_t" onclick="dtTab('dtw')" style="border-radius:7px;border:1px solid var(--border);padding:7px 15px">Work Orders (966)</div>
    <div class="tab" id="dt_sv_t" onclick="dtTab('dts')" style="border-radius:7px;border:1px solid var(--border);padding:7px 15px">Surveys (595)</div>
    <span style="font-size:.7rem;color:var(--muted)">Click highlighted cells to edit</span>
    <button class="save-btn" id="savebtn" onclick="saveAll()" style="margin-left:auto">&#10003; Save Changes</button>
  </div>
  <div id="dtw_sec">
    <div class="filters"><input id="dtw_q" placeholder="Filter..." oninput="fDTW()" style="min-width:240px"><button class="exp-btn" onclick="xWO()">&#8659; CSV</button></div>
    <div class="tbl-w"><table><thead><tr>
      <th>WO #</th><th>Building</th><th>City</th><th>St</th><th>Pri</th><th>Status</th><th>Scope</th><th>CBRE/Non</th><th>D2?</th><th>Amount</th><th>Date</th>
    </tr></thead><tbody id="dtwTb"></tbody></table></div>
    <div class="pg"><button onclick="dtwP(-1)">&#8592;</button><span id="dtwPI"></span><button onclick="dtwP(1)">&#8594;</button></div>
  </div>
  <div id="dts_sec" style="display:none">
    <div class="filters"><input id="dts_q" placeholder="Filter..." oninput="fDTS()" style="min-width:240px"><button class="exp-btn" onclick="xSV()">&#8659; CSV</button></div>
    <div class="tbl-w"><table><thead><tr>
      <th>Row</th><th>Property</th><th>City</th><th>St</th><th>Date</th><th>Inspector</th><th>Severity</th><th>All Done</th><th>D2?</th><th>WOs Req</th><th>WOs Comp</th><th></th>
    </tr></thead><tbody id="dtsTb"></tbody></table></div>
    <div class="pg"><button onclick="dtsP(-1)">&#8592;</button><span id="dtsPI"></span><button onclick="dtsP(1)">&#8594;</button></div>
  </div>
</div>

<!-- LIVE ASSESSMENTS -->
<div class="page" id="la">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap">
    <div>
      <div style="font-size:.9rem;font-weight:700;color:var(--white)">Live Assessment Tracker</div>
      <div style="font-size:.72rem;color:var(--muted);margin-top:2px">Live data from Smartsheet &mdash; auto-refreshes every 10 min</div>
    </div>
    <button onclick="reloadLA()" style="background:var(--card2);border:1px solid var(--border);color:var(--53gl);padding:6px 13px;border-radius:6px;font-size:.74rem;cursor:pointer">&#8635; Refresh Now</button>
    <a href="https://app.smartsheet.com/b/publish?EQBCT=172a3ee1368046d98b6b853c9d154cfa" target="_blank" style="background:var(--card2);border:1px solid var(--border);color:var(--muted);padding:6px 13px;border-radius:6px;font-size:.74rem;text-decoration:none">&#8599; Open full view</a>
  </div>
  <div style="border-radius:9px;overflow:hidden;border:1px solid var(--border);background:#fff">
    <iframe id="la_frame"
      src="https://app.smartsheet.com/b/publish?EQBCT=172a3ee1368046d98b6b853c9d154cfa"
      style="width:100%;height:78vh;border:none;display:block"
      title="Live Assessment Tracker">
    </iframe>
  </div>
</div>

<!-- WO MODAL -->
<div class="mo" id="woMo" onclick="closeMo('woMo',event)">
  <div class="mc"><button class="mc-x" onclick="document.getElementById('woMo').classList.remove('open')">&#10005;</button>
    <h2 id="woMoT"></h2><div class="ms" id="woMoS"></div><div id="woMoB"></div>
  </div>
</div>
<!-- SURVEY MODAL -->
<div class="mo" id="svMo" onclick="closeMo('svMo',event)">
  <div class="mc"><button class="mc-x" onclick="document.getElementById('svMo').classList.remove('open')">&#10005;</button>
    <h2 id="svMoT"></h2><div class="ms" id="svMoS"></div><div id="svMoB"></div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const woData=__WO__;
const svData=__SV__;
const tmData=__TM__;
const rdData=__RD__;

let woE=woData.map((r,i)=>({...r,_i:i}));
let svE=svData.map((r,i)=>({...r,_i:i}));
let tmE=tmData.map((r,i)=>({...r,_i:i}));

const G='#78BE20',D='#006033',N='#003087',R='#ef4444',Y='#f59e0b',B='#3b82f6',T='#14b8a6';
const PAL=[G,B,Y,R,T,'#f97316','#a855f7','#6b8f72'];
Chart.defaults.color='#6b8f72';Chart.defaults.borderColor='#2a3040';
Chart.defaults.font.family='Segoe UI,system-ui,sans-serif';Chart.defaults.font.size=11;

function donut(id,labels,vals,colors){
  return new Chart(document.getElementById(id),{type:'doughnut',
    data:{labels,datasets:[{data:vals,backgroundColor:colors,borderWidth:2,borderColor:'#161b22',hoverOffset:7}]},
    options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.label}: ${c.raw} (${(c.raw/vals.reduce((a,b)=>a+b,0)*100).toFixed(1)}%)`}}},cutout:'66%',animation:{duration:600}}});
}
function hbar(id,labels,vals,colors){
  return new Chart(document.getElementById(id),{type:'bar',
    data:{labels,datasets:[{data:vals,backgroundColor:colors||PAL,borderRadius:5}]},
    options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{grid:{color:'#2a3040'}},y:{grid:{display:false}}},animation:{duration:500}}});
}
function bar(id,labels,vals,colors){
  return new Chart(document.getElementById(id),{type:'bar',
    data:{labels,datasets:[{data:vals,backgroundColor:colors||PAL,borderRadius:5}]},
    options:{plugins:{legend:{display:false}},scales:{x:{grid:{color:'#2a3040'}},y:{grid:{color:'#2a3040'}}},animation:{duration:500}}});
}

// ---- OVERVIEW ----
function initOV(){
  document.getElementById('ov_kpis').innerHTML=[
    {v:'966',l:'Total Work Orders',s:'All statuses',a:G},
    {v:'441',l:'CBRE In Scope',s:'Scenario 1 · 45.7%',a:G},
    {v:'489',l:'Client In Scope',s:'Scenario 3 · 50.6%',a:N},
    {v:'99',l:'Day 2 WOs',s:'Items flagged Day 2',a:Y},
    {v:'595',l:'Field Surveys',s:'Properties visited',a:B},
    {v:'82.8%',l:'Sites w/ Issues',s:'497 of 595',a:R},
    {v:'1,551',l:'WOs Requested',s:'From field surveys',a:'#a855f7'},
    {v:'6.3%',l:'WO Completion',s:'97 completed',a:G},
  ].map(k=>`<div class="kpi" style="--accent:${k.a}"><div class="val">${k.v}</div><div class="lbl">${k.l}</div><div class="sub">${k.s}</div></div>`).join('');

  donut('cScope',['CBRE In Scope','Client In Scope','CBRE Holds Contract','Referral'],[441,489,34,2],[G,B,Y,'#a855f7']);
  document.getElementById('scopeDL').innerHTML=[['CBRE In Scope',G],['Client In Scope',B],['CBRE Holds',Y],['Referral','#a855f7']].map(([l,c])=>`<div class="item"><div class="dot" style="background:${c}"></div>${l}</div>`).join('');
  bar('cStatus',['Dispatched','Completed','Disp/EA','Closed Pend','Disp Ack','Cancelled','Open'],[731,103,45,26,21,15,9],[G,'#00e09a',B,Y,'#a855f7',R,'#f97316']);
  donut('cSev',['Yellow','Green','Blue'],[335,258,2],[Y,G,B]);
  document.getElementById('sevDL').innerHTML=[['Yellow — Needs Attention',Y],['Green — Good',G],['Blue — Special',B]].map(([l,c])=>`<div class="item"><div class="dot" style="background:${c}"></div>${l}</div>`).join('');
  const _svDay={'2026-09-04':0,'2026-09-05':0,'2026-09-06':0,'2026-09-07':0};
  svData.forEach(r=>{if(r.date&&_svDay[r.date]!==undefined)_svDay[r.date]++;});
  new Chart(document.getElementById('cDaily'),{type:'line',data:{labels:['Sep 4','Sep 5','Sep 6','Sep 7'],datasets:[
    {label:'Work Orders',data:[4,412,550,0],borderColor:G,backgroundColor:G+'22',fill:true,tension:.4,pointRadius:5},
    {label:'Surveys',data:[_svDay['2026-09-04'],_svDay['2026-09-05'],_svDay['2026-09-06'],_svDay['2026-09-07']],borderColor:B,backgroundColor:B+'22',fill:true,tension:.4,pointRadius:5}
  ]},options:{plugins:{legend:{labels:{boxWidth:9}}},scales:{x:{grid:{color:'#2a3040'}},y:{grid:{color:'#2a3040'}}}}});
  bar('cState',['MI','TX','CA','AZ','FL'],[447,300,157,54,8],PAL);
  bar('cPipe',['Requested','Created','Dispatched','Completed','Cancelled'],[1551,1550,1037,97,92],[B,G,Y,'#00e09a',R]);

  const grps=[['Maintenance & Repair',398],['Janitorial',348],['Grounds & Parking',139],['Banking Equipment',27],['Furniture/Fixture',21],['Security',20],['Moves/Adds',10],['Env/H/S',3]];
  document.getElementById('grpList').innerHTML=grps.map(([n,v])=>`<div class="sr"><span class="nm">${n}</span><div style="flex:1;margin:0 9px"><div class="pb"><div class="pf" style="width:${(v/398*100).toFixed(0)}%;background:${G}"></div></div></div><span class="vl">${v}</span></div>`).join('');
  const sts=[['MI',219],['TX',193],['CA',156],['AZ',19],['FL',6]];
  document.getElementById('stList').innerHTML=sts.map(([s,v])=>`<div class="sr"><span class="nm" style="min-width:26px">${s}</span><div style="flex:1;margin:0 9px"><div class="pb"><div class="pf" style="width:${(v/219*100).toFixed(0)}%;background:${B}"></div></div></div><span class="vl">${v}</span></div>`).join('');
}

// ---- WORK ORDERS ----
let woPage=0,woF=[]; const woPer=25;
function initWO(){
  document.getElementById('wo_kpis').innerHTML=[
    {v:'966',l:'Total WOs',a:G},{v:'748',l:'Priority 1',s:'High urgency',a:R},
    {v:'731',l:'Dispatched',s:'75.7%',a:B},{v:'103',l:'Completed by Tech',s:'10.7%',a:G},
    {v:'99',l:'Day 2 Items',s:'Flagged for Day 2',a:Y},
    {v:'$'+woData.reduce((a,r)=>a+(parseFloat(r.amount)||0),0).toLocaleString('en',{maximumFractionDigits:0}),l:'Total Bid Value',a:'#a855f7'},
  ].map(k=>`<div class="kpi" style="--accent:${k.a}"><div class="val">${k.v}</div><div class="lbl">${k.l}</div><div class="sub">${k.s||''}</div></div>`).join('');
  donut('cPri',['P1','P2','P3','P4','P5','P6'],[748,71,103,30,11,3],[R,'#f97316',Y,G,B,'#6b8f72']);
  hbar('cGrp',['Maint & Repair','Janitorial','Grounds & Parking','Banking Equip','Furniture/Fix','Security','Moves/Adds','Env/H/S'],[398,348,139,27,21,20,10,3],PAL);
  const states=[...new Set(woData.map(r=>r.state))].filter(Boolean).sort();
  const scopes=[...new Set(woData.map(r=>r.scope))].filter(Boolean).sort();
  const pris=[...new Set(woData.map(r=>r.priority))].filter(Boolean).sort();
  const stats=[...new Set(woData.map(r=>r.status))].filter(Boolean).sort();
  [['wf_st',states],['wf_sc',scopes],['wf_pr',pris],['wf_ss',stats]].forEach(([id,arr])=>arr.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById(id).appendChild(o);}));
  woF=[...woE];renderWO();
}
function fWO(){
  const st=v('wf_st'),sc=v('wf_sc'),pr=v('wf_pr'),ss=v('wf_ss'),d2=v('wf_d2'),q=v('wf_q').toLowerCase();
  woF=woE.filter(r=>(!st||r.state===st)&&(!sc||r.scope===sc)&&(!pr||r.priority===pr)&&(!ss||r.status===ss)&&(d2===''||String(Number(r.day2))===d2)&&(!q||[r.wo,r.building,r.city,r.pcode,r.vendor,r.assignee].join(' ').toLowerCase().includes(q)));
  woPage=0;renderWO();
}
function renderWO(){
  document.getElementById('woTb').innerHTML=woF.slice(woPage*woPer,(woPage+1)*woPer).map(r=>`<tr>
    <td style="color:${G};font-weight:600;cursor:pointer" onclick="openWOMo(${r._i})">${r.wo}</td>
    <td>${r.building}</td><td>${r.city}</td>
    <td><span class="badge bgr">${r.state}</span></td>
    <td><span style="color:${pC(r.priority)};font-weight:700">${r.priority}</span></td>
    <td>${sBadge(r.status)}</td><td>${scBadge(r.scope)}</td>
    <td style="max-width:140px;overflow:hidden;text-overflow:ellipsis">${r.group||''}</td>
    <td>${r.day2?'<span class="day2-chip">D2</span>':'<span style="color:var(--muted);font-size:.65rem">D1</span>'}</td>
    <td>${r.amount?'$'+Number(r.amount).toLocaleString('en',{maximumFractionDigits:0}):'—'}</td>
    <td style="color:var(--muted)">${r.date}</td>
    <td><button onclick="openWOMo(${r._i})" style="background:${D};border:none;color:#fff;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:.67rem">View</button></td>
  </tr>`).join('');
  pi('woPI',woPage,woF.length,woPer);
}
function woP(d){woPage+=d;if(woPage<0)woPage=0;const mp=Math.ceil(woF.length/woPer)-1;if(woPage>mp)woPage=mp;renderWO();}

// ---- SURVEYS ----
let svPage=0,svF=[]; const svPer=25;
function initSV(){
  const total=svData.length;
  const hadIssues=svData.filter(r=>Number(r.issues)>0||r.severity==='Yellow'||r.severity==='Blue').length;
  const clean=svData.filter(r=>Number(r.issues)===0&&r.severity==='Green').length;
  const yellow=svData.filter(r=>r.severity==='Yellow').length;
  const green=svData.filter(r=>r.severity==='Green').length;
  const woReqTotal=svData.reduce((a,r)=>a+(Number(r.woReq)||0),0);
  const pct=(hadIssues/total*100).toFixed(1);
  document.getElementById('sv_kpis').innerHTML=[
    {v:String(total),l:'Total Surveys',a:G},
    {v:String(hadIssues),l:'Had Issues',s:pct+'% of sites',a:R},
    {v:String(clean),l:'Clean Sites',s:'No issues',a:G},
    {v:String(yellow),l:'Yellow',s:'Needs attention',a:Y},
    {v:String(green),l:'Green',s:'Good condition',a:G},
    {v:woReqTotal.toLocaleString(),l:'WOs Requested',s:'From surveys',a:B},
  ].map(k=>`<div class="kpi" style="--accent:${k.a}"><div class="val">${k.v}</div><div class="lbl">${k.l}</div><div class="sub">${k.s||''}</div></div>`).join('');
  const dayMap={'2026-09-04':0,'2026-09-05':0,'2026-09-06':0,'2026-09-07':0};
  svData.forEach(r=>{if(r.date&&dayMap[r.date]!==undefined)dayMap[r.date]++;});
  bar('cSvD',['Sep 4','Sep 5','Sep 6','Sep 7'],[dayMap['2026-09-04'],dayMap['2026-09-05'],dayMap['2026-09-06'],dayMap['2026-09-07']],[G,G,G,G]);
  const stIs={},stTot={};
  svData.forEach(r=>{if(!r.state)return;stTot[r.state]=(stTot[r.state]||0)+1;if(Number(r.issues)>0)stIs[r.state]=(stIs[r.state]||0)+1;});
  const stL=Object.keys(stTot).sort();
  new Chart(document.getElementById('cSvSt'),{type:'bar',data:{labels:stL,datasets:[
    {label:'Issues',data:stL.map(s=>stIs[s]||0),backgroundColor:R+'88',borderRadius:4},
    {label:'Clean',data:stL.map(s=>(stTot[s]||0)-(stIs[s]||0)),backgroundColor:G+'88',borderRadius:4}
  ]},options:{plugins:{legend:{labels:{boxWidth:9}}},scales:{x:{stacked:true,grid:{color:'#2a3040'}},y:{stacked:true,grid:{color:'#2a3040'}}}}});
  const states=[...new Set(svData.map(r=>r.state))].filter(Boolean).sort();
  const dates=[...new Set(svData.map(r=>r.date).filter(d=>d&&d.startsWith('2026')))].sort();
  const ppms=[...new Set(svData.map(r=>r.ppm))].filter(Boolean).sort();
  const rems=[...new Set(svData.map(r=>r.rem))].filter(Boolean).sort();
  const rds=[...new Set(svData.map(r=>r.rd))].filter(Boolean).sort();
  states.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('sf_st').appendChild(o);});
  dates.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('sf_dt').appendChild(o);});
  ppms.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('sf_ppm').appendChild(o);});
  rems.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('sf_rem').appendChild(o);});
  rds.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('sf_rd').appendChild(o);});
  svF=[...svE];renderSV();
}
function fSV(){
  const st=v('sf_st'),sv_=v('sf_sv'),dt=v('sf_dt'),d2=v('sf_d2'),ppm=v('sf_ppm'),rem=v('sf_rem'),rd=v('sf_rd'),q=v('sf_q').toLowerCase();
  svF=svE.filter(r=>
    (!st||r.state===st)&&(!sv_||r.severity===sv_)&&(!dt||r.date===dt)&&
    (d2===''||(d2==='1'?String(r.hasDay2).toLowerCase().includes('yes'):!String(r.hasDay2).toLowerCase().includes('yes')))&&
    (!ppm||r.ppm===ppm)&&(!rem||r.rem===rem)&&(!rd||r.rd===rd)&&
    (!q||[r.name,r.city,r.inspector,r.propid,r.ppm,r.rem,r.rd].join(' ').toLowerCase().includes(q)));
  svPage=0;renderSV();
}
function renderSV(){
  document.getElementById('svTb').innerHTML=svF.slice(svPage*svPer,(svPage+1)*svPer).map(r=>`<tr>
    <td style="color:var(--muted);font-size:.68rem">${r.rownum}</td>
    <td style="font-weight:600;color:${G};cursor:pointer" onclick="openSVMo(${r._i})">${r.name}</td>
    <td>${r.city}</td><td><span class="badge bgr">${r.state}</span></td>
    <td style="color:var(--muted)">${r.date}</td><td>${r.inspector}</td>
    <td style="font-size:.7rem;color:var(--muted)">${r.ppm||'—'}</td>
    <td style="font-size:.7rem;color:var(--muted)">${r.rem||'—'}</td>
    <td style="font-size:.7rem;color:var(--muted)">${r.rd||'—'}</td>
    <td>${sevB(r.severity)}</td>
    <td>${r.hasDay2&&String(r.hasDay2).toLowerCase().includes('yes')?'<span class="day2-chip">D2</span>':'<span style="color:var(--muted);font-size:.65rem">—</span>'}</td>
    <td style="text-align:center">${r.woReq||0}</td><td style="text-align:center">${r.woComp||0}</td>
    <td>${r.allDone==='Yes'?'<span class="badge bg">Yes</span>':'<span class="badge br">No</span>'}</td>
    <td>${r.signage==='Yes'?'<span class="badge by">&#9888;</span>':r.signage==='No'?'<span class="badge bg">&#10003;</span>':'—'}</td>
    <td><button onclick="openSVMo(${r._i})" style="background:${D};border:none;color:#fff;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:.67rem">View</button></td>
  </tr>`).join('');
  pi('svPI',svPage,svF.length,svPer);
}
function svP(d){svPage+=d;if(svPage<0)svPage=0;const mp=Math.ceil(svF.length/svPer)-1;if(svPage>mp)svPage=mp;renderSV();}

// ---- TEAM ----
let tmPage=0,tmF=[]; const tmPer=30;
function initTM(){
  const total=tmData.length;
  const assignees=new Set(tmData.map(r=>r.Assigned)).size;
  const teams=new Set(tmData.map(r=>r.Team)).size;
  const stateC={};tmData.forEach(r=>{stateC[r.State]=(stateC[r.State]||0)+1;});
  document.getElementById('tm_kpis').innerHTML=[
    {v:String(total),l:'Total Properties',a:G},{v:String(assignees),l:'Field Inspectors',s:'Unique assignees',a:B},
    {v:String(teams),l:'Teams',s:'Team assignments',a:N},
    {v:Object.entries(stateC).sort((a,b)=>b[1]-a[1])[0]?.[0]||'—',l:'Top State',s:(Object.entries(stateC).sort((a,b)=>b[1]-a[1])[0]?.[1]||0)+' properties',a:Y},
  ].map(k=>`<div class="kpi" style="--accent:${k.a}"><div class="val">${k.v}</div><div class="lbl">${k.l}</div><div class="sub">${k.s||''}</div></div>`).join('');

  const aCnt={};tmData.forEach(r=>{aCnt[r.Assigned]=(aCnt[r.Assigned]||0)+1;});
  const top15=Object.entries(aCnt).sort((a,b)=>b[1]-a[1]).slice(0,15);
  hbar('cTmA',top15.map(x=>x[0]),top15.map(x=>x[1]),PAL);
  bar('cTmS',Object.keys(stateC).sort(),Object.keys(stateC).sort().map(s=>stateC[s]),PAL);

  const states=[...new Set(tmData.map(r=>r.State))].filter(Boolean).sort();
  const teams_=[...new Set(tmData.map(r=>r.Team))].filter(Boolean).sort();
  states.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('tf_st').appendChild(o);});
  teams_.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;document.getElementById('tf_tm').appendChild(o);});
  tmF=[...tmE];renderTM();
}
function fTM(){
  const st=v('tf_st'),tm_=v('tf_tm'),q=v('tf_q').toLowerCase();
  tmF=tmE.filter(r=>(!st||r.State===st)&&(!tm_||r.Team===tm_)&&(!q||[r.Assigned,r.PropertyName,r.City,r.PropertyID].join(' ').toLowerCase().includes(q)));
  tmPage=0;renderTM();
}
function renderTM(){
  document.getElementById('tmTb').innerHTML=tmF.slice(tmPage*tmPer,(tmPage+1)*tmPer).map(r=>`<tr>
    <td><span class="badge bb" style="font-size:.63rem">${r.Team}</span></td>
    <td style="font-weight:600;color:${G}">${r.Assigned}</td>
    <td style="color:var(--muted)">${r.PropertyID}</td>
    <td style="color:var(--muted)">${r.CMAPropertyID}</td>
    <td>${r.PropertyName}</td>
    <td style="color:var(--muted)">${r.Address}</td>
    <td>${r.City}</td>
    <td><span class="badge bgr">${r.State}</span></td>
    <td style="color:var(--muted);font-size:.7rem">${r.Ownership}</td>
  </tr>`).join('');
  pi('tmPI',tmPage,tmF.length,tmPer);
}
function tmP(d){tmPage+=d;if(tmPage<0)tmPage=0;const mp=Math.ceil(tmF.length/tmPer)-1;if(tmPage>mp)tmPage=mp;renderTM();}

// ---- DATA TABLES ----
let dtwPage=0,dtsPage=0,dtwF=[],dtsF=[]; const dtPer=30;
function initDT(){dtwF=[...woE];dtsF=[...svE];renderDTW();renderDTS();}
function fDTW(){const q=v('dtw_q').toLowerCase();dtwF=woE.filter(r=>!q||[r.wo,r.building,r.city,r.state].join(' ').toLowerCase().includes(q));dtwPage=0;renderDTW();}
function fDTS(){const q=v('dts_q').toLowerCase();dtsF=svE.filter(r=>!q||[r.name,r.city,r.state,r.inspector].join(' ').toLowerCase().includes(q));dtsPage=0;renderDTS();}
function renderDTW(){
  document.getElementById('dtwTb').innerHTML=dtwF.slice(dtwPage*dtPer,(dtwPage+1)*dtPer).map(r=>`<tr>
    <td style="color:${G};font-weight:600">${r.wo}</td>
    <td contenteditable="true" oninput="eWO(${r._i},'building',this.textContent)">${r.building}</td>
    <td>${r.city}</td><td>${r.state}</td>
    <td><span style="color:${pC(r.priority)};font-weight:700">${r.priority}</span></td>
    <td contenteditable="true" oninput="eWO(${r._i},'status',this.textContent)">${r.status}</td>
    <td>${scBadge(r.scope)}</td><td>${r.cbre}</td>
    <td>${r.day2?'<span class="day2-chip">D2</span>':'D1'}</td>
    <td contenteditable="true" oninput="eWO(${r._i},'amount',this.textContent)">${r.amount}</td>
    <td style="color:var(--muted)">${r.date}</td>
  </tr>`).join('');
  pi('dtwPI',dtwPage,dtwF.length,dtPer);
}
function renderDTS(){
  document.getElementById('dtsTb').innerHTML=dtsF.slice(dtsPage*dtPer,(dtsPage+1)*dtPer).map(r=>`<tr>
    <td style="color:var(--muted)">${r.rownum}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'name',this.textContent)" style="color:${G};font-weight:600">${r.name}</td>
    <td>${r.city}</td><td>${r.state}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'date',this.textContent)">${r.date}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'inspector',this.textContent)">${r.inspector}</td>
    <td onclick="cycleSev(${r._i},this)" style="cursor:pointer" title="Click to change severity">${sevB(r.severity)}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'allDone',this.textContent)">${r.allDone}</td>
    <td>${r.hasDay2&&String(r.hasDay2).toLowerCase().includes('yes')?'<span class="day2-chip">D2</span>':'—'}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'woReq',this.textContent)" style="text-align:center">${r.woReq}</td>
    <td contenteditable="true" oninput="eSV(${r._i},'woComp',this.textContent)" style="text-align:center">${r.woComp}</td>
    <td><button onclick="openSVMo(${r._i})" style="background:${D};border:none;color:#fff;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:.67rem">View</button></td>
  </tr>`).join('');
  pi('dtsPI',dtsPage,dtsF.length,dtPer);
}
function dtwP(d){dtwPage+=d;if(dtwPage<0)dtwPage=0;const mp=Math.ceil(dtwF.length/dtPer)-1;if(dtwPage>mp)dtwPage=mp;renderDTW();}
function dtsP(d){dtsPage+=d;if(dtsPage<0)dtsPage=0;const mp=Math.ceil(dtsF.length/dtPer)-1;if(dtsPage>mp)dtsPage=mp;renderDTS();}
function dtTab(t){
  document.getElementById('dtw_sec').style.display=t==='dtw'?'block':'none';
  document.getElementById('dts_sec').style.display=t==='dts'?'block':'none';
  document.getElementById('dt_wo_t').classList.toggle('active',t==='dtw');
  document.getElementById('dt_sv_t').classList.toggle('active',t==='dts');
}
function eWO(i,f,v_){const r=woE.find(x=>x._i===i);if(r)r[f]=v_;}
function eSV(i,f,v_){const r=svE.find(x=>x._i===i);if(r)r[f]=v_;}
function cycleSev(i,td){
  const r=svE.find(x=>x._i===i);if(!r)return;
  const opts=['Green','Yellow','Blue'];
  const cur=opts.indexOf(r.severity);
  r.severity=opts[(cur+1)%opts.length];
  td.innerHTML=sevB(r.severity);
}
function saveAll(){
  try{localStorage.setItem('53wo',JSON.stringify(woE));localStorage.setItem('53sv',JSON.stringify(svE));}catch(e){}
  const b=document.getElementById('savebtn');
  b.textContent='&#10003; Saved!';b.style.background='#78BE20';b.style.color='#000';
  setTimeout(()=>{b.innerHTML='&#10003; Save Changes';b.style.cssText='';},2200);
}

// ---- MODALS ----
function openWOMo(i){
  const r=woE.find(x=>x._i===i);if(!r)return;
  document.getElementById('woMoT').textContent=`WO ${r.wo} — ${r.building}`;
  document.getElementById('woMoS').textContent=`${r.city}, ${r.state} · ${r.priority} · ${r.status} · ${r.date}`;
  const d2lbl=r.day2?'<span class="day2-chip" style="font-size:.8rem">DAY 2 ITEM</span>':'';
  document.getElementById('woMoB').innerHTML=`
    ${d2lbl?`<div style="margin-bottom:12px">${d2lbl}</div>`:''}
    <div class="mg">
      ${[['Work Order #',r.wo],['Building',r.building],['City / State',`${r.city}, ${r.state}`],['Priority',`<span style="color:${pC(r.priority)};font-weight:700">${r.priority}</span>`],['Status',sBadge(r.status)],['Scope',scBadge(r.scope)],['CBRE/Non',r.cbre],['Category',r.group],['Bid Amount',r.amount?'$'+Number(r.amount).toLocaleString():'—'],['Date Entered',r.date],['Assigned Vendor',r.vendor||'—'],['Assignee',r.assignee||'—'],['Building ID',r.buildingId||'—'],['Problem Code',r.pcode]].map(([l,v_])=>`<div class="mf"><div class="mf-l">${l}</div><div class="mf-v">${v_||'—'}</div></div>`).join('')}
    </div>
    <div class="ms-sec"><h4>Problem Description</h4><div style="font-size:.79rem;color:var(--muted);line-height:1.6;white-space:pre-wrap;background:var(--card2);border-radius:6px;padding:10px 13px">${r.probDesc||'No description.'}</div></div>`;
  document.getElementById('woMo').classList.add('open');
}
function openSVMo(i){
  const r=svE.find(x=>x._i===i);if(!r)return;
  document.getElementById('svMoT').textContent=`${r.name}`;
  document.getElementById('svMoS').textContent=`${r.address||''} ${r.city}, ${r.state} · ID: ${r.propid} · Inspected: ${r.date}`;
  const d2=r.hasDay2&&String(r.hasDay2).toLowerCase().includes('yes');
  const propWOs=woE.filter(w=>w.buildingId&&r.propid&&w.buildingId.toLowerCase()===r.propid.toLowerCase());
  document.getElementById('svMoB').innerHTML=`
    ${d2?'<div style="margin-bottom:12px"><span class="day2-chip" style="font-size:.8rem">HAS DAY 2 ISSUES</span></div>':''}
    <div class="mg">
      ${[['Inspector',r.inspector],['Severity',sevB(r.severity)],['Date',r.date],['State',r.state],['PPM',r.ppm||'—'],['REM',r.rem||'—'],['RD',r.rd||'—'],['RSM',r.rsm||'—'],['WOs Requested',r.woReq||0],['WOs Created',r.woCreated||0],['WOs Dispatched',r.woDisp||0],['WOs Completed',r.woComp||0],['WOs Cancelled',r.woCan||0],['All Done?',r.allDone],['Signage Issues',r.signage],['Priority Score',r.priScore||'—']].map(([l,v_])=>`<div class="mf"><div class="mf-l">${l}</div><div class="mf-v">${v_||'—'}</div></div>`).join('')}
    </div>
    ${propWOs.length?`<div class="ms-sec"><h4>Work Orders for this Property (${propWOs.length})</h4><div>${propWOs.map(w=>`<span class="wchip" onclick="openWOMo(${w._i})" title="${w.status}">${w.wo} <span style="color:${pC(w.priority)};font-size:.63rem">${w.priority}</span>${w.day2?'<span class="day2-chip" style="padding:0 4px;font-size:.55rem">D2</span>':''} · ${w.status}</span>`).join('')}</div></div>`:''}
    <div class="ms-sec"><h4>Issues Noted</h4><div style="font-size:.77rem;color:var(--muted);line-height:1.6;background:var(--card2);border-radius:6px;padding:10px 13px">${r.issues||'No issues recorded.'}</div></div>`;
  document.getElementById('svMo').classList.add('open');
}
function closeMo(id,e){if(e.target===document.getElementById(id))document.getElementById(id).classList.remove('open');}

// ---- HELPERS ----
function v(id){return document.getElementById(id).value;}
function pi(id,page,total,per){document.getElementById(id).textContent=`Page ${page+1} of ${Math.max(1,Math.ceil(total/per))} · ${total.toLocaleString()} records`;}
function pC(p){return{P1:'#ef4444',P2:'#f97316',P3:'#f59e0b',P4:'#78BE20',P5:'#3b82f6',P6:'#6b8f72'}[p]||'#6b8f72';}
function sBadge(s){
  if(s.includes('Completed')) return `<span class="badge bg">${s}</span>`;
  if(s==='Dispatched'||s.includes('Disp')) return `<span class="badge bb">${s}</span>`;
  if(s==='Cancelled') return `<span class="badge br">${s}</span>`;
  if(s.includes('Closed')) return `<span class="badge by">${s}</span>`;
  return `<span class="badge bgr">${s}</span>`;
}
function scBadge(s){
  if(s==='CBRE In Scope') return `<span class="badge bg">${s}</span>`;
  if(s==='Client In Scope') return `<span class="badge bdn">${s}</span>`;
  if(s==='CBRE Holds Contract') return `<span class="badge by">${s}</span>`;
  return `<span class="badge bgr">${s}</span>`;
}
function sevB(s){
  if(s==='Green') return `<span class="badge bg">&#10003; Green</span>`;
  if(s==='Yellow') return `<span class="badge by">&#9888; Yellow</span>`;
  if(s==='Blue') return `<span class="badge bb">&#9432; Blue</span>`;
  return `<span class="badge bgr">${s||'—'}</span>`;
}

// ---- EXPORT ----
function csv(arr,fields){return[fields.join(','),...arr.map(r=>fields.map(f=>{const x=r[f]??'';return typeof x==='string'&&(x.includes(',')||x.includes('"'))?`"${x.replace(/"/g,'""')}"`:x;}).join(','))].join('\\n');}
function dl(c,n){const a=document.createElement('a');a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(c);a.download=n;a.click();}
function xWO(){dl(csv(woE,['wo','building','city','state','priority','status','scope','cbre','day2','amount','date','group','vendor','assignee','probDesc']),'5third_work_orders.csv');}
function xSV(){dl(csv(svE,['rownum','propid','name','city','state','date','inspector','ppm','rem','rd','rsm','severity','allDone','hasDay2','woReq','woComp','woDisp','woCan']),'5third_surveys.csv');}
function xTM(){dl(csv(tmE,['Team','Assigned','PropertyID','CMAPropertyID','PropertyName','Address','City','State','Zip','County','Ownership','Type']),'5third_team_assignments.csv');}

// ---- LIVE ASSESSMENTS (iframe) ----
function reloadLA(){
  const f=document.getElementById('la_frame');
  if(f){f.src=f.src;}
}
function loadLA(){reloadLA();}

// ---- NAV ----
function nav(id,el){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tabs .tab').forEach(t=>t.classList.remove('active'));
  document.getElementById(id).classList.add('active');el.classList.add('active');
  if(id==='la')loadLA();
}
setInterval(()=>{if(document.getElementById('la').classList.contains('active'))loadLA();},10*60*1000);

// ---- INIT ----
document.getElementById('ts').textContent='Updated '+new Date().toLocaleString();
initOV();initWO();initSV();initTM();initDT();
try{const w=localStorage.getItem('53wo');const s=localStorage.getItem('53sv');
  if(w){woE=JSON.parse(w);woF=[...woE];renderWO();dtwF=[...woE];renderDTW();}
  if(s){svE=JSON.parse(s);svF=[...svE];renderSV();dtsF=[...svE];renderDTS();}
}catch(e){}
</script>"""

HTML = HTML.replace('__WO__', WO).replace('__SV__', SV).replace('__TM__', TM).replace('__RD__', RD)

# Write index.html for GitHub Pages, also keep local copy
out_index = os.path.join(os.path.dirname(__file__), 'index.html')
with open(out_index, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"Done: {len(HTML)//1024} KB")
