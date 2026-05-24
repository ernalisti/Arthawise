import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] * {
    color: #c9cdd8 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #7c8394 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #161b27 0%, #1a2035 100%);
    border: 1px solid #1e2d45;
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card.income::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-card.expense::before { background: linear-gradient(90deg, #ef4444, #f87171); }
.metric-card.netcf::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.metric-card.txn::before     { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.metric-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7280;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1.2;
}
.metric-value.positive { color: #10b981; }
.metric-value.negative { color: #ef4444; }
.metric-sub {
    font-size: 0.72rem;
    color: #4b5563;
    margin-top: 6px;
    font-weight: 500;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 36px 0 20px 0;
}
.section-badge {
    background: #1e2535;
    border: 1px solid #2d3748;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #6b7280;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0;
}
.section-divider {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e2535, transparent);
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #0d1f35 0%, #111827 100%);
    border: 1px solid #1e3a5f;
    border-left: 3px solid #3b82f6;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-top: 12px;
}
.insight-box .insight-title {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3b82f6;
    margin-bottom: 6px;
}
.insight-box p {
    font-size: 0.83rem;
    color: #94a3b8;
    line-height: 1.65;
    margin: 0;
}
.insight-box .rec {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #1e3a5f;
    font-size: 0.8rem;
    color: #64748b;
}
.insight-box .rec strong { color: #7dd3fc; }

/* Chart container */
.chart-wrap {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 4px;
}

/* Filter pill */
.filter-active {
    background: #1e3a5f;
    border: 1px solid #2563eb;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: #60a5fa;
    display: inline-block;
    margin: 2px;
}

h1 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; }
h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; }

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib Theme ──────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor':  '#161b27',
    'axes.facecolor':    '#161b27',
    'axes.edgecolor':    '#1e2535',
    'axes.labelcolor':   '#6b7280',
    'axes.titlecolor':   '#e2e8f0',
    'xtick.color':       '#4b5563',
    'ytick.color':       '#4b5563',
    'grid.color':        '#1e2535',
    'grid.linewidth':    0.8,
    'text.color':        '#e2e8f0',
    'font.family':       'sans-serif',
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.spines.left':  False,
    'axes.spines.bottom':False,
})

PALETTE = {
    'income':  '#10b981',
    'expense': '#ef4444',
    'blue':    '#3b82f6',
    'purple':  '#8b5cf6',
    'amber':   '#f59e0b',
    'teal':    '#14b8a6',
    'muted':   '#374151',
    'label':   '#9ca3af',
}

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('Data_Finance_6_Bulan.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Category'] != 'Uncategorized'].reset_index(drop=True)
    df['Year']      = df['Date'].dt.year
    df['Month']     = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].isin([5, 6])
    month_names = {7:'Juli', 8:'Agustus', 9:'September',
                   10:'Oktober', 11:'November', 12:'Desember'}
    df['Month_Label'] = df['Month'].map(month_names)
    return df

df_raw = load_data()

