import numpy as np
from numba import cuda, float32

@cuda.jit
def add_matrices(matrix1, matrix2, matrix_sum):
    i, j = cuda.grid(2)
    if i < matrix1.shape[0] and j < matrix1.shape[1]:
        matrix_sum[i, j] = matrix1[i, j] + matrix2[i, j]

if __name__ == '__main__':
    # take input from user for matrices
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    matrix1 = np.random.rand(rows, cols).astype(np.float32)
    matrix2 = np.random.rand(rows, cols).astype(np.float32)

    # create a CUDA device array to store the matrices and the matrix sum
    matrix1_device = cuda.to_device(matrix1)
    matrix2_device = cuda.to_device(matrix2)
    matrix_sum_device = cuda.device_array((rows, cols), dtype=np.float32)

    # set the number of threads per block and blocks per grid
    threads_per_block = (16, 16)
    blocks_per_grid_x = (cols + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (rows + threads_per_block[1] - 1) // threads_per_block[1]

    # launch the CUDA kernel
    add_matrices[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block](matrix1_device, matrix2_device, matrix_sum_device)

    # get the matrix sum from the device array
    matrix_sum = matrix_sum_device.copy_to_host()

    # print the matrix sum
    print("The matrix sum is:", matrix_sum)
