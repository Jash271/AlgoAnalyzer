import yfinance as yf
import numpy as np
import pandas as pd
import os
import multiprocessing
from datetime import date, timedelta
import datetime
import json


from .technicals.ema_crossover import moving_average_ema as e
from .technicals.sma_crossover import moving_average_sma as s
from .technicals.macd import macd as m

class Analyzer:
    def __init__(self, Jobs):

        self.Jobs = Jobs
        

    def get_res(self):
        r = self.master(self.Jobs)
        return r

    def gateway(self, Job):
        pid = os.getpid()
        print(pid, datetime.datetime.now())
        method = Job["Method"]
        if method == "EMA":

            k = e(Job, pid)
            return k
        elif method == "SMA":
            k = s(Job, pid)
            return k
        elif method == "MACD":
            k = m(Job, pid)
            return k



    def master(self, Jobs):
        p = multiprocessing.Pool(os.cpu_count())
        result = p.map(self.gateway, Jobs)
        d = {}
        d["summary"] = result
        res = self.formatter_json(d)
        date = datetime.datetime.now().isoformat()
        date = date.replace(":","_")
        date = date.replace(".","_")
        outfile = open(f"{date}_results.json", "w")
        json.dump(d, outfile, indent=4)
        return res

    def formatter_json(self, x):
        ticks = []
        result = {}
        
        for d in x["summary"]:
            # get key value of x
            

            for k, v in d.items():
                tick = k.split("_")[1]

                Job_Id = k.split("_")[0]
                if tick not in ticks:
                    ticks.append(tick)
                    result[tick] = [v]
                else:
                    result[tick].append(v)
        return result
