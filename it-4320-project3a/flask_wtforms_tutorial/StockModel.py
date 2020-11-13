class StockModel:
    """ Model for converting the stock data json to usable object."""
    
    def __init__(self, data):
        self.open = float(data['1. open'])
        self.high = float(data['2. high'])
        self.low = float(data['3. low'])
        self.close = float(data['4. close'])
        self.volume = data['5. volume']
