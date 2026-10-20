# 05 — Human-Computer Interaction & Data Visualization

## Kesesuaian dengan transkrip

Proyek ini membuat dashboard interaktif untuk pengelolaan aset infrastruktur dengan **data sintetis**. Materi narasumber menekankan bahwa UI harus dirancang untuk kebutuhan pengguna, bukan selera pembuat; data rumit sebaiknya diringkas menjadi visual yang bermakna; prototipe perlu dievaluasi; dan setiap chart dipilih sesuai pertanyaannya.

Implementasi mengadaptasi prinsip berikut:

- **User-centered design:** persona, kebutuhan fungsional/nonfungsional, dan rencana usability testing tersedia di `docs_persona_dan_pengujian.md`.
- **Mengurangi beban kognitif:** KPI ringkas ditampilkan di awal dan filter ditempatkan di sidebar dengan label yang eksplisit.
- **Visualisasi yang sesuai:** line chart untuk tren biaya dari waktu ke waktu, bar chart untuk membandingkan kategori, pie chart untuk proporsi kondisi, dan scatter plot untuk hubungan downtime dengan biaya.
- **Interaksi:** filter wilayah/kategori/tanggal, hover detail di scatter plot, tabel aset, expander untuk riwayat pemeliharaan, serta unduh CSV.
- **Kejujuran visual:** grafik tidak memakai efek 3D dekoratif; satuan dan label sumbu disediakan; kondisi filter kosong juga diberi pesan.

## Menjalankan dashboard

Python 3.10+ disarankan.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

Browser akan membuka aplikasi Streamlit secara lokal. Jika file CSV belum ada, dashboard juga mencoba membuat data sintetis secara otomatis.

## Repo referensi

- [jywade/Streamlit-Data-App](https://github.com/jywade/Streamlit-Data-App) — contoh dashboard dengan Streamlit, Pandas, Plotly, filter tanggal/wilayah, visualisasi interaktif, dan opsi melihat/mengunduh data.
- [fneum/streamlit-tutorial](https://github.com/fneum/streamlit-tutorial) — contoh ringkas integrasi Streamlit dan Plotly.
- [Dokumentasi resmi Streamlit: st.plotly_chart](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart) — perilaku dan opsi grafik interaktif.

Tautan di atas adalah referensi publik yang mendukung materi, bukan repo resmi milik narasumber webinar. Dataset dashboard ini dibuat khusus untuk latihan.
