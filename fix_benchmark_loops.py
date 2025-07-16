#!/usr/bin/env python3
"""
Perbaikan untuk MLSPred-Bench: memastikan semua 12 benchmark diproses
"""

import re

def analyze_and_fix_loops():
    """Menganalisis dan memperbaiki loop yang membatasi pemrosesan benchmark"""

    print("=" * 60)
    print("PERBAIKAN LOOP BENCHMARK PROCESSING")
    print("=" * 60)

    # Baca file original
    with open('/Users/hilmania/Works/MLSPred-Bench/mlspred_bench_v001.py', 'r') as f:
        content = f.read()

    # Analisis loop patterns
    loop_patterns = [
        r'for i in range\(\d+,\s*\d+,\s*-1\):',  # range dengan angka eksplisit
        r'#for i in range\(\d+,\s*\d+,\s*-1\):',  # range yang dikomentari
    ]

    print("Loop patterns yang ditemukan:")
    for pattern in loop_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            print(f"  Line {line_num}: {match.group()}")

    print()

    # Cek for potential issues
    issues_found = []

    # 1. Cek loop yang membatasi
    limited_loops = re.finditer(r'for i in range\(11,\s*\d+,\s*-1\):', content)
    for match in limited_loops:
        line_num = content[:match.start()].count('\n') + 1
        issues_found.append(f"Line {line_num}: Loop terbatas ditemukan: {match.group()}")

    # 2. Cek commented loops yang mungkin aktif
    commented_loops = re.finditer(r'#for i in range\(\d+,\s*\d+,\s*-1\):', content)
    for match in commented_loops:
        line_num = content[:match.start()].count('\n') + 1
        issues_found.append(f"Line {line_num}: Loop terkomentari: {match.group()}")

    if issues_found:
        print("Issues yang ditemukan:")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print("Tidak ada issues loop yang jelas terlihat")

    print()
    print("=" * 60)

    return issues_found

def create_monitoring_version():
    """Membuat versi dengan monitoring yang lebih baik"""

    print("Membuat versi dengan monitoring yang ditingkatkan...")

    # Baca original file
    with open('/Users/hilmania/Works/MLSPred-Bench/mlspred_bench_v001.py', 'r') as f:
        content = f.read()

    # Tambahkan monitoring di awal loop Section 10
    section10_pattern = r'(for i in range\(len\(bnchmrk_names_list\)-1, -1, -1\):)\s*\n(#for i in range\(11, 9, -1\):)'
    section10_replacement = r'''\1
    print(f"Section 10: Processing benchmark {i+1}/12 ({bnchmrk_names_list[i]})")
#\2'''

    content = re.sub(section10_pattern, section10_replacement, content)

    # Tambahkan monitoring di awal loop Section 11
    section11_pattern = r'(for i in range\(len\(bnchmrk_names_list\)-1, -1, -1\):)\s*\n(#for i in range\(11, 9, -1\):)'
    section11_replacement = r'''\1
    print(f"Section 11: Creating ML-Ready dataset for benchmark {i+1}/12 ({bnchmrk_names_list[i]})")
#\2'''

    content = re.sub(section11_pattern, section11_replacement, content)

    # Simpan versi dengan monitoring
    with open('/Users/hilmania/Works/MLSPred-Bench/mlspred_bench_v001_monitored.py', 'w') as f:
        f.write(content)

    print("Versi dengan monitoring disimpan sebagai: mlspred_bench_v001_monitored.py")

if __name__ == "__main__":
    issues = analyze_and_fix_loops()
    create_monitoring_version()

    print()
    print("REKOMENDASI:")
    print("1. Jalankan: mlspred_bench_v001_monitored.py untuk melihat monitoring")
    print("2. Pastikan tidak ada error/exception yang menghentikan loop prematur")
    print("3. Cek ketersediaan file interim untuk semua benchmark")
    print("4. Monitor memory usage selama processing")
