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

LARGE_FONT = ("Robot", 18)

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


class InteropClient(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Interoperability Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (LoadPage,):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nesw")

        self.show_frame(LoadPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.server = None
        self.client_running = False
        self.server_thread = threading.Thread(target=self.create_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        label = tk.Label(self, text="""ALPHA Bitcoin trading application
        use at your own risk there is no promise
        of warranty.""", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        button = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_page))
        button.pack()

        button = ttk.Button(self, text="Disagree", command=quit)
        button.pack()

    def create_server(self):
        """
        Connect the client to the interoperability server
        """
        while not self.client_running:
            try:
                print("[*] Attempting to connect to interoperability server...")

                sleep(0.1)

                self.relay = RelayService(url="URL",
                                     username="USERNAME",
                                     password="PASSWORD")
                self.server = SimpleXMLRPCServer(
                    ('127.0.0.1', 9000),
                    logRequests=True,
                    allow_none=True)
                self.server.register_instance(self.relay)
                self.server.serve_forever()

                self.client_running = True
            except:
                self.client_running = False
                self.server = None

                sleep(0.1)


if __name__ == '__main__':
    try:
        print('Use Control-C to exit')
        InteropClient().mainloop()
    except KeyboardInterrupt:
        print('Exiting')
