from time import sleep
import logging

def start_program(thr_name):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Thread %s: starting", thr_name)   


    for i in range(5):
        for j in range (20):
            print(f"{j}; ", end="")
            sleep(0.1)
        print()
