import random

def generate_random_bits(n):
    return [random.randint(0, 1) for _ in range(n)]

def generate_random_bases(n):
    return [random.choice(['+', 'x']) for _ in range(n)]

def measure_qubit(qubit, basis):
    if qubit['basis'] == basis:
        return qubit['bit']
    else:
        return random.randint(0, 1)

def bb84_protocol(n):
    # Alice's part
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)
    
    # Alice prepares qubits
    qubits = [{'bit': bit, 'basis': basis} for bit, basis in zip(alice_bits, alice_bases)]
    
    # Bob's part
    bob_bases = generate_random_bases(n)
    bob_measurements = [measure_qubit(qubit, basis) for qubit, basis in zip(qubits, bob_bases)]
    
    # Alice and Bob compare bases
    matching_bases = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    
    # Generate key from matching bases
    key = [alice_bits[i] for i in matching_bases]
    
    return key, matching_bases

def simulate_eavesdropping(qubits, eavesdropper_bases):
    eavesdropper_measurements = [measure_qubit(qubit, basis) for qubit, basis in zip(qubits, eavesdropper_bases)]
    
    # Eavesdropper's interference changes the qubits
    for i, basis in enumerate(eavesdropper_bases):
        if basis != qubits[i]['basis']:
            qubits[i]['bit'] = eavesdropper_measurements[i]
            qubits[i]['basis'] = basis
    
    return qubits

# Example usage
if __name__ == "__main__":
    n = 100  # number of qubits
    
    print("Simulating BB84 protocol without eavesdropping:")
    key, matching_bases = bb84_protocol(n)
    print(f"Generated key length: {len(key)}")
    print(f"First 10 bits of the key: {key[:10]}")
    
    print("\nSimulating BB84 protocol with eavesdropping:")
    # Alice's part
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)
    qubits = [{'bit': bit, 'basis': basis} for bit, basis in zip(alice_bits, alice_bases)]
    
    # Eavesdropper's part
    eve_bases = generate_random_bases(n)
    qubits = simulate_eavesdropping(qubits, eve_bases)
    
    # Bob's part
    bob_bases = generate_random_bases(n)
    bob_measurements = [measure_qubit(qubit, basis) for qubit, basis in zip(qubits, bob_bases)]
    
    # Alice and Bob compare bases
    matching_bases = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    
    # Generate key from matching bases
    key_alice = [alice_bits[i] for i in matching_bases]
    key_bob = [bob_measurements[i] for i in matching_bases]
    
    print(f"Alice's key length: {len(key_alice)}")
    print(f"Bob's key length: {len(key_bob)}")
    print(f"Number of matching bits: {sum(a == b for a, b in zip(key_alice, key_bob))}")
    print(f"Error rate: {1 - sum(a == b for a, b in zip(key_alice, key_bob)) / len(key_alice):.2%}")
