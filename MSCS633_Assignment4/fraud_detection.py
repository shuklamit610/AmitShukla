
"""
Credit Card Fraud Detection using PyOD AutoEncoder

Purpose:
Detect fraudulent credit card transactions using an
unsupervised deep-learning anomaly detection model.

Dataset: creditcard.csv
Model: PyOD AutoEncoder
"""

import os
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

from pyod.models.auto_encoder import AutoEncoder

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

RANDOM_STATE = 42
DATASET_PATH = "data/raw/creditcard.csv"

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

MAX_TRAIN_SAMPLES = 30000

# Reproducibility
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)
torch.manual_seed(RANDOM_STATE)

# Limit CPU threads for the Intel Mac
torch.set_num_threads(2)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("\n" + "=" * 60)
print("CREDIT CARD FRAUD DETECTION USING AUTOENCODER")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)

# Separate input features and target
X = df.drop(columns=["Class"])
y = df["Class"].astype(int)

print("\nTransaction distribution:")
print(y.value_counts())


# --------------------------------------------------
# 3. Split dataset into training, validation and test
# --------------------------------------------------

print("\nSplitting dataset...")

# First split: 60% training and 40% temporary data
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.40,
    stratify=y,
    random_state=RANDOM_STATE
)

# Second split: 20% validation and 20% testing
X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=RANDOM_STATE
)

print("Training records:", len(X_train))
print("Validation records:", len(X_val))
print("Testing records:", len(X_test))


# --------------------------------------------------
# 4. Prepare legitimate training transactions
# --------------------------------------------------

print("\nPreparing legitimate transactions...")

# The AutoEncoder learns only from legitimate transactions
X_train_normal = X_train.loc[y_train == 0]

print("Legitimate training records:", len(X_train_normal))

# Limit training size for CPU performance
if len(X_train_normal) > MAX_TRAIN_SAMPLES:
    X_train_normal = X_train_normal.sample(
        n=MAX_TRAIN_SAMPLES,
        random_state=RANDOM_STATE
    )

print("Records selected for model training:", len(X_train_normal))


# --------------------------------------------------
# 5. Feature scaling
# --------------------------------------------------

print("\nScaling input features...")

# Fit scaler using legitimate training data only
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_normal)

# Transform validation and test data using the same scaler
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("Feature scaling completed.")


# --------------------------------------------------
# 6. Build and train AutoEncoder
# --------------------------------------------------

print("\nInitializing PyOD AutoEncoder...")

model = AutoEncoder(
    contamination=0.01,
    preprocessing=False,
    lr=0.001,
    epoch_num=10,
    batch_size=512,
    hidden_neuron_list=[32, 16, 16, 32],
    dropout_rate=0.1,
    verbose=1,
    random_state=RANDOM_STATE
)

print("\nTraining AutoEncoder...")
print("Training uses legitimate transactions only.")

model.fit(X_train_scaled)

print("\nAutoEncoder training completed!")


# --------------------------------------------------
# 7. Calculate reconstruction anomaly scores
# --------------------------------------------------

print("\nCalculating anomaly scores...")

# Higher scores indicate more anomalous transactions
val_scores = model.decision_function(X_val_scaled)
test_scores = model.decision_function(X_test_scaled)


# --------------------------------------------------
# 8. Select threshold using validation data
# --------------------------------------------------

print("\nSelecting fraud detection threshold...")

precision_values, recall_values, thresholds = (
    precision_recall_curve(y_val, val_scores)
)

# Calculate F1 score for each available threshold
f1_values = (
    2 * precision_values[:-1] * recall_values[:-1]
    / (precision_values[:-1] + recall_values[:-1] + 1e-10)
)

best_index = np.argmax(f1_values)
best_threshold = thresholds[best_index]

print("Selected threshold:", best_threshold)
print("Validation precision:", precision_values[best_index])
print("Validation recall:", recall_values[best_index])
print("Validation F1-score:", f1_values[best_index])


# --------------------------------------------------
# 9. Evaluate model on unseen test data
# --------------------------------------------------

print("\nEvaluating model on test data...")

# Higher anomaly scores are classified as fraud
y_pred = (test_scores >= best_threshold).astype(int)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

roc_auc = roc_auc_score(y_test, test_scores)
avg_precision = average_precision_score(y_test, test_scores)

cm = confusion_matrix(y_test, y_pred)

print("\n" + "=" * 60)
print("FINAL MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy:          {accuracy:.4f}")
print(f"Precision:         {precision:.4f}")
print(f"Recall:            {recall:.4f}")
print(f"F1-score:          {f1:.4f}")
print(f"ROC-AUC:           {roc_auc:.4f}")
print(f"Average Precision: {avg_precision:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Fraud"],
        zero_division=0
    )
)


# --------------------------------------------------
# 10. Save evaluation metrics
# --------------------------------------------------

metrics = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score",
        "ROC-AUC",
        "Average Precision",
        "Selected Threshold"
    ],
    "Value": [
        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        avg_precision,
        best_threshold
    ]
})

metrics.to_csv(
    RESULTS_DIR / "evaluation_metrics.csv",
    index=False
)

print("\nEvaluation metrics saved.")


# --------------------------------------------------
# 11. Generate confusion matrix visualization
# --------------------------------------------------

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Legitimate", "Fraud"]
)

disp.plot(values_format="d")
plt.title("Credit Card Fraud Detection - Confusion Matrix")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "confusion_matrix.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 12. Generate reconstruction error visualization
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    test_scores[y_test.to_numpy() == 0],
    bins=50,
    alpha=0.6,
    label="Legitimate Transactions"
)

plt.hist(
    test_scores[y_test.to_numpy() == 1],
    bins=50,
    alpha=0.6,
    label="Fraudulent Transactions"
)

plt.axvline(
    best_threshold,
    linestyle="--",
    label="Selected Threshold"
)

plt.xlabel("AutoEncoder Anomaly Score")
plt.ylabel("Number of Transactions")
plt.title("Anomaly Score Distribution")
plt.legend()

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "anomaly_score_distribution.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 13. Save test predictions
# --------------------------------------------------

predictions = pd.DataFrame({
    "Actual_Class": y_test.to_numpy(),
    "Anomaly_Score": test_scores,
    "Predicted_Class": y_pred
})

predictions.to_csv(
    RESULTS_DIR / "test_predictions.csv",
    index=False
)

print("\nTest predictions saved.")

print("\nGenerated files:")
print("- results/evaluation_metrics.csv")
print("- results/confusion_matrix.png")
print("- results/anomaly_score_distribution.png")
print("- results/test_predictions.csv")

print("\n" + "=" * 60)
print("FRAUD DETECTION EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 60)