MONTH_ORDER  = ['Juli','Agustus','September','Oktober','November','Desember']
MONTH_NAMES  = {7:'Juli',8:'Agustus',9:'September',10:'Oktober',11:'November',12:'Desember'}
DAY_NAMES    = {0:'Senin',1:'Selasa',2:'Rabu',3:'Kamis',4:'Jumat',5:'Sabtu',6:'Minggu'}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 Finance Tracker")
    st.markdown("<div style='height:1px;background:#1e2535;margin:12px 0 20px'></div>", unsafe_allow_html=True)

    st.markdown("### Filter Data")

    all_months  = MONTH_ORDER
    sel_months  = st.multiselect("Bulan", all_months, default=all_months)

    all_cats    = sorted(df_raw['Category'].unique().tolist())
    sel_cats    = st.multiselect("Kategori", all_cats, default=all_cats)

    all_accs    = sorted(df_raw['Account'].unique().tolist())
    sel_accs    = st.multiselect("Metode Pembayaran", all_accs, default=all_accs)

    st.markdown("<div style='height:1px;background:#1e2535;margin:20px 0 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:#374151;text-align:center'>Dataset: Jul–Des 2025</div>", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_raw[
    (df_raw['Month_Label'].isin(sel_months)) &
    (df_raw['Category'].isin(sel_cats)) &
    (df_raw['Account'].isin(sel_accs))
].copy()

expenses_df = df[df['Type'] == 'EXPENSE'].copy()
income_df   = df[df['Type'] == 'INCOME'].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 32px 0 8px 0;'>
  <div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;
              letter-spacing:0.15em;color:#374151;margin-bottom:8px'>
    CAPSTONE PROJECT · PERSONAL FINANCE
  </div>
  <h1 style='font-size:2rem;font-weight:800;color:#f1f5f9;margin:0;line-height:1.2'>
    Dashboard Keuangan Pribadi
  </h1>
  <div style='font-size:0.85rem;color:#4b5563;margin-top:8px'>
    Periode Juli – Desember 2025 &nbsp;·&nbsp; Analisis transaksi harian
  </div>
</div>
""", unsafe_allow_html=True)

# ── Overview Metrics ──────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

total_income  = income_df['Amount'].sum()
total_expense = expenses_df['Amount'].sum()
net_cf        = total_income - total_expense
total_txn     = len(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card income">
      <div class="metric-label">Total Pemasukan</div>
      <div class="metric-value positive">Rp {total_income/1e6:.2f}jt</div>
      <div class="metric-sub">{len(income_df)} transaksi</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card expense">
      <div class="metric-label">Total Pengeluaran</div>
      <div class="metric-value negative">Rp {total_expense/1e6:.2f}jt</div>
      <div class="metric-sub">{len(expenses_df)} transaksi</div>
    </div>""", unsafe_allow_html=True)

with col3:
    cf_class = "positive" if net_cf >= 0 else "negative"
    cf_sign  = "+" if net_cf >= 0 else ""
    st.markdown(f"""
    <div class="metric-card netcf">
      <div class="metric-label">Net Cash Flow</div>
      <div class="metric-value {cf_class}">{cf_sign}Rp {net_cf/1e6:.2f}jt</div>
      <div class="metric-sub">{'Surplus' if net_cf >= 0 else 'Defisit'} keseluruhan</div>
    </div>""", unsafe_allow_html=True)

with col4:
    avg_exp = expenses_df['Amount'].mean() if len(expenses_df) > 0 else 0
    st.markdown(f"""
    <div class="metric-card txn">
      <div class="metric-label">Total Transaksi</div>
      <div class="metric-value">{total_txn:,}</div>
      <div class="metric-sub">Rata-rata Rp {avg_exp:,.0f}/transaksi</div>
    </div>""", unsafe_allow_html=True)

# ── Helper: section header ────────────────────────────────────────────────────
def section_header(badge, title):
    st.markdown(f"""
    <div class="section-header">
      <span class="section-badge">{badge}</span>
      <span class="section-title">{title}</span>
      <div class="section-divider"></div>
    </div>""", unsafe_allow_html=True)

def insight_box(text, rec=None):
    rec_html = f'<div class="rec"><strong>💡 Rekomendasi:</strong> {rec}</div>' if rec else ''
    st.markdown(f"""
    <div class="insight-box">
      <div class="insight-title">Insight</div>
      <p>{text}</p>
      {rec_html}
    </div>""", unsafe_allow_html=True)

# ── Q1 — Net Cash Flow ────────────────────────────────────────────────────────
section_header("Q1", "Cash Flow Analysis")

monthly_cf = df.groupby(['Year','Month','Type'])['Amount'].sum().unstack(fill_value=0).reset_index()
for col in ['EXPENSE','INCOME']:
    if col not in monthly_cf.columns: monthly_cf[col] = 0
monthly_cf['Net_Cash_Flow'] = monthly_cf['INCOME'] - monthly_cf['EXPENSE']
monthly_cf['Label'] = monthly_cf['Month'].map(MONTH_NAMES)
monthly_cf = monthly_cf[monthly_cf['Label'].isin(sel_months)].copy()
monthly_cf['_ord'] = monthly_cf['Label'].apply(lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 99)
monthly_cf = monthly_cf.sort_values('_ord')

