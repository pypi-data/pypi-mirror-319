import cirq
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Zeeq:
    def __init__(self):
        self.circuit = cirq.Circuit()
        self.qubits = []
        self.simulator = cirq.Simulator()

    def interpret(self, command):
        """Interprets natural language commands for quantum circuit operations."""
        command = command.lower()

        try:
            if "create a circuit" in command:
                self.create_circuit(command)
            elif "add classical register" in command:
                logging.warning("Cirq does not use classical registers explicitly.")
            elif "initialize state" in command:
                self.initialize_state(command)
            elif "apply" in command and "gate" in command:
                self.apply_gate(command)
            elif "reset qubit" in command:
                self.reset_qubit(command)
            elif "add barrier" in command:
                logging.warning("Barriers are not used in Cirq.")
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
            self.qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
            self.circuit = cirq.Circuit()
            logging.info(f"Quantum circuit with {num_qubits} qubits created.")
        except ValueError:
            logging.error("Invalid number of qubits specified.")

    def initialize_state(self, command):
        """Initialize the state of the qubits."""
        try:
            state_vector = [complex(float(x)) for x in command.split("to state")[1].strip().split()]
            if len(state_vector) != 2 ** len(self.qubits):
                logging.error("State vector dimension does not match number of qubits.")
                return
            # Add an initialization moment (requires custom initialization in Cirq)
            init_gate = cirq.StatePreparationChannel(state_vector)
            self.circuit.append(init_gate(*self.qubits))
            logging.info(f"Qubits initialized to state {state_vector}.")
        except Exception as e:
            logging.error(f"Error initializing state: {e}")

    def apply_gate(self, command):
        """Apply quantum gates."""
        try:
            if "hadamard" in command:
                qubit = int(command.split("to qubit")[1].strip())
                self.circuit.append(cirq.H(self.qubits[qubit]))
                logging.info(f"Hadamard gate applied to qubit {qubit}.")
            elif "x gate" in command:
                qubit = int(command.split("to qubit")[1].strip())
                self.circuit.append(cirq.X(self.qubits[qubit]))
                logging.info(f"X gate applied to qubit {qubit}.")
            elif "rx gate" in command:
                parts = command.split("rx gate")[1].split("to qubit")
                angle = float(parts[0].strip())
                qubit = int(parts[1].strip())
                self.circuit.append(cirq.rx(angle)(self.qubits[qubit]))
                logging.info(f"RX gate with angle {angle} applied to qubit {qubit}.")
            else:
                logging.warning("Gate command not recognized.")
        except Exception as e:
            logging.error(f"Error applying gate: {e}")

    def reset_qubit(self, command):
        """Reset a specific qubit or all qubits."""
        try:
            if "all qubits" in command:
                self.circuit.append(cirq.ResetChannel().on_each(*self.qubits))
                logging.info("All qubits have been reset.")
            else:
                qubit = int(command.split("reset qubit")[1].strip())
                self.circuit.append(cirq.ResetChannel().on(self.qubits[qubit]))
                logging.info(f"Qubit {qubit} has been reset.")
        except Exception as e:
            logging.error(f"Error resetting qubit: {e}")

    def display_circuit(self):
        """Display the current quantum circuit."""
        if self.circuit:
            print(self.circuit)
        else:
            logging.warning("No circuit has been created yet.")

    def export_circuit(self, command):
        """Export the circuit to a file."""
        try:
            filename = command.split("to file")[1].strip()
            if not filename.endswith(".txt"):
                filename += ".txt"
            with open(filename, "w") as f:
                f.write(str(self.circuit))
            logging.info(f"Circuit exported to {filename}.")
        except Exception as e:
            logging.error(f"Error exporting circuit: {e}")

    def measure_qubits(self, command):
        """Measure qubits."""
        try:
            if "all" in command:
                self.circuit.append(cirq.measure(*self.qubits))
                logging.info("Measured all qubits.")
            else:
                qubit = int(command.split("measure qubit")[1].strip())
                self.circuit.append(cirq.measure(self.qubits[qubit]))
                logging.info(f"Measured qubit {qubit}.")
        except Exception as e:
            logging.error(f"Error measuring qubits: {e}")

    def draw_bloch_sphere(self, command):
        """Draw the Bloch sphere for a qubit."""
        try:
            qubit = int(command.split("draw bloch sphere for qubit")[1].strip())
            result = self.simulator.simulate(self.circuit)
            bloch_vector = cirq.bloch_vector_from_state_vector(result.final_state_vector, qubit)
            logging.info(f"Bloch sphere vector for qubit {qubit}: {bloch_vector}.")
            # Plotting requires external libraries, if necessary.
        except Exception as e:
            logging.error(f"Error drawing Bloch sphere: {e}")

    def run_circuit(self, command):
        """Run the circuit on the simulator."""
        try:
            shots = int(command.split("run the circuit")[1].split("times")[0].strip())
            result = self.simulator.run(self.circuit, repetitions=shots)
            logging.info(f"Execution result: {result}")
        except Exception as e:
            logging.error(f"Error running circuit: {e}")
