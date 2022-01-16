import yfinance as yf

import numpy as np
import pandas as pd
import os
import multiprocessing
from datetime import date, timedelta
import datetime
import json
from ..chart import chart



def moving_average_ema(Job, pid):
    try:
        category = Job["Method"]
        tc = yf.Ticker(Job["Ticker"])
        df = tc.history(period=Job["look_back_period"])
        dates = df.index.tolist()
        ref_len = len(dates)
        ref_date = dates[0]

        corr_date = ref_date - timedelta(days=5000)
        df = tc.history(start=corr_date)
        corr_len = len(df.index.tolist())

        adj_len = corr_len - ref_len

        l = Job["Long_Term_Period"]
        s = Job["Short_Term_Period"]
        l_label = f"EMA_{l}"
        s_label = f"EMA_{s}"

        df[l_label] = df.Close.ewm(span=Job["Long_Term_Period"], min_periods=1).mean()
        df[s_label] = df.Close.ewm(span=Job["Short_Term_Period"], min_periods=1).mean()

        df = df.iloc[adj_len:, :]
        # Take Position on the Start Day 

        # Caculate NetPl
        dates_1 = [dates[0]]
        actions = [0]
        cash_on_hand = Job["Capital"]
        position = 0  # 1 denotes taking a long position
        long_positions = []
        square_offs = []
        summary = {}
        net_pl = 0
        

        for i in range(1, len(df)):
            curr_long = df.iloc[i][l_label]
            curr_short = df.iloc[i][s_label]
            prev_long = df.iloc[i - 1][l_label]
            prev_short = df.iloc[i - 1][s_label]

            if (
                (curr_short > curr_long)
                and (prev_short < prev_long)
                and (position == 0)
            ):
                # Generate Buy Signal
                actions.append(1)
                shares = int(cash_on_hand / df.iloc[i]["Close"])
                investment_value = shares * df.iloc[i]["Close"]
                cash_on_hand -= investment_value
                date = dates[i]
                d = {}
                d["Shares"] = shares
                d["Date"] = date.isoformat()
                d["Investment_Value"] = investment_value
                d["Action"] = "Buy"
                d["Buy_Price"] = df.iloc[i]["Close"]
                long_positions.append(d)
                position = 1

            # check if stop_Loss key exists in Job
            elif "stop_Loss" in Job and position == 1:
                actions.append(2)
                flag = long_positions[-1]["Buy_Price"] * (1 - (Job["stop_Loss"] * 0.01))
                print(flag, long_positions[-1]["Buy_Price"])
                if df.iloc[i]["Close"] < flag:
                    print("Stop Loss Triggered",Job["Ticker"])
                    # Generate Sell Signal
                    prev_position = long_positions[-1]
                    new_value = df.iloc[i]["Close"] * prev_position["Shares"]
                    cash_on_hand += new_value
                    shares = long_positions[-1]["Shares"]
                    investment_value = shares * df.iloc[i]["Close"]
                    cash_on_hand += investment_value
                    date = dates[i].isoformat()
                    d = {}
                    d["Shares"] = prev_position["Shares"]
                    d["Date"] = dates[i].isoformat()
                    d["Investment_Value"] = new_value
                    d["Action"] = "Sell"
                    d["Sell_Price"] = df.iloc[i]["Close"]
                    d["Type"] = "Stop Loss"
                    netpl = new_value - prev_position["Investment_Value"]
                    net_pl += netpl
                    d["Net_PL"] = netpl

                    square_offs.append(d)
                    position = 0

            elif (
                (curr_short < curr_long)
                and (prev_short > prev_long)
                and (position == 1)
            ):

                # Square of the Position
                actions.append(-1)
                prev_position = long_positions[-1]
                new_value = df.iloc[i]["Close"] * prev_position["Shares"]
                cash_on_hand += new_value
                d = {}
                d["Shares"] = prev_position["Shares"]
                d["Date"] = dates[i].isoformat()
                d["Investment_Value"] = new_value
                d["Action"] = "Sell"
                d["Sell_Price"] = df.iloc[i]["Close"]
                netpl = new_value - prev_position["Investment_Value"]
                net_pl += netpl
                d["Net_PL"] = netpl

                square_offs.append(d)
                position = 0
            else:
                actions.append(0)

        df["Signal"] = actions  
        summary["Cash_on_Hand"] = cash_on_hand
        summary["Net_PL"] = net_pl
        summary["Buy_Signals"] = long_positions
        summary["Sell_Signals"] = square_offs
        summary["Job_ID"] = pid
        summary["Job_details"] = Job

        if len(long_positions) > len(square_offs):
            summary["Current_Investment"] = long_positions[-1]

        data = {}
        tick = Job["Ticker"]
        
        m=chart.generate_and_save_chart(df,Job,pid)
        summary["Chart"] = m
        data[f"{pid}_{tick}_{category}"] = summary
        
        return data
    except (Exception) as e:
        print(e)
