from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Zeeq:
    def __init__(self):
        self.circuit = None
        self.backend = Aer.get_backend('qasm_simulator')
        self.statevector_backend = Aer.get_backend('statevector_simulator')

    def interpret(self, command):
        """Interprets natural language commands for quantum circuit operations."""
        command = command.lower()

        try:
            if "create a circuit" in command:
                self.create_circuit(command)
            elif "add classical register" in command:
                self.add_classical_register(command)
            elif "initialize state" in command:
                self.initialize_state(command)
            elif "apply" in command and "gate" in command:
                self.apply_gate(command)
            elif "reset qubit" in command:
                self.reset_qubit(command)
            elif "add barrier" in command:
                self.add_barrier(command)
            elif "display the circuit" in command:
                self.display_circuit()
            elif "export the circuit" in command:
                self.export_circuit(command)
            elif "measure" in command:
                self.measure_qubits(command)
            elif "run the circuit" in command:
                self.run_circuit(command)
            elif "draw bloch sphere" in command:
                self.draw_bloch_sphere(command)
            else:
                logging.warning("Command not recognized.")
        except Exception as e:
            logging.error(f"Error interpreting command: {command}. Details: {e}")

    def create_circuit(self, command):
        """Create a quantum circuit with specified number of qubits."""
        try:
            num_qubits = int(command.split("with")[1].split("qubits")[0].strip())
            self.circuit = QuantumCircuit(num_qubits, num_qubits)
            logging.info(f"Quantum circuit with {num_qubits} qubits created.")
        except ValueError:
            logging.error("Invalid number of qubits specified.")

    def add_classical_register(self, command):
        """Add a classical register for measurement."""
        try:
            num_bits = int(command.split("with")[1].split("bits")[0].strip())
            self.circuit.add_register(num_bits)
            logging.info(f"Classical register with {num_bits} bits added.")
        except ValueError:
            logging.error("Invalid number of bits specified.")

    def initialize_state(self, command):
        """Initialize the state of the qubits."""
        try:
            state_vector = [float(x) for x in command.split("to state")[1].strip().split()]
            self.circuit.initialize(state_vector, range(len(state_vector)))
            logging.info(f"Qubits initialized to state {state_vector}.")
        except Exception as e:
            logging.error(f"Error initializing state: {e}")

    def apply_gate(self, command):
        """Apply quantum gates."""
        try:
            if "hadamard" in command:
                qubit = int(command.split("to qubit")[1].strip())
                self.circuit.h(qubit)
                logging.info(f"Hadamard gate applied to qubit {qubit}.")
            elif "x gate" in command:
                qubit = int(command.split("to qubit")[1].strip())
                self.circuit.x(qubit)
                logging.info(f"X gate applied to qubit {qubit}.")
            elif "rx gate" in command:
                angle, qubit = map(float, command.split("rx gate")[1].split("to qubit"))
                self.circuit.rx(angle, int(qubit))
                logging.info(f"RX gate with angle {angle} applied to qubit {int(qubit)}.")
            else:
                logging.warning("Gate command not recognized.")
        except Exception as e:
            logging.error(f"Error applying gate: {e}")

    def reset_qubit(self, command):
        """Reset a specific qubit or all qubits."""
        try:
            if "all qubits" in command:
                self.circuit.reset(range(self.circuit.num_qubits))
                logging.info("All qubits have been reset.")
            else:
                qubit = int(command.split("reset qubit")[1].strip())
                self.circuit.reset(qubit)
                logging.info(f"Qubit {qubit} has been reset.")
        except Exception as e:
            logging.error(f"Error resetting qubit: {e}")

    def add_barrier(self, command):
        """Add a barrier to the circuit."""
        try:
            if "all qubits" in command:
                self.circuit.barrier()
                logging.info("Barrier added across all qubits.")
            else:
                qubits = [int(q) for q in command.split("qubit")[1:]]
                self.circuit.barrier(qubits)
                logging.info(f"Barrier added to qubits {qubits}.")
        except Exception as e:
            logging.error(f"Error adding barrier: {e}")

    def display_circuit(self):
        """Display the current quantum circuit."""
        if self.circuit:
            print(self.circuit.draw())
        else:
            logging.warning("No circuit has been created yet.")

    def export_circuit(self, command):
        """Export the circuit to a QASM file."""
        try:
            filename = command.split("to file")[1].strip()
            if not filename.endswith(".qasm"):
                filename += ".qasm"
            with open(filename, "w") as f:
                f.write(self.circuit.qasm())
            logging.info(f"Circuit exported to {filename}.")
        except Exception as e:
            logging.error(f"Error exporting circuit: {e}")

    def measure_qubits(self, command):
        """Measure qubits."""
        try:
            if "all" in command:
                self.circuit.measure_all()
                logging.info("Measured all qubits.")
            else:
                qubit = int(command.split("measure qubit")[1].strip())
                self.circuit.measure(qubit, qubit)
                logging.info(f"Measured qubit {qubit}.")
        except Exception as e:
            logging.error(f"Error measuring qubits: {e}")

    def draw_bloch_sphere(self, command):
        """Draw the Bloch sphere for a qubit."""
        try:
            qubit = int(command.split("draw bloch sphere for qubit")[1].strip())
            statevector = execute(self.circuit, self.statevector_backend).result().get_statevector()
            plot_bloch_multivector(statevector).show()
            logging.info(f"Bloch sphere for qubit {qubit} displayed.")
        except Exception as e:
            logging.error(f"Error drawing Bloch sphere: {e}")

    def run_circuit(self, command):
        """Run the circuit on the simulator."""
        try:
            shots = int(command.split("run the circuit")[1].split("times")[0].strip())
            job = execute(self.circuit, self.backend, shots=shots)
            result = job.result()
            counts = result.get_counts(self.circuit)
            logging.info(f"Execution result: {counts}")
        except Exception as e:
            logging.error(f"Error running circuit: {e}")
