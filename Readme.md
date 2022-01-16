# AlgoAnalyzer

### AlgoAnalyzer is a package for designing your trading strategies and run simulations to backtest your strategies and check their robustness

<br>

---

## User Guide
### Note for Indian Equtites append .NS to the end of the stock symbol
### **Eg: For YESBANK enter the Ticker name as YESBANK.NS**

### You can define multiple strategies and back test them simultaneously

### Submit your strategy as a list of dictionary following the below format

```
[
        {
            "Ticker": "YESBANK.NS", # This is the Symbol Name
            "Capital": 100000, # Define the capital you want to trade with 
            "Method": "EMA", # Define the technical indicator you want to use
            "Short_Term_Period": 20, # Define the short term period for the technical indicator
            "Long_Term_Period": 50, # Define the long term period for the technical indicator
            "look_back_period": "1y",  # Avalible Lookback periods are “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            "interval": "1d",
            "stop_loss": 5 # Define stoploss for damage control 
        }

]


```
---

### Understanding the Keys defined in the Dictionary

- ### Ticker: This is the Symbol Name
- ### Capital: Define the capital you want to trade with
- ### Method: Define the technical indicator you want to use (As of now the package supports these indicators)
    - ### `EMA`: Exponential Moving Average - Crossover Strategy
    - ### `SMA`: Simple Moving Average - Crossover Strategy
    - ### `MACD`: Moving Average Convergence Divergence - Crossover Strategy
- ### Short_Term_Period: Define the short term period for the technical indicator(for CrossOver Strategy)
- ### Long_Term_Period: Define the long term period for the technical indicator(for CrossOver Strategy)
- ### look_back_period: The time period for which you want to backtest your strategy
    - ### Avalible Lookback periods are “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
- ### interval: Define the data interval for the technical indicator (It is generally advised to use 1d interval unless you to setup an Intraday strategy)
    - ### Avalible Intervals are “1m”, “5m”, “15m”, “30m”, “1h”, “4h”, “1d”, “1wk”, “1mo” 
- ### stop_loss: Define stoploss for damage control to override you strategy . **This is denoted as % so keep the stop_loss value between 0 and 100** 

---

### Once you have defined your strategy, you can run the simulation by passing initialzing the runner class and then invoking the get_res() method.

### Charts will be generated for each strategy and the charts will be saved as interactive html files in the same directory as the python file.

### Final Results will be saved in a {timestamp}_results.json file in the same directory as the python file.
---

## Sample code to demonstrate the whole process

