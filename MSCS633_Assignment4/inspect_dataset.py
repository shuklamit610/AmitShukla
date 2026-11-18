
"""
Credit Card Fraud Detection
Dataset inspection program

Author: MSCS Student
Purpose: Inspect transaction data before model training.
"""

import pandas as pd

# Dataset location
DATASET_PATH = "data/raw/creditcard.csv"

# Load the dataset
df = pd.read_csv(DATASET_PATH)

# Display dataset information
print("=" * 55)
print("CREDIT CARD FRAUD DETECTION - DATASET INSPECTION")
print("=" * 55)

print("\nDataset Shape:", df.shape)

# Display class distribution
print("\nTransaction Class Distribution:")
print(df["Class"].value_counts().sort_index())

# Calculate fraud percentage
fraud_percentage = df["Class"].mean() * 100

print(f"\nFraud Percentage: {fraud_percentage:.4f}%")

# Check missing values
print("\nTotal Missing Values:", df.isnull().sum().sum())

# Display feature columns
print("\nAvailable Columns:")
print(df.columns.tolist())

# Display descriptive statistics
print("\nTransaction Amount Statistics:")
print(df["Amount"].describe())

print("\nDataset inspection completed successfully.")
