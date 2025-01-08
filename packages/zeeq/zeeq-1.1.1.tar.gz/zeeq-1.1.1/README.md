### **Zeeq: Quantum Natural Language Interpreter**

Zeeq is a natural language-based interface for designing, simulating, and running quantum circuits using Qiskit. It enables users to interact with quantum programming through intuitive English commands, making quantum computing accessible to everyone—from beginners to experienced developers.

---

### **Features and Commands**

Zeeq supports a comprehensive range of commands for creating and manipulating quantum circuits. These commands are organized into intuitive categories for easy use.

---

#### **1. Create a Circuit**
- **Command**:  
  - `Create a circuit with [number] qubits`  
- **Description**: Initializes a quantum circuit with the specified number of qubits.
- **Example**:  
  - `Create a circuit with 3 qubits`

---

#### **2. Apply Quantum Gates**
Zeeq allows the application of quantum gates to specific qubits. Below is the list of supported gates:

| **Gate** | **Command**                                                                 | **Description**                                                                                     | **Example**                                              |
|----------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **H**    | `Apply Hadamard gate to qubit [n]`                                          | Creates a superposition state for the specified qubit.                                              | `Apply Hadamard gate to qubit 0`                         |
| **X**    | `Apply X gate to qubit [n]`                                                | Flips the state of the specified qubit (quantum NOT gate).                                          | `Apply X gate to qubit 1`                                |
| **Y**    | `Apply Y gate to qubit [n]`                                                | Applies a Pauli-Y operation, flipping the qubit with a phase.                                       | `Apply Y gate to qubit 2`                                |
| **Z**    | `Apply Z gate to qubit [n]`                                                | Applies a phase flip to the qubit.                                                                 | `Apply Z gate to qubit 0`                                |
| **S**    | `Apply S gate to qubit [n]`                                                | Applies a 90-degree phase shift.                                                                   | `Apply S gate to qubit 1`                                |
| **T**    | `Apply T gate to qubit [n]`                                                | Applies a 45-degree phase shift.                                                                   | `Apply T gate to qubit 2`                                |
| **RX**   | `Apply RX gate [angle] to qubit [n]`                                       | Rotates the qubit around the X-axis by the specified angle (in radians).                           | `Apply RX gate 1.57 to qubit 0`                          |
| **RY**   | `Apply RY gate [angle] to qubit [n]`                                       | Rotates the qubit around the Y-axis by the specified angle (in radians).                           | `Apply RY gate 3.14 to qubit 1`                          |
| **RZ**   | `Apply RZ gate [angle] to qubit [n]`                                       | Rotates the qubit around the Z-axis by the specified angle (in radians).                           | `Apply RZ gate 1.0 to qubit 2`                           |
| **SX**   | `Apply SX gate to qubit [n]`                                               | Applies the square root of the Pauli-X gate.                                                       | `Apply SX gate to qubit 0`                               |
| **CNOT** | `Apply CNOT gate from qubit [control] to qubit [target]`                   | Creates entanglement between two qubits using a controlled NOT gate.                               | `Apply CNOT gate from qubit 0 to qubit 1`                |
| **SWAP** | `Apply SWAP gate between qubit [n] and qubit [m]`                          | Swaps the states of the two specified qubits.                                                      | `Apply SWAP gate between qubit 1 and qubit 2`            |
| **Toffoli** | `Apply Toffoli gate to qubits [control1], [control2], and [target]`      | Applies a controlled-controlled NOT gate (Toffoli gate).                                           | `Apply Toffoli gate to qubits 0, 1, and 2`               |

---

#### **3. Measure Qubits**
- **Command**:  
  - `Measure all qubits`  
  - `Measure qubit [n]`
- **Description**: Measures all or specific qubits and maps their states to classical bits.
- **Example**:  
  - `Measure all qubits`  
  - `Measure qubit 0`

---

#### **4. Initialize States**
- **Command**: `Initialize state to [state vector]`
- **Description**: Initializes the qubits to a specific quantum state using a state vector. The vector must have valid amplitudes.
- **Example**:  
  - `Initialize state to 0.707 0 0.707 0`

---

#### **5. Reset Qubits**
- **Command**:  
  - `Reset all qubits`  
  - `Reset qubit [n]`
- **Description**: Resets all or specific qubits to the \( |0\rangle \) state.
- **Example**:  
  - `Reset all qubits`  
  - `Reset qubit 1`

---

#### **6. Add Barriers**
- **Command**:  
  - `Add barrier to all qubits`  
  - `Add barrier to qubits [n, m, ...]`
- **Description**: Adds barriers to separate operations visually or logically.
- **Example**:  
  - `Add barrier to all qubits`  
  - `Add barrier to qubits 0 and 1`

---

#### **7. Display Circuit**
- **Command**: `Display the circuit`
- **Description**: Outputs an ASCII representation of the current quantum circuit.
- **Example**:  
  - `Display the circuit`

---

#### **8. Export Circuit**
- **Command**: `Export the circuit to file [filename]`
- **Description**: Exports the quantum circuit to a QASM file for external use.
- **Example**:  
  - `Export the circuit to file circuit.qasm`

---

#### **9. Run the Circuit**
- **Command**: `Run the circuit [number] times`
- **Description**: Executes the quantum circuit on a simulator and returns the result.
- **Example**:  
  - `Run the circuit 1000 times`

---

#### **10. Visualize Bloch Sphere**
- **Command**: `Draw Bloch sphere for qubit [n]`
- **Description**: Visualizes the quantum state of a specific qubit on the Bloch sphere (requires visualization libraries).
- **Example**:  
  - `Draw Bloch sphere for qubit 0`

---

### **Example Workflow**

```plaintext
Create a circuit with 3 qubits  
Apply Hadamard gate to qubit 0  
Apply CNOT gate from qubit 0 to qubit 1  
Apply RX gate 1.57 to qubit 2  
Measure all qubits  
Run the circuit 1000 times  
Display the circuit  
Export the circuit to file example.qasm  
```

---

### **Why Use Zeeq?**
1. **Simplifies Quantum Programming**: Users can create and manipulate quantum circuits in plain English.
2. **Intuitive Commands**: No need to learn Qiskit syntax or quantum theory to get started.
3. **Versatile**: Supports various quantum gates and operations for different applications.
4. **Beginner-Friendly**: Designed for educational and professional use cases alike.

Zeeq is your bridge between quantum programming and practical implementation!