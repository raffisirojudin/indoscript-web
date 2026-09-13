import sys
import re
import math
import random

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# Map tipe eksepsi Python bawaan ke Bahasa Indonesia
KAMUS_EROR = {
    "ZeroDivisionError": "KesalahanBagiNol",
    "NameError": "KesalahanNama",
    "TypeError": "KesalahanTipe",
    "ValueError": "KesalahanNilai",
    "IndexError": "KesalahanIndeks",
    "FileNotFoundError": "BerkasTidakDitemukan",
}

TEKS_BANTUAN = """
==================================================
           BANTUAN SINTAKS INDOSCRIPT             
==================================================
1. Cetak Ke Layar:
   cetak <ekspresi>
   Contoh: cetak "Halo dunia"

2. Simpan Variabel:
   simpan <nama_var> = <nilai>
   Contoh: simpan angka = 100
   Contoh: simpan buah = ["apel", "pisang"]

3. Input Pengguna:
   tanya <nama_var> = "<pesan prompt>"
   Contoh: tanya nama = "Masukkan nama Anda:"

4. Percabangan (Kondisi):
   jika <kondisi> maka
       <perintah>
   kalau_tidak
       <perintah>
   selesai

5. Perulangan:
   ulang <jumlah> kali
       <perintah>
   selesai

   selama <kondisi>
       <perintah>
   selesai

6. Manipulasi Daftar (List):
   tambah <nama_list> = <nilai>
   hapus <nama_list> = <nilai>
   ukuran(<nama_list>)  # Mendapatkan panjang list/teks

7. Operasi Berkas (File I/O):
   tulis_file "<path_file>" = "<isi_teks>"
   baca_file("<path_file>")

8. Fungsi Bawaan Matematika & Acak:
   acak(<min>, <max>)   # Angka acak bulat
   akar(<angka>)        # Akar kuadrat
   pangkat(<x>, <y>)    # x dipangkatkan y

9. Fungsi Kustom:
   fungsi <nama_fungsi>(<param1>, <param2>)
       <perintah>
       kembalikan <nilai>
   selesai

   panggil <nama_fungsi>(<argumen>)

10. Perintah Sistem:
   bantuan  : Menampilkan daftar sintaks me-refresh ingatan sintaks
   keluar   : Keluar dari REPL interaktif
==================================================
"""

