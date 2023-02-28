import multiprocessing

def convert_sentence(sentence, result):
    alternate_sentence = ''
    for i in range(len(sentence)):
        if i % 2 == 0:
            alternate_sentence += sentence[i].upper()
        else:
            alternate_sentence += sentence[i].lower()
    result.put(alternate_sentence)

if __name__ == '__main__':
    # take input from user
    sentence = input("Enter a sentence: ")

    # create a multiprocessing queue to store the result
    result = multiprocessing.Queue()

    # create a process for each CPU core
    processes = []
    for i in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=convert_sentence, args=(sentence, result))
        processes.append(process)
        process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()

    # get the alternate sentence from the queue
    alternate_sentence = result.get()
    for i in range(multiprocessing.cpu_count() - 1):
        result.get()

    # print the alternate sentence
    print("The alternate sentence is:", alternate_sentence)