if len(monthly_cf) >= 2:
    first_ncf = monthly_cf.iloc[0]['Net_Cash_Flow']
    last_ncf  = monthly_cf.iloc[-1]['Net_Cash_Flow']
    pct_change = ((last_ncf - first_ncf) / abs(first_ncf)) * 100 if first_ncf != 0 else 0
    worst_month = monthly_cf.loc[monthly_cf['Net_Cash_Flow'].idxmin(), 'Label']
    avg_ncf = monthly_cf['Net_Cash_Flow'].mean()

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    # Bar chart NCF
    colors_ncf = [PALETTE['income'] if v >= 0 else PALETTE['expense'] for v in monthly_cf['Net_Cash_Flow']]
    bars = axes[0].bar(monthly_cf['Label'], monthly_cf['Net_Cash_Flow'],
                       color=colors_ncf, width=0.55, zorder=2)
    axes[0].axhline(0, color='#374151', linewidth=1, linestyle='--')
    axes[0].set_title('Net Cash Flow Bulanan', fontsize=11, fontweight='bold', pad=12)
    axes[0].set_ylabel('Rp', color=PALETTE['label'], fontsize=9)
    axes[0].grid(axis='y', zorder=1)
    axes[0].tick_params(axis='x', labelsize=8)
    for bar, val in zip(bars, monthly_cf['Net_Cash_Flow']):
        axes[0].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + (max(monthly_cf['Net_Cash_Flow'])*0.02),
                     f'Rp{val/1e6:.1f}jt', ha='center', va='bottom', fontsize=7.5,
                     color=PALETTE['label'])

    # Line chart income vs expense
    x = range(len(monthly_cf))
    axes[1].fill_between(x, monthly_cf['INCOME'], alpha=0.15, color=PALETTE['income'])
    axes[1].fill_between(x, monthly_cf['EXPENSE'], alpha=0.15, color=PALETTE['expense'])
    axes[1].plot(x, monthly_cf['INCOME'],  marker='o', color=PALETTE['income'],
                 linewidth=2, markersize=6, label='Pemasukan')
    axes[1].plot(x, monthly_cf['EXPENSE'], marker='s', color=PALETTE['expense'],
                 linewidth=2, markersize=6, label='Pengeluaran')
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels(monthly_cf['Label'].tolist(), fontsize=8)
    axes[1].set_title('Pemasukan vs Pengeluaran', fontsize=11, fontweight='bold', pad=12)
    axes[1].set_ylabel('Rp', color=PALETTE['label'], fontsize=9)
    axes[1].grid(axis='y')
    axes[1].legend(fontsize=8, framealpha=0, labelcolor='#9ca3af')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    pct_sign = "+" if pct_change >= 0 else ""
    insight_box(
        f"Net cash flow rata-rata bulanan sebesar <strong>Rp {avg_ncf:,.0f}</strong> (surplus). "
        f"Perubahan dari bulan pertama ke terakhir sebesar <strong>{pct_sign}{pct_change:.1f}%</strong>, "
        f"dengan titik terendah pada <strong>{worst_month} 2025</strong>.",
        rec="Siapkan sinking fund khusus akhir tahun sejak pertengahan tahun agar surplus tidak merosot tajam di bulan terakhir."
    )

# ── Q2 — Spending per Category ────────────────────────────────────────────────
section_header("Q2", "Spending Pattern per Category")

