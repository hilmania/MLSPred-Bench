#!/usr/bin/env python3
"""
Analisis kondisi yang menyebabkan benchmark tidak diproses
"""

def analyze_benchmark_conditions():
    print("=" * 70)
    print("ANALISIS KONDISI PEMROSESAN BENCHMARK")
    print("=" * 70)

    # Simulasi benchmark creation logic
    benchmark_sph_list = [2, 5, 15, 30]
    benchmark_sop_list = [1, 2, 5]
    benchmark_tot_list = [(a, b) for a in benchmark_sph_list for b in benchmark_sop_list]
    bnchmrk_names_list = [f"bmrk{1+i:02d}" for i in range(len(benchmark_tot_list))]
    preferred_gap_times_mins_list = [x[0] + x[1] for x in benchmark_tot_list]

    win_len_secs = 5

    print("Analisis kondisi pemrosesan untuk setiap benchmark:")
    print()

    for i, (sph, sop) in enumerate(benchmark_tot_list):
        benchmark_id = bnchmrk_names_list[i]
        gap_len_mins = sph + sop
        num_of_pre_segs = sph * 60 // win_len_secs

        print(f"{benchmark_id} (SPH={sph}min, SOP={sop}min):")
        print(f"  Gap time required: {gap_len_mins} minutes")
        print(f"  num_of_pre_segs: {num_of_pre_segs}")

        # Analisis kemungkinan masalah
        potential_issues = []

        if gap_len_mins < 10:
            potential_issues.append(f"Gap time sangat kecil ({gap_len_mins}min) - mungkin kurang data yang memenuhi syarat")

        if num_of_pre_segs < 10:
            potential_issues.append(f"Segments sedikit ({num_of_pre_segs}) - mungkin tidak cukup data")

        if gap_len_mins > 30:
            potential_issues.append(f"Gap time besar ({gap_len_mins}min) - kemungkinan lebih banyak data valid")

        if potential_issues:
            print("  Potential issues:")
            for issue in potential_issues:
                print(f"    - {issue}")
        else:
            print("  Tidak ada masalah yang jelas")

        print()

    print("=" * 70)
    print("KESIMPULAN:")
    print("=" * 70)

    print("Benchmark dengan gap time kecil (BM01-BM09) mungkin tidak memiliki:")
    print("1. Cukup seizure dengan gap time yang memadai")
    print("2. Data interictal yang cukup dari non-seizure sessions")
    print("3. File montage yang valid")
    print()

    print("Benchmark dengan gap time besar (BM10-BM12) lebih mungkin berhasil karena:")
    print("1. Persyaratan gap time lebih mudah dipenuhi dengan data yang tersedia")
    print("2. Lebih banyak seizure yang memenuhi kriteria minimum gap")
    print("3. SPH yang lebih besar memberikan lebih banyak data per seizure")
    print()

    print("Untuk debugging lebih lanjut, perlu dicek:")
    print("1. Berapa banyak seizure yang memenuhi gap time requirement untuk setiap benchmark")
    print("2. Apakah ada non-seizure sessions yang tersedia untuk interictal data")
    print("3. Apakah ada error dalam file montage atau interim data")

if __name__ == "__main__":
    analyze_benchmark_conditions()
