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
import logging
import subprocess
import io
import multiprocessing

__author__ = 'Vale Tolpegin'

LARGE_FONT = ("Robot", 36)
MEDIUM_FONT = ("Robot", 24)
SMALL_FONT = ("Robot", 18)

log_capture = io.StringIO()

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

        container = ttk.Frame(self, padding="5 5 5 5")
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

        self.parent = parent

        # Creating server time display
        timelbl = ttk.Label(self, text="--:--", font=LARGE_FONT)

        # Creating authentication fields
        urllbl = ttk.Label(self, text="URL", font=SMALL_FONT)
        usernamelbl = ttk.Label(self, text="USR", font=SMALL_FONT)
        passwordlbl = ttk.Label(self, text="PWD", font=("Robot", 17))

        self.url = ttk.Entry(self)
        self.username = ttk.Entry(self)
        self.password = ttk.Entry(self)

        # Creating off axis target field
        self.off_axis_dfttxt = "Off-Axis Target: -----------------"
        self.off_axis_targetlbl = ttk.Label(self, text=self.off_axis_dfttxt, font=SMALL_FONT)

        # Creating telemetry upload rate info field
        self.telemetry_dfttxt = "Telemetry Upload Rate (Hz): -----"
        self.telemetrylbl = ttk.Label(self, text=self.telemetry_dfttxt, font=SMALL_FONT)

        # Placing everything on frame
        timelbl.place(relx=0.5, y=20, anchor="center")
        urllbl.place(x=20, rely=0.15, anchor="n")
        self.url.place(relx=0.28, rely=0.15, anchor="n")
        usernamelbl.place(x=20, rely=0.2, anchor="n")
        self.username.place(relx=0.28, rely=0.2, anchor="n")
        passwordlbl.place(x=20, rely=0.25, anchor="n")
        self.password.place(relx=0.28, rely=0.25, anchor="n")
        self.off_axis_targetlbl.place(x=138, rely=0.35, anchor="n")
        self.telemetrylbl.place(x=138, rely=0.40, anchor="n")

        self.server = None
        self.client_running = False
        self.initialize()

        self.update()

    def update(self):
        global log_capture

        log = log_capture.getvalue()
        if log != "":
            print(log.replace("\n", ""))
            log_capture.seek(0)
            log_capture.truncate()

        self.parent.after(1000, self.update)

    def initialize(self):
        if self.client_running:
            self.server.server_close()

        self.server = None
        self.client_running = False
        self.server_thread = threading.Thread(target=self.create_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def create_server(self):
        """
        Connect the client to the interoperability server
        """
        url = str(self.url.get())
        username = str(self.username.get())
        password = str(self.password.get())

        msg_base = "Attempting to connect to interop server"
        msg = msg_base + " at \"" + url + "\" with the username \"" + username + "\" and the password \"" + password + "\""
        logging.debug(msg)
        subprocess.Popen(['espeak', '-s150', '-ven+f1', msg_base], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()

        if url != "" and username != "" and password != "":
            try:
                self.relay = RelayService(url=url,
                                    username=username,
                                    password=password)
                self.server = SimpleXMLRPCServer(
                    ('127.0.0.1', 9000),
                    logRequests=True,
                    allow_none=True)
                self.server.register_instance(self.relay)
                self.client_running = True
                self.server.serve_forever()
            except:
                self.client_running = False
                self.server = None

                self.parent.after(1000, self.initialize)
        else:
            self.parent.after(1000, self.initialize)


if __name__ == '__main__':
    logging.basicConfig(stream=log_capture, format='[%(asctime)s %(threadName)s]  %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    try:
        print('Use Control-C to exit')
        client = InteropClient()
        client.minsize(500, 500)
        client.resizable(width=False, height=False)
        client.mainloop()
    except KeyboardInterrupt:
        print('Exiting')
