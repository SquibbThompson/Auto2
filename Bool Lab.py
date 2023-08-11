import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Convert binary string to matrix
def string_to_bin_matrix(bin_string):
    return [[int(bit) for bit in line] for line in bin_string.split('\n') if line]

# Convert user criteria to pattern
def get_user_criteria():
    positions = ["⌈", "‾", "⌉", "<-", "->", "⌊", "_", "⌋"]
    pattern = [None] * 9
    print("\nEnter the state for each position (0 for off_switch, 1 for on_switch):")
    for idx, pos in enumerate(positions):
        while True:
            try:
                state = int(input(f"{pos}: "))
                if state in [0, 1]:
                    pattern[idx if idx < 4 else idx + 1] = state
                    break
                else:
                    print("Invalid input. Please enter 0 or 1.")
            except ValueError:
                print("Invalid input. Please enter 0 or 1.")
    pattern[4] = 1
    return np.array(pattern).reshape(3, 3)

# Prompt for acceptable counts
def get_acceptable_counts(prompt):
    print(prompt)
    while True:
        try:
            counts = input("Enter the counts separated by commas: ")
            counts = [int(count) for count in counts.split(",")]
            return counts
        except ValueError:
            print("Invalid input. Please enter a comma-separated list of numbers.")

# Update function
def update_matrix(matrix, on_acceptable_counts, on_acceptable_patterns, off_unacceptable_patterns):
    updated_matrix = matrix.copy()
    height, width = matrix.shape

    for i in range(height):
        for j in range(width):
            n_on_switch = 0
            neighborhood = []
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if x >= 0 and y >= 0 and x < height and y < width:
                        if matrix[x, y] == 1:
                            n_on_switch += 1
                        neighborhood.append(matrix[x, y])
                    else:
                        neighborhood.append(0)
            neighborhood = np.array(neighborhood).reshape(3, 3)

            if matrix[i, j] == 0:
                if n_on_switch in on_acceptable_counts or any(np.array_equal(neighborhood, pattern) for pattern in on_acceptable_patterns):
                    updated_matrix[i, j] = 1
            elif matrix[i, j] == 1:
                match_counts = sum([np.array_equal(neighborhood, pattern) for pattern in off_unacceptable_patterns])
                if match_counts == len(off_unacceptable_patterns):
                    updated_matrix[i, j] = 0

    return updated_matrix

# Binary string definition
binary_string = """
1001001001001001
0110110110110110
1001001001001001
0110110110110110
1001001001001001
0110110110110110
1001001001001001
0110110110110110
""".strip()

# Generate initial state
initial_state = np.array(string_to_bin_matrix(binary_string))

# Get user criteria for turning a cell "on"
print("\nCriteria for turning an off_switch cell to on_switch:")
on_counts = get_acceptable_counts("Enter the number of on_switch neighbors required (e.g., 2,3,6):")
on_patterns = [get_user_criteria() for _ in range(int(input("How many on_switch patterns would you like to define? ")))]
# Get user criteria for turning a cell "off"
print("\nCriteria for turning an on_switch cell to off_switch:")
off_patterns = [get_user_criteria() for _ in range(int(input("How many off_switch patterns would you like to define? ")))]

# Animation function
def animate(i):
    global initial_state
    initial_state = update_matrix(initial_state, on_counts, on_patterns, off_patterns)
    plt.imshow(initial_state, cmap='binary')

# Setup animation
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, animate, frames=1000, interval=200)

plt.show()
