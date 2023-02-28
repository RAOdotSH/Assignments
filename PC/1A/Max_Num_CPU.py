import multiprocessing
import random

def find_max(numbers, result):
    max_number = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > max_number:
            max_number = numbers[i]
    result.put(max_number)

if __name__ == '__main__':
    # take input from user
    n = int(input("Enter the number of elements: "))
    numbers = []

    # populate the list with random elements using random function
    for i in range(n):
        numbers.append(random.randint(0, 999))
    
    # print the list
    print("The list is:", numbers)

    # create a multiprocessing queue to store the result
    result = multiprocessing.Queue()

    # create a process for each CPU core
    processes = []
    print("CPU Count is: ", multiprocessing.cpu_count())
    for i in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=find_max, args=(numbers, result))
        processes.append(process)
        process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()

    # get the maximum number from the queue
    max_number = result.get()
    for i in range(multiprocessing.cpu_count() - 1):
        result.get()
    
    # print the maximum number
    print("The maximum number is:", max_number)
