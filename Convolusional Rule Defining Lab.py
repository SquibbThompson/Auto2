import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.signal import convolve2d

# convert binary string to matrix
def string_to_bin_matrix(bin_string):
    bin_string = bin_string.replace(" ", "")
    bin_string = bin_string.replace("]","")
    bin_string = bin_string.replace("[", "")
    return [[int(bit) for bit in line] for line in bin_string.split('\n') if line]

# define the function that checks and updates the matrix
def update_matrix(matrix):
    height, width = matrix.shape

    # Define the convolution kernel to sum the neighbors
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])

    # Convolve the matrix with the kernel to get the sum of neighbors for each cell
    neighbor_sums = convolve2d(matrix, kernel, mode='same', boundary='symm')

    # Define the criteria for active neighbors
    active_neighbors_criteria = {4,5,6,7,8}

    # Create a mask for cells that meet the active neighbors criteria
    criteria_mask = np.isin(neighbor_sums, list(active_neighbors_criteria))

    # Invert the cell color if an 'Inactive' cell borders exactly n[n] 'Active' cells
    updated_matrix = np.where((matrix == 0) & criteria_mask, 1, matrix)

    # Turn two diagonal 'Active' cells to 'Inactive' if criteria are met
    updated_matrix = np.where((matrix == 1) & criteria_mask, 0, updated_matrix)

    return updated_matrix

# Insert Bin Array
binary_string = """

0000000000000000000000000000000000000000
0111111111111111111111111111111111111110
0111111111111111111111111111111111111110
0110000000000000000000000000000000000110
0110111111111111111111111111111111110110
0110111111111111111111111111111111110110
0110110000000000000000000000000000110110
0110110000000000000000000000000000110110
0110110011111111111111111111111100110110
0110110011111111111111111111111100110110
0110110011000000000000000000001100110110
0110110011011111111111111111101100110110
0110110011011111111111111111101100110110
0110110011011000000000000001101100110110
0110110011011000000000000001101100110110
0110110011011000000000000001101100110110
0110110011011000000110110001101100110110
0110110011011000001101100001101100110110
0110110011011000011011000001101100110110
0110110011011000110110000001101100110110
0110110011011000101100010001101100110110
0110110011011000011000110001101100110110
0110110011011000110001100001101100110110
0110110011011000100011010001101100110110
0110110011011000000000000001101100110110
0110110011011000000000000001101100110110
0110110011011000000000000001101100110110
0110110011011111111111111111101100110110
0110110011011111111111111111101100110110
0110110011000000000000000000001100110110
0110110011111111111111111111111100110110
0110110011111111111111111111111100110110
0110110000000000000000000000000000110110
0110110000000000000000000000000000110110
0110111111111111111111111111111111110110
0110111111111111111111111111111111110110
0110000000000000000000000000000000000110
0111111111111111111111111111111111111110
0111111111111111111111111111111111111110
0000000000000000000000000000000000000000

""".strip()

# generate initial state
initial_state = np.array(string_to_bin_matrix(binary_string))

# animate cellular automata evolution
def animate(i):
    global initial_state

    initial_state = update_matrix(initial_state)
    plt.imshow(initial_state, cmap='binary')

fig, ax = plt.subplots()
global ani
ani = animation.FuncAnimation(fig, animate, frames=34, interval=34)

# Save the animation as a GIF
ani.save('Barbershop Pole Psuedo_transpose, n_Active==(4,5,6,7,8).gif', writer='pillow', fps=14)

plt.show()
