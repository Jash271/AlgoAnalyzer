
import yfinance as yf

import numpy as np
import pandas as pd
import os
import multiprocessing
from datetime import date, timedelta
import datetime
import json

from ..chart import chart

def macd(Job, pid):
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

    l = 26
    s = 12
    l_label = f"EMA_12"
    s_label = f"EMA_26"
    df["macd"] = (
        df.Close.ewm(span=12, min_periods=1).mean()
        - df.Close.ewm(span=26, min_periods=1).mean()
    )
    df["signal"] = df.macd.ewm(span=9, min_periods=1).mean()
    df = df.iloc[adj_len:, :]

    dates_1 = [dates[0]]
    actions = [0]
    cash_on_hand = Job["Capital"]
    position = 0  # 1 denotes taking a long position
    long_positions = []
    square_offs = []
    summary = {}
    net_pl = 0

    dates = df.index.tolist()
    for i in range(1, len(df)):
        curr_signal = df.iloc[i]["signal"]
        curr_macd = df.iloc[i]["macd"]
        prev_signal = df.iloc[i - 1]["signal"]
        prev_macd = df.iloc[i - 1]["macd"]

        if (curr_macd > curr_signal) and (prev_signal > prev_macd) and (position == 0):
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

        elif "stop_Loss" in Job and position == 1:
            if df.iloc[i]["Close"] < long_positions[-1]["Buy_Price"] * (
                1 - (Job["stop_Loss"] / 100)
            ):
                # Generate Sell Signal
                actions.append(2)
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

        elif (curr_macd < curr_signal) and (prev_macd > prev_signal) and (position == 1):
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
    summary["Net_PL"] = net_pl
    summary["Buy_Signals"] = long_positions
    summary["Sell_Signals"] = square_offs
    summary["Job_ID"] = pid
    summary["Job_details"] = Job

    if len(long_positions) > len(square_offs):
        summary["Current_Investment"] = long_positions[-1]

    data = {}
    tick = Job["Ticker"]
    m=chart.generate_macd_chart(df, Job,pid)
    summary["Chart"] = m
    data[f"{pid}_{tick}_{category}"] = summary
    

    return data