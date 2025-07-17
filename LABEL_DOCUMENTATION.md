# Dokumentasi Label CSV MLSPred-Bench

## Struktur Label di File CSV

Berdasarkan analisis kode Section 11, berikut adalah informasi lengkap tentang label yang ada di file CSV yang dihasilkan:

### **Format File CSV**

Setiap benchmark menghasilkan **6 file CSV** untuk labels:
- `*_train_labels.csv` - Label untuk data training
- `*_valid_labels.csv` - Label untuk data validation
- `*_tests_labels.csv` - Label untuk data testing

### **Struktur Label**

#### **1. Label Values (Binary Classification)**
```
0 = Interictal (Normal/Non-seizure)
1 = Preictal (Pre-seizure)
```

#### **2. Label Distribution per Seizure**
Untuk setiap seizure, data dibagi menjadi dua bagian equal:
- **First half**: Preictal data (label = 1)
- **Second half**: Interictal data (label = 0)

### **Perhitungan Label per Benchmark**

#### **Formula Dasar:**
```python
# Sampling parameters
win_len_secs = 5  # Window length in seconds
sph_len_mins = [2, 5, 15, 30]  # SPH per benchmark

# Calculations per seizure
s_i = 2 * 60 * sph_len_mins // win_len_secs  # Total segments per seizure
si_by_two = s_i // 2  # Half of segments (preictal portion)

# Label assignment per seizure:
# Segments 0 to (si_by_two-1): label = 1 (preictal)
# Segments si_by_two to (s_i-1): label = 0 (interictal)
```

#### **Contoh Konkret per Benchmark:**

| Benchmark | SPH (min) | Segments per Seizure | Preictal Labels (1) | Interictal Labels (0) |
|-----------|-----------|---------------------|--------------------|--------------------|
| BM01      | 2         | 48                  | 24                 | 24                 |
| BM02      | 2         | 48                  | 24                 | 24                 |
| BM03      | 2         | 48                  | 24                 | 24                 |
| BM04      | 5         | 120                 | 60                 | 60                 |
| BM05      | 5         | 120                 | 60                 | 60                 |
| BM06      | 5         | 120                 | 60                 | 60                 |
| BM07      | 15        | 360                 | 180                | 180                |
| BM08      | 15        | 360                 | 180                | 180                |
| BM09      | 15        | 360                 | 180                | 180                |
| BM10      | 30        | 720                 | 360                | 360                |
| BM11      | 30        | 720                 | 360                | 360                |
| BM12      | 30        | 720                 | 360                | 360                |

### **Struktur Data dalam CSV**

#### **Format CSV:**
```csv
1
1
1
...
1
0
0
0
...
0
```

Setiap baris dalam CSV berisi **satu label** (0 atau 1) untuk satu segment EEG.

#### **Kode Pembuat Label:**
```python
# Initialize label arrays
temp_labls_train = np.zeros(train_fold_depth)
temp_labls_valid = np.zeros(valid_fold_depth)
temp_labls_tests = np.zeros(tests_fold_depth)

# For each seizure, set first half as preictal (label=1)
for each_seizure:
    start_index = seizure_start_position
    temp_labls_train[start_index:start_index+si_by_two] = 1
    # Second half remains 0 (interictal)

# Write to CSV
with open(csv_file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    A = []
    for x in temp_labls_train.astype(int):
        A.append([x])
    csvwriter.writerows(A)
```

### **Total Label Count per File**

#### **Formula:**
```
Total labels per CSV = Number_of_seizures × Segments_per_seizure
```

#### **Contoh untuk BM01:**
```
- 48 segments per seizure
- If 10 seizures in training set:
  Total labels in train_labels.csv = 10 × 48 = 480 labels
  - 240 labels = 1 (preictal)
  - 240 labels = 0 (interictal)
```

### **Temporal Arrangement**

#### **Label Sequence per Seizure:**
```
Seizure 1: [1,1,1,...,1,0,0,0,...,0]  (24 ones + 24 zeros for BM01)
Seizure 2: [1,1,1,...,1,0,0,0,...,0]  (24 ones + 24 zeros for BM01)
...
Seizure N: [1,1,1,...,1,0,0,0,...,0]  (24 ones + 24 zeros for BM01)
```

#### **Complete Label File Structure:**
```
Row 1-24:     1 (Seizure 1 preictal)
Row 25-48:    0 (Seizure 1 interictal)
Row 49-72:    1 (Seizure 2 preictal)
Row 73-96:    0 (Seizure 2 interictal)
...
```

### **Balanced Dataset Guarantee**

Dataset dijamin **balanced** karena:
- Setiap seizure memberikan equal number preictal dan interictal segments
- Total labels: 50% class 0, 50% class 1
- Formula: `total_preictal_labels = total_interictal_labels = total_labels / 2`

### **File Naming Convention**

```
tuhszr_sngfld_unscld_unfilt_blcrnd_srate256Hz_bmrkXX_sphYYm_sopZZm_seg05s_ovr00s_fold00_tuhstd_[train|valid|tests]_labels.csv
```

Dimana:
- `XX` = benchmark number (01-12)
- `YY` = SPH in minutes
- `ZZ` = SOP in minutes

### **Usage Example**

```python
import pandas as pd

# Load labels
labels = pd.read_csv('train_labels.csv', header=None)
labels = labels[0].values  # Convert to numpy array

# Check balance
preictal_count = np.sum(labels == 1)
interictal_count = np.sum(labels == 0)
print(f"Preictal: {preictal_count}, Interictal: {interictal_count}")
print(f"Balance ratio: {preictal_count/len(labels):.2f}")
```

### **Important Notes**

1. **Binary Classification**: Hanya ada 2 kelas (0 dan 1)
2. **Perfect Balance**: Selalu 50-50 distribution
3. **Temporal Order**: Labels mengikuti urutan temporal data
4. **Consistent Structure**: Semua benchmark menggunakan struktur yang sama
5. **No Header**: CSV files tidak memiliki header, langsung data numerik

Dataset ini siap digunakan untuk binary classification epileptic seizure prediction tasks!
