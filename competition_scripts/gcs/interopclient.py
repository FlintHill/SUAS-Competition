from __future__ import print_function
from interop import AsyncClient
from interop import Telemetry
from time import time
from time import sleep
import argparse
from xmlrpc.server import SimpleXMLRPCServer

import tkinter as tk
from tkinter import ttk as ttk
import threading

__author__ = 'Vale Tolpegin'

class RelayService:
    def __init__(self, url, username, password):
        self.client = AsyncClient(url=url,
                                  username=username,
                                  password=password)
        self.last_telemetry = time()

    def post_telemetry(self, lat, lon, alt, heading):
        """
        POST telemetry to interoperability server.
        """
        t = Telemetry(latitude=lat,
                      longitude=lon,
                      altitude_msl=alt,
                      uas_heading=heading)
        self.client.post_telemetry(t)

        new_time = time()
        print(1 / (new_time - self.last_telemetry))
        self.last_telemetry = new_time

        return True

    def get_server_info(self):
        """
        GET server information.
        """
        info = self.client.get_server_info().result()
        return str(info.message)


class Main(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self)

        self.title('Interoperability Client')

        self.server = None
        self.kwargs = kwargs
        self.initialize()

    def initialize(self):
        self.grid()

        self.lbl_ip_address = ttk.Label(self, anchor=tk.E, text=' Input: ')
        self.lbl_ip_address.grid(column=0, row=0, sticky='w')

        #self.input_text = ScrolledText.ScrolledText(self, state='normal')
        #self.input_text.grid(column=0, row=1, columnspan=2, sticky='nesw', padx=3, pady=3)
        #self.input_text.insert(tk.END, "Enter text to parse")

        self.lbl_ip_address = ttk.Label(self, anchor=tk.E, text=' Output: ')
        self.lbl_ip_address.grid(column=0, row=2, sticky='w')

        #self.output_text = ScrolledText.ScrolledText(self, state='disabled')
        #self.output_text.grid(column=0, row=3, columnspan=2, sticky='nesw', padx=3, pady=3)

        #self.btn_convert = ttk.Button(self, text='Exit', command=self.handle_close)
        #self.btn_convert.grid(column=0, row=3, columnspan=2, sticky='s', pady=15)

        self.resizable(True, True)
        self.minsize(300, 300)

        self.protocol("WM_DELETE_WINDOW", self.handle_close)

        self.server_thread = threading.Thread(target=self.create_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def handle_close(self):
        exit(0)

    def create_server(self):
        """
        Connect the client to the interoperability server
        """
        client_running = False
        while not client_running:
            try:
                print("[*] Attempting to connect to interoperability server...")

                sleep(0.1)

                self.relay = RelayService(url=self.kwargs.get("cmd_args").url,
                                     username=self.kwargs.get("cmd_args").username,
                                     password=self.kwargs.get("cmd_args").password)
                self.server = SimpleXMLRPCServer(
                    ('127.0.0.1', 9000),
                    logRequests=True,
                    allow_none=True)
                self.server.register_instance(self.relay)
                self.server.serve_forever()

                client_running = True
            except:
                self.server = None

                sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AUVSI SUAS Server Interface Relay')
    parser.add_argument(
        '--url',
        dest='url',
        help='Interoperability Server URL, example: http://10.10.130.10:80',
        required=True)
    parser.add_argument(
        '--username',
        dest='username',
        help='Interoperability Username, example: calpoly-broncos',
        required=True)
    parser.add_argument('--password',
                        dest='password',
                        help='Interoperability Password, example: 4597630144',
                        required=True)

    cmd_args = parser.parse_args()

    try:
        print('Use Control-C to exit')
        Main(cmd_args=cmd_args).mainloop()
        #server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