if len(expenses_df) > 0:
    expense_by_cat = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    monthly_exp_cat = expenses_df.groupby(['Month','Category'])['Amount'].sum().reset_index()
    avg_monthly_cat = monthly_exp_cat.groupby('Category')['Amount'].mean().sort_values(ascending=False)
    top_cat = expense_by_cat.idxmax()
    top_pct = expense_by_cat.max() / expense_by_cat.sum() * 100

    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))

    # Pie chart
    colors_pie = sns.color_palette('viridis', len(expense_by_cat))
    wedges, texts, autotexts = axes[0].pie(
        expense_by_cat.values, labels=expense_by_cat.index,
        autopct='%1.1f%%', startangle=90, colors=colors_pie,
        textprops={'fontsize': 8, 'color': '#9ca3af'},
        wedgeprops={'linewidth': 1.5, 'edgecolor': '#161b27'}
    )
    for at in autotexts: at.set_color('#e2e8f0'); at.set_fontsize(7.5)
    axes[0].set_title('Proporsi Total Pengeluaran', fontsize=11, fontweight='bold', pad=12)

    # Bar chart avg monthly
    colors_bar = sns.color_palette('plasma', len(avg_monthly_cat))
    bars = axes[1].barh(avg_monthly_cat.index, avg_monthly_cat.values,
                        color=colors_bar, height=0.55)
    axes[1].invert_yaxis()
    axes[1].set_title('Rata-rata Pengeluaran Bulanan per Kategori', fontsize=11, fontweight='bold', pad=12)
    axes[1].set_xlabel('Rp', color=PALETTE['label'], fontsize=9)
    axes[1].grid(axis='x')
    axes[1].tick_params(axis='y', labelsize=8)
    for bar, val in zip(bars, avg_monthly_cat.values):
        axes[1].text(val + avg_monthly_cat.max()*0.01, bar.get_y() + bar.get_height()/2,
                     f'Rp {val:,.0f}', va='center', fontsize=7.5, color=PALETTE['label'])

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"Kategori <strong>{top_cat}</strong> menyumbang proporsi terbesar sebesar "
        f"<strong>{top_pct:.1f}%</strong> dari total pengeluaran, dengan rata-rata bulanan "
        f"<strong>Rp {avg_monthly_cat.max():,.0f}</strong>.",
        rec="Optimalkan stok bahan pokok mandiri atau terapkan meal-prep untuk menekan pengeluaran impulsif di kategori dominan."
    )

# ── Q3 — Weekday vs Weekend ───────────────────────────────────────────────────
section_header("Q3", "Temporal / Seasonal Behavior")

if len(expenses_df) > 0:
    exp_copy = expenses_df.copy()
    exp_copy['IsWeekend'] = exp_copy['DayOfWeek'].isin([5,6])
    wkd_avg = exp_copy.groupby('IsWeekend')['Amount'].mean()
    wkd_avg.index = wkd_avg.index.map({False:'Weekday', True:'Weekend'})
    selisih_pct = ((wkd_avg.get('Weekend',0) - wkd_avg.get('Weekday',0)) / wkd_avg.get('Weekday',1)) * 100

    # Daily breakdown too
    exp_copy['DayName'] = exp_copy['DayOfWeek'].map(DAY_NAMES)
    day_avg = exp_copy.groupby(['DayOfWeek','DayName'])['Amount'].mean().reset_index().sort_values('DayOfWeek')

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    bar_colors = [PALETTE['blue'], PALETTE['expense']]
    bars = axes[0].bar(wkd_avg.index, wkd_avg.values, color=bar_colors, width=0.4)
    axes[0].set_title('Rata-rata Pengeluaran: Weekday vs Weekend', fontsize=11, fontweight='bold', pad=12)
    axes[0].set_ylabel('Rata-rata Rp', color=PALETTE['label'], fontsize=9)
    axes[0].grid(axis='y')
    for bar, val in zip(bars, wkd_avg.values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + wkd_avg.max()*0.01,
                     f'Rp {val:,.0f}', ha='center', fontsize=8.5, color=PALETTE['label'])

    day_colors = [PALETTE['expense'] if d in [5,6] else PALETTE['blue'] for d in day_avg['DayOfWeek']]
    axes[1].bar(day_avg['DayName'], day_avg['Amount'], color=day_colors, width=0.55)
    axes[1].set_title('Rata-rata Pengeluaran per Hari', fontsize=11, fontweight='bold', pad=12)
    axes[1].set_ylabel('Rp', color=PALETTE['label'], fontsize=9)
    axes[1].grid(axis='y')
    axes[1].tick_params(axis='x', labelsize=8)
    wkd_patch = mpatches.Patch(color=PALETTE['expense'], label='Weekend')
    wkday_patch = mpatches.Patch(color=PALETTE['blue'], label='Weekday')
    axes[1].legend(handles=[wkday_patch, wkd_patch], fontsize=8, framealpha=0, labelcolor='#9ca3af')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    direction = "lebih tinggi" if selisih_pct > 0 else "lebih rendah"
    insight_box(
        f"Rata-rata pengeluaran Weekend <strong>{direction} {abs(selisih_pct):.1f}%</strong> "
        f"dibandingkan Weekday (Rp {wkd_avg.get('Weekday',0):,.0f} vs Rp {wkd_avg.get('Weekend',0):,.0f}).",
        rec="Tetapkan weekend budget khusus — misalnya batas Rp200.000/hari untuk pengeluaran non-esensial di Sabtu dan Minggu."
    )

