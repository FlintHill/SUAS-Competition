from interop import Client
import multiprocessing

# The following settings are for our test interoperability server
MSL_ALT = 22
URL = "http://10.10.130.2:8000"
USERNAME = "Flint"
PASSWORD = "271824758"

def crash_interop_client():
    test_client = Client(22, URL, USERNAME, PASSWORD)

    print("This code is never reached")

if __name__ == '__main__':
    # Run the following two lines to crash an interop client
    test_process = multiprocessing.Process(target=crash_interop_client)
    test_process.start()

    # Run the following lines to successfully create an interop client
    #test_client = Client(22, URL, USERNAME, PASSWORD)
    #print("This code is always reached")
