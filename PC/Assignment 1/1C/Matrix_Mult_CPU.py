import multiprocessing

def add_matrices(matrix1, matrix2, result):
    # perform matrix addition
    matrix_sum = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] + matrix2[i][j])
        matrix_sum.append(row)
    result.put(matrix_sum)

if __name__ == '__main__':
    # take input from user for matrices
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    matrix1 = []
    matrix2 = []
    print("Enter the elements of matrix 1:")
    for i in range(rows):
        row = []
        for j in range(cols):
            element = int(input())
            row.append(element)
        matrix1.append(row)
    print("Enter the elements of matrix 2:")
    for i in range(rows):
        row = []
        for j in range(cols):
            element = int(input())
            row.append(element)
        matrix2.append(row)

    # create a multiprocessing queue to store the result
    result = multiprocessing.Queue()

    # create a process for each CPU core
    processes = []
    for i in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=add_matrices, args=(matrix1, matrix2, result))
        processes.append(process)
        process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()

    # get the matrix sum from the queue
    matrix_sum = result.get()
    for i in range(multiprocessing.cpu_count() - 1):
        result.get()

    # print the matrix sum
    print("The sum of matrices is:")
    for row in matrix_sum:
        print(row)
