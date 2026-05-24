# Personal Finance Tracker Dashboard

Dashboard interaktif untuk analisis keuangan pribadi Juli–Desember 2025.

## Struktur File

```
├── app.py
├── requirements.txt
└── Data_Finance_6_Bulan.csv   ← letakkan di folder yang sama
```

## Cara Deploy ke Streamlit Cloud

1. Upload semua file ke **satu repository GitHub** (public)
2. Pastikan `Data_Finance_6_Bulan.csv` ikut di-push ke repo
3. Buka [share.streamlit.io](https://share.streamlit.io)
4. Klik **New app** → pilih repo → set `Main file path: app.py`
5. Klik **Deploy**

## Fitur Dashboard

- **Overview** — Total income, expense, net cash flow, jumlah transaksi
- **Filter sidebar** — by bulan, kategori, metode pembayaran
- **Q1** — Tren Net Cash Flow bulanan
- **Q2** — Proporsi & rata-rata pengeluaran per kategori
- **Q3** — Perbandingan Weekday vs Weekend
- **Q4** — Stabilitas pemasukan bulanan (tertinggi, terendah, selisih)
- **Q5** — Frekuensi & rata-rata nilai per metode pembayaran
- **Q6** — Total pengeluaran per hari dalam seminggu
