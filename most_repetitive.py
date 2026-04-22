# Q1: Find the most repetitive element in a list using a dictionary

L1 = [1, 2, 2, 3, 2, 3, 4, 5]

freq = {}

for num in L1:
    freq[num] = freq.get(num, 0) + 1

most_repetitive = max(freq, key=freq.get)

print("Frequency Dictionary:", freq)
print("Most Repetitive Element:", most_repetitive)
