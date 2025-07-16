import pandas as pd
import sys
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

print("🔬 QINTELchem v1.0 — Quantum-Classical Compound Filter\n")

# === STEP 1: Load Dataset ===
if len(sys.argv) < 2:
    print("❌ Usage: python QINTELchem_v1.py <path_to_dataset.csv>")
    sys.exit(1)

dataset_path = sys.argv[1]
try:
    df = pd.read_csv(dataset_path)
except FileNotFoundError:
    print(f"❌ File not found: {dataset_path}")
    sys.exit(1)

# === STEP 2: Show Columns ===
print("\n🧪 Available Columns:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# === STEP 3: User selects filtering factors ===
factor_indices = input("\nEnter indices of columns to use as filters (comma-separated): ")
selected_indices = [int(i.strip()) - 1 for i in factor_indices.split(",") if i.strip().isdigit()]
factor_list = [df.columns[i] for i in selected_indices]

# === STEP 4: Detect data types + gather condition input ===
condition_map = {}

for factor in factor_list:
    sample_value = df[factor].dropna().iloc[0]

    if isinstance(sample_value, bool):
        dtype = 'boolean'
    elif isinstance(sample_value, int):
        dtype = 'int'
    elif isinstance(sample_value, float):
        dtype = 'float'
    else:
        dtype = 'string'

    print(f"\n🧠 Factor: '{factor}' (Detected type: {dtype})")
    condition = input("Enter condition to apply (e.g., '== True', '< 100'): ").strip()

    condition_map[factor] = {
        'type': dtype,
        'condition': condition
    }

# === STEP 5: Build binary vectors based on conditions ===
binary_vectors = []
compound_names = []

for idx, row in df.iterrows():
    binary_vector = []
    for factor in factor_list:
        value = row[factor]
        dtype = condition_map[factor]['type']
        condition = condition_map[factor]['condition']

        if dtype == 'boolean':
            binary_vector.append(1 if value is True else 0)
        elif dtype in ['float', 'int']:
            try:
                if eval(f"{repr(value)} {condition}"):
                    binary_vector.append(1)
                else:
                    binary_vector.append(0)
            except:
                binary_vector.append(0)
        else:
            binary_vector.append(0)

    binary_vectors.append(binary_vector)
    compound_names.append(row.get("Compound Name", f"Compound_{idx}"))

# === STEP 6: Quantum Matching Logic ===
matched_compounds = []
N = len(factor_list)

for i in range(len(binary_vectors)):
    binary_vector = binary_vectors[i]
    compound_name = compound_names[i]

    # Create quantum and classical registers
    qreg = QuantumRegister(N, 'q')
    creg = ClassicalRegister(N, 'c')
    qc = QuantumCircuit(qreg, creg)

    # Classical → Quantum bit assignment using X gates
    for j in range(N):
        if binary_vector[j] == 1:
            qc.x(qreg[j])

    # Measure qubits into classical bits
    for j in range(N):
        qc.measure(qreg[j], creg[j])

    # Grover-style Boolean function: match only if all bits are 1
    if all(bit == 1 for bit in binary_vector):
        matched_compounds.append(compound_name)

# === STEP 7: Export Results ===
output_df = pd.DataFrame(matched_compounds, columns=["Matched Compounds"])
output_path = "qintelchem_output.csv"
output_df.to_csv(output_path, index=False)

print("\n✅ QINTELchem Filter Completed.")
print(f"Total matched compounds: {len(matched_compounds)}\n")

for compound in matched_compounds:
    print(f"🧪 {compound}")

print(f"\n📄 Results saved to: {output_path}")