# ── Q4 — Income Stability ─────────────────────────────────────────────────────
section_header("Q4", "Income Stability Analysis")

if len(income_df) > 0:
    monthly_income = income_df.groupby(['Year','Month'])['Amount'].sum().reset_index()
    monthly_income['Label'] = monthly_income['Month'].map(MONTH_NAMES)
    monthly_income = monthly_income[monthly_income['Label'].isin(sel_months)].copy()
    monthly_income['_ord'] = monthly_income['Label'].apply(lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 99)
    monthly_income = monthly_income.sort_values('_ord')

    max_inc = monthly_income.loc[monthly_income['Amount'].idxmax()]
    min_inc = monthly_income.loc[monthly_income['Amount'].idxmin()]
    selisih = max_inc['Amount'] - min_inc['Amount']

    fig, ax = plt.subplots(figsize=(12, 4))
    bar_colors = [PALETTE['expense'] if v == monthly_income['Amount'].min()
                  else PALETTE['income'] for v in monthly_income['Amount']]
    bars = ax.bar(monthly_income['Label'], monthly_income['Amount'],
                  color=bar_colors, width=0.55, zorder=2)
    ax.grid(axis='y', zorder=1)
    ax.set_title('Total Pemasukan Bulanan (Jul–Des 2025)', fontsize=11, fontweight='bold', pad=12)
    ax.set_ylabel('Rp', color=PALETTE['label'], fontsize=9)
    ax.tick_params(axis='x', labelsize=9)
    for bar, val in zip(bars, monthly_income['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + monthly_income['Amount'].max()*0.01,
                f'Rp {val/1e6:.2f}jt', ha='center', va='bottom', fontsize=8, color=PALETTE['label'])
    inc_patch  = mpatches.Patch(color=PALETTE['income'],  label='Pemasukan normal')
    low_patch  = mpatches.Patch(color=PALETTE['expense'], label='Pemasukan terendah')
    ax.legend(handles=[inc_patch, low_patch], fontsize=8, framealpha=0, labelcolor='#9ca3af')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"Pemasukan tertinggi terjadi pada <strong>{max_inc['Label']} 2025</strong> "
        f"(Rp {max_inc['Amount']:,.0f}) dan terendah pada <strong>{min_inc['Label']} 2025</strong> "
        f"(Rp {min_inc['Amount']:,.0f}), dengan selisih <strong>Rp {selisih:,.0f}</strong>.",
        rec="Sisihkan kelebihan dari bulan-bulan pemasukan tinggi sebagai income buffer untuk menutup bulan-bulan pemasukan rendah."
    )

# ── Q5 — Metode Pembayaran ────────────────────────────────────────────────────
section_header("Q5", "Metode Pembayaran")

if len(expenses_df) > 0:
    payment_freq = expenses_df.groupby('Account')['Amount'].agg(
        Frekuensi='count', Total='sum', Rata_rata='mean'
    ).sort_values('Frekuensi', ascending=False).reset_index()

    top_acc = payment_freq.iloc[0]

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    # Frekuensi
    colors_freq = sns.color_palette('Blues_r', len(payment_freq))
    bars = axes[0].bar(payment_freq['Account'], payment_freq['Frekuensi'],
                       color=colors_freq, width=0.55, zorder=2)
    axes[0].set_title('Frekuensi Penggunaan Metode Pembayaran', fontsize=11, fontweight='bold', pad=12)
    axes[0].set_xlabel('Metode Pembayaran', color=PALETTE['label'], fontsize=9)
    axes[0].set_ylabel('Jumlah Transaksi', color=PALETTE['label'], fontsize=9)
    axes[0].grid(axis='y', zorder=1)
    axes[0].tick_params(axis='x', labelsize=8)
    for bar, val in zip(bars, payment_freq['Frekuensi']):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     str(int(val)), ha='center', fontsize=9, color=PALETTE['label'])

    # Rata-rata
    colors_avg = sns.color_palette('Oranges_r', len(payment_freq))
    bars2 = axes[1].bar(payment_freq['Account'], payment_freq['Rata_rata'],
                        color=colors_avg, width=0.55, zorder=2)
    axes[1].set_title('Rata-rata Nilai Transaksi per Metode', fontsize=11, fontweight='bold', pad=12)
    axes[1].set_xlabel('Metode Pembayaran', color=PALETTE['label'], fontsize=9)
    axes[1].set_ylabel('Rata-rata Rp', color=PALETTE['label'], fontsize=9)
    axes[1].grid(axis='y', zorder=1)
    axes[1].tick_params(axis='x', labelsize=8)
    for bar, val in zip(bars2, payment_freq['Rata_rata']):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + payment_freq['Rata_rata'].max()*0.01,
                     f'Rp {val:,.0f}', ha='center', fontsize=7.5, color=PALETTE['label'])

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"Metode pembayaran paling sering digunakan adalah <strong>{top_acc['Account']}</strong> "
        f"dengan <strong>{int(top_acc['Frekuensi'])} transaksi</strong> dan rata-rata nilai "
        f"<strong>Rp {top_acc['Rata_rata']:,.0f}</strong> per transaksi.",
        rec="Aktifkan notifikasi transaksi real-time dan tetapkan batas top-up bulanan pada metode pembayaran yang paling sering digunakan."
    )

