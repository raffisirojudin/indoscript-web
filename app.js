let pyodide;
let editor;

// --- FITUR BAGIKAN (1/3): Pembaca tautan dari URL ---
function cekTautanBerbagi() {
  if (window.location.hash) {
    try {
      const base64 = window.location.hash.substring(1);
      return decodeURIComponent(escape(atob(base64)));
    } catch (e) {
      console.error("Gagal membaca tautan:", e);
    }
  }
  return null;
}

// Daftar contoh kode
const CONTOH_KODE = {
  halo: `# Program Pertama
simpan nama = "Dunia"
cetak "Halo " + nama + "!"

simpan daftar_angka = [1, 2, 3]
tambah daftar_angka = 4
cetak daftar_angka`,

  looping: `# Contoh Perulangan
simpan hitungan = 3
selama hitungan > 0
    cetak "Hitung mundur: " + tulisan(hitungan)
    simpan hitungan = hitungan - 1
selesai
cetak "Selesai!"`,

  fungsi: `# Contoh Fungsi Matematika
fungsi tambah_lima(angka)
    kembalikan angka + 5
selesai

simpan hasil = panggil tambah_lima(10)
cetak "Hasil: " + tulisan(hasil)
cetak "Akar dari 81 adalah: " + tulisan(akar(81))`
};

// 1. Register Bahasa & Syntax Highlighting IndoScript di Monaco Editor
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.38.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
  
  // Daftarkan bahasa 'indoscript'
  monaco.languages.register({ id: 'indoscript' });

  // Tentukan warna & aturan kata kunci
  monaco.languages.setMonarchTokensProvider('indoscript', {
    keywords: [
      'simpan', 'cetak', 'tanya', 'jika', 'maka', 'kalau_tidak', 
      'selesai', 'ulang', 'kali', 'selama', 'tambah', 'hapus', 
      'tulis_file', 'fungsi', 'kembalikan', 'panggil'
    ],
    builtins: ['ukuran', 'akar', 'pangkat', 'acak', 'baca_file', 'tulisan', 'bulat', 'desimal'],
    tokenizer: {
      root: [
        [/[a-zA-Z_]\w*/, {
          cases: {
            '@keywords': 'keyword',
            '@builtins': 'predefined',
            '@default': 'identifier'
          }
        }],
        [/#.*/, 'comment'],
        [/"[^"]*"/, 'string'],
        [/\d+/, 'number'],
      ]
    }
  });

  // Atur tema warna khusus
  monaco.editor.defineTheme('indoscript-theme', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: '569CD6', fontStyle: 'bold' },
      { token: 'predefined', foreground: 'DCDCAA' },
      { token: 'string', foreground: 'CE9178' },
      { token: 'number', foreground: 'B5CEA8' },
      { token: 'comment', foreground: '6A9955' }
    ],
    colors: {}
  });

  // --- FITUR BAGIKAN (2/3): Utamakan isi dari URL jika ada ---
  const kodeAwal = cekTautanBerbagi() || CONTOH_KODE.halo;

  editor = monaco.editor.create(document.getElementById('editor-container'), {
    value: kodeAwal,
    language: 'indoscript',
    theme: 'indoscript-theme',
    automaticLayout: true,
    fontSize: 14
  });
});

// 2. Inisialisasi Pyodide Engine
async function initPyodide() {
  const statusEl = document.getElementById('status');
  const outputEl = document.getElementById('console-output');
  const runBtn = document.getElementById('run-btn');

  try {
    pyodide = await loadPyodide();
    
    // Custom handling untuk fungsi input()/tanya agar muncul prompt browser
    pyodide.setInterruptBuffer();
    
    let response = await fetch('interpreter.py');
    let interpreterCode = await response.text();
    
    pyodide.FS.writeFile('interpreter.py', interpreterCode);
    
    await pyodide.runPythonAsync(`
import sys
import io
import builtins
from interpreter import Interpreter

# Override input() bawaan python agar kompatibel dengan browser prompt
def browser_input(prompt_text=""):
    import js
    res = js.prompt(prompt_text)
    return res if res is not None else ""

builtins.input = browser_input
interpreter_instance = Interpreter()
    `);

    statusEl.innerText = "● Mesin Siap";
    statusEl.style.color = "#4EC9B0";
    outputEl.innerText = "IndoScript v0.1.0 Engine Siap.\nKlik 'Jalankan' untuk mengeksekusi kode.\n----------------------------------------\n";
    runBtn.disabled = false;
  } catch (err) {
    statusEl.innerText = "● Gagal Memuat";
    statusEl.style.color = "#F44747";
    outputEl.innerText = "Error memuat engine: " + err.message;
  }
}

// 3. Fungsi Jalankan Kode
async function jalankanKode() {
  const outputEl = document.getElementById('console-output');
  const code = editor.getValue();
  
  // Bersihkan layar console sebelum kode baru dieksekusi
  outputEl.innerText = "";

  try {
    pyodide.globals.set("kode_user", code);
    let output = await pyodide.runPythonAsync(`
buffer = io.StringIO()
sys.stdout = buffer

baris_mentah = kode_user.splitlines()
daftar_baris = [(idx + 1, baris) for idx, baris in enumerate(baris_mentah)]

try:
    interpreter_instance.jalankan_blok(daftar_baris)
except Exception as e:
    print(f"[ErorWeb] {e}")

sys.stdout = sys.__stdout__
buffer.getvalue()
    `);
    
    outputEl.innerText = output || "(Selesai tanpa keluaran)\n";
    outputEl.scrollTop = outputEl.scrollHeight;
  } catch (err) {
    outputEl.innerText = "[KesalahanSistemWeb]: " + err.message + "\n";
  }
}

// 4. Fitur Pendukung
function bersihkanConsole() {
  document.getElementById('console-output').innerText = "";
}

function muatContoh(kunci) {
  if (CONTOH_KODE[kunci]) {
    editor.setValue(CONTOH_KODE[kunci]);
  }
}

// --- FITUR BAGIKAN (3/3): Pembuat link tautan ke clipboard ---
async function bagikanKode() {
  const code = editor.getValue();
  
  try {
    const base64 = btoa(unescape(encodeURIComponent(code)));
    const urlBagikan = window.location.origin + window.location.pathname + '#' + base64;
    
    // 1. Opsi Share bawaan HP / Browser (WhatsApp, Telegram, dll)
    if (navigator.share) {
      await navigator.share({
        title: 'IndoScript Playground',
        text: 'Lihat kode IndoScript yang aku buat ini:',
        url: urlBagikan
      });
    } else {
      // 2. Fallback untuk browser PC (Salin ke Clipboard)
      await navigator.clipboard.writeText(urlBagikan);
      alert("Tautan kode berhasil disalin! Kamu bisa langsung paste di chat atau media sosial.");
    }
  } catch (err) {
    // Abaikan eror jika pengguna membatalkan dialog share
    if (err.name !== 'AbortError') {
      alert("Gagal membagikan: " + err.message);
    }
  }
}

initPyodide();
