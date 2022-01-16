from AlgoAnalyzer import Analyzer  as a

if __name__ == "__main__":

    Jobs = [
        {
            "Ticker": "YESBANK.NS",
            "Capital": 100000,
            "Method": "EMA",
            "Short_Term_Period": 20,
            "Long_Term_Period": 50,
            # Avalible Lookback periods are “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            "look_back_period": "1y",
            "interval": "1d",
            # "stop_loss": 5
        },
        
        {
            "Ticker": "ZEEMEDIA.NS",
            "Capital": 100000,
            "Method": "SMA",
            "Short_Term_Period": 5,
            "Long_Term_Period": 10,
            # Avalible Lookback periods are “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            "look_back_period": "6mo",
            "interval": "1d",
            # "stop_loss": 5
        },
        {
            "Ticker": "ZOMATO.NS",
            "Capital": 100000,
            "Method": "MACD",
            # Avalible Lookback periods are “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            "look_back_period": "1y",
            "interval": "1d",
        },
    ]

    a.Analyzer(Jobs).get_res()

