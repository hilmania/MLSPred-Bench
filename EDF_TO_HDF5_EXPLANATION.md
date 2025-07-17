# Penjelasan Detail: Bagaimana File EDF Digabungkan ke HDF5

## ❌ **BUKAN**: Semua EDF dari semua pasien digabungkan ke satu HDF5

## ✅ **YANG SEBENARNYA**: Proses Bertahap dengan Multiple Level

---

## **Level 1: Concatenation per Session (Section 7)**

### **Input:**
```
Patient aaaaabcd/
├── Session s001/
│   ├── recording_001.edf    # 1 jam pertama
│   ├── recording_002.edf    # 1 jam kedua
│   ├── recording_003.edf    # 1 jam ketiga
│   └── ...
└── Session s002/
    ├── recording_001.edf
    └── recording_002.edf
```

### **Process:**
```python
# Untuk SETIAP SESSION, concatenate multiple recordings
for session in patient_sessions:
    session_data = []

    # Load semua EDF files dalam satu session
    for edf_file in session_recordings:
        eeg_data = mne.io.read_raw_edf(edf_file)
        session_data.append(eeg_data)

    # Concatenate dalam session yang sama
    full_session_data = np.concatenate(session_data, axis=1)  # Time dimension

    # Save per session
    np.save(f"raweeg/{session_id}.npy", full_session_data)
```

### **Output Level 1:**
```
raweeg/
├── trn_abc_s001_le2.npy    # Session 1 lengkap (continuous EEG)
├── trn_abc_s002_le2.npy    # Session 2 lengkap
├── vld_def_s001_le2.npy    # Session dari patient lain
└── ...
```

**Satu file .npy = Satu session lengkap dari satu pasien**

---

## **Level 2: Extract Seizure Segments (Section 10)**

### **Process:**
```python
# Untuk setiap benchmark dan setiap seizure:
for benchmark in benchmarks:
    for seizure in valid_seizures:
        # Load session data yang mengandung seizure ini
        session_data = np.load(f"montage/{seizure_session_id}.npy")

        # Extract segments 5-detik dari periode preictal
        preictal_start = seizure_time - SPH_duration
        segments = extract_5sec_windows(session_data, preictal_start, SPH_duration)

        # Extract segments interictal dari non-seizure session
        interictal_segments = extract_5sec_windows(non_seizure_session_data)

        # Combine preictal + interictal untuk satu seizure
        seizure_dataset = np.concatenate([segments, interictal_segments])

        # Save per seizure per benchmark
        np.save(f"interim/...bmrk{XX}_sz{YYYY}_{patient}_{split}_values.npy", seizure_dataset)
```

### **Output Level 2:**
```
interim/
├── tuhszr_interm_...bmrk01_sz0001_abc_s001_train_values.npy    # 1 seizure data
├── tuhszr_interm_...bmrk01_sz0002_def_s001_train_values.npy    # 1 seizure data
├── tuhszr_interm_...bmrk01_sz0003_ghi_s002_valid_values.npy    # 1 seizure data
└── ...
```

**Satu file .npy = Data dari satu seizure (preictal + interictal segments)**

---

## **Level 3: Final ML-Ready HDF5 (Section 11)**

### **Process:**
```python
# Untuk setiap benchmark:
for benchmark in benchmarks:

    # Collect semua seizures untuk training
    train_data = []
    train_labels = []

    # Load semua interim files untuk benchmark ini
    train_interim_files = find_files(f"*bmrk{benchmark_id}*train*")

    for interim_file in train_interim_files:
        seizure_data = np.load(interim_file)  # Shape: (segments, channels, samples)
        train_data.append(seizure_data)

        # Create labels untuk seizure ini
        n_segments = seizure_data.shape[0]
        seizure_labels = [1] * (n_segments//2) + [0] * (n_segments//2)  # 50% preictal, 50% interictal
        train_labels.extend(seizure_labels)

    # Combine ALL training seizures untuk benchmark ini
    final_train_data = np.concatenate(train_data, axis=0)

    # Save ke HDF5
    with h5py.File(f"bmrk{benchmark_id}_train_values.hdf5", 'w') as f:
        f.create_dataset('tracings', data=final_train_data)
```

### **Output Level 3:**
```
fld_sng/
├── tuhszr_sngfld_...bmrk01_...train_values.hdf5    # ALL training seizures for BM01
├── tuhszr_sngfld_...bmrk01_...valid_values.hdf5    # ALL validation seizures for BM01
├── tuhszr_sngfld_...bmrk01_...tests_values.hdf5    # ALL test seizures for BM01
├── tuhszr_sngfld_...bmrk02_...train_values.hdf5    # ALL training seizures for BM02
└── ...
```

**Satu file HDF5 = Semua seizures dari multiple patients untuk satu benchmark dan satu split**

---

## **🔍 Summary: Apa yang Digabungkan ke HDF5?**

### **BUKAN:**
- ❌ Semua EDF files dari semua pasien
- ❌ Raw continuous EEG data
- ❌ Satu HDF5 untuk semua data

### **YANG BENAR:**
- ✅ **Segmented data** (5-detik windows) dari **multiple seizures**
- ✅ **Filtered by benchmark** (SPH/SOP configuration)
- ✅ **Separated by dataset split** (train/valid/test)
- ✅ **Balanced preictal/interictal** segments

### **Struktur Data dalam HDF5:**
```python
# Shape dalam HDF5:
data.shape = (total_segments, samples_per_segment, channels)
            # (N, 1280, 20)
            # N = sum of segments from all seizures in this split

# Contoh untuk BM01 training:
# - 100 seizures × 48 segments = 4800 total segments
# - Shape: (4800, 1280, 20)
# - Labels: 2400 preictal (1) + 2400 interictal (0)
```

---

## **📊 Hierarchy Visualization:**

```
TUSZ Raw Data
├── Patient A
│   ├── Session 1: recording_001.edf + recording_002.edf → raweeg/A_s001.npy
│   └── Session 2: recording_001.edf → raweeg/A_s002.npy
├── Patient B
│   └── Session 1: recording_001.edf + recording_002.edf → raweeg/B_s001.npy
└── ...

↓ Extract seizure segments

Interim Seizure Data
├── Seizure 1 (from Patient A): interim/...sz0001_A_train.npy
├── Seizure 2 (from Patient A): interim/...sz0002_A_train.npy
├── Seizure 3 (from Patient B): interim/...sz0003_B_valid.npy
└── ...

↓ Combine by benchmark + split

Final ML-Ready HDF5
├── bmrk01_train.hdf5: [Seizure1 + Seizure2 + Seizure5 + ...] (from train patients)
├── bmrk01_valid.hdf5: [Seizure3 + Seizure7 + Seizure9 + ...] (from valid patients)
└── bmrk01_tests.hdf5: [Seizure4 + Seizure6 + Seizure8 + ...] (from test patients)
```

Jadi **HDF5 final berisi segmented data dari multiple seizures, bukan raw EDF files**! 🧠⚡
