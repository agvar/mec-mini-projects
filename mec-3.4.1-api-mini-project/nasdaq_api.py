import os
import requests
import json
from dotenv import load_dotenv
def nasdaq_api(params):
    response=requests.get(base_url,params=params)
    data=json.loads(response.content)
    column_names=data['dataset_data']['column_names']
    data=data['dataset_data']['data']
    open_prices=[]
    day_diff=[]
    closing_price=[]
    traded_volume=[]

    for i in range(len(column_names)):
        if column_names[i] == 'Open':
            idx_open = i
        if column_names[i] == 'Close':
            idx_close = i
        if column_names[i] == 'Traded Volume':
            idx_tradedv = i
        if column_names[i] == 'High':
            idx_high = i
        if column_names[i] == 'Low':
            idx_low = i

    for data_row in data:
        if data_row[idx_open]:
            open_prices.append(data_row[idx_open])
        if data_row[idx_high]-data_row[idx_low]:
            day_diff.append(data_row[idx_high]-data_row[idx_low])
        if data_row[idx_close]:
            closing_price.append(data_row[idx_close])
        if data_row[idx_tradedv]:
            traded_volume.append(data_row[idx_tradedv])

    traded_volume.sort()
    if len(traded_volume) % 2:

        median = traded_volume[len(traded_volume) // 2]
    else:
        median = (traded_volume[(len(traded_volume) // 2) - 1] + traded_volume[(len(traded_volume) // 2)]) / 2


    print(f"Lowest opening price : {round(min(open_prices),2)}")
    print(f"Highest opening price :{round(max(open_prices),2)}")
    print(f"largest change in any one day (based on High and Low price) : {round(max(day_diff),2)}")
    print(f"argest change between any two days (based on Closing Price) : {round(max(closing_price)-min(closing_price),2)}")
    print(f"Average daily trading volume during this year : {round(sum(traded_volume)/len(traded_volume),2)}")
    print(f"median trading volume during this year : {round(median,2)}")

if __name__=="__main__":
    start_date='2017-01-01'
    end_date = '2017-12-31'
    base_url = "https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X/data.json"
    load_dotenv()
    API_KEY = os.getenv('NASDAQ_API_KEY')
    params={'api_key':API_KEY,'start_date':start_date,'end_date':end_date}
    nasdaq_api(params)
