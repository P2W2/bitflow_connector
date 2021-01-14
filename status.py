import threading
import pandas as pd


def init():
    global clients
    clients = {}
    global df
    df = pd.DataFrame()
    global data_lock
    data_lock = threading.Lock()
