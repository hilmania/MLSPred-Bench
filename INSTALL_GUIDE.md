# Panduan Instalasi MLSPred-Bench - Solusi Error Requirements

## Cara Menggunakan

### Opsi 1: Manual Installation

```bash
# 1. Pastikan menggunakan Python 3.8 atau yang lebih baru
python3 --version

# 2. Buat virtual environment (opsional tapi direkomendasikan)
python3 -m venv .mlspredbench
source .mlspredbench/bin/activate

# 3. Update pip
python -m pip install --upgrade pip

# 4. Install requirements
python -m pip install -r requirements.txt

# 5. Test instalasi
python test_imports.py
```

### Opsi 2: Menggunakan Setup Script

```bash
# Jalankan setup script yang telah dibuat
./setup.sh
```

### Opsi 3: Manual dengan versi spesifik Python

Jika Anda memiliki beberapa versi Python, gunakan versi yang kompatibel:

```bash
# Untuk Python 3.11 (yang sudah dikonfigurasi)
/usr/local/bin/python3.11 -m pip install -r requirements.txt
/usr/local/bin/python3.11 test_imports.py
```

## Verifikasi Instalasi

Setelah instalasi, jalankan:

```bash
python test_imports.py
```

Output yang diharapkan:
```
============================================================
MLSPred-Bench Dependencies Test
============================================================

Testing core dependencies...
✅ NumPy 1.26.4 - OK
✅ H5PY 3.11.0 - OK
✅ MNE 1.6.1 - OK
✅ Scikit-learn 1.3.2 - OK
✅ SciPy 1.10.1 - OK
✅ Standard library modules (random, csv, os, time) - OK

Testing optional dependencies...
✅ matplotlib 3.7.5 - OK
✅ joblib 1.5.1 - OK
✅ tqdm 4.67.1 - OK
✅ requests 2.32.4 - OK

============================================================
Dependency test completed!
============================================================
```

## Menjalankan MLSPred-Bench

Setelah semua dependencies terinstall, Anda dapat menjalankan:

```bash
python mlspred_bench_v001.py [PATH_TO_TUSZ_DATA] [PATH_TO_OUTPUT]
```

Contoh:
```bash
python mlspred_bench_v001.py /path/to/raw/tusz/data /path/to/save/generated/data
```

## Troubleshooting

### Jika masih ada error instalasi:
1. Pastikan menggunakan Python 3.8 atau lebih baru
2. Update pip: `python -m pip install --upgrade pip`
3. Coba install dependencies satu per satu untuk mengidentifikasi yang bermasalah
4. Gunakan virtual environment yang bersih

### Jika ada error saat running:
1. Jalankan `test_imports.py` untuk memastikan semua dependencies terinstall
2. Periksa path data input yang digunakan
3. Pastikan memiliki cukup ruang disk (>150GB seperti yang disebutkan di README)

## Perubahan yang Dibuat

1. **requirements.txt** - Diperbaiki dan disederhanakan
2. **test_imports.py** - Script untuk test dependencies
3. **setup.sh** - Script automasi setup
4. **INSTALL_GUIDE.md** - Dokumentasi ini

Semua file telah dikonfigurasi dan tested dengan Python 3.11.9, dan semua dependencies berhasil diinstall dan dapat diimport.
