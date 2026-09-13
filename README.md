# IndoScript Web Playground

**IndoScript** adalah bahasa pemrograman edukatif berbahasa Indonesia. Repositori ini berisi **Web Playground** resmi yang memungkinkan siapa saja mencoba dan mengeksekusi sintaks IndoScript secara langsung di browser tanpa perlu proses instalasi atau *setup environment*.

---

## 🚀 Fitur Utama

* **100% Client-Side Execution:** Berjalan sepenuhnya di browser pengguna menggunakan Pyodide (Python WebAssembly), sehingga sangat cepat dan hemat energi server.
* **Code Editor Interaktif:** Menggunakan Monaco Editor (mesin utama VS Code) lengkap dengan *syntax highlighting* khusus sintaks IndoScript.
* **Web Console:** Menampilkan keluaran (*output*) dan pesan eror secara *real-time*.
* **Fitur Bagikan (Share Link):** Mengubah kode yang ditulis menjadi URL unik (Base64) untuk dibagikan ke media sosial atau teman.
* **Desain Responsif:** Mendukung tampilan layar desktop (kiri-kanan) dan perangkat seluler / HP (atas-bawah).
* **Pustaka Contoh Kode:** Menyediakan contoh program bawaan untuk membantu pemula memahami konsep dasar.

---

## 💻 Contoh Sintaks IndoScript

```indoscript
# Program Utama IndoScript
simpan nama = "Dunia"
cetak "Halo " + nama + "!"

# Perulangan
simpan hitungan = 3
selama hitungan > 0
    cetak "Hitung mundur: " + str(hitungan)
    simpan hitungan = hitungan - 1
selesai

# Fungsi
fungsi tambah_lima(angka)
    kembalikan angka + 5
selesai

simpan hasil = panggil tambah_lima(10)
cetak "Hasil: " + str(hasil)
