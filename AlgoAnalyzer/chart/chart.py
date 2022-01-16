import plotly.graph_objects as go
import plotly
import datetime
import os



def generate_and_save_chart(df, Job,pid):
    # PLot candlestick data on the graph with lines of moving average and highlight points of intersection
    # filter df where signal==1
    buys = df[df["Signal"] == 1]
    sells = df[df["Signal"] == -1]
    sl = df[df["Signal"] == 2]
    
    
    method = Job["Method"]
    name = Job["Ticker"]
    l = Job["Long_Term_Period"]
    s = Job["Short_Term_Period"]
    stp = f"{method}_{s}"
    ltp = f"{method}_{l}"
    trace1 = {
        "x": df.index,
        "open": df.Open,
        "close": df.Close,
        "high": df.High,
        "low": df.Low,
        "type": "candlestick",
        "name": Job["Ticker"].split(".")[0],
        "showlegend": True,
    }
    trace2 = {
        "x": df.index,
        "y": df[ltp],
        "type": "scatter",
        "mode": "lines",
        "line": {"width": 1, "color": "black"},
        "name": f"Moving average_{l}",
        "showlegend": True,
    }
    trace3 = {
        "x": df.index,
        "y": df[stp],
        "type": "scatter",
        "mode": "lines",
        "line": {"width": 1, "color": "red"},
        "name": f"Moving average_{s}",
        "showlegend": True,
    }

    data = [trace1, trace2, trace3]
    
    name = Job["Ticker"].split(".")[0]
    layout = go.Layout({"title": {"text": f'{name}', "font": {"size": 15}}})
    fig = go.Figure(data=data, layout=layout)

    
    # set width as 100 and height as 100 in write_html method

    

    # save fig as svg file
    # Done
    date = datetime.datetime.now().isoformat()
    # replace . with _ in date string
    name = name.split(".")[0]
    date=date.replace(".","_")
    date=date.replace(":","_")
    k = f"{name}_{l}_{s}_{method}_{pid}_{date}.html"
    
    k=k.replace(":","_")
    fig.write_html(f"{k}")
    return [k]
    
    
    
def generate_macd_chart(df,Job,pid):
    # Plot candle stick chart from df
    name = Job["Ticker"]
    
    
    """trace1 = {
        "x": df.index,
        "open": df.Open,
        "close": df.Close,
        "high": df.High,
        "low": df.Low,
        "type": "candlestick",
        "name": Job["Ticker"],
        "showlegend": True,
        
    }"""

    trace2 = {
        "x": df.index,
        "y": df["macd"],
        "type": "scatter",
        "mode": "lines",
        "line": {"width": 1, "color": "red"},
        "name": f"MACD Line",
        "showlegend": True,
        


    }
    trace3 = {
        "x": df.index,
        "y": df["signal"],
        "type": "scatter",
        "mode": "lines",
        "line": {"width": 1, "color": "black"},
        "name": f"Signal Line",
        "showlegend": True,
        
    }
    
    

    
    data = [trace2, trace3]
    name = Job["Ticker"].split(".")[0]

    layout = go.Layout({"title": {"text": f'{name}', "font": {"size": 15}}})
    fig = go.Figure(data=data, layout=layout)
    date = datetime.datetime.now().isoformat()
    date=date.replace(".","_")
    date=date.replace(":","_")
    
    s = f"{name}_macd_signal_{pid}_{date}.html"
    s=s.replace(":","_")
    
    fig.write_html(s)
    
    
    


    trace1 = {
        "x": df.index,
        "open": df.Open,
        "close": df.Close,
        "high": df.High,
        "low": df.Low,
        "type": "candlestick",
        "name": Job["Ticker"].split(".")[0],
        "showlegend": True,
        
    }
    

    data = [trace1]
    name = Job["Ticker"].split(".")[0]
    layout = go.Layout({"title": {"text": f'{name}', "font": {"size": 15}}})
    fig = go.Figure(data=data, layout=layout)
    date = datetime.datetime.now().isoformat()
    name = name.split(".")[0]
    date=date.replace(".","_")
    date=date.replace(":","_")
    k= f"{name}_candle_{pid}_{date}.html"
    
    
    fig.write_html(k)
    return [s,k]
    
    

