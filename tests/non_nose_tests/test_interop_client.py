#from multiprocessing import Manager
from time import sleep
from SUASSystem import InteropClientConverter

if __name__ == '__main__':
    interop_client = InteropClientConverter()

    while True:
        print(interop_client.get_obstacles())

        sleep(1)