class Interpreter:
    def __init__(self):
        self.memori = {}
        self.fungsi_map = {}

    def panggil_fungsi(self, nama_fn, *args):
        if nama_fn not in self.fungsi_map:
            raise Exception(f"Fungsi '{nama_fn}' belum dibuat.")
        
        params, blok_fn = self.fungsi_map[nama_fn]
        if len(params) != len(args):
            raise Exception(f"Fungsi '{nama_fn}' butuh {len(params)} argumen, tapi diberi {len(args)}.")
        
        memori_lokal = self.memori.copy()
        for p, a in zip(params, args):
            memori_lokal[p] = a
        
        try:
            self.jalankan_blok(blok_fn, memori_lokal)
        except ReturnException as ret:
            return ret.value
        return None

    def evaluasi_ekspresi(self, ekspresi, memori_lokal):
        def replacer(match):
            fn_name = match.group(1)
            args_str = match.group(2)
            return f"__panggil('{fn_name}'{', ' + args_str if args_str.strip() else ''})"

        ekspresi_mod = re.sub(r'panggil\s+([a-zA-Z_]\w*)\s*\((.*?)\)', replacer, ekspresi)

        context = {
            "__panggil": lambda fn_name, *args: self.panggil_fungsi(fn_name, *args),
            "str": str, "int": int, "float": float, "len": len, "list": list, "dict": dict,
            "ukuran": len,
            "akar": math.sqrt,
            "pangkat": pow,
            "acak": random.randint,
            "baca_file": lambda path: open(path, "r", encoding="utf-8").read(),
        }
        return eval(ekspresi_mod, context, memori_lokal)

    def eksekusi_baris(self, baris, baris_ke):
        try:
            if baris in ("bantuan", "help"):
                print(TEKS_BANTUAN)

            elif baris.startswith("kembalikan "):
                ekspresi = baris[11:].strip()
                val = self.evaluasi_ekspresi(ekspresi, self.memori)
                raise ReturnException(val)

            elif baris.startswith("panggil "):
                self.evaluasi_ekspresi(baris, self.memori)

            elif baris.startswith("tanya "):
                bagian = baris[6:].split("=")
                nama_var = bagian[0].strip()
                prompt = bagian[1].strip().strip('"')
                jawaban = input(prompt + " ")
                self.memori[nama_var] = int(jawaban) if jawaban.isdigit() else jawaban

            elif baris.startswith("simpan "):
                bagian = baris[7:].split("=", 1)
                nama_var = bagian[0].strip()
                ekspresi = bagian[1].strip()
                self.memori[nama_var] = self.evaluasi_ekspresi(ekspresi, self.memori)

            elif baris.startswith("tambah "):
                bagian = baris[7:].split("=", 1)
                nama_var = bagian[0].strip()
                nilai = self.evaluasi_ekspresi(bagian[1].strip(), self.memori)
                if nama_var in self.memori and isinstance(self.memori[nama_var], list):
                    self.memori[nama_var].append(nilai)
                else:
                    raise Exception(f"Variabel '{nama_var}' bukan daftar (list).")

            elif baris.startswith("hapus "):
                bagian = baris[6:].split("=", 1)
                nama_var = bagian[0].strip()
                nilai = self.evaluasi_ekspresi(bagian[1].strip(), self.memori)
                if nama_var in self.memori and isinstance(self.memori[nama_var], list):
                    if nilai in self.memori[nama_var]:
                        self.memori[nama_var].remove(nilai)
                    else:
                        raise Exception(f"Elemen '{nilai}' tidak ditemukan di daftar '{nama_var}'.")
                else:
                    raise Exception(f"Variabel '{nama_var}' bukan daftar (list).")

            elif baris.startswith("tulis_file "):
                bagian = baris[11:].split("=", 1)
                file_path = self.evaluasi_ekspresi(bagian[0].strip(), self.memori)
                isi_teks = self.evaluasi_ekspresi(bagian[1].strip(), self.memori)
                with open(str(file_path), "w", encoding="utf-8") as f:
                    f.write(str(isi_teks))

            elif baris.startswith("cetak "):
                isi = baris[6:].strip()
                hasil = self.evaluasi_ekspresi(isi, self.memori)
                print(hasil)

            else:
                print(f"[KesalahanSintaks] Baris {baris_ke}: Perintah '{baris}' tidak dikenal.")

        except ReturnException:
            raise
        except Exception as e:
            nama_eror = type(e).__name__
            nama_id = KAMUS_EROR.get(nama_eror, nama_eror)
            print(f"[{nama_id}] Baris {baris_ke}: {e}")

    def jalankan_blok(self, daftar_baris, memori_custom=None):
        memori_awal = self.memori
        if memori_custom is not None:
            self.memori = memori_custom

        i = 0
        while i < len(daftar_baris):
            baris_ke, baris = daftar_baris[i]
            baris = baris.strip()

            if not baris or baris.startswith("#"):
                i += 1
                continue

            if baris.startswith("fungsi "):
                sisa = baris[7:].strip()
                nama_fn = sisa.split("(")[0].strip()
                params_raw = sisa[sisa.find("(")+1 : sisa.rfind(")")]
                params = [p.strip() for p in params_raw.split(",") if p.strip()]

                i += 1
                blok_fn = []
                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    blok_fn.append(daftar_baris[i])
                    i += 1
                self.fungsi_map[nama_fn] = (params, blok_fn)

            elif baris.startswith("ulang ") and baris.endswith(" kali"):
                jumlah = int(self.evaluasi_ekspresi(baris[6:-5].strip(), self.memori))
                i += 1
                blok = []
                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    blok.append(daftar_baris[i])
                    i += 1
                for _ in range(jumlah):
                    self.jalankan_blok(blok)

            elif baris.startswith("selama "):
                kondisi = baris[7:].strip()
                i += 1
                blok_selama = []
                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    blok_selama.append(daftar_baris[i])
                    i += 1
                while self.evaluasi_ekspresi(kondisi, self.memori):
                    self.jalankan_blok(blok_selama)

            elif baris.startswith("jika ") and baris.endswith(" maka"):
                kondisi = baris[5:-5].strip()
                i += 1
                blok_maka, blok_kalau_tidak = [], []
                di_kalau_tidak = False

                while i < len(daftar_baris) and daftar_baris[i][1].strip() != "selesai":
                    if daftar_baris[i][1].strip() == "kalau_tidak":
                        di_kalau_tidak = True
                    else:
                        (blok_kalau_tidak if di_kalau_tidak else blok_maka).append(daftar_baris[i])
                    i += 1

                if self.evaluasi_ekspresi(kondisi, self.memori):
                    self.jalankan_blok(blok_maka)
                else:
                    self.jalankan_blok(blok_kalau_tidak)

            else:
                self.eksekusi_baris(baris, baris_ke)

            i += 1

        self.memori = memori_awal


def mulai_repl():
    """Shell Interaktif untuk IndoScript"""
    print("=== IndoScript 0.1.0 Interactive Shell ===")
    print("Ketik 'bantuan' untuk melihat daftar perintah, atau 'keluar' / Ctrl+C untuk berhenti.\n")
    
    interpreter = Interpreter()
    baris_ke = 1

    while True:
        try:
            baris_input = input("indo> ")
            if baris_input.strip() == "keluar":
                break
            if not baris_input.strip():
                continue

            daftar_baris = [(baris_ke, baris_input)]
            baris_ke += 1

            # Deteksi pembuka blok untuk mendukung multi-line REPL
            b_strip = baris_input.strip()
            butuh_blok = (
                b_strip.startswith("fungsi ") or 
                b_strip.startswith("selama ") or
                (b_strip.startswith("jika ") and b_strip.endswith(" maka")) or 
                (b_strip.startswith("ulang ") and b_strip.endswith(" kali"))
            )

            if butuh_blok:
                kedalaman = 1
                while kedalaman > 0:
                    sub_baris = input("...   ")
                    s_strip = sub_baris.strip()
                    if s_strip.startswith("fungsi ") or s_strip.startswith("selama ") or (s_strip.startswith("jika ") and s_strip.endswith(" maka")) or (s_strip.startswith("ulang ") and s_strip.endswith(" kali")):
                        kedalaman += 1
                    elif s_strip == "selesai":
                        kedalaman -= 1
                    daftar_baris.append((baris_ke, sub_baris))
                    baris_ke += 1

            interpreter.jalankan_blok(daftar_baris)

        except (KeyboardInterrupt, EOFError):
            print("\nSampai jumpa!")
            break


def main():
    if len(sys.argv) < 2:
        mulai_repl()
    else:
        nama_file = sys.argv[1]
        try:
            with open(nama_file, "r") as f:
                baris_mentah = f.readlines()
            
            daftar_baris = [(idx + 1, baris) for idx, baris in enumerate(baris_mentah)]
            interpreter = Interpreter()
            interpreter.jalankan_blok(daftar_baris)
        except FileNotFoundError:
            print(f"[BerkasTidakDitemukan] File '{nama_file}' tidak ditemukan.")

if __name__ == "__main__":
    main()