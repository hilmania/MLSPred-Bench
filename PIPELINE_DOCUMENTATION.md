# Alur Lengkap MLSPred-Bench: Generate Dataset dari TUSZ

## Overview Pipeline

MLSPred-Bench adalah tool untuk mengkonversi raw EEG data dari Temple University Hospital Seizure (TUSZ) dataset menjadi ML-ready benchmark dataset untuk epileptic seizure prediction. Pipeline terdiri dari **11 section utama** yang berjalan secara sequential.

---

## **Section 1: Import Libraries**

**Tujuan:** Import semua library yang diperlukan untuk processing

```python
import numpy as np, h5py, mne, csv, os, time
from sklearn.preprocessing import scale, minmax_scale
from sklearn.utils import shuffle
```

**Output:** Environment siap untuk processing

---

## **Section 2: Define Needed Functions**

**Tujuan:** Definisi fungsi utility seperti insertion sort

**Fungsi Utama:**
- `insertion_sort()`: Sorting algorithm untuk data arrangement

---

## **Section 3: Create Target Paths**

**Tujuan:** Setup struktur direktori untuk menyimpan output

**Input:**
- `source_path`: Path ke raw TUSZ data
- `target_path`: Path untuk menyimpan generated data

**Process:**
```python
# Struktur direktori yang dibuat:
target_path/
├── meta_data/     # Metadata extracted dari TUSZ
├── raweeg/        # Raw EEG data yang sudah diorganisir
├── montage/       # Montage calculations (bipolar)
├── interim/       # Interim dataset files
└── fld_sng/       # Final ML-ready single-fold datasets
```

**Output:** Struktur direktori siap

---

## **Section 4: Identify Available Records**

**Tujuan:** Scan dan inventarisasi semua file yang tersedia di TUSZ dataset

**Process:**
1. **Scan Directory Structure:**
   ```
   TUSZ/
   ├── train/     # Training patients
   ├── dev/       # Development/validation patients
   └── eval/      # Evaluation/test patients
   ```

2. **Identify File Types:**
   - `.edf`: Raw EEG recordings
   - `.csv_bi`: Seizure annotation files
   - `.txt`: Session summary files

3. **Build File Inventory:**
   - List semua recording paths
   - Map patient → sessions → files
   - Count total recordings per dataset split

**Output:**
- `all_edf_fls_list`: List semua EDF files
- `all_csv_fls_list`: List semua annotation files
- `path_counts_dict`: Statistik files per dataset

---

## **Section 5: Extract TUH Metadata**

**Tujuan:** Parse seizure annotations dan convert ke format yang user-friendly

**Process:**
1. **Parse CSV Annotation Files:**
   ```csv
   # Format TUSZ annotation:
   start_time,stop_time,label,confidence
   12.5,18.7,seiz,1.0
   ```

2. **Extract Seizure Information:**
   - Start time dan end time setiap seizure
   - Calculate seizure duration
   - Map seizures ke corresponding sessions

3. **Build Metadata Structures:**
   ```python
   seiz_strt_time_dict = {session_id: [start_times]}
   seiz_ends_time_dict = {session_id: [end_times]}
   seiz_dura_time_dict = {session_id: [durations]}
   ```

**Output:**
- Structured seizure metadata untuk semua sessions
- Timing information untuk seizure events

---

## **Section 6: Identify Channels & Sampling Rates**

**Tujuan:** Analyze EEG recordings untuk determine channels dan sampling rates

**Process:**
1. **Load EEG Headers:**
   ```python
   for edf_file in edf_files:
       eeg_data = mne.io.read_raw_edf(edf_file, preload=False)
       channels = eeg_data.ch_names
       sampling_rate = eeg_data.info['sfreq']
   ```

2. **Standardize Channel Names:**
   - Map different channel naming conventions
   - Select 20 standard EEG channels
   - Handle missing channels

3. **Validate Sampling Rates:**
   - Check consistency within sessions
   - Identify need for resampling

