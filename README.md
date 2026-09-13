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

## 🛠️ Kata Kunci & Fungsi Bawaan

### 1. Kata Kunci Utama (Keywords)

| Kata Kunci | Deskripsi | Contoh Penggunaan |
| :--- | :--- | :--- |
| `simpan` | Deklarasi atau mengubah nilai variabel | `simpan umur = 20` |
| `cetak` | Menampilkan keluaran ke konsol | `cetak "Halo Dunia"` |
| `tanya` | Menerima masukan (*input*) dari pengguna | `simpan nama = tanya("Nama kamu: ")` |
| `jika` ... `maka` | Percabangan kondisi | `jika nilai > 70 maka` |
| `kalau_tidak` | Alternatif jika kondisi `jika` tidak terpenuhi | `kalau_tidak` |
| `selama` | Perulangan berdasarkan kondisi boolean | `selama hitungan > 0` |
| `ulang` ... `kali` | Perulangan dengan jumlah pasti | `ulang 5 kali` |
| `selesai` | Penutup blok struktur (kondisi, loop, atau fungsi) | `selesai` |
| `fungsi` | Deklarasi fungsi baru | `fungsi hitung(a, b)` |
| `panggil` | Memanggil fungsi yang telah didefinisikan | `simpan x = panggil hitung(2, 3)` |
| `kembalikan` | Mengembalikan nilai dari dalam fungsi | `kembalikan a + b` |
| `tambah` | Menambahkan elemen ke dalam daftar (*list*) | `tambah daftar_angka = 10` |
| `hapus` | Menghapus elemen dari daftar (*list*) berdasarkan nilai | `hapus daftar_angka = 10` |

---

### 2. Fungsi Bawaan (Built-in Functions)

#### 🧮 Matematika & Angka Acak
* **`akar(n)`**: Menghitung akar kuadrat dari bilangan $n$.
  ```indoscript
  simpan hasil = akar(16) # Hasil: 4

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
