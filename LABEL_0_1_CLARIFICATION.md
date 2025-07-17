# Label 0 vs 1: Klarifikasi Interictal vs Preictal

## 🎯 **Jawaban Langsung:**

**Label 0 (Interictal) = Kondisi NORMAL/BASELINE**
**Label 1 (Preictal) = Menuju seizure (kemungkinan ictal akan terjadi)**

**BUKAN sebaliknya!**

---

## **🧠 Definisi Medis yang Benar**

### **Interictal (Label 0):**
```
✅ Kondisi EEG normal/baseline
✅ Tidak ada tanda-tanda seizure akan terjadi
✅ Brain activity dalam keadaan stabil
✅ Pasien dalam kondisi normal day-to-day
✅ Jauh dari waktu seizure (hours to days)
```

### **Preictal (Label 1):**
```
⚠️ Brain mulai menunjukkan perubahan menuju seizure
⚠️ Subtle patterns yang mengindikasikan seizure approach
⚠️ Transition state dari normal ke seizure
⚠️ Terjadi SPH minutes sebelum seizure onset
⚠️ Kondisi "high risk" seizure akan terjadi
```

---

## **📊 Timeline dengan Labels**

```
EEG States Timeline:
──────────────────────────────────────────────────────────────────────

Normal EEG  │  PREICTAL   │ SOP GAP │ ICTAL │ Postictal │ Normal EEG
(hours)     │   (SPH)     │  (SOP)  │       │           │ (hours)
            │             │         │       │           │
LABEL: 0    │   LABEL: 1  │  X      │   X   │     X     │  LABEL: 0
(interictal)│  (preictal) │(excluded)│(excluded)│(excluded)│(interictal)
            │             │         │       │           │
Low Risk    │  High Risk  │         │Seizure│ Recovery  │ Low Risk
Seizure     │  Seizure    │         │Happening│          │ Seizure
```

---

## **🔍 Data Source Analysis**

### **Label 0 (Interictal) Data Sources:**
```python
# Dari kode MLSPred-Bench:
# Line 1223-1227: Extract interictal segments
temp_nsz = pats_with_seizures_nonseiz_session_ids_dict[temp_key]
temp_npy = mont_path+temp_nsz[0]+'.npy'
temp_mnt = np.load(temp_npy)

# Explanation:
# - Diambil dari "nonseiz_session" = NON-SEIZURE sessions
# - Recordings ketika pasien TIDAK mengalami seizure
# - EEG dalam kondisi normal/baseline
# - Bisa dari hari/waktu yang completely different
```

### **Label 1 (Preictal) Data Sources:**
```python
# Line 1229-1234: Extract preictal segments
start_ind = pres_cum_strt_samp_sph_mins_dict[benchmark_id][j] + (k-num_of_pre_segs)*win_seg_samps
temp_array_3D[k,:,:] = temp_array_read[:,start_ind:end_index]

# Explanation:
# - Diambil dari SPH minutes sebelum seizure onset
# - Dari recording yang SAMA dengan seizure session
# - EEG menunjukkan subtle changes menuju seizure
# - Specifically periode "high risk" seizure
```

---

## **💡 Logical Reasoning**

### **Mengapa Label 0 = Normal/Baseline?**
```python
# Clinical Logic:
if brain_state == "normal":
    seizure_risk = "low"
    label = 0  # Interictal
    patient_status = "safe for normal activities"

if brain_state == "approaching_seizure":
    seizure_risk = "high"
    label = 1  # Preictal
    patient_status = "needs precautions"
```

### **Machine Learning Perspective:**
```python
# Prediction Task:
model_input = "5-second EEG window"
model_output = {
    0: "Normal brain state (safe)",
    1: "Pre-seizure state (warning!)"
}

# Clinical Application:
if prediction == 0:
    action = "Continue normal activities"
if prediction == 1:
    action = "Take precautions - seizure likely coming"
```

---

## **📚 Literature Standard**

### **Terminologi Medis:**
```
Interictal Period:
- "Between seizures"
- Normal brain electrical activity
- No seizure-related abnormalities
- Baseline/reference state

Preictal Period:
- "Before seizure"
- Transitional brain state
- Early seizure-related changes
- Warning/prodrome phase
```

### **Research Convention:**
```python
# Standard dalam seizure prediction literature:
baseline_class = {
    "name": "interictal",
    "label": 0,
    "meaning": "normal_state",
    "clinical_action": "no_intervention_needed"
}

warning_class = {
    "name": "preictal",
    "label": 1,
    "meaning": "seizure_approaching",
    "clinical_action": "take_precautions"
}
```

---

## **🎯 Contoh Konkret**

### **Scenario 1: Patient Normal Day**
```
Time: Tuesday 10:00 AM
EEG: Normal background activity
Seizure Risk: Low
Label: 0 (Interictal)
Patient: Can drive, work normally
```

### **Scenario 2: 30 Minutes Before Seizure**
```
Time: Tuesday 2:30 PM
EEG: Subtle frequency changes detected
Seizure Risk: High (seizure at 3:00 PM)
Label: 1 (Preictal)
Patient: Should stop driving, find safe place
```

### **Scenario 3: Next Day After Seizure**
```
Time: Wednesday 9:00 AM
EEG: Back to normal baseline
Seizure Risk: Low
Label: 0 (Interictal)
Patient: Can resume normal activities
```

---

## **⚖️ Why This Makes Sense**

### **From Patient Perspective:**
```
Label 0 (Interictal): "I feel normal, brain is stable"
Label 1 (Preictal): "Something's changing, seizure might come"

# It would be illogical if:
Label 0 meant "seizure coming" → Patient in danger
Label 1 meant "normal state" → No warning system
```

### **From Clinical Utility:**
```python
# Early Warning System Logic:
if model.predict(eeg_window) == 0:
    alert_level = "GREEN - Normal state"
    recommendation = "Continue activities"

if model.predict(eeg_window) == 1:
    alert_level = "RED - Seizure risk detected"
    recommendation = "Take immediate precautions"
```

---

## **🔍 MLSPred-Bench Confirmation**

### **Data Organization:**
```python
# Balanced dataset per seizure:
preictal_segments = SPH_minutes * 60 / window_length  # Label 1
interictal_segments = SPH_minutes * 60 / window_length  # Label 0

# Sources:
preictal_source = "SPH minutes before seizure onset"  # High risk period
interictal_source = "Non-seizure recording sessions"  # Normal/safe period
```

### **File Naming Convention:**
```
# Preictal files (Label 1):
*_train_values.h5 (first half = interictal, second half = preictal)
*_train_labels.csv (0 for first half, 1 for second half)

# The pattern confirms:
# Label 0 = Interictal = Normal state
# Label 1 = Preictal = Warning state
```

---

## **💡 Key Takeaway**

**Label 0 (Interictal) = KONDISI NORMAL**
- Brain dalam keadaan stabil
- Tidak ada indikasi seizure akan terjadi
- Safe untuk aktivitas normal
- Low seizure risk

**Label 1 (Preictal) = SEIZURE AKAN TERJADI**
- Brain menunjukkan perubahan menuju seizure
- High seizure risk dalam SPH minutes
- Butuh tindakan pencegahan
- Warning state

**Jadi pemahaman Anda terbalik - Label 0 itu kondisi normal/safe, bukan yang menuju seizure!** 🧠⚡
