# Hifzhul Ad'iyyah — E-Learning (Flask)

Ringkasan
- Project: E‑Learning sederhana untuk kursus "Hifzhul Ad'iyyah" (doa harian).
- Stack: Python, Flask, Flask‑SQLAlchemy, Flask‑Login, Jinja2, Tailwind (CDN).
- Tujuan: demo aplikasi pembelajaran dengan peran Admin / Instructor / Student, modul, penilaian, progress, dan UX bernuansa Islami.

Isi Repository
- `app/` — aplikasi Flask (blueprints, models, routes, templates, static assets).
- `run.py` — entrypoint; membuat DB (`db.create_all()`), men‑seed data contoh, lalu menjalankan dev server.
- `requirements.txt` — dependensi Python.
- `instance/` — (opsional) folder instance untuk konfigurasi run-time.

Persiapan Lingkungan (Windows PowerShell)
1. Buat virtualenv dan aktifkan:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependensi:

```powershell
pip install -r requirements.txt
```

Menjalankan Aplikasi (dev)

```powershell
# dari folder proyek (mis. D:\PORTOFOLIO\doa harian)
python run.py
# buka http://127.0.0.1:5000
```

Seed Data & Kredensial Contoh
- `admin` / `admin123` (role: admin)
- `instructor1` / `instructor123` (role: instructor)
- `student1` / `student123` (role: student)

Catatan: `run.py` membuat data contoh setiap kali dijalankan hanya ketika DB kosong. Jika ingin mengulang seed, hapus file DB (biasanya `instance/*.db`) lalu jalankan ulang `python run.py`.

Static Assets (harus ditambahkan manual bila belum ada)
- Hero image: `app/static/img/yuk_berdoa.png` — file PNG untuk hero landing page. Jika belum ada, ada fallback SVG `app/static/img/yuk_berdoa.svg`.
- (Opsional) Audio doa: `app/static/audio/doa_pendek.mp3` — jika ada, assessment modal akan memainkannya.

Perilaku UX penting
- Flash logout: pesan logout menggunakan `flash('Semoga hari Anda diberkahi — Anda telah logout.', 'info')` dan sekarang auto-dismiss setelah 3 detik.
  - Lokasi implementasi: `app/templates/base.html` (atribut `data-autoclose="3000"`, CSS `.flash.hide`, dan JS auto-close).
  - Jika Anda ingin mengubah durasi, edit nilai `data-autoclose` atau ubah JS di `base.html`.

Struktur Model (singkat)
- `User` — field utama: `id, username, full_name, email, password_hash, role`.
- `Course` — `modules` (relasi), `enrollments`.
- `Module` — `assessments`.
- `Assessment`, `Result` — untuk tugas/penilaian dan nilai.
- `Enrollment` — melacak progres siswa per course.

Hal yang Perlu Diperhatikan / Troubleshooting
- Jika terjadi `TemplateSyntaxError` terkait `url_for(...)`, pastikan tanda kutip seimbang di template (sering terjadi jika filename string dipotong atau ada tanda kutip tambahan).
- Jika server keluar dengan error saat `python run.py`, lihat stacktrace di terminal; jika error menunjuk template, periksa file yang disebut dan baris di template.
- Untuk reset DB: hentikan server, hapus file DB di `instance/` (atau sesuai konfigurasi), jalankan `python run.py` untuk seed ulang.

Pengembangan Lanjutan
- Menambahkan file audio murattal untuk tiap doa, integrasi penyimpanan cloud untuk asset, atau migrasi ke Flask‑Migrate.
- Menambahkan tes unit untuk model dan route.

Kontak & Lisensi
- Ini proyek demo/portofolio — sesuaikan lisensi menurut kebutuhan Anda.

---
Terima kasih — kalau mau saya bisa:
- menambahkan file `yuk_berdoa.png` bila Anda upload di chat, atau
- ubah durasi auto-dismiss untuk flash logout, atau
- buatkan skrip reset DB yang lebih aman.
