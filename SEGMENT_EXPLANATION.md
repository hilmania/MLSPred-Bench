# Segment dalam Data HDF5 MLSPred-Bench

## 🎯 **Definisi Segment:**

**Segment = Window temporal EEG dengan durasi tetap (5 detik)**

Setiap segment berisi EEG data dari 20 channels selama 5 detik pada sampling rate 256 Hz.

---

## **📊 Struktur Segment Detail**

### **Dimensi Segment:**
```python
# Single segment dimensions:
channels = 20          # EEG electrode channels
duration = 5           # seconds
sampling_rate = 256    # Hz
samples_per_segment = duration * sampling_rate = 1280

# Shape per segment:
segment_shape = (20, 1280)  # [channels, time_samples]
```

### **Array Structure dalam HDF5:**
```python
# 3D array dalam file HDF5:
data_shape = (total_segments, 20, 1280)
#             ↑             ↑   ↑
#             segments      ch  samples

# Example untuk BM01:
BM01_shape = (48, 20, 1280)  # 48 segments per seizure
#             ↑
#             24 preictal + 24 interictal segments
```

---

## **⏰ Temporal Meaning of Segments**

### **Segment = Time Window:**
```
Continuous EEG Recording:
────────────────────────────────────────────────────────
│ Seg1 │ Seg2 │ Seg3 │ Seg4 │ ... │ SegN │
│ 5sec │ 5sec │ 5sec │ 5sec │     │ 5sec │
└──────┴──────┴──────┴──────┴─────┴──────┘
  0-5s   5-10s  10-15s 15-20s       N*5s

# Each segment = 5-second slice of continuous EEG
```

### **Seizure Timeline Segmentation:**
```
SPH=30 min before seizure:
─────────────────────────────────────────────────────
│Seg1│Seg2│...│Seg360│SOP GAP│SEIZURE│
│ 5s │ 5s │   │ 5s   │  5min │       │
└────┴────┴───┴──────┴───────┴───────┘
-35min              -5min     0

# 30 minutes ÷ 5 seconds = 360 segments (preictal)
# Plus 360 interictal segments = 720 total per seizure
```

---

## **🔍 Segment Content Analysis**

### **What's Inside Each Segment:**
```python
# Single segment data:
segment_data = {
    "shape": (20, 1280),
    "content": "5 seconds of raw EEG",
    "channels": [
        "Fp1-F7", "F7-T3", "T3-T5", "T5-O1",  # Left temporal chain
        "Fp2-F8", "F8-T4", "T4-T6", "T6-O2",  # Right temporal chain
        "Fp1-F3", "F3-C3", "C3-P3", "P3-O1",  # Left parasagittal
        "Fp2-F4", "F4-C4", "C4-P4", "P4-O2",  # Right parasagittal
        "Fz-Cz", "Cz-Pz", "T3-C3", "C3-Cz",   # Central montage
        "Cz-C4", "C4-T4"                       # Additional central
    ],
    "units": "microvolts (µV)",
    "preprocessing": "filtered, artifact-reduced"
}
```

### **Temporal Resolution:**
```python
# Time resolution per segment:
sampling_interval = 1/256  # ≈ 3.9 milliseconds
time_points = [0, 3.9ms, 7.8ms, ..., 4996.1ms]  # 1280 points
total_duration = 5.0  # seconds exactly

# Each segment captures:
brain_activity_snapshot = "5-second continuous neural activity"
```

---

## **📋 Segment Organization per Benchmark**

### **BM01 Example (SPH=2min, SOP=1min):**
```python
# Per seizure organization:
total_segments_per_seizure = 48
preictal_segments = 24  # First 24 segments
interictal_segments = 24  # Last 24 segments

# Segment timeline:
preictal_timeline = {
    "segment_1": "minutes -3:00 to -2:55 before seizure",
    "segment_2": "minutes -2:55 to -2:50 before seizure",
    "...": "...",
    "segment_24": "minutes -1:05 to -1:00 before seizure"
}

interictal_timeline = {
    "segment_25": "from different non-seizure recording",
    "segment_26": "from different non-seizure recording",
    "...": "...",
    "segment_48": "from different non-seizure recording"
}
```

