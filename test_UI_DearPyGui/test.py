import logging
import threading

from UI import start_UI
from program import start_program

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    thr_1 = threading.Thread(target=start_UI, args=("UI",))
    thr_2 = threading.Thread(target=start_program, args=("program",))
    logging.info("Main    : before running thread")
    thr_1.start()
    thr_2.start()
    logging.info("Main    : wait for the thread to finish")
    thr_1.join()
    logging.info("Main    : all done")