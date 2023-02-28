import random
import numpy as np
from numba import cuda

@cuda.jit
def find_max(numbers, result):
    thread_id = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x
    stride = cuda.gridDim.x * cuda.blockDim.x

    max_number = numbers[0]
    i = thread_id
    while i < len(numbers):
        if numbers[i] > max_number:
            max_number = numbers[i]
        i += stride

    cuda.atomic.max(result, 0, max_number)

if __name__ == '__main__':
    # take input from user
    n = int(input("Enter the number of elements: "))
    numbers = np.zeros(n, dtype=np.int32)

    # populate the list with random elements using random function
    for i in range(n):
        numbers[i] = random.randint(0, 999)

    # create a CUDA device array to store the result
    result = cuda.device_array(1, dtype=np.int32)
    result[0] = numbers[0]

    # set the number of threads per block and blocks per grid
    threads_per_block = 128
    blocks_per_grid = (n + threads_per_block - 1) // threads_per_block

    # launch the CUDA kernel
    find_max[blocks_per_grid, threads_per_block](numbers, result)

    # get the maximum number from the device array
    max_number = result[0]

    # print the maximum number
    print("The maximum number is:", max_number)