### **BM12 Example (SPH=30min, SOP=5min):**
```python
# Per seizure organization:
total_segments_per_seizure = 720
preictal_segments = 360  # First 360 segments
interictal_segments = 360  # Last 360 segments

# Segment timeline:
preictal_timeline = {
    "segment_1": "minutes -35:00 to -34:55 before seizure",
    "segment_2": "minutes -34:55 to -34:50 before seizure",
    "...": "...",
    "segment_360": "minutes -5:05 to -5:00 before seizure"
}
```

---

## **🎯 Segment vs Label Mapping**

### **Direct 1:1 Correspondence:**
```python
# HDF5 file structure:
hdf5_data = np.array(shape=(total_segments, 20, 1280))

# CSV label structure:
csv_labels = np.array(shape=(total_segments,))

# Mapping:
for i in range(total_segments):
    segment_i = hdf5_data[i, :, :]  # Shape: (20, 1280)
    label_i = csv_labels[i]         # Shape: scalar (0 or 1)

    # Interpretation:
    if label_i == 1:
        meaning = "segment_i contains preictal EEG pattern"
    else:
        meaning = "segment_i contains interictal EEG pattern"
```

### **Row Index Correspondence:**
```python
# File access pattern:
hdf5_row_10 = hdf5_data[10, :, :]    # 11th segment (0-indexed)
csv_row_10 = csv_labels[10]          # 11th label

# They correspond to the same 5-second EEG window!
```

---

## **🔬 Clinical Interpretation of Segments**

### **Preictal Segments (Label=1):**
```python
preictal_segment_characteristics = {
    "temporal_location": "SPH minutes before seizure onset",
    "expected_patterns": [
        "Subtle frequency changes",
        "Increased synchronization",
        "Amplitude variations",
        "Connectivity pattern shifts"
    ],
    "clinical_meaning": "Brain transitioning toward seizure state",
    "detection_goal": "Identify these patterns for early warning"
}
```

### **Interictal Segments (Label=0):**
```python
interictal_segment_characteristics = {
    "temporal_location": "During non-seizure recordings",
    "expected_patterns": [
        "Normal background activity",
        "Alpha/beta/theta rhythms",
        "No seizure-related changes",
        "Baseline neural activity"
    ],
    "clinical_meaning": "Normal brain function",
    "detection_goal": "Distinguish from preictal patterns"
}
```

---

## **⚡ Processing Pipeline**

### **From Continuous EEG to Segments:**
```python
# Step 1: Continuous EEG recording
raw_eeg = "Hours of continuous 20-channel recording"

# Step 2: Seizure annotation
seizure_times = "Medical expert marked seizure onsets"

# Step 3: SPH/SOP calculation
preictal_periods = "SPH minutes before each seizure"
excluded_periods = "SOP minutes immediately before seizure"

# Step 4: Segmentation
for each_preictal_period:
    segments = split_into_5_second_windows(preictal_period)
    save_as_hdf5_rows(segments)

# Step 5: Labeling
labels = assign_preictal_interictal_labels(segments)
save_as_csv(labels)
```

---

## **💡 Key Insights**

### **Why 5-Second Segments?**
```python
segment_duration_rationale = {
    "computational_efficiency": "Manageable data size for ML",
    "temporal_resolution": "Captures short-term EEG dynamics",
    "clinical_relevance": "Sufficient for pattern detection",
    "literature_standard": "Common window size in seizure research",
    "real_time_feasibility": "Practical for online prediction"
}
```

### **Segment Independence Assumption:**
```python
# MLSPred-Bench treats segments as:
independence_assumption = {
    "each_segment": "independent sample",
    "temporal_context": "not explicitly modeled",
    "pros": "Simple ML model training",
    "cons": "Loses temporal dependencies",
    "future_work": "Sequential models (RNN/LSTM) could use temporal info"
}
```

---

## **🎯 Summary**

**Segment = 5-second window dari continuous EEG recording**

```python
segment_definition = {
    "duration": "5 seconds",
    "channels": "20 EEG electrodes",
    "samples": "1280 time points",
    "shape": "(20, 1280)",
    "meaning": "Snapshot of brain electrical activity",
    "purpose": "Unit of analysis for seizure prediction"
}

# In MLSPred-Bench context:
segment_role = {
    "input": "Feature vector for ML model",
    "output": "Binary prediction (preictal vs interictal)",
    "clinical_goal": "Early seizure warning system"
}
```

**Jadi setiap row dalam HDF5 file = satu segment = 5 detik aktivitas otak dari 20 channel EEG!** 🧠⚡📊
