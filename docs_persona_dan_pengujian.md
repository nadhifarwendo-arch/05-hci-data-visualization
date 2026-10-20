# Persona, kebutuhan, dan evaluasi UI

## Persona pengguna

**Nama:** Budi Pratama (persona fiktif)  
**Peran:** Analis pengelolaan aset  
**Tujuan:** Memahami tren biaya pemeliharaan dan menemukan aset yang perlu ditindaklanjuti tanpa membaca ratusan baris data satu per satu.  
**Masalah:** Sulit menyaring data menurut wilayah dan kategori; terlalu banyak angka tanpa ringkasan; laporan harus mudah dibagikan.  
**Perilaku:** Menggunakan laptop saat rapat dan perlu melihat ringkasan dengan cepat.

## Kebutuhan fungsional

- Filter aset berdasarkan wilayah dan kategori.
- Filter kejadian pemeliharaan berdasarkan rentang tanggal.
- Menampilkan KPI, tren bulanan, perbandingan kategori, proporsi kondisi, dan relasi biaya-downtime.
- Menampilkan data rinci saat dibutuhkan dan mengunduh data terfilter sebagai CSV.

## Kebutuhan nonfungsional

- Label grafik dan sumbu harus jelas.
- Gunakan warna dan kontras yang dapat dibaca serta jangan menyampaikan makna hanya melalui warna.
- Layout konsisten dan filter diberi nama eksplisit.
- Dashboard tetap menjelaskan saat hasil filter kosong.
- Hindari efek 3D, bayangan berlebihan, dan distorsi sumbu.

## Rencana evaluasi pengguna

Minta 3–5 orang mencoba tugas ini: (1) cari jumlah aset kritis pada satu wilayah, (2) lihat perubahan biaya pemeliharaan dalam rentang waktu tertentu, (3) temukan aset dengan skor kondisi rendah, dan (4) unduh tabel hasil filter. Catat keberhasilan tugas, waktu penyelesaian, dan bagian yang membingungkan. Perbaiki prototipe berdasarkan umpan balik, lalu ulangi tes.

## Prinsip dari materi

Dashboard mengikuti siklus analisis kebutuhan → desain → prototipe → evaluasi; menggunakan ringkasan dan detail-on-demand; memilih line chart untuk tren waktu, bar chart untuk perbandingan kategori, scatter plot untuk hubungan dua variabel numerik, dan pie chart untuk proporsi. Persona ini adalah contoh latihan, bukan hasil survei pengguna nyata.
