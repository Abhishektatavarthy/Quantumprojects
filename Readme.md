---
# 🌐 QuantumProjects  
### A Suite of Quantum Logic Engines by Abhishek Tatavarthy  

---

## 📌 About the Project

**QuantumProjects** is a collection of original quantum-inspired engines that solve real-world problems through simulation-based quantum logic. Built entirely without lab access or hardware support, this project reflects the creativity, curiosity, and self-learning of a 19-year-old quantum enthusiast.

It includes modules for:
- Financial dataset screening
- Chemical compound filtering
- Quantum teleportation simulation

---

## 📦 Modules Included

### 🔷 1. QINTEL Finance
A quantum-inspired decision engine that filters stock datasets based on user-defined conditions, mapped onto qubit logic.

- Features:
  - Boolean, float, and int filtering
  - Rule-based binary vector construction
  - Quantum-style filtering circuit per row
- 📄 [Full Module Documentation (PDF)](docs/QINTEL_Finance_README.pdf)

---

### 🔶 2. QINTEL Chem
A molecule filter that uses similar logic to screen chemical compounds by dipole moment, toxicity, and more.

- Features:
  - Dynamic detection of property types
  - User-defined condition inputs
  - Quantum register simulation for compound matching
- 📄 [Full Module Documentation (PDF)](docs/QINTEL_Chem_README.pdf)

---

### 🌀 3. Quantum Teleportation Engine
A complete teleportation simulator that handles both 1-qubit and 2-qubit state transfers using Bell pair protocols and statevector analysis.

- Features:
  - Arbitrary complex input from user
  - Fidelity calculation and Bloch visualization
  - Bell-mode and tensor-mode teleportation logic
- 📄 [Full Module Documentation (PDF)](docs/Quantum_Portal_README.pdf)

---

## 🧪 How to Run

Each `.py` file inside the `modules/` folder is a standalone quantum engine.

To run any of them:

````
python module_name.py
````

Examples:

* `QINTEL_Finance_v0.py` → Load stock data and apply filter rules
* `QINTELchem_v0.py` → Load compound data and simulate molecule filtering
* `quantum_portal.py` → Enter a quantum state and teleport it

---

## 📁 Repository Structure

```
QuantumProjects/
├── modules/
│   ├── QINTEL_Finance_v0.py
│   ├── QINTELchem_v0.py
│   └── quantum_portal.py
│
├── docs/
│   ├── QINTEL_Finance_README.pdf
│   ├── QINTEL_Chem_README.pdf
│   └── Quantum_Portal_README.pdf
│
├── LICENSE
├── README.md   ← This file
```

---

## 🔮 Future Development Plans

* Implement Grover-based quantum filtering
* Add molecule simulation features (Qiskit Nature or ORCA)
* Build quantum ML pipelines for stock/molecule prediction
* Release QINTEL-Bio for protein-level filtering
* Port circuits to real IBMQ quantum hardware

---

## ⚠️ Disclaimer

This project was developed by a 19-year-old student with no access to labs, simulators, or formal quantum infrastructure.
Any bugs or limitations will be improved in future versions.

✨ The goal is to make each version faster, smarter, and more quantum-powered than ever.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
(c) 2025 Abhishek Tatavarthy

---

## 🙌 Acknowledgements

Powered by:

* [Qiskit](https://qiskit.org)
* [Python](https://python.org)
* Curiosity, creativity, and a little madness 🤍

```
---

