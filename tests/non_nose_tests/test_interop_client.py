#from multiprocessing import Manager
from time import sleep
from SUASSystem import InteropClientConverter

if __name__ == '__main__':
    #interop_status = Manager.Value('b', "disconnected")

    interop_client = InteropClientConverter(interop_status)

    while True:
        # get_obstacles()
        print(interop_client.get_obstacles())

        sleep(1)