**Output:**
- `channels_list_dict`: Standardized channels per session
- `sampling_rate_dict`: Sampling rates per session
- Channel mapping untuk montage calculations

---

## **Section 7: Extract Raw EEG Data**

**Tujuan:** Load dan concatenate raw EEG data dari multiple recordings per session

**Process:**
1. **Load Multiple EDF Files per Session:**
   ```python
   session_eeg_data = []
   for edf_file in session_files:
       eeg = mne.io.read_raw_edf(edf_file, preload=True)
       session_eeg_data.append(eeg)
   ```

2. **Concatenate Recordings:**
   ```python
   concatenated_eeg = mne.concatenate_raws(session_eeg_data)
   ```

3. **Resample to 256 Hz:**
   ```python
   if eeg.info['sfreq'] != 256:
       eeg.resample(256)
   ```

4. **Save Processed Data:**
   ```python
   np.save(f"{raweeg_path}{session_id}.npy", eeg_array)
   ```

**Output:**
- Raw EEG data tersimpan sebagai `.npy` files
- Uniform sampling rate (256 Hz)
- Continuous data per session

---

## **Section 8: Calculate Montages**

**Tujuan:** Convert raw EEG ke bipolar montage untuk seizure analysis

**Process:**
1. **Define Bipolar Montage:**
   ```python
   # Standard 20-channel bipolar montage
   montage_pairs = [
       ('Fp1', 'F7'), ('F7', 'T3'), ('T3', 'T5'), ('T5', 'O1'),
       ('Fp2', 'F8'), ('F8', 'T4'), ('T4', 'T6'), ('T6', 'O2'),
       # ... total 20 pairs
   ]
   ```

2. **Calculate Differential Signals:**
   ```python
   for pair in montage_pairs:
       bipolar_signal = eeg[pair[0]] - eeg[pair[1]]
       montage_data.append(bipolar_signal)
   ```

3. **Save Montage Data:**
   ```python
   montage_array = np.array(montage_data)  # Shape: (20, time_samples)
   np.save(f"{montage_path}{session_id}.npy", montage_array)
   ```

**Output:**
- Bipolar montage data (20 channels)
- Enhanced seizure-related signal characteristics
- Files saved di `montage/` directory

---

## **Section 9: Analyze Metadata for Benchmarks**

**Tujuan:** Analyze seizure timing untuk determine benchmark eligibility

**Process:**
1. **Calculate Cumulative Times:**
   ```python
   # Convert seizure times ke cumulative time across multiple recordings
   for session in sessions:
       cumulative_start_times = []
       cumulative_end_times = []
       # Calculate based on recording durations
   ```

2. **Identify Patients with Seizures:**
   - List patients yang memiliki seizure sessions
   - List patients yang memiliki non-seizure sessions (untuk interictal data)

3. **Build Session Mapping:**
   ```python
   # Map sessions ke train/validation/test splits
   train_sessions = [sessions from train/ directory]
   valid_sessions = [sessions from dev/ directory]
   test_sessions = [sessions from eval/ directory]
   ```

**Output:**
- Seizure timing information
- Patient categorization
- Session splits untuk ML training

---

## **Section 10: Create Interim Dataset**

**Tujuan:** Generate interim dataset files untuk setiap benchmark configuration

**Process:**
1. **Define Benchmark Parameters:**
   ```python
   benchmark_sph_list = [2, 5, 15, 30]    # SPH in minutes
   benchmark_sop_list = [1, 2, 5]         # SOP in minutes
   # Creates 12 benchmarks total (4×3 combinations)
   ```

2. **For Each Benchmark:**
   ```python
   for benchmark in benchmarks:
       gap_time_required = sph + sop

       # Find seizures with sufficient gap time
       valid_seizures = []
       for seizure in seizures:
           if gap_before_seizure >= gap_time_required:
               valid_seizures.append(seizure)
   ```

