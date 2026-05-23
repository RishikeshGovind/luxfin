// ─── LuxFin shared utilities ──────────────────────────────────────────────────

const APP_NAME    = 'LuxFin';
const APP_VERSION = '1.0';

// ─── ECB Data Portal API (migrated from deprecated SDW host Oct 2025) ────────
const ECB_SDW_BASE = 'https://data-api.ecb.europa.eu/service/data';
const EUROSTAT_BASE = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data';

// Map panel config — offset center east to account for left control card
const MAP_CENTER_LU = [6.13, 49.81];
const MAP_ZOOM_LU   = 8.5;

// ─── Map choropleth indicator definitions ─────────────────────────────────────
const COMMUNE_INDICATORS = {
  population: {
    label: 'Population',
    unit: '',
    format: v => Number(v).toLocaleString('en-LU'),
    colorScale: ['#e0f2fe', '#0369a1'],
    breaks: [1000, 3000, 7000, 15000, 40000, 130000],
    colors: ['#e0f2fe','#7dd3fc','#38bdf8','#0ea5e9','#0284c7','#075985','#0c4a6e']
  },
  employment_rate: {
    label: 'Employment Rate (%)',
    unit: '%',
    format: v => v.toFixed(1) + '%',
    breaks: [59, 61, 63, 65, 68, 72],
    colors: ['#fef3c7','#fde68a','#fbbf24','#f59e0b','#d97706','#b45309','#78350f']
  },
  unemployment_rate: {
    label: 'Unemployment Rate (%)',
    unit: '%',
    format: v => v.toFixed(1) + '%',
    breaks: [3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
    colors: ['#f0fdf4','#bbf7d0','#86efac','#4ade80','#22c55e','#16a34a','#15803d']
  },
  income_index: {
    label: 'Income Index (LU=100)',
    unit: '',
    format: v => v.toFixed(0),
    breaks: [80, 88, 95, 102, 112, 125],
    colors: ['#ede9fe','#ddd6fe','#c4b5fd','#a78bfa','#8b5cf6','#7c3aed','#6d28d9']
  },
  foreign_pop_pct: {
    label: 'Foreign Population (%)',
    unit: '%',
    format: v => v.toFixed(1) + '%',
    breaks: [28, 35, 42, 50, 58, 65],
    colors: ['#fff7ed','#fed7aa','#fdba74','#fb923c','#f97316','#ea580c','#c2410c']
  },
  degurba: {
    label: 'Urbanisation (DEGURBA)',
    unit: '',
    format: v => ['','Urban','Town/Suburb','Rural'][v] || String(v),
    categorical: true,
    classes: [
      { key: 1, label: 'Urban',       color: '#0369a1' },
      { key: 2, label: 'Town/Suburb', color: '#0891b2' },
      { key: 3, label: 'Rural',       color: '#4ade80' }
    ]
  },
  proxy_risk: {
    label: 'Prototype Proxy Risk',
    unit: '',
    format: v => Number(v) === 1 ? 'Flagged' : 'Not flagged',
    categorical: true,
    classes: [
      { key: 0, label: 'Not flagged', color: '#dbeafe' },
      { key: 1, label: 'Proxy flagged', color: '#dc2626' }
    ],
    note: 'Socioeconomic proxy only — not a fiscal distress event.'
  },
  unemp_z: {
    label: 'Unemployment z-score',
    unit: '',
    format: v => Number(v).toFixed(2),
    breaks: [-1.0, -0.5, 0, 0.5, 1.0, 1.5],
    colors: ['#dbeafe','#bfdbfe','#fde68a','#fbbf24','#fb923c','#ef4444','#991b1b'],
    note: 'Higher values indicate above-average unemployment relative to the 2021 commune distribution.'
  },
  income_z: {
    label: 'Income z-score',
    unit: '',
    format: v => Number(v).toFixed(2),
    breaks: [-1.5, -1.0, -0.5, 0, 0.5, 1.0],
    colors: ['#991b1b','#ef4444','#fb923c','#fde68a','#bfdbfe','#60a5fa','#1d4ed8'],
    note: 'Lower values indicate below-average income index relative to the 2021 commune distribution.'
  },
  emp_z: {
    label: 'Employment z-score',
    unit: '',
    format: v => Number(v).toFixed(2),
    breaks: [-1.5, -1.0, -0.5, 0, 0.5, 1.0],
    colors: ['#991b1b','#ef4444','#fb923c','#fde68a','#bbf7d0','#4ade80','#15803d'],
    note: 'Lower values indicate below-average employment relative to the 2021 commune distribution.'
  }
};

// ─── Stress indicator component weights ───────────────────────────────────────
const STRESS_COMPONENTS = [
  {
    id: 'bond_concentration',
    label: 'Bond Concentration',
    desc: 'Govt bond holdings as % of total bank assets',
    weight: 0.30,
    unit: '%',
    lowThresh: 3.0,
    highThresh: 10.0,
    invertSign: false
  },
  {
    id: 'credit_govt_share',
    label: 'Public Credit Share',
    desc: 'Credit to general government as % of total credit',
    weight: 0.30,
    unit: '%',
    lowThresh: 6.0,
    highThresh: 16.0,
    invertSign: false
  },
  {
    id: 'fiscal_balance',
    label: 'Fiscal Balance',
    desc: 'General government balance (% of GDP). Surplus = low stress',
    weight: 0.25,
    unit: '% GDP',
    lowThresh: -3.0,
    highThresh: 3.0,
    invertSign: true   // positive balance = low stress
  },
  {
    id: 'sector_size',
    label: 'Banking Sector Size',
    desc: 'Total bank assets as multiple of nominal GDP',
    weight: 0.15,
    unit: 'x GDP',
    lowThresh: 8.0,
    highThresh: 16.0,
    invertSign: false
  }
];

// ─── Color palette ────────────────────────────────────────────────────────────
const COLORS = {
  accent:    '#1d4ed8',
  red:       '#ef3340',   // Luxembourg flag red
  green:     '#16a34a',
  amber:     '#f59e0b',
  muted:     '#6b7280',
  banking:   '#1d4ed8',
  govt:      '#dc2626',
  composite: '#c8a135',
  private:   '#0891b2'
};

// ─── Formatting helpers ───────────────────────────────────────────────────────
function fmtBn(v, decimals = 1) {
  if (v == null || isNaN(v)) return '–';
  return '€' + Number(v).toFixed(decimals) + ' bn';
}

function fmtPct(v, decimals = 1) {
  if (v == null || isNaN(v)) return '–';
  return Number(v).toFixed(decimals) + '%';
}

function fmtMultiple(v, decimals = 1) {
  if (v == null || isNaN(v)) return '–';
  return Number(v).toFixed(decimals) + 'x';
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getLastValue(arr) {
  return arr?.[arr.length - 1] ?? null;
}

function getYoY(arr, idx) {
  if (!arr || idx < 1) return null;
  const prev = arr[idx - 1], curr = arr[idx];
  if (!prev || !curr) return null;
  return ((curr - prev) / Math.abs(prev)) * 100;
}

// ─── Color interpolation for choropleth ───────────────────────────────────────
function getChoroplethColor(value, indicator) {
  const cfg = COMMUNE_INDICATORS[indicator];
  if (!cfg) return '#e5e7eb';
  if (cfg.categorical) {
    return cfg.classes.find(c => c.key === value)?.color || '#e5e7eb';
  }
  const breaks = cfg.breaks;
  const colors  = cfg.colors;
  if (value == null || isNaN(value)) return '#e5e7eb';
  for (let i = 0; i < breaks.length; i++) {
    if (value <= breaks[i]) return colors[i];
  }
  return colors[colors.length - 1];
}

// ─── ECB SDW data fetcher ──────────────────────────────────────────────────────
async function fetchECBSeries(seriesKey) {
  const url = `${ECB_SDW_BASE}/${seriesKey}?format=jsondata&detail=dataonly`;
  const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
  if (!res.ok) throw new Error(`ECB SDW HTTP ${res.status}`);
  const data = await res.json();
  const series = Object.values(data.dataSets[0].series)[0];
  const timeDim = data.structure.dimensions.observation.find(d => d.id === 'TIME_PERIOD');
  const years  = timeDim.values.map(v => parseInt(v.id.substring(0, 4)));
  const values = timeDim.values.map((_, i) => series.observations[i]?.[0] ?? null);
  return { years, values };
}

// ─── Eurostat API fetcher ─────────────────────────────────────────────────────
async function fetchEurostatSeries(datasetId, params) {
  const qs = new URLSearchParams({ format: 'JSON', lang: 'EN', ...params }).toString();
  const url = `${EUROSTAT_BASE}/${datasetId}?${qs}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Eurostat HTTP ${res.status}`);
  const data = await res.json();
  const timeDim = data.dimension.time;
  const years = Object.keys(timeDim.category.index).map(y => parseInt(y)).sort();
  const valueArr = years.map(y => {
    const idx = timeDim.category.index[String(y)];
    return data.value[idx] ?? null;
  });
  return { years, values: valueArr };
}

// ─── Stress score computation ─────────────────────────────────────────────────
function computeStressScores(bankingData, fiscalData) {
  const years = bankingData.annual.years;
  return years.map((year, i) => {
    const b = bankingData.annual;
    const f = fiscalData.annual;

    const bondConc  = (b.govt_bonds_held[i] / b.total_assets[i]) * 100;
    const creditShr = (b.credit_govt[i] / (b.credit_govt[i] + b.credit_private[i])) * 100;
    const fiscalBal = f.balance_pct_gdp[i];
    const sectorSz  = b.total_assets[i] / f.gdp_eur_bn[i];

    const scores = STRESS_COMPONENTS.map(comp => {
      let rawVal;
      if (comp.id === 'bond_concentration') rawVal = bondConc;
      else if (comp.id === 'credit_govt_share') rawVal = creditShr;
      else if (comp.id === 'fiscal_balance') rawVal = fiscalBal;
      else if (comp.id === 'sector_size') rawVal = sectorSz;

      const lo = comp.lowThresh, hi = comp.highThresh;
      let norm = Math.max(0, Math.min(1, (rawVal - lo) / (hi - lo)));
      if (comp.invertSign) norm = 1 - norm;
      return { id: comp.id, rawVal, norm, weight: comp.weight };
    });

    const composite = scores.reduce((s, c) => s + c.norm * c.weight, 0);
    return { year, composite, components: scores, bondConc, creditShr, fiscalBal, sectorSz };
  });
}

// ─── Risk level classification ────────────────────────────────────────────────
function stressLevel(score) {
  if (score < 0.25) return { label: 'Low',      color: '#16a34a', bg: '#dcfce7' };
  if (score < 0.50) return { label: 'Moderate', color: '#f59e0b', bg: '#fef3c7' };
  if (score < 0.75) return { label: 'Elevated', color: '#ea580c', bg: '#ffedd5' };
  return               { label: 'High',     color: '#dc2626', bg: '#fee2e2' };
}
