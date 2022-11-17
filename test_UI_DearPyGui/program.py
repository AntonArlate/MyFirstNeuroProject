from time import sleep
import logging
data = []


def start_program(thr_name, q):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Thread %s: starting", thr_name)   

    for i in range(10):
        sleep (0.4)
        data.append(i)
        print (data)
    q.task_done()

def calc (thr_name, q):
    for i in range(len(data)):
        sleep(0.4)
        data.pop()
    q.task_done()


    # for i in range(5):
    #     for j in range (20):
    #         print(f"{j}; ", end="")
    #         sleep(0.1)
    #     print()