3. **Extract Preictal & Interictal Segments:**
   ```python
   # For each valid seizure:
   preictal_start = seizure_start - sph_duration
   preictal_end = seizure_start

   # Extract data segments (5-second windows)
   win_len_secs = 5
   segments = extract_windows(preictal_start, preictal_end, win_len_secs)

   # Add matching interictal data from non-seizure sessions
   interictal_segments = extract_interictal_data(non_seizure_sessions)
   ```

4. **Save Interim Files:**
   ```python
   # Format: tuhszr_interm_..._bmrkXX_..._szrXXXX_...train_values.npy
   interim_data = np.concatenate([preictal_segments, interictal_segments])
   np.save(interim_file_path, interim_data)
   ```

**Output:**
- Interim dataset files per seizure per benchmark
- Shape: `(segments, channels, samples_per_segment)`
- Files di `interim/` directory

---

## **Section 11: Create ML-Ready Dataset**

**Tujuan:** Combine interim files menjadi final ML-ready datasets

**Process:**
1. **For Each Benchmark:**
   ```python
   for benchmark_id in benchmark_list:
       # Collect all interim files for this benchmark
       interim_files = find_interim_files(benchmark_id)
   ```

2. **Separate by Dataset Split:**
   ```python
   train_files = [f for f in interim_files if 'train' in f]
   valid_files = [f for f in interim_files if 'valid' in f]
   test_files = [f for f in interim_files if 'tests' in f]
   ```

3. **Combine Data:**
   ```python
   # Load and concatenate all seizures for each split
   train_data = []
   train_labels = []

   for file in train_files:
       seizure_data = np.load(file)
       train_data.append(seizure_data)

       # Create labels: first half=1 (preictal), second half=0 (interictal)
       n_segments = seizure_data.shape[0]
       labels = [1] * (n_segments//2) + [0] * (n_segments//2)
       train_labels.extend(labels)

   final_train_data = np.concatenate(train_data, axis=0)
   ```

4. **Save Final Files:**
   ```python
   # Save feature data as HDF5
   with h5py.File(f'{output_path}_train_values.hdf5', 'w') as f:
       f.create_dataset('tracings', data=final_train_data)

   # Save labels as CSV
   with open(f'{output_path}_train_labels.csv', 'w') as f:
       writer = csv.writer(f)
       for label in train_labels:
           writer.writerow([label])
   ```

**Output:**
- **6 files per benchmark** (total 72 files):
  - `*_train_values.hdf5` & `*_train_labels.csv`
  - `*_valid_values.hdf5` & `*_valid_labels.csv`
  - `*_tests_values.hdf5` & `*_tests_labels.csv`

---

## **Data Flow Summary**

```
TUSZ Raw Data (.edf, .csv_bi)
    ↓ Section 4-5
Metadata Extraction & Seizure Annotations
    ↓ Section 6-7
Raw EEG Data (.npy) + Channel/Rate Info
    ↓ Section 8
Bipolar Montage Data (.npy)
    ↓ Section 9-10
Interim Datasets per Seizure (.npy)
    ↓ Section 11
ML-Ready Datasets (.hdf5 + .csv)
```

## **Final Output Structure**

```
target_path/fld_sng/
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._train_values.hdf5
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._train_labels.csv
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._valid_values.hdf5
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._valid_labels.csv
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._tests_values.hdf5
├── tuhszr_sngfld_..._bmrk01_sph02m_sop01m_..._tests_labels.csv
├── ... (similar for bmrk02 through bmrk12)
```

## **Key Features**

- **12 Benchmarks**: Different SPH/SOP combinations
- **Balanced Dataset**: 50% preictal, 50% interictal
- **Patient-Independent**: Train/validation/test splits by different patients
- **Standardized**: 256 Hz sampling, 20-channel bipolar montage, 5-second windows
- **ML-Ready**: HDF5 features + CSV labels, ready for deep learning frameworks

Pipeline ini menghasilkan comprehensive benchmark dataset untuk epileptic seizure prediction research! 🧠⚡
