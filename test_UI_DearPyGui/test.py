from queue import Queue
import logging
import threading

from UI import start_UI
from program import start_program
from program import calc
import pyqt
from pyqt import start_pyqt

# pyuic5 xyz.ui > xyz.py 


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")

    q = Queue()

    print("генерация данных")
    q.put("генерация данных")
    thr_1 = threading.Thread(target=start_program, args=("program", q))
    thr_1.start()
    q.join()
    print("данные готовы")

    print("инициализация UI")
    q.put("инициализация UI")
    thr_2 = threading.Thread(target=start_pyqt, args=("pyqt", q))
    thr_2.start()
    q.join()
    print("UI загружен")

    print("запускаем итератор")
    q.put("запускаем итератор")
    thr_1 = threading.Thread(target=calc, args=("calc", q, ))
    thr_1.start()
    q.join()
    print("программа выполнена")

    
    # thr_1 = threading.Thread(target=start_UI, args=("UI",))
    
    # thr_3 = threading.Thread(target=start_pyqt, args=("pyqt",))

    # thr_1.start()
    
    
    # thr_3.start()
    # logging.info("thr_3 start")
    # print (bool(thr_3.even.isSet))
    
    # while not even:
    #     even.wait(1)
    
    # print (even.isSet)




    # thr_2 = threading.Thread(target=start_program, args=("program",))
    # thr_2.start()
    # logging.info("thr_2 start")
