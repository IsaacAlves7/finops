import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt

def get_stock_data(stock_name):
    stock_data = get_history(symbol= stock_name, start=date(2015,1,1), end=date(2021,9,27))
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Day'] = stock_data['Date'].dt.day
    stock_data['Year'] = stock_data['Date'].dt.year
    return stock_data

def reduce_columns(stock_data):
    return stock_data[['Date', 'Symbol', 'Close', 'VWAP', 'Volume', 'Turnover', '%Deliverble', 'Year', 'Month', 'Day']]

def get_yearly_data(stock_data, year):
    return stock_data[stock_data['Year'] == year]

def get_corr_months(yearly_data):
    return yearly_data[['Close','Volume','Turnover','%Deliverble', 'Month']].groupby(['Month']).corr()

def get_corr_plot(corr_data, yearly_data):
    corr_data = corr_data.reset_index()
    corr_data = corr_data[corr_data['level_1'] != 'Close'] #eliminating the rows with close values
    corr_data = corr_data[['Month', 'level_1', 'Close']]
    corr_data = corr_data.groupby('level_1')['Close'].apply(list)
    corr_data = corr_data.apply(pd.Series).T
    plt.subplot(1,2,1)
    plt.plot(corr_data)
    plt.legend(["%Deliverable", "Turnover", "Volume"], loc ="lower right")
    
    plt.subplot(1,2,2)
    plt.plot(yearly_data.Date, yearly_data.Close)
    plt.show()
    

if __name__ == "__main__":
    data = get_stock_data('RELIANCE')
    reduced_column_data = reduce_columns(data)
    yearly_data = get_yearly_data(reduced_column_data, 2020)
    corelation_table = get_corr_months(yearly_data)
    get_corr_plot(corelation_table, yearly_data)    
