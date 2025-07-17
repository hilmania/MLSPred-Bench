# Mapping Exact: Label CSV ↔ Data HDF5

## 🎯 **One-to-One Correspondence**

**Setiap baris di CSV label** memiliki **exact correspondence** dengan **satu row di HDF5 data**.

---

## **📊 Struktur Data**

### **HDF5 Data Shape:**
```python
# File: bmrk01_train_values.hdf5
# Dataset name: 'tracings'
# Shape: (total_segments, samples_per_segment, channels)
#        (N, 1280, 20)

# Dimana:
# - N = total segments dari semua seizures di training set
# - 1280 = samples per segment (5 seconds × 256 Hz)
# - 20 = channels (bipolar montage)
```

### **CSV Labels Shape:**
```python
# File: bmrk01_train_labels.csv
# Shape: (N, 1) - N rows, 1 column
# Values: 0 atau 1

# Dimana N sama dengan dimensi pertama HDF5
```

---

## **🔗 Exact Mapping**

### **Row-by-Row Correspondence:**

```python
# Contoh untuk benchmark BM01 (SPH=2 min):
s_i = 2 * 60 * 2 // 5 = 48 segments per seizure
si_by_two = 48 // 2 = 24 segments

# Misal ada 3 seizures di training set:
```

### **Seizure 1 (rows 0-47):**
```
HDF5 row 0:  [EEG data segment 1 dari seizure 1] ← CSV row 0:  1 (preictal)
HDF5 row 1:  [EEG data segment 2 dari seizure 1] ← CSV row 1:  1 (preictal)
HDF5 row 2:  [EEG data segment 3 dari seizure 1] ← CSV row 2:  1 (preictal)
...
HDF5 row 23: [EEG data segment 24 dari seizure 1] ← CSV row 23: 1 (preictal)
HDF5 row 24: [EEG data segment 25 dari seizure 1] ← CSV row 24: 0 (interictal)
HDF5 row 25: [EEG data segment 26 dari seizure 1] ← CSV row 25: 0 (interictal)
...
HDF5 row 47: [EEG data segment 48 dari seizure 1] ← CSV row 47: 0 (interictal)
```

### **Seizure 2 (rows 48-95):**
```
HDF5 row 48: [EEG data segment 1 dari seizure 2] ← CSV row 48: 1 (preictal)
HDF5 row 49: [EEG data segment 2 dari seizure 2] ← CSV row 49: 1 (preictal)
...
HDF5 row 71: [EEG data segment 24 dari seizure 2] ← CSV row 71: 1 (preictal)
HDF5 row 72: [EEG data segment 25 dari seizure 2] ← CSV row 72: 0 (interictal)
...
HDF5 row 95: [EEG data segment 48 dari seizure 2] ← CSV row 95: 0 (interictal)
```

### **Seizure 3 (rows 96-143):**
```
HDF5 row 96:  [EEG data segment 1 dari seizure 3] ← CSV row 96:  1 (preictal)
HDF5 row 97:  [EEG data segment 2 dari seizure 3] ← CSV row 97:  1 (preictal)
...
HDF5 row 119: [EEG data segment 24 dari seizure 3] ← CSV row 119: 1 (preictal)
HDF5 row 120: [EEG data segment 25 dari seizure 3] ← CSV row 120: 0 (interictal)
...
HDF5 row 143: [EEG data segment 48 dari seizure 3] ← CSV row 143: 0 (interictal)
```

---

## **🔍 Contoh Konkret: Label = 1 di Baris 10**

### **Pertanyaan:** Label dengan nilai 1 pada baris ke-10, menunjukkan apa di file HDF5?

### **Jawaban:**

**CSV row 10: label = 1**

**Berarti:**
1. **Di HDF5 row 10** berisi **EEG data segment ke-11** (index 10, counting from 0)
2. **Segment ini adalah PREICTAL data** (karena label = 1)
3. **Segment ini berasal dari seizure pertama** (karena row 10 < 24, masih dalam range seizure 1)
4. **Data shape: (1280, 20)** - 1280 samples × 20 channels
5. **Time window: 5 detik EEG data** pada 256 Hz sampling rate
6. **Temporal position: Segment ke-11 dari total 24 preictal segments** dalam seizure 1

### **Detail Segment:**
```python
# Akses data:
import h5py
import pandas as pd

# Load data dan labels
with h5py.File('bmrk01_train_values.hdf5', 'r') as f:
    eeg_data = f['tracings'][:]  # Shape: (N, 1280, 20)

labels = pd.read_csv('bmrk01_train_labels.csv', header=None)[0].values

# Row 10 analysis:
segment_10_data = eeg_data[10]  # Shape: (1280, 20)
segment_10_label = labels[10]   # Value: 1

print(f"Segment 10 label: {segment_10_label}")  # Output: 1
print(f"Segment 10 shape: {segment_10_data.shape}")  # Output: (1280, 20)
print(f"Type: {'Preictal' if segment_10_label == 1 else 'Interictal'}")  # Output: Preictal
```

---

## **⏰ Temporal Information**

### **Label = 1 di baris 10 berarti:**

**Temporal position dalam seizure:**
- Seizure 1 memiliki 24 preictal segments (rows 0-23)
- Row 10 = segment ke-11 dari 24 preictal segments
- Time position: ~55-60 detik sebelum seizure onset
  - (Calculation: (11/24) × 2 minutes = ~55 seconds into preictal period)

### **EEG Content:**
- **5-detik window** EEG data dari patient tertentu
- **20 channels** bipolar montage
- **256 Hz sampling** (1280 samples)
- **Recorded timing:** 55-60 detik sebelum seizure start
- **Clinical significance:** Data dalam seizure prediction horizon (SPH)

---

## **📋 Summary Mapping Rules**

```python
# General mapping formula:
CSV_row_index = HDF5_row_index = segment_index

# Label interpretation:
if label == 1:
    segment_type = "Preictal"
    timing = "Within SPH before seizure"
elif label == 0:
    segment_type = "Interictal"
    timing = "From non-seizure session OR post-SOP period"

# Seizure identification:
seizure_number = row_index // s_i  # s_i = segments per seizure
segment_within_seizure = row_index % s_i

# Preictal vs Interictal within seizure:
if segment_within_seizure < (s_i // 2):
    position = "Preictal portion"
else:
    position = "Interictal portion"
```

**Jadi baris 10 dengan label=1 di CSV secara exact menunjukkan preictal EEG segment ke-11 dari seizure pertama di HDF5 row 10!** 🧠⚡