```
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


```
**It is important to have this code snippet in your file since multiprocessing module is used internally and not having this could possibly lead to errors**
```
if __name__ == "__main__":
```
---
###  Output as obtained in the {timestamp}_results.json file
```
{
    "summary": [
        {
            "10020_YESBANK.NS_EMA": {
                "Net_PL": -3487.9485216140747,
                "Buy_Signals": [
                    {
                        "Shares": 7751,
                        "Date": "2021-09-27T00:00:00",
                        "Investment_Value": 99987.89704322815,
                        "Action": "Buy",
                        "Buy_Price": 12.899999618530273
                    },
                    {
                        "Shares": 6893,
                        "Date": "2021-12-09T00:00:00",
                        "Investment_Value": 96502.0,
                        "Action": "Buy",
                        "Buy_Price": 14.0
                    }
                ],
                "Sell_Signals": [
                    {
                        "Shares": 7751,
                        "Date": "2021-11-26T00:00:00",
                        "Investment_Value": 96499.94852161407,
                        "Action": "Sell",
                        "Sell_Price": 12.449999809265137,
                        "Net_PL": -3487.9485216140747
                    }
                ],
                "Job_ID": 10020,
                "Job_details": {
                    "Ticker": "YESBANK.NS",
                    "Capital": 100000,
                    "Method": "EMA",
                    "Short_Term_Period": 20,
                    "Long_Term_Period": 50,
                    "look_back_period": "1y",
                    "interval": "1d"
                },
                "Current_Investment": {
                    "Shares": 6893,
                    "Date": "2021-12-09T00:00:00",
                    "Investment_Value": 96502.0,
                    "Action": "Buy",
                    "Buy_Price": 14.0
                },
                "Chart": [
                    "YESBANK_50_20_EMA_10020_2022-01-14T17_50_02_377762.html"
                ]
            }
        },
        {
            "22996_ZEEMEDIA.NS_SMA": {
                "Net_PL": 41241.543095588684,
                "Buy_Signals": [
                    {
                        "Shares": 11049,
                        "Date": "2021-09-02T00:00:00",
                        "Investment_Value": 99993.4521074295,
                        "Action": "Buy",
                        "Buy_Price": 9.050000190734863
                    },
                    {
                        "Shares": 11597,
                        "Date": "2021-11-11T00:00:00",
                        "Investment_Value": 151920.70442390442,
                        "Action": "Buy",
                        "Buy_Price": 13.100000381469727
                    },
                    {
                        "Shares": 10619,
                        "Date": "2021-12-07T00:00:00",
                        "Investment_Value": 132206.5479745865,
                        "Action": "Buy",
                        "Buy_Price": 12.449999809265137
                    }
                ],
                "Sell_Signals": [
                    {
                        "Shares": 11049,
                        "Date": "2021-10-12T00:00:00",
                        "Investment_Value": 151923.75,
                        "Action": "Sell",
                        "Sell_Price": 13.75,
                        "Net_PL": 51930.297892570496
                    },
                    {
                        "Shares": 11597,
                        "Date": "2021-11-22T00:00:00",
                        "Investment_Value": 132205.79557609558,
                        "Action": "Sell",
                        "Sell_Price": 11.399999618530273,
                        "Net_PL": -19714.908847808838
                    },
                    {
                        "Shares": 10619,
                        "Date": "2021-12-22T00:00:00",
                        "Investment_Value": 141232.7020254135,
                        "Action": "Sell",
                        "Sell_Price": 13.300000190734863,
                        "Net_PL": 9026.154050827026
                    }
                ],
                "Job_ID": 22996,
                "Job_details": {
                    "Ticker": "ZEEMEDIA.NS",
                    "Capital": 100000,
                    "Method": "SMA",
                    "Short_Term_Period": 5,
                    "Long_Term_Period": 10,
                    "look_back_period": "6mo",
                    "interval": "1d"
                },
                "Chart": [
                    "ZEEMEDIA_10_5_SMA_22996_2022-01-14T17_50_01_931633.html"
                ]
            }
        },
        {
            "21828_ZOMATO.NS_MACD": {
                "Net_PL": -16501.861557006836,
                "Buy_Signals": [
                    {
                        "Shares": 706,
                        "Date": "2021-07-29T00:00:00",
                        "Investment_Value": 99934.30215454102,
                        "Action": "Buy",
                        "Buy_Price": 141.5500030517578
                    },
                    {
                        "Shares": 694,
                        "Date": "2021-08-13T00:00:00",
                        "Investment_Value": 95320.90423583984,
                        "Action": "Buy",
                        "Buy_Price": 137.35000610351562
                    },
                    {
                        "Shares": 681,
                        "Date": "2021-08-18T00:00:00",
                        "Investment_Value": 91900.94792175293,
                        "Action": "Buy",
                        "Buy_Price": 134.9499969482422
                    },
                    {
                        "Shares": 644,
                        "Date": "2021-08-31T00:00:00",
                        "Investment_Value": 86650.20196533203,
                        "Action": "Buy",
                        "Buy_Price": 134.5500030517578
                    },
                    {
                        "Shares": 600,
                        "Date": "2021-10-18T00:00:00",
                        "Investment_Value": 86430.00183105469,
                        "Action": "Buy",
                        "Buy_Price": 144.0500030517578
                    },
                    {
                        "Shares": 586,
                        "Date": "2021-11-10T00:00:00",
                        "Investment_Value": 79725.30178833008,
                        "Action": "Buy",
                        "Buy_Price": 136.0500030517578
                    },
                    {
                        "Shares": 645,
                        "Date": "2021-12-31T00:00:00",
                        "Investment_Value": 88622.99606323242,
                        "Action": "Buy",
                        "Buy_Price": 137.39999389648438
                    },
                    {
                        "Shares": 627,
                        "Date": "2022-01-13T00:00:00",
                        "Investment_Value": 83453.7038269043,
                        "Action": "Buy",
                        "Buy_Price": 133.10000610351562
                    }
                ],
                "Sell_Signals": [
                    {
                        "Shares": 706,
                        "Date": "2021-08-05T00:00:00",
                        "Investment_Value": 95274.69784545898,
                        "Action": "Sell",
                        "Sell_Price": 134.9499969482422,
                        "Net_PL": -4659.604309082031
                    },
                    {
                        "Shares": 694,
                        "Date": "2021-08-17T00:00:00",
                        "Investment_Value": 91955.0,
                        "Action": "Sell",
                        "Sell_Price": 132.5,
                        "Net_PL": -3365.9042358398438
                    },
                    {
                        "Shares": 681,
                        "Date": "2021-08-23T00:00:00",
                        "Investment_Value": 86657.25,
                        "Action": "Sell",
                        "Sell_Price": 127.25,
                        "Net_PL": -5243.69792175293
                    },
                    {
                        "Shares": 644,
                        "Date": "2021-09-20T00:00:00",
                        "Investment_Value": 86489.20196533203,
                        "Action": "Sell",
                        "Sell_Price": 134.3000030517578,
                        "Net_PL": -161.0
                    },
                    {
                        "Shares": 600,
                        "Date": "2021-10-25T00:00:00",
                        "Investment_Value": 79619.99816894531,
                        "Action": "Sell",
                        "Sell_Price": 132.6999969482422,
                        "Net_PL": -6810.003662109375
                    },
                    {
                        "Shares": 586,
                        "Date": "2021-12-01T00:00:00",
                        "Investment_Value": 88720.39642333984,
                        "Action": "Sell",
                        "Sell_Price": 151.39999389648438,
                        "Net_PL": 8995.094635009766
                    },
                    {
                        "Shares": 645,
                        "Date": "2022-01-07T00:00:00",
                        "Investment_Value": 83366.25,
                        "Action": "Sell",
                        "Sell_Price": 129.25,
                        "Net_PL": -5256.746063232422
                    }
                ],
                "Job_ID": 21828,
                "Job_details": {
                    "Ticker": "ZOMATO.NS",
                    "Capital": 100000,
                    "Method": "MACD",
                    "look_back_period": "1y",
                    "interval": "1d"
                },
                "Current_Investment": {
                    "Shares": 627,
                    "Date": "2022-01-13T00:00:00",
                    "Investment_Value": 83453.7038269043,
                    "Action": "Buy",
                    "Buy_Price": 133.10000610351562
                },
                "Chart": [
                    "ZOMATO.NS_macd_signal_21828_2022-01-14T17_50_02_041010.html",
                    "ZOMATO_candle_21828_2022-01-14T17_50_02_349608.html"
                ]
            }
        }
    ]
}
```
---
### Analyzing the Output

- ### The `Net_PL` is the total profit/loss of the strategy.
- ### The `Buy_Signals` is a list of all the buy signals.
    - ### Each Buy_Signal has the following fields:
        - ### Shares: The number of shares bought.
        - ### Date: The date of transaction.
        - ### Investment_Value: The value of the investment.
        - ### Action: Buy.
        - ### Buy_Price`: The price at which the shares are bought.
- ### The `Sell_Signals` is a list of all the sell signals.
    - ### Each Sell_Signal has the following fields:
        - ### Shares: The number of shares sold.
        - ### Date: The date of transaction.
        - ### Investment_Value: The value of the investment.
        - ### Action: Sell.
        - ### Sell_Price: The price at which the shares are sold.
        - ### Net_PL: The profit/loss of the transaction.

- ### The `Current_Investment` is the investment that is currently being held.
    
- ### The `Chart` is a list of files, which is file name of charts generated for your strategy