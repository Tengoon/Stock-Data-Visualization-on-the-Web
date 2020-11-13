'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests as rq
from datetime import datetime
from datetime import date
import pygal
from .StockModel import StockModel


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def queryStockData(symbol,chart_type,time_series,start_date,end_date):
        """ Given a set of inputs performs a stock query """
        API_URL = "https://www.alphavantage.co/query"
        API_KEY = "SPFP6JN8KMDZ9IPM"
        
        series = time_series
        # If statements to change key depending on the Time Serires selected.
        if series == "2":
            timeSeries = "Time Series (Daily)"
            function = "TIME_SERIES_DAILY"
        elif series == "3":
            timeSeries = "Weekly Time Series"
            function = "TIME_SERIES_WEEKLY"
        elif series == "4":
            timeSeries = "Monthly Time Series"
            function= "TIME_SERIES_MONTHLY"
        else:
            timeSeries = "Time Series (5min)"
            function = "TIME_SERIES_INTRADAY"
            
        data = {
            "function": function,
            "symbol": symbol,
            "outputsize":"full",
            "interval":"5min",
            "apikey":API_KEY
            }

        #Sending our request to the API using the information we put in the data collection.
        apiCall = rq.get(API_URL, params=data)

        #Stores the json-enconded content in the retrieved data.
        response = apiCall.json()
        
        
        
        dates = []
        opens = []
        highs = []
        lows = []
        closes = []

        #Parsing the dates from the user input
        startDate = start_date
        endDate = end_date
        
        for date, stockData in response[timeSeries].items():
            #Parsing the date from the api record.
            entryDate = convert_date(date)

            #Populating lists with data, within the given date range, from API
            if (entryDate >= startDate and entryDate <= endDate):
                model = StockModel(stockData)
                opens.append(model.open)
                highs.append(model.high)
                lows.append(model.low)
                closes.append(model.close)
                dates.append(date)

        #If true, prints line chart. Else prints the bar chart.
        if chart_type == "2":
            chart = pygal.Line(x_label_rotation=45)
            chart.x_labels = dates
            chart.title = "Stock Date for " + symbol + ": " + start_date.strftime("%m/%d/%Y") + " to " + end_date.strftime("%m/%d/%Y")
            chart.add("Open",opens)
            chart.add("High",highs)
            chart.add("Low", lows)
            chart.add("Close",closes)
            #chart.render_in_browser()
            chart_data = chart.render_data_uri()
            return chart_data
        else:
            chart = pygal.Bar(x_label_rotation=45)
            chart.title = "Stock Date for " + symbol + ": " + start_date.strftime("%m/%d/%Y") + " to " + end_date.strftime("%m/%d/%Y")
            chart.x_labels = dates
            chart.add("Open",opens)
            chart.add("High",highs)
            chart.add("Low", lows)
            chart.add("Close",closes)
            chart_data = chart.render_data_uri()
            return chart_data
