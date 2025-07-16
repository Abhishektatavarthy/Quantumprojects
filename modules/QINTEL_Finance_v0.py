import sys
import pandas as pd
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

# === STEP 0: Terminal-Based CSV Input ===
if len(sys.argv) < 2:
    print("Usage: python QINTEL_Finance_v0.py <path_to_dataset.csv>")
    sys.exit(1)

dataset_path = sys.argv[1]
try:
    df = pd.read_csv(dataset_path)
except FileNotFoundError:
    print(f"❌ File not found: {dataset_path}")
    sys.exit(1)

# === STEP 1: Dataset Frequency Input ===
print("QINTEL Finance – Live Dataset Analyzer")
frequency = input("Enter the dataset frequency (daily/weekly/monthly): ").strip().lower()
valid_frequencies = ['daily', 'weekly', 'monthly']
if frequency not in valid_frequencies:
    print("Invalid input. Defaulting to 'daily'.")
    frequency = 'daily'
filename_prefix = f"{frequency}_qintel_output"

# === STEP 2: Factor Selection ===
print("\nAvailable Columns:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

factor_indices = input("Enter indices of columns to use as factors (comma-separated): ")
selected_indices = [int(i.strip()) - 1 for i in factor_indices.split(",") if i.strip().isdigit()]
factor_list = [df.columns[i] for i in selected_indices]

# === STEP 3: Detect Types and Ask for Conditions ===
condition_map = {}
for factor in factor_list:
    sample = df[factor].iloc[0]
    if isinstance(sample, bool):
        dtype = 'boolean'
    elif isinstance(sample, int):
        dtype = 'int'
    elif isinstance(sample, float):
        dtype = 'float'
    else:
        dtype = 'string'

    print(f"\nColumn: '{factor}' (Detected type: {dtype})")
    condition = input("Enter condition (e.g., '== True', '< 100'): ").strip()

    condition_map[factor] = {
        'type': dtype,
        'condition': condition
    }

# === STEP 4: Quantum Filter Core ===
N = len(factor_list)
matching_stocks = []

for index, row in df.iterrows():
    # Build classical binary vector
    binary_vector = []
    for factor in factor_list:
        value = row[factor]
        dtype = condition_map[factor]['type']
        condition = condition_map[factor]['condition']

        if dtype == 'boolean':
            binary_vector.append(1 if value is True else 0)
        elif dtype in ['float', 'int']:
            try:
                binary_vector.append(1 if eval(f"{repr(value)} {condition}") else 0)
            except:
                binary_vector.append(0)
        else:
            binary_vector.append(0)

    # Quantum setup
    qreg = QuantumRegister(N, "qreg")
    creg = ClassicalRegister(N, "creg")
    qc = QuantumCircuit(qreg, creg)

    # Initialize qubits using binary vector (X if 1)
    for i in range(N):
        if binary_vector[i] == 1:
            qc.x(qreg[i])

    # Measure (not logically necessary here but completes the circuit)
    for i in range(N):
        qc.measure(qreg[i], creg[i])

    # Boolean logic: if all qubits are |1⟩, consider it a match
    if all(bit == 1 for bit in binary_vector):
        stock_name = row.get("Stock Name", f"Stock {index}")
        matching_stocks.append(stock_name)

# === STEP 5: Export Results ===
output_path = f"{filename_prefix}.csv"
output_df = pd.DataFrame(matching_stocks, columns=["Matching Stocks"])
output_df.to_csv(output_path, index=False)

print(f"\n✅ QINTEL Filter Completed.")
print(f"Total matching stocks: {len(matching_stocks)}")
print(f"Results saved to: {output_path}")
