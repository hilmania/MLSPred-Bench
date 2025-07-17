# Cara Menggunakan Data MLSPred-Bench: Handling Label Patterns

## 🤔 **Pertanyaan Kunci**

"Jika di awal baris sudah ada label preictal terlebih dulu, bukan fase interictal atau normal, bagaimana cara menggunakan datanya?"

---

## **📊 Struktur Data MLSPred-Bench**

### **Pattern Label dalam Dataset:**
```
Row 0-23:    1,1,1,...,1    (Seizure 1 - Preictal)
Row 24-47:   0,0,0,...,0    (Seizure 1 - Interictal)
Row 48-71:   1,1,1,...,1    (Seizure 2 - Preictal)
Row 72-95:   0,0,0,...,0    (Seizure 2 - Interictal)
Row 96-119:  1,1,1,...,1    (Seizure 3 - Preictal)
Row 120-143: 0,0,0,...,0    (Seizure 3 - Interictal)
```

**Ya, memang di awal baris ada label preictal dulu!** Ini adalah **by design**.

---

## **🎯 Interpretasi yang Benar**

### **BUKAN Timeline Kronologis:**
❌ **Salah:** Data disusun berdasarkan urutan waktu real
❌ **Salah:** Row 0 = waktu paling awal, Row N = waktu terakhir

### **✅ Data Structure by Seizure:**
✅ **Benar:** Data diorganisir per seizure event
✅ **Benar:** Setiap seizure berkontribusi 2 tipe data: preictal + interictal
✅ **Benar:** Urutan row mengikuti struktur data, bukan timeline

---

## **🧠 Cara Penggunaan yang Benar**

### **1. Machine Learning Training:**

```python
import h5py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
with h5py.File('bmrk01_train_values.hdf5', 'r') as f:
    X = f['tracings'][:]  # Features

y = pd.read_csv('bmrk01_train_labels.csv', header=None)[0].values  # Labels

# Machine Learning approach - treat each row independently
# NO assumption about temporal order between rows
model = RandomForestClassifier()
model.fit(X.reshape(X.shape[0], -1), y)  # Flatten features

# Prediction on new data
predictions = model.predict(new_data)
```

### **2. Deep Learning Approach:**

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class EEGDataset(Dataset):
    def __init__(self, hdf5_file, csv_file):
        with h5py.File(hdf5_file, 'r') as f:
            self.data = f['tracings'][:]
        self.labels = pd.read_csv(csv_file, header=None)[0].values

    def __getitem__(self, idx):
        # Each sample is independent
        # No temporal relationship assumed between consecutive indices
        return torch.tensor(self.data[idx]), torch.tensor(self.labels[idx])

    def __len__(self):
        return len(self.data)

# Usage
dataset = EEGDataset('bmrk01_train_values.hdf5', 'bmrk01_train_labels.csv')
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)  # Shuffle is OK!

# Train model
for batch_data, batch_labels in dataloader:
    # Each sample is treated independently
    # Model learns: "Given this 5-second EEG, is it preictal or interictal?"
    pass
```

---

## **⚠️ Key Understanding**

### **1. Independent Samples:**
```python
# Each row is an INDEPENDENT sample
# Question per sample: "Is this 5-second EEG segment preictal or interictal?"

row_0_data:  5-second EEG → model → prediction: preictal (1)
row_1_data:  5-second EEG → model → prediction: preictal (1)
row_24_data: 5-second EEG → model → prediction: interictal (0)
```

### **2. No Sequential Assumption:**
```python
# WRONG approach:
# Assuming row_0 happens before row_1 in real-time

# CORRECT approach:
# Each row is independent sample from different temporal contexts
```

### **3. Training Paradigm:**
```
Goal: Learn to distinguish preictal vs interictal patterns
Method: Show model many examples of both types
Result: Model learns EEG patterns, not temporal sequences
```

---

## **🔬 Research Usage Patterns**

### **1. Standard Supervised Learning:**
```python
# Most common approach
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# Shuffle is ENCOURAGED - no temporal dependency assumed
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
```

### **2. Cross-Validation:**
```python
from sklearn.model_selection import StratifiedKFold

# Standard CV - treats samples independently
cv = StratifiedKFold(n_splits=5, shuffle=True)
scores = cross_val_score(model, X, y, cv=cv)
```

### **3. Patient-Independent Evaluation:**
```python
# Use different splits for robust evaluation
train_data = load_data('bmrk01_train_values.hdf5', 'bmrk01_train_labels.csv')
valid_data = load_data('bmrk01_valid_values.hdf5', 'bmrk01_valid_labels.csv')
test_data = load_data('bmrk01_tests_values.hdf5', 'bmrk01_tests_labels.csv')

# Train on training patients, test on different patients
model.fit(train_data)
performance = model.evaluate(test_data)
```

---

## **🎯 Practical Application**

### **Real-World Deployment:**
```python
# In real-time seizure prediction system:

def predict_seizure_risk(eeg_segment_5sec):
    """
    Input: Single 5-second EEG segment
    Output: Probability of being in preictal state
    """
    features = preprocess(eeg_segment_5sec)  # Same preprocessing as training
    probability = model.predict_proba(features)[0][1]  # P(preictal)

    if probability > threshold:
        return "HIGH SEIZURE RISK - Alert patient"
    else:
        return "Normal brain activity"

# Usage in real-time:
while monitoring_patient:
    current_5sec_eeg = get_latest_eeg()
    risk_assessment = predict_seizure_risk(current_5sec_eeg)
    display_alert(risk_assessment)
```

---

## **📈 Performance Metrics**

### **Evaluation Approach:**
```python
from sklearn.metrics import classification_report, confusion_matrix

# Standard binary classification metrics
predictions = model.predict(X_test)

print(classification_report(y_test, predictions,
                          target_names=['Interictal', 'Preictal']))

# Confusion Matrix
# [[TN, FP],
#  [FN, TP]]
```

### **Clinical Metrics:**
```python
# Seizure prediction specific metrics
sensitivity = TP / (TP + FN)  # True positive rate
specificity = TN / (TN + FP)  # True negative rate
false_alarm_rate = FP / (FP + TN)  # Critical for clinical use
```

---

## **🚨 Common Mistakes to Avoid**

### **❌ Wrong Assumptions:**
```python
# DON'T do this:
# Assuming temporal order within batch
for i in range(len(data)-1):
    if labels[i] == 1 and labels[i+1] == 0:
        print("Transition from preictal to interictal")  # WRONG!

# DON'T do this:
# Using time-series models expecting sequential data
lstm_model.fit(X.reshape(1, len(X), features))  # WRONG approach!
```

### **✅ Correct Approach:**
```python
# DO this:
# Treat each sample independently
for sample, label in zip(data, labels):
    prediction = model.predict(sample)
    evaluate_single_prediction(prediction, label)

# DO this:
# Use appropriate models for independent samples
random_forest.fit(X, y)  # Good
svm.fit(X, y)           # Good
cnn.fit(X, y)           # Good for spatial patterns
```

---

## **💡 Key Takeaway**

**MLSPred-Bench data structure dimulai dengan preictal labels bukan karena error, tapi karena:**

1. **Design choice** untuk organize data by seizure
2. **Each row = independent sample**, bukan sequential timeline
3. **Model learns patterns**, bukan temporal sequences
4. **Evaluation focuses on pattern recognition**, bukan time-series prediction

**Gunakan data sebagai independent samples untuk supervised learning, jangan interpret sebagai temporal sequence!** 🧠⚡📊
