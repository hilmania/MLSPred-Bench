#!/usr/bin/env python3
"""
Debug script untuk menganalisis mengapa hanya BM10, BM11, BM12 yang dihasilkan
"""

# Simulasi benchmark creation logic dari kode asli
benchmark_sph_list = [2, 5, 15, 30]
benchmark_sop_list = [1, 2, 5]
benchmark_tot_list = [(a, b) for a in benchmark_sph_list for b in benchmark_sop_list]
bnchmrk_names_list = [f"bmrk{1+i:02d}" for i in range(len(benchmark_tot_list))]
preferred_gap_times_mins_list = [x[0] + x[1] for x in benchmark_tot_list]

print("=" * 60)
print("ANALISIS BENCHMARK MLSPred-Bench")
print("=" * 60)

print(f"benchmark_sph_list: {benchmark_sph_list}")
print(f"benchmark_sop_list: {benchmark_sop_list}")
print(f"benchmark_tot_list: {benchmark_tot_list}")
print(f"bnchmrk_names_list: {bnchmrk_names_list}")
print(f"preferred_gap_times_mins_list: {preferred_gap_times_mins_list}")
print()

print("Mapping Benchmark ke SPH/SOP:")
for i, (sph, sop) in enumerate(benchmark_tot_list):
    print(f"  {bnchmrk_names_list[i]}: SPH={sph}min, SOP={sop}min, Gap={sph+sop}min")
print()

# Analisis loop ranges
num_of_bmrks = len(bnchmrk_names_list)
print(f"Total benchmarks: {num_of_bmrks}")
print()

print("Range Analysis:")
full_range = list(range(len(bnchmrk_names_list)-1, -1, -1))
partial_range = list(range(11, 9, -1))

print(f"range(len(bnchmrk_names_list)-1, -1, -1) = range({len(bnchmrk_names_list)-1}, -1, -1)")
print(f"  → {full_range}")
print(f"  → Memproses benchmark indices: {full_range}")
print(f"  → Memproses benchmarks: {[bnchmrk_names_list[i] for i in full_range]}")
print()

print(f"range(11, 9, -1) = {partial_range}")
print(f"  → Memproses benchmark indices: {partial_range}")
print(f"  → Memproses benchmarks: {[bnchmrk_names_list[i] for i in partial_range]}")
print()

print("=" * 60)
print("KEMUNGKINAN PENYEBAB MASALAH:")
print("=" * 60)

print("1. KODE YANG DIKOMENTARI:")
print("   Line 1163: #for i in range(11, 9, -1):")
print("   Line 1328: #for i in range(11, 9, -1):")
print("   → Jika baris ini yang aktif, hanya BM11 dan BM12 yang diproses")
print()

print("2. KEMUNGKINAN KONDISI LAIN:")
print("   - Ada error/exception yang menyebabkan loop berhenti prematur")
print("   - Ada kondisi if yang membatasi pemrosesan benchmark")
print("   - File interim untuk BM01-BM09 tidak ditemukan/tidak valid")
print("   - Memory/disk space habis saat processing benchmark awal")
print()

print("3. SOLUSI YANG DISARANKAN:")
print("   - Pastikan loop menggunakan: for i in range(len(bnchmrk_names_list)-1, -1, -1):")
print("   - Tambahkan logging/print statements untuk debugging")
print("   - Cek apakah file interim untuk semua benchmark tersedia")
print("   - Cek error handling dan exception yang mungkin terjadi")
print()

print("=" * 60)
