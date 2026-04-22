# Find the most repetitive element in a list

# Input list
L1 = [1, 2, 2, 3, 2, 3, 4, 5]

# Step 1: Count occurrences
num_counter = {}

for i in L1:
    if i in num_counter:
        num_counter[i] += 1
    else:
        num_counter[i] = 1

print("Frequency dictionary:", num_counter)

# Step 2: Find the most frequent element
temp = 0
final_result = None

for k, v in num_counter.items():
    print(f"k: {k}, v: {v}, temp: {temp}")
    if v > temp:
        temp = v
        final_result = k

print("\nMost repetitive element:", final_result)
