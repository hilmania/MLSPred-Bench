# SPH vs SOP: Mapping ke Data Preictal dan Interictal

## 🎯 **Jawaban Langsung:**

**SPH = Preictal Duration**
**SOP = Gap Period (Buffer Zone)**

---

## **⏰ Timeline Visual Explanation**

```
Seizure Timeline:
────────────────────────────────────────────────────────────────────────
Normal EEG     │  PREICTAL   │ SOP GAP │ ICTAL │ Postictal │ Normal EEG
               │   (SPH)     │  (SOP)  │       │           │
               │             │         │       │           │
               ├─────────────┼─────────┼───────┼───────────┤
               │             │         │       │           │
        Seizure Onset - (SPH + SOP)    │    Seizure      Next
              ↑             ↑         ↑     Onset       Seizure
         Preictal Start  Preictal   SOP    │
                         End       Start   │
                                          ↓
                                   DATA EXCLUDED
```

### **Contoh dengan SPH=30 menit, SOP=2 menit:**
```
Timeline (menit sebelum seizure):
[-32] ──── [-2] ── [0] ────────────────────
  ↑         ↑      ↑
  │         │      Seizure Onset
  │         SOP Gap Start (no data)
  Preictal Start (30 menit data)
```

---

## **📊 Kode Implementation Analysis**

### **1. Parameter Definition:**
```python
# Dari kode mlspred_bench_v001.py line 1003-1004:
benchmark_sph_list = [2, 5, 15, 30]   # SPH values (minutes)
benchmark_sop_list = [1, 2, 5]        # SOP values (minutes)

# Line 1115-1116:
sph_len_mins = benchmark_tot_list[i][0]  # SPH duration
sop_len_mins = benchmark_tot_list[i][1]  # SOP duration
gap_len_mins = sph_len_mins + sop_len_mins  # Total gap required
```

### **2. Data Extraction Logic:**
```python
# Line 1143-1144: Calculate preictal start time
pres_cum_strt_temp_sph_mins = x_list[j]-(gap_len_mins*60)
# x_list[j] = seizure onset time
# gap_len_mins*60 = (SPH + SOP) in seconds

# Jadi: preictal_start = seizure_onset - (SPH + SOP)
```

### **3. Window Generation:**
```python
# Line 1203: Number of preictal segments
num_of_pre_segs = sph_len_mins*60//win_len_secs
# SPH menentukan berapa banyak preictal windows

# Line 1204: Total segments (preictal + interictal)
num_of_tot_segs = 2*num_of_pre_segs
# Balanced: sama banyak preictal dan interictal
```

---

## **🔍 Data Extraction Detail**

### **Preictal Data:**
```python
# Line 1229-1234: Extract preictal segments
for k in range(num_of_pre_segs, num_of_tot_segs):
    start_ind = pres_cum_strt_samp_sph_mins_dict[benchmark_id][j] + (k-num_of_pre_segs)*win_seg_samps
    end_index = start_ind + win_seg_samps
    temp_array_3D[k,:,:] = temp_array_read[:,start_ind:end_index]

# Explanation:
# - Starts from: seizure_onset - (SPH + SOP)
# - Duration: SPH minutes
# - Windows: SPH*60/window_length segments
```

### **Interictal Data:**
```python
# Line 1223-1227: Extract interictal segments
for k in range(0,end_sequence):
    start_ind = k*win_seg_samps
    end_index = start_ind+win_seg_samps
    temp_array_3D[k,:,:] = temp_mnt[:,start_ind:end_index]

# Explanation:
# - From: non-seizure sessions (completely different recordings)
# - Duration: same as preictal (SPH minutes worth)
# - Windows: same number as preictal
```

---

## **📋 Benchmark Examples**

### **BM01: SPH=2, SOP=1**
```
Timeline:
[-3 min] ──── [-1 min] ── [0 seizure]
   ↑             ↑           ↑
   │             │           Seizure onset
   │             SOP gap (1 min excluded)
   Preictal start (2 min data extracted)

Data:
- Preictal: 2 minutes sebelum SOP gap
- Interictal: 2 minutes dari non-seizure session
- Windows: 2*60/5 = 24 segments each (5-second windows)
- Total: 48 segments per seizure
```

### **BM12: SPH=30, SOP=5**
```
Timeline:
[-35 min] ──── [-5 min] ── [0 seizure]
   ↑             ↑           ↑
   │             │           Seizure onset
   │             SOP gap (5 min excluded)
   Preictal start (30 min data extracted)

Data:
- Preictal: 30 minutes sebelum SOP gap
- Interictal: 30 minutes dari non-seizure session
- Windows: 30*60/5 = 360 segments each
- Total: 720 segments per seizure
```

---

## **⚖️ SPH vs SOP Roles**

### **SPH (Seizure Prediction Horizon):**
```
✅ Defines preictal duration
✅ Determines how much preictal data to extract
✅ Sets prediction timeframe ("predict X minutes ahead")
✅ Controls number of windows per seizure
✅ Main parameter for benchmark difficulty
```

### **SOP (Seizure Occurrence Period):**
```
⚠️ Creates buffer zone before seizure
⚠️ Excludes transition period (unreliable data)
⚠️ Prevents contamination from ictal patterns
⚠️ Standard practice in prediction research
⚠️ Quality control mechanism
```

---

## **💡 Key Insights**

### **1. Data Mapping:**
```
SPH = Amount of preictal data extracted
SOP = Amount of data excluded before seizure

Combined: SPH + SOP = minimum gap required between seizures
```

### **2. Clinical Interpretation:**
```python
# If SPH = 30 minutes, SOP = 5 minutes:
clinical_question = "Can we predict seizure 30 minutes in advance?"
safety_margin = "Stop data collection 5 minutes before seizure"
prediction_utility = "30-minute warning for patient preparation"
```

### **3. Research Design:**
```python
# Different benchmarks test different prediction horizons:
short_term_prediction = "SPH = 2-5 minutes"   # Immediate warning
medium_term_prediction = "SPH = 15 minutes"   # Moderate preparation
long_term_prediction = "SPH = 30 minutes"     # Full preparation time

# SOP ensures data quality across all timeframes
```

---

## **🎯 Summary Table**

| Benchmark | SPH (min) | SOP (min) | Preictal Duration | Gap Before Seizure |
|-----------|-----------|-----------|-------------------|-------------------|
| BM01      | 2         | 1         | 2 minutes         | 3 minutes total   |
| BM02      | 2         | 2         | 2 minutes         | 4 minutes total   |
| BM03      | 2         | 5         | 2 minutes         | 7 minutes total   |
| BM04      | 5         | 1         | 5 minutes         | 6 minutes total   |
| BM05      | 5         | 2         | 5 minutes         | 7 minutes total   |
| BM06      | 5         | 5         | 5 minutes         | 10 minutes total  |
| BM07      | 15        | 1         | 15 minutes        | 16 minutes total  |
| BM08      | 15        | 2         | 15 minutes        | 17 minutes total  |
| BM09      | 15        | 5         | 15 minutes        | 20 minutes total  |
| BM10      | 30        | 1         | 30 minutes        | 31 minutes total  |
| BM11      | 30        | 2         | 30 minutes        | 32 minutes total  |
| BM12      | 30        | 5         | 30 minutes        | 35 minutes total  |

**Interictal data untuk semua benchmark diambil dari non-seizure sessions dengan durasi yang sama dengan SPH!** 🧠⚡
