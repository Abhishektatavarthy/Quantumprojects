# quantum_portal.py

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector, state_fidelity, partial_trace
from qiskit.visualization import plot_bloch_multivector
import numpy as np
import time
import sys

# ========== SINGLE QUBIT TELEPORTATION (BELL PAIR MODE) ==========
def teleport_single_qubit_state(alpha, beta):
    """Teleport an arbitrary 1-qubit state |psi> = alpha|0> + beta|1> using Bell pair protocol."""
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(2, "c")
    qc = QuantumCircuit(q, c)

    qc.initialize([alpha, beta], q[0])
    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.h(q[0])
    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])

    with qc.if_test((c, 1)):
        qc.x(q[2])
    with qc.if_test((c, 2)):
        qc.z(q[2])
    with qc.if_test((c, 3)):
        qc.x(q[2])
        qc.z(q[2])

    backend = Aer.get_backend("aer_simulator")
    qc = qc.reverse_bits()
    result = Statevector.from_instruction(qc)
    return partial_trace(result, [0, 1])  # Bob's qubit

# ========== SINGLE QUBIT: USER-DEFINED ARBITRARY STATE ==========
def teleport_user_qubit():
    """Prompt user for alpha and beta, teleport the state, and return Bob's state and fidelity."""
    alpha = complex(input("Enter alpha (e.g., 0.6+0j): "))
    beta = complex(input("Enter beta (e.g., 0.8+0j): "))
    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    alpha /= norm
    beta /= norm

    result = teleport_single_qubit_state(alpha, beta)
    expected = Statevector([alpha, beta])
    fidelity = state_fidelity(result, expected)
    return result, fidelity

# ========== TWO QUBIT TELEPORTATION (TENSOR DECOMPOSITION MODE) ==========
def teleport_twoqubit_tensor_mode(a, b, c, d):
    """Teleport a 2-qubit state using tensor decomposition and post-selection."""
    norm = np.sqrt(abs(a)**2 + abs(b)**2 + abs(c)**2 + abs(d)**2)
    a, b, c, d = a/norm, b/norm, c/norm, d/norm

    phi0 = teleport_single_qubit_state(a, b)
    phi1 = teleport_single_qubit_state(c, d)

    zero = np.array([1, 0])
    one = np.array([0, 1])
    state_0 = np.kron(zero, phi0.data)
    state_1 = np.kron(one,  phi1.data)
    final_state = state_0 + state_1
    final_state /= np.linalg.norm(final_state)

    expected = Statevector([a, b, c, d])
    fidelity = state_fidelity(expected, final_state)
    return final_state, fidelity

# ========== TWO QUBIT TELEPORTATION (DOUBLE BELL STATE MODE) ==========
def teleport_twoqubit_bellmode(a, b, c, d):
    """Teleport a 2-qubit state using two Bell pairs and two 1-qubit teleportations."""
    norm = np.sqrt(abs(a)**2 + abs(b)**2 + abs(c)**2 + abs(d)**2)
    a, b, c, d = a/norm, b/norm, c/norm, d/norm

    psi = Statevector([a, b, c, d])
    reduced_q0 = partial_trace(psi, [1])
    reduced_q1 = partial_trace(psi, [0])

    vec0 = reduced_q0.data[:, 0]
    vec1 = reduced_q1.data[:, 0]

    phi0 = teleport_single_qubit_state(vec0[0], vec0[1])
    phi1 = teleport_single_qubit_state(vec1[0], vec1[1])

    final_state = np.kron(phi0.data, phi1.data)
    fidelity = state_fidelity(psi, final_state)
    return final_state, fidelity

# ========== TOOLS: DISPLAY & FIDELITY ==========
def display_state(statevector):
    print("\n🧾 Final Statevector:")
    for i, amp in enumerate(statevector):
        label = format(i, f'0{int(np.log2(len(statevector)))}b')
        print(f"|{label}⟩ : {amp:.4f}")


def fidelity_check(target, actual):
    return state_fidelity(Statevector(target), Statevector(actual))


def show_bloch(qubit_state):
    """Visualize a single-qubit state on the Bloch sphere."""
    plot_bloch_multivector(qubit_state).show()

# ========== ANIMATION & ATTRIBUTION ==========
def spinning_qubit():
    frames = [
        "   ○       \n  /|\\      \n / | \\     \n    |      \n   / \\     ",
        "   ○       \n   |\\      \n   | \\     \n   |       \n  / \\      ",
        "   ○       \n  /|\\      \n / | \\     \n    |      \n   / \\     ",
        "   ○       \n  /|       \n / |       \n   |       \n  / \\      ",
    ]
    print("🚀 Initializing Quantum Portal...\n")
    for _ in range(2):
        for frame in frames:
            sys.stdout.write("\033[H\033[J")
            print(frame)
            time.sleep(0.3)
    print("\n⚛️  Qubits spun up and entangled. Portal is stable.\n")

# ========== THE END ==========
print("\n🚀 Quantum Portal initialized. If you’re reading this, you just teleported logic across the void. Nice job, Quantum Sorcerer 🧙‍♂️⚛️")
print("🔗 Powered by Qiskit • © IBM Quantum")
spinning_qubit()