# ── Q6 — Spending by Day of Week ──────────────────────────────────────────────
section_header("Q6", "High-Impact Transactions — Pengeluaran per Hari")

if len(expenses_df) > 0:
    exp_day = expenses_df.copy()
    exp_day['DayName'] = exp_day['DayOfWeek'].map(DAY_NAMES)
    daily_total = exp_day.groupby(['DayOfWeek','DayName'])['Amount'].sum().reset_index().sort_values('DayOfWeek')

    max_day = daily_total.loc[daily_total['Amount'].idxmax()]
    min_day = daily_total.loc[daily_total['Amount'].idxmin()]
    selisih = max_day['Amount'] - min_day['Amount']

    fig, ax = plt.subplots(figsize=(12, 4))
    bar_colors = [PALETTE['expense'] if v == daily_total['Amount'].max()
                  else '#374151' if v == daily_total['Amount'].min()
                  else PALETTE['blue'] for v in daily_total['Amount']]
    bars = ax.bar(daily_total['DayName'], daily_total['Amount'],
                  color=bar_colors, width=0.55, zorder=2)
    ax.grid(axis='y', zorder=1)
    ax.set_title('Total Pengeluaran per Hari dalam Seminggu (Jul–Des 2025)', fontsize=11, fontweight='bold', pad=12)
    ax.set_ylabel('Total Rp', color=PALETTE['label'], fontsize=9)
    ax.tick_params(axis='x', labelsize=9)
    for bar, val in zip(bars, daily_total['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + daily_total['Amount'].max()*0.01,
                f'Rp {val/1e6:.1f}jt', ha='center', va='bottom', fontsize=8, color=PALETTE['label'])
    high_patch = mpatches.Patch(color=PALETTE['expense'], label=f'Tertinggi ({max_day["DayName"]})')
    low_patch  = mpatches.Patch(color='#374151',          label=f'Terendah ({min_day["DayName"]})')
    mid_patch  = mpatches.Patch(color=PALETTE['blue'],    label='Hari lainnya')
    ax.legend(handles=[high_patch, low_patch, mid_patch], fontsize=8, framealpha=0, labelcolor='#9ca3af')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"Total pengeluaran tertinggi terjadi pada hari <strong>{max_day['DayName']}</strong> "
        f"(Rp {max_day['Amount']:,.0f}) dan terendah pada hari <strong>{min_day['DayName']}</strong> "
        f"(Rp {min_day['Amount']:,.0f}), dengan selisih <strong>Rp {selisih:,.0f}</strong>.",
        rec=f"Jadikan hari {max_day['DayName']} sebagai 'review day' mingguan — evaluasi dan geser pembelian non-esensial ke hari dengan pengeluaran lebih rendah."
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top:1px solid #1e2535;padding-top:20px;text-align:center;
            font-size:0.72rem;color:#374151;font-weight:500'>
  Personal Finance Tracker Dashboard · Capstone Project Dicoding 2025
</div>""", unsafe_allow_html=True)
